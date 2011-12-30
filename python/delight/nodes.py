import sys, inspect, operator, copy, re, types
from math import *

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI


from .items import Item
from .containers import Container, Group, Master
from .attributes import (Address, Attribute, Boolean, Color, ColorArray, ComponentData, Enum, File, Float, Float2, Float3, Image,  
                         Integer, LightData, Matrix, Message, Normal, Point, String, UV, Vector)

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

class Function(object):
    def __init__(self, name='myFunction', type='void', rsl='', inputs=[], outputs=[]):
        self.name = name
        self.type = type
        self.rsl = rsl
        self.inputs = inputs
        self.outputs = outputs
    
class Shader(object):
    includes = []
    aovs = []
    rslprepare = None
    rslpreparepost = None
    rsl = None
    rslpost = None    
    melpost = None
    utilfuncs = []
    headerbegin = None
    headerend = None
    classification = None
    swatcher = '3delight'
    typeid = None
    __master = None
    __outputs = {}

    @classmethod
    def validateItem(cls, element):
        element.validate()
        if isinstance(element, Container):
            for child in element.children:
                cls.validateItem(child)

    @classmethod
    def getIncludes(cls):
        includes = []
        for supercls in reversed(inspect.getmro(cls)):
            for name, attr in inspect.getmembers(supercls):
                if name == 'includes':
                    includes.extend(filter(lambda i: i not in includes, attr))
        return includes
    
    @classmethod
    def getClassAttributes(cls, func=lambda attr: True):
        # find all attributes in all base classes that match the supplied keywords
        attrs = []
        
        # we want two levels of sorting --
        #  first, we want child classes above their parents
        #  second, we want attributes in the order they were declared
        mro = inspect.getmro(cls)
        for clsorder, supercls in zip(range(0, len(mro)), mro):
            for name, attr in supercls.__dict__.items():
                if isinstance(attr, Item) and func(attr):
                    attr._clsorder = clsorder
                    attrs.append(attr)
                    attr._name = name
                    
        # sort according to the class order, then the order they were declared 
        def sortHelper(v1, v2):
            if v1._clsorder < v2._clsorder:
                return -1
            elif v1._clsorder > v2._clsorder:
                return 1
            else:
                if v1._counter < v2._counter:
                    return -1
                elif v1._counter > v2._counter:
                    return 1
                else:
                    return 0

        return sorted(attrs, cmp=sortHelper)

    @classmethod
    def setupAttributes(cls):
        
        
        # set each item's longname if it has none 
        for name, attr in inspect.getmembers(cls):
            if isinstance(attr, Item) and attr.longname == None:
                # handle __blah variables -- python prefixes them with _classname
                # we have to un-prefix them
                demangled_name = re.sub('^_\w+__', '__', name)
                attr.longname = demangled_name

        # 
        allattribs = cls.getClassAttributes()

        # we need to make a copy, since Maya cannot share attributes between nodes, and our nodes
        # are allowed to share a base class
        allattribs = copy.deepcopy(allattribs)
        
        # Set newly copied attributes back to class
        attribs = []
        for attr in allattribs:
            setattr(cls, attr._name, attr)
            
            # add top level attrs
            if attr.parent == None:
                attribs.append(attr)

        # create a group for non-grouped attributes
        groupName = cls.__name__.replace('dl_', '').replace('Shape', '')
        if groupName[-1].isupper():
            groupName = groupName + ' ' + 'Attributes'
        else:
            groupName = groupName + 'Attributes'
        ungroupedAttributes = filter(lambda attr: isinstance(attr, Attribute), attribs)
        topGroup = Group(ungroupedAttributes, longname=groupName, collapse=False)
        attribs = [topGroup] + filter(lambda attr: not isinstance(attr, Attribute), attribs)
        
        attribs.sort(key=lambda item: item._counter if item._counter is not None else sys.maxint)
        
#        attribs = []
#        for attr in unsortedAttribs:
#            if attr._counter is not None:
#                attribs.insert(attr._counter, attr)
#            else:
#                attribs.append(attr)
            
            
        # create the top-level master container
        cls.__master = Master(attribs)

        # aovs are only used by getDelight(), so we don't need to copy them
        cls.__aovs = cls.__master.filterAttributes(lambda attr: isinstance(attr, Attribute) and attr.aov == True)

        # messages
        cls.__messages = cls.__master.filterAttributes(lambda attr: isinstance(attr, Attribute) and attr.message == True)

        # combine includes from base classes
        cls.__includes = cls.getIncludes() 
        
        # run validation logic on items
        cls.validateItem(cls.__master)
        for aov in cls.__aovs:
            cls.validateItem(aov)

    @classmethod
    def initialize(cls):
        cls.setupAttributes()
        cls.__master.createAttributes()
        cls.__master.addAttributes()

        # build a list mapping plugs to python attributes
        # TODO: can't use a dict -- at the moment
        cls.__outputs = dict([(attr.longname, attr) for attr in cls.__master.filterAttributes(lambda p: p.output)])

        # link inputs to outputs
        attribs = cls.__master.filterAttributes(lambda a: a.affect and not a.message and not a.aov and not a.nomaya)
        for input in filter(lambda a: not a.output, attribs):
            for output in filter(lambda p: p.output and not p.internal, attribs):
                try:
                    cls.attributeAffects(input.obj, output.obj)
                except Exception, e:
                    raise RuntimeError(str(e) + ': "%s" affects "%s"' % (input.longname, output.longname))

    @classmethod
    def getTemplate(cls):
        if hasattr(cls, 'template'):
            return cls.template
        else:
            return """
            %s
            global proc AE%sTemplate(string $node)
            {
                %s
            }
            """ % (cls.__master.getHelpers().replace('TEMPLATE', cls.__name__),
                   cls.__name__,
                   cls.__master.getTemplate().replace('TEMPLATE', cls.__name__))

    @classmethod
    def getFunctionSignature(cls, inputs, outputs, prepare=False, end=False, name=None, rsltype='void'):
        
        prefix=''
        if prepare:
            prefix='prepare'
        elif end:
            prefix='end'
            
        rsl = ''
        rsl += '%s\n'%rsltype
        if len(prefix):
            rsl += '%s_'%prefix
        
        if name == None:
            name = 'maya_%s'%cls.__name__
            
        rsl += '%s(\n' % name

        if len(inputs):
            rsl += '\t// Inputs\n'
            rsl += '\t//\n'
            for attr in inputs:
                if attr.rsltype != 'void':
                    rsl += '\t' + attr.getRSL() + ';\n'
                
        if len(outputs):
            rsl += '\t// Outputs\n'
            rsl += '\t//\n'
            for attr in outputs:
                if attr.rsltype != 'void':
                    rsl += '\t' + attr.getRSL() + ';\n'
                    
        rsl += '\t)\n'
        return rsl
    
    @classmethod
    def getFunctionBody(cls, prepare=False, funckey=None):
        
        rsl = ''

        # add the rsl block from each superclass
        mro = inspect.getmro(cls)
        
        #
        rslattrname = 'rsl'
        if prepare:
            rslattrname += 'prepare'
        rslpostattrname = '%spost' % rslattrname
        
        for supercls in reversed(mro):
            rslattr = supercls.__dict__.get(rslattrname, None)
            if rslattr:
                if type(rslattr) == types.StringType:
                    rsl += rslattr.rstrip(' ')
                elif funckey is not None and type(rslattr) == types.DictType:
                    rsl += rslattr[funckey].rstrip(' ')
                        
        for supercls in mro:
            rslpostattr=supercls.__dict__.get(rslpostattrname, None)
            if rslpostattr:
                if type(rslpostattr) == types.StringType:
                    rsl += rslpostattr.rstrip(' ')
                elif funckey is not None and type(rslpostattr) == types.DictType:
                    rsl += rslpostattr[funckey].rstrip(' ')
                    
        return rsl
    
        
    @classmethod
    def getRSL(cls):
        rsl = ''
        rsl += '#ifndef __%s_h\n' % cls.__name__
        rsl += '#define __%s_h\n' % cls.__name__
        rsl += '\n'

        inputs = []
        outputs = []
        for p in cls.__master.filterAttributes(lambda attr: isinstance(attr, Attribute) \
                                                         and attr.getDelight() != None \
                                                         and attr.getRSL() != None
                                                         and not attr.message and not attr.aov and not attr.utility):
            if p.output:
                outputs.append(p)
            else:
                inputs.append(p)

        aovs = filter(lambda attr: attr.getDelight() != None \
                                    and attr.getRSL() != None, cls.__aovs)

        messages = filter(lambda attr: attr.getDelight() != None \
                                    and attr.getRSL() != None, cls.__messages)

        if cls.rsl:
            rsl += '/*\n'
    
            if len(inputs):
                rsl += 'begin inputs\n'
                for attr in inputs:
                    rsl += '\t' + attr.getDelight() + '\n'
                rsl += 'end inputs\n'
                rsl += '\n'
                    
            if len(outputs):
                rsl += 'begin outputs\n'
                for attr in outputs:
                    rsl += '\t' + attr.getDelight() + '\n'
                rsl += 'end outputs\n'
                rsl += '\n'
    
            if len(messages):
                if messages[0].messagetype != None:
                    messagetype = messages[0].messagetype
                else:
                    messagetype = messages[0].longname
                rsl += 'begin shader_extra_parameters ' + messagetype + '\n'
                for attr in messages:
                    rsl += '\t' + attr.getRSL() + ' = ' + str(attr.getRSLValue(attr.default)) + ';\n'
                rsl += 'end shader_extra_parameters\n'
                rsl += '\n'
    
            for attr in aovs:
                rsl += 'begin shader_extra_parameters ' + attr.longname + '\n'
                rsl += '#ifdef USE_AOV_' + attr.longname + '\n'
                rsl += '\t' + attr.getRSL() + ';\n'
                rsl += '#endif\n'
                rsl += 'end shader_extra_parameters\n'
                rsl += '\n'
                
            rsl += '*/\n'
        
        if cls.headerbegin:
            rsl += '%s\n'%cls.headerbegin
            
        if len(cls.__includes):
            rsl += '\n'
            rsl += '\n'.join(['#include "%s"' % i for i in cls.__includes])
            rsl += '\n'

        rsl += '\n'
        
        # UTILS
        for func in cls.utilfuncs:
            rsl += cls.getFunctionSignature(func.inputs, func.outputs, name=func.name, rsltype=func.type)
            rsl += '{\n'
            rsl += func.rsl + '\n'
            rsl += '}\n\n'
            
        if cls.rsl:
            if cls.rslprepare:
                rsl += cls.getFunctionSignature(inputs, outputs, prepare=True)
                rsl += '{\n'
                rsl += cls.getFunctionBody(prepare=True)
                rsl += '}\n'
                rsl += '\n'
    
            rsl += cls.getFunctionSignature(inputs, outputs, end=cls.rslprepare)
            rsl += '{\n'
            rsl += cls.getFunctionBody()
            rsl += '}\n'
                
        rsl += '\n'
        
        if cls.headerend:
            rsl += '%s\n'%cls.headerend
        
        rsl += '#endif /* __%s_h */\n' % cls.__name__
        
        return rsl 
            
    @classmethod
    def register(cls, obj):
#        if cls.rsl == None:
#            raise TypeError('Node %s has no rsl' % cls.__name__)
        
        if cls.classification == None:
            raise TypeError('Node %s has no classification' % cls.__name__)
        
        if cls.typeid == None:
            raise TypeError('Node %s has no typeid' % cls.__name__)

        plugin = OpenMayaMPx.MFnPlugin(obj, '3Delight', '1.0', 'Any')
        
        classification = cls.classification
        if cls.swatcher:
            classification += ':swatch/' + cls.swatcher
        
        try:
            plugin.registerNode(cls.__name__,
                                OpenMaya.MTypeId(cls.typeid), 
                                lambda: OpenMayaMPx.asMPxPtr(cls()), 
                                lambda: cls.initialize(), 
                                cls.nodetype, 
                                classification)
            OpenMaya.MGlobal.executeCommand(cls.getTemplate())
            if cls.melpost != None:
                OpenMaya.MGlobal.executeCommand(cls.melpost)
        except Exception, e:
            sys.stderr.write("Failed to register %s: %s"  % (cls.__name__, str(e)))
            raise
        
        postCmd = \
        """
            if (`window -exists createRenderNodeWindow`)
            {
                refreshCreateRenderNodeWindow(\"%s\");
            }
        """ % classification
        OpenMaya.MGlobal.executeCommand(postCmd)

    @classmethod
    def deregister(cls, obj):
        plugin = OpenMayaMPx.MFnPlugin(obj, '3Delight', '1.0', 'Any')
        try:
            plugin.deregisterNode(OpenMaya.MTypeId(cls.typeid))
        except Exception, e:
            sys.stderr.write("Failed to deregister %s: %s"  % (cls.__name__, str(e)))
            raise


class ShadingNode(OpenMayaMPx.MPxNode, Shader):
    nodetype = OpenMayaMPx.MPxNode.kDependNode

    # required, otherwise deleting connected nodes deletes the node itself
    def postConstructor(self):
        self.setExistWithoutInConnections(True)
        self.setExistWithoutOutConnections(True)


class ShadingCodeNode(ShadingNode):
    
    shadingCode = String(output=True, norsl=True, internal=True)
    shadingParameters = String(output=True, norsl=True, internal=True)

    #
    def getShadingCode(self):
        return self.__class__.getFunctionBody()
    
    #
    def getShadingParametersAttributes(self):
        return self.__class__.getClassAttributes(lambda attr: isinstance(attr, Attribute) and attr.message is not None and attr.obj is not None and not attr.utility)
    
    #
    def getShadingParameters(self):
        shadingParameters = ''
        for p in self.getShadingParametersAttributes():
            delightCode = p.getDelight()
            if delightCode:
                if p.aov:
                    shadingParameters += 'shader_output '
                elif p.output:
                    shadingParameters += 'output '
                shadingParameters+= '%s\n'%delightCode
        return shadingParameters
    
    def getInternalValueInContext(self, plug, dataHandle, ctx):
        attrObj = plug.attribute()
        if attrObj == self.shadingCode.obj:
            shadingCode = self.getShadingCode()
            dataHandle.setMObject(OpenMaya.MFnStringData().create(shadingCode))
            return True
        elif attrObj == self.shadingParameters.obj:
            shadingParameters = self.getShadingParameters()
            dataHandle.setMObject(OpenMaya.MFnStringData().create(shadingParameters))
            return True
        
        return False



#
#class ShadingCodeExtern(ShadingCodeNode):    
#    
#    @classmethod 
#    def setupAttributes(cls):
#        attrLabels=[]
#        for p in cls.getClassAttributes(lambda attr: isinstance(attr, Attribute) and not attr.message and not attr.output and not attr.norsl and not attr.hidden):
#            attrLabels.append(p._name)
#        attrLabels.sort()
#        attrLabels.insert(0, 'None')
#        cls.externParameters = Enum(shortname='eps', label='Extern Parameters', array=True, norsl=True, default=attrLabels[0], choices=attrLabels)
#        super(ShadingCodeExtern, cls).setupAttributes()
#    
#    #
#    def getExternParameters(self, data):
#        cls=self.__class__
#        externParametersHdl = data.inputArrayValue(cls.externParameters.obj)
#        externParameters = []
#        if externParametersHdl.elementCount():
#            while(True):
#                idx = externParametersHdl.inputValue().asShort()
#                externParameters.append(cls.externParameters.choices[idx])
#                try:
#                    externParametersHdl.next()
#                except:
#                    break
#                
#        return externParameters
#    
#    #
#    def getShadingCode(self, data):
#        cls=self.__class__
#        shadingCode= ''
#        externParams = self.getExternParameters(data)
#        thisName = OpenMaya.MFnDependencyNode(self.thisMObject()).name()
#        for p in cls.getClassAttributes(lambda attr: isinstance(attr, Attribute) and attr.message is not None and attr.obj is not None and attr._name in externParams):
#            shadingCode += '%s=%s_%s;\n'%(p.getDelightName(), thisName, p.getDelightName())
#            
#        shadingCode += super(ShadingCodeExtern, self).getShadingCode(data)
#        
#        return shadingCode
#    
#    #
#    def getShadingParametersAttributes(self, data):
#        cls=self.__class__
#        externParams = self.getExternParameters(data)
#        return cls.getClassAttributes(lambda attr: isinstance(attr, Attribute) and attr.message is not None and attr.obj is not None and not attr.utility and attr._name not in externParams)
#    
#    #
#    def getShadingParameters(self, data):
#        shadingParameters = ''
#        thisName = OpenMaya.MFnDependencyNode(self.thisMObject()).name()
#        externParams = self.getExternParameters(data)
#        for p in super(ShadingCodeExtern, self).getShadingParametersAttributes(data):
#            delightCode = p.getDelight()
#            if delightCode and p._name in externParams:
#                
#                # NOTE: OK, this is very hacky...but it works:
#                # Since the input becomes an extern param, it must be unique in case of multiple instances, thus the node name prefix
#                # If it is rename the rsl code with old name is no longer valid
#                # So we still add the orig name but as an output so it can be assigned with the extern shader parameter, this is done in getShadingCode
#                shadingParameters += 'shader_input %s=%s\n'%(p.getDelight().replace(p._name, '%s_%s'%(thisName, p._name)), str(p.getRSLValue(p.getValue(data))))
#                shadingParameters += 'output %s\n'%delightCode
#        shadingParameters += super(ShadingCodeExtern, self).getShadingParameters(data)
#        
#        return shadingParameters
    
class ShadingComponentBase(object):
        
    componentChildren = []
    for channel in ComponentData.channels:
        exec 'output_%s = %s(shortname="o%s", internal=True, output=True)'%(channel.longname, channel.type, channel.shortname)
        exec 'componentChildren.append(output_%s)'%channel.longname
    outputComponent = ComponentData(longname='outputComponent', shortname='ocmp', children=componentChildren, output=True)
    
    outColor = Color(output=True)
    outTransparency = Color(output=True, default=0)
    normalCamera = Normal(shortname='n', hidden=True, keyable=False, affect=False)
    pointCamera = Point(hidden=True, norsl=True, keyable=False, affect=False)
    rayDirection = Vector(hidden=True, norsl=True, keyable=False, affect=False)
    tangentUCamera = Vector(hidden=True, norsl=True, keyable=False, affect=False)
    tangentVCamera = Vector(hidden=True, norsl=True, keyable=False, affect=False)
    matrixEyeToWorld = Matrix(shortname='mew', storable=False, hidden=True, norsl=True, keyable=False, affect=False)
    matrixWorldToEye = Matrix(shortname='mwc', storable=False, hidden=True, norsl=True, keyable=False, affect=False)

    lightDirection = Vector(shortname='ld', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightIntensity = Color(shortname='li', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightAmbient = Boolean(shortname='la', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightDiffuse = Boolean(shortname='ldf', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightSpecular = Boolean(shortname='ls', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightShadowFraction = Float(shortname='lsf', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    preShadowIntensity = Float(shortname='psi', default=1, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightBlindData = Address(shortname='lbld', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightDataArray = LightData(shortname='ltd',
                                          lightDirection=lightDirection,
                                          lightIntensity=lightIntensity,
                                          lightAmbient=lightAmbient,
                                          lightDiffuse=lightDiffuse,
                                          lightSpecular=lightSpecular,
                                          lightShadowFraction=lightShadowFraction,
                                          preShadowIntensity=preShadowIntensity,
                                          lightBlindData=lightBlindData, 
                                          array=True, storable=False, hidden=True, norsl=True, keyable=False, affect=False)

    def compute(self, plug, data):
        if plug == self.outColor.obj:
            data.outputValue(plug).set3Float(1.0, 1.0, 1.0)
        elif plug == self.outTransparency.obj:
            data.outputValue(plug).set3Float(0.0, 0.0, 0.0)
        else:
            return OpenMaya.MStatus.kUnknownParameter
        
        data.setClean(plug)
        
        return OpenMaya.MStatus.kSuccess
    
    
class ShadingCodeComponent(ShadingCodeNode, ShadingComponentBase):
    classification = 'rendernode/3delight/shadingcomponent:shader/shadingcomponent'
    includes = ['utils.h', 'component_utils.h']

 
class ShadingComponent(ShadingNode, ShadingComponentBase):
    classification = 'rendernode/3delight/shadingcomponent:shader/shadingcomponent'
    swatcher = '3delight_surface'
    includes = ['utils.h', 'component_utils.h']
    
    #
    mute = Boolean(shortname='mute', default=False, storage='uniform', help="Turn off computation of this component.")
    contribution = Float(shortname='ct', default=1, storage='uniform', help="Weight used to normalize this component's contribution to the lighting model.")
    intensity = Float(default=1, help="Intensity of this component")
    color = Color(help="Color of this component")
    shadeCurves = Boolean(default=False, help="Shade curves without normals.")
    componentAttributes = Group([mute, contribution, intensity, color, shadeCurves], collapse=False, order=0)
    
    rsl = \
    """
    #ifndef SHADER_TYPE_light
    
    float globalIntensity = i_intensity * i_contribution;
        
    if(i_mute > 0 || globalIntensity <= 0)
        return;
        
    extern point P;
    extern vector I;
    extern color Cs;
    
    //
    color surfaceColor = i_color * Cs;
    
    //
    vector In = normalize(I);
    vector V = -In;
    
    normal Nn;
    normal Nf;
    if (i_shadeCurves) {
        // fake a normal 
        Nn = normal(V);
        Nf = Nn;
    }
    else {
        // use the surface normal
        Nn = normalize(i_normalCamera);
        Nf = ShadingNormal(Nn);
    }
    
    """
    
    rslpost = \
    """
    #endif // SHADER_TYPE_light
    """
    
    
class DiffuseBase(object):
    
    lightTypes=['Direct', 'Indirect', 'Direct & Indirect']
    lightType = Enum(default=lightTypes[2], choices=lightTypes, help="Whether to respond to CG lights, indirect lighting, or both. ")
    
    rsl = \
    """
    uniform string baseCategory = "";
    if (i_lightType == 0)
        baseCategory = "diffuse&-indirect";
    else if (i_lightType == 1)
        baseCategory = "indirect";
    else if (i_lightType == 2)
        baseCategory = "diffuse";
            
    float useDirect = 0;
    if (i_lightType == 0 || i_lightType == 2)
        useDirect = 1;
        
    float useIndirect = 0;
    if (i_lightType == 1 || i_lightType == 2)
        useIndirect = 1;
    """
    

class PointCloudBase(object):

    ptcFile = File(label='Point Cloud File', help='Point cloud file to use.')
    ptcIntensity = Float(default=1, label='Intensity',  help='Intensity of point cloud.')
    ptcBlur = Float(default=0.1, label='Blur', help='How much to blur the point cloud')
    ptcClamp = Boolean(shortname='ptcc', default=True, label='Clamp', help='')
    ptcSortBleeding = Boolean(default=True, label='Sort Bleeding', help='')
    ptcMaxSolidAngle = Float(default=0.1, label='Max Solid Angle', help='')
    ptcBias = Float(shortname='ptbi', default=0.1, label='Bias', help='')
    ptcMaxDist = Float(default=-1, label='Max Distance', help='')
    ptcSampleBase = Float(shortname='ptsb', default=1, label='Sample Base', help='')
    pointCloudGroup = Group([ptcFile, ptcIntensity, ptcBlur, ptcBias, ptcMaxDist, ptcClamp, ptcSortBleeding, ptcMaxSolidAngle, ptcSampleBase], label='Point Cloud')

    rsl = \
    """
    color ptcColor = 0;
    float ptcAlpha = 0;
    string ptcFiles[];
    """
        
class RaytraceBase(object):

    rayMethod = Enum(shortname='ram', default='Trace', choices=['Trace', 'Gather'], storage='uniform', label='Method',
                                help="Which shadeop to use, trace() or gather().")
    raySamples = Integer(default=1, label='Samples', softmax=16, storage='uniform',
                                    help="The number of rays to shoot. More samples allow you to achieve better antialiasing or glossy and translucent effects. More samples also means slower rendering.")
    rayBlur = Float(shortname='bl', min=0, softmax=1, default=0, label='Blur',
                               help="Blurriness of the raytracing. 0 is a cone angle of 0 degrees, 1 is 5 degrees. Larger values of blur will require more samples.")
    raySubset = String(storage='uniform', shortname='ss', label='Subset',
                                  help="The name of the set of objects that contribute raytracing in your scene. Leave this blank to cause all objects to partake in raytracing. You can speed up the calculations by reducing the number of objects to test for raytracings. ")
    rayMaxDistance = Float(default=-1, storage='uniform', label='Max Distance',
                                      help="The maximum distance to consider when calculating ray intersections. Setting this parameter to a negative number is effectively equivalent to setting the distance to infinity. (And a lot easier). ")
    rayBias = Float(shortname='rabi', default=-1, storage='uniform', softmin=0, label='Max Bias',
                               help="Specifies a bias for ray's starting point to avoid potentially erroneous intersections with emitting surface. A value of `-1' forces 3DELIGHT to take the default value as specified by the Trace:Bias attribute.")
    rayFalloff = Enum(default='None', choices=['None', 'Linear', 'Quadratic'], label='Falloff',
                           help="How reflection/refractionn from objects falls off with distance.")
    rayFalloffColor = Color(default=0, label='Falloff Color',
                           help="Color to fade to where reflection/refraction color falls off.")
    rayTracingGroup = Group([rayMethod, raySamples, rayBlur, raySubset, rayMaxDistance, rayBias, rayFalloff, rayFalloffColor],  label='Ray Tracing')

    rsl = \
    """
    float rayDist = 1e99;

    point origin = P;
    normal dir = Nn;

    uniform float traceDisplacements = 0;
    attribute("trace:displacements", traceDisplacements);
    if (traceDisplacements == 0) {
        // get the undisplaced surface point and normal from the displacement shader
        displacement("__Porig", origin);
        displacement("__Norig", dir);
    }

    dir = normalize(dir);
    """
                
class EnvironmentMapBase(object):

    mapContribution = Float(min=0, max=1, default=1, storage='uniform', help="Contribution of environment lights to the diffuse color.")
    mapBlur = Float(min=-1, max=1, default=0, help="Amount to blur the environment map.")
    mapBlurS = Float(min=-1, max=1, default=0, help="Amount to blur the environment map in S.")
    mapBlurT = Float(min=-1, max=1, default=0, help="Amount to blur the environment map in T.")
    mapFilter = Enum(default='Gaussian', choices=['Gaussian', 'Triangle', 'Box'])
    physicalSkySamples = Integer(default=-1, min=1, softmax=64,
        help="""Number of samples to use when dl_envLightShape's Environment Method == 'Physical Sky'.
            If < 0, dl_envLightShape's physkyProceduralSamples parm is used.""")
    mapGroup = Group([mapContribution, mapBlur, mapBlurS, mapBlurT, mapFilter, physicalSkySamples], label='Environment Map')
    
    rsl = \
    """
    uniform string envFilter;
    if (i_mapFilter == 0)
        envFilter = "gaussian";
    else if (i_mapFilter == 1)
        envFilter = "triangle";
    else
        envFilter = "box";
    
    color envColor = 0;
    """

class ReflectionRefractionComponent(RaytraceBase, PointCloudBase, EnvironmentMapBase, ShadingComponent):
    
    includes = ['ray_utils.h', 'env_utils.h']
    
    indexOfRefraction = Float(default=1, softmax=3, storage='uniform',
                                      help="(Relative) index of refraction of material. The index of refraction from air to glass is 1.5. Air to water is 1.33. ")
    
    # hidden until sorted out 
    maxIntensity = Float(default=-1, storage='uniform', hidden=True,
                                 help="""To prevent the reflection/refraction intensity from becoming unboundedly
                                         large when the distance < falloffdist, it is
                                         smoothly clamped to this maximum value.""");
                                         
    calculationMethod = Enum(shortname='cam', label='Method', storage='uniform', default='Ray Tracing',
                            choices=['Ray Tracing', 'Point Cloud', 'None (Environment Only)'],
                            help="Method of calculating inter object")

    generalAttributes = Group([calculationMethod, RaytraceBase.rayTracingGroup, PointCloudBase.pointCloudGroup], collapse=False,  order=1)                                     
    
                    
class Displacement(ShadingNode):
    classification = 'rendernode/3delight/displacement:shader/displacement'
    swatcher = '3delight_displacement'
    
    displacement = Float(shortname='od', output=True, storable=False, writable=False, norsl=True)
    outColor = Color(output=True)
    outAlpha = Float(output=True)

    __Porig = Point(output=True, message=True, messagetype='displacement', storage='varying')
    __Norig = Normal(output=True, message=True, messagetype='displacement', storage='varying')
    

class LightBase(OpenMayaMPx.MPxLocatorNode, Shader):
    nodetype = OpenMayaMPx.MPxNode.kLocatorNode
    classification = 'rendernode/3delight/light:light'
    
    
 # outputs
    lightDirection = Vector(shortname='ld', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightIntensity = Color(shortname='li', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightAmbient = Boolean(shortname='la', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightDiffuse = Boolean(shortname='ldf', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightSpecular = Boolean(shortname='ls', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightShadowFraction = Float(shortname='lsf', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    preShadowIntensity = Float(shortname='psi', default=1, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightBlindData = Address(shortname='lbld', storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    lightDataArray = LightData(shortname='ltd',
                                          lightDirection=lightDirection,
                                          lightIntensity=lightIntensity,
                                          lightAmbient=lightAmbient,
                                          lightDiffuse=lightDiffuse,
                                          lightSpecular=lightSpecular,
                                          lightShadowFraction=lightShadowFraction,
                                          preShadowIntensity=preShadowIntensity,
                                          lightBlindData=lightBlindData, 
                                          array=True, storable=False, hidden=True, norsl=True, keyable=False, affect=False)
    
    # required by 3dfm
    shadowmapname = String(default='', message=True, messagetype='lightsource')
    emitSpecular = Boolean(shortname='es', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    emitDiffuse = Boolean(shortname='ed', default=True, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)
    emitAmbient = Boolean(shortname='ea', default=False, storable=False, writable=False, hidden=True, norsl=True, keyable=False, affect=False)

    __nondiffuse = Float(default=False, output=True, message=True, messagetype='lightsource')
    __nonspecular = Float(default=False, storage='varying', output=True, message=True, messagetype='lightsource')
        
class Light(LightBase):

    intensity = Float(min=0, softmax=1, default=1, storage='uniform')
    lightColor = Color(storage='uniform')
    
    # required, otherwise deleting connected nodes deletes the node itself
    def postConstructor(self):
        self.setExistWithoutInConnections(True)
        self.setExistWithoutOutConnections(True)

    # default icon
    def draw(self, view, path, style, status):
        thisNode = self.thisMObject()

        view.beginGL()
        glFT.glBegin(OpenMayaRender.MGL_LINES)
        glFT.glVertex3f(-1,0,0)
        glFT.glVertex3f(1,0,0)
        glFT.glVertex3f(0,-1,0)
        glFT.glVertex3f(0,1,0)
        glFT.glVertex3f(0,0,-1)
        glFT.glVertex3f(0,0,1)
        glFT.glEnd()
        view.endGL()

    rsl = \
    """
    extern color Cl;
    extern vector L;
    extern point Ps;
    extern point P;
    extern normal N;
    extern normal Ns;
    extern vector I;
    extern float __nonspecular;
    extern float __nondiffuse;
        
    """

class EnvLight(Light):
    
    #
    Light._LightBase__nondiffuse.default=True
    Light._LightBase__nonspecular.default=True
    
    # environment
    envMap = Image(label='Environment Map',
                           help="Environment map to use for reflections.")

    envMethod = Enum(shortname='envMethod',
                                label='Environment Method',
                                default='Environment Map',
                                choices=['None', 'Environment Map', 'Physical Sky'])

    # procedural sky
    physkyJustSun = Boolean(shortname="js", default=False, label="JustSun")
    physkySunLightRotation = Vector(shortname="slr", default=(-60, 0, 0), label="SunLightRotation")
    physkyCloudTex = Image(default="", label="CloudTex")
    physkyGroundTex = Image(default="", label="GroundTex")
    physkyTextureBlur = Float(shortname="texb", default=0, label="TextureBlur")
    physkyFakeSkyBlur = Float(shortname="fsb", min=0, max=1, default=0, label="FakeSkyBlur")
    physkyFakeSkyBlurUpBias = Float(shortname="fsbub",
                    min=-1, max=1, default=0, label="FakeSkyBlurUpBias")

    physkyProceduralSamples = Float(shortname="procsamps", default=1, label="ProceduralSamples(Default)",
        help="Numbr of samples, used ONLY for objects with reflection/refaction/specular nodes that have Physical Sky Samples < 0.")
    physkyProceduralBlur = Float(shortname="procBlur", default=0, label="ProceduralBlur(Default)",
        help="Sky blur amount, used ONLY for objects with reflection/refaction/specular nodes that have MapBlur < 0.")
    physkyMultiplier = Float(shortname="mult", default=1, label="Multiplier")

    physkyRgbUnitConversion = Float3(default=0, label="RgbUnitConversion")
    physkyHaze = Float(default=0, label="Haze")
    physkyRedBlueShift = Float(shortname="rbs", default=0, label="RedBlueShift")
    physkySaturation = Float(default=1, label="Saturation")
    physkyHorizonHeight = Float(shortname="hht", default=0, label="HorizonHeight")
    physkyHorizonBlur = Float(shortname="hbl", default=0.1, label="HorizonBlur")
    physkyGroundColour = Color(shortname="groundColour", default=0.2, label="GroundColour")
    physkyNightColour = Color(shortname="ncl", default=0, label="NightColour")
    
    physkySunDiskIntensity = Float(shortname="sdi", default=1, label="SunDiskIntensity")
    physkySunDiskScale = Float(shortname="sds", default=4, label="SunDiskScale")
    physkySunGlowIntensity = Float(shortname="sgi", default=1, label="SunGlowIntensity")
    physkySunMaxIntensity = Float(shortname="smi", default=500000, label="SunMaxIntensity")
    
    physkyYIsUp = Boolean(default=True, label="YIsUp")
    
    physkyCoordsys = String(shortname="cs", default="world", label="Coordsys")

    physkyBakeSkyMap = Boolean(shortname="bsm", default=False, label="BakeSkyMap")
    physkyBakeSkyMapFile = String(shortname="bsmf", default="sky.bake", label="BakeSkyMapFile")

    physicalSky = Group([physkySunLightRotation, physkyJustSun, physkyCloudTex, physkyGroundTex, physkyTextureBlur, 
        physkyProceduralSamples, physkyProceduralBlur, physkyMultiplier, physkyRgbUnitConversion,
        physkyHaze, physkyRedBlueShift, physkySaturation, physkyHorizonHeight, physkyHorizonBlur, physkyFakeSkyBlur, physkyFakeSkyBlurUpBias,
        physkyGroundColour, physkyNightColour, physkySunDiskIntensity, physkySunDiskScale, physkySunGlowIntensity,
        physkySunMaxIntensity, physkyYIsUp, physkyCoordsys, physkyBakeSkyMap, physkyBakeSkyMapFile])
    envSpace = Message(shortname='esp',
                               default='world', 
                               label='Coordinate System',
                               help="The coordinate system used to place the environment map.")
    envExposure = Float(softmin=-6, softmax=6, default=0, storage='uniform',
                                label='Exposure',
                                help="""Adjusts the exposure level. Negative values darken, 
                                        positive values brighten. Affects mostly highlights.""")
    envGamma = Float(min=0.0001, max=5, default=1, storage='uniform',
                             label='Gamma',
                             help="Adjusts the gamma. Affects mostly midtones.")
    envOffset = Float(min=-1, max=1, default=0, storage='uniform',
                              label='Offset',
                              help="""Offset.""")
    envColorCorrection = Group([envExposure, envGamma, envOffset], label='Color Correction')
    
    
    occMaxDistance = Float(softmin=0, default=1e38, storage='uniform',
                                   label='Max Distance',
                                   help="(Ray Tracing, Point Cloud) Maximum distance to consider for occlusion.")
    # Ray Tracing
    occConeAngle = Float(min=0, softmax=90, default=90, storage='uniform',
                                 label='Cone Angle',
                                 help="""(Ray Tracing) Cone angle to consider for reflection occlusion. This should 
                                         be a small number.""")
    occSamples = Integer(min=64, max=256, default=64,
                                 label='Samples',
                                help="""(Ray Tracing) The number of rays to trace to compute occlusion.
                                         If set to zero, The "irradiance:nsamples" attribute is used.""")
    occAdaptiveSampling = Boolean(default=False,
                                          label='Adaptive Sampling',
                                          help="(Ray Tracing) Enables or disables adaptive sampling.")
    occRayBias = Float(default=0.1,
                               min=0, softmax=2,
                               label='Ray Bias',
                               help="""(Ray Tracing, Point Cloud) Specifies a bias for ray's starting point to avoid potentially erroneous 
                                       intersections with the emitting surface.""")

  
    occFalloffMode = Enum(default='Linear',
                                  choices=['Exponential', 'Linear'],
                                  label='Falloff Mode',
                                  help="""(Ray Tracing, Point Cloud) Specifies the falloff curve to use.""")
    occFalloff = Float(default=1, min=0, softmax=5,
                               label='Falloff',
                               help="""(Ray Tracing, Point Cloud) This shapes the falloff curve. In the exponential case the curve is exp( -falloff * hitdist ) 
                                       and in the linear case it is pow(1-hitdist/maxdist, falloff).""")
    occPtcFile = File(default='',
                                label='Point Cloud File',
                                help="""(Point Cloud) The point cloud file in which baked points are stored.""")
    occMaxSolidAngle = Float(softmin=0.01, softmax=0.5, default=0.1, storage='uniform',
                                     label='Max Solid Angle',
                                     help="""(Point Cloud) This is a quality vs speed control knob.""")
    occClamp = Boolean(shortname='ocl',
                               default=True,
                               label='Clamp',
                               help="""(Point Cloud) Setting this parameter to 1 will force 3DELIGHT to account for
                                       occlusion in dense environments. The results obtained with this
                                       parameter on should look similar to what a Ray Tracing rendering
                                       would give. Enabling this parameter will slow down the Point Cloud
                                       algorithm by a factor of 2.""")
    occSampleBase = Float(default=1,
                                  label='Sample Base',
                                  help="""(Point Cloud) Scales the amount of jittering of the start position of rays. The default
                                          is to jitter over the area of one micropolygon.""")
    occHitSides = Enum(default='Both',
                               choices=['Front', 'Back', 'Both'],
                               label='Hit Sides',
                               help="""(Point Cloud) Specifies which side(s) of the point cloud's samples will produce occlusion.""")
    
  
    
    occIntensity = Float(min=0, softmax=1, default=1, storage='uniform', 
                                 label='Intensity',
                                 help='Multiplier on occlusion.')
    occColor = Color(shortname='occ', default=0, storage='uniform',
                             label='Color',
                             help="Color of occlusion.")
    occBias = Float(shortname='ocb',
                            min=0, max=1, default=0.5, storage='uniform',
                            label='Bias',
                            help="""Bias is a a normalized gamma correction factor.
                                    Values greater than .5 lighten the result, values
                                    less than .5 make it darker.""")
    occGain = Float(shortname='ocg',
                            min=0, max=1, default=0.5, storage='uniform',
                            label='Gain',
                            help="""Gain is used to favor dark area when less than
                                    0.5 or light areas when greater than 0.5.""")
    occRemapping = Group([occIntensity, occColor, occBias, occGain],
                                  label='Remapping')

    occPointCloud = Group([occPtcFile, occMaxSolidAngle, occClamp, occSampleBase, occHitSides], label="Point Cloud")
    
    occRayTracing = Group([occSamples, occAdaptiveSampling, occRayBias], label="Ray Tracing",)

    occAdvanced = Group([occMaxDistance, occConeAngle, occFalloffMode, occFalloff],
                                label='Advanced')
    
     
    
class Utility(ShadingNode):
    classification = "rendernode/3delight/utility:utility/general"


class Texture2D(ShadingNode):
    classification = 'rendernode/3delight/texture/2d:texture/2d'
    includes = ['utils.h']

    defaultColor = Color(default=(.5,.5,.5))
    colorGain    = Color(default=(1,1,1))
    colorOffset  = Color(default=(0,0,0))
    alphaGain   = Float(default=1)
    alphaOffset = Float(default=0)     
    alphaIsLuminance = Boolean(default=False)
    invert = Boolean(default=False)

    ColorBalance = Group([defaultColor,colorGain,colorOffset,alphaGain,alphaOffset,alphaIsLuminance])
    Effects = Group([invert])
    
    uvFilterSize = Float2(shortname='ufs', notemplate=True)
    uvCoord = UV(shortname='uv')
    UVCoordinates = Group([uvCoord], label='UV Coordinates')    
    
    outColor = Color(output=True)
    outAlpha = Float(output=True)
    outTransparency = Color(output=True, default=0)
 
    rsl = \
    """
    varying float ss = i_uvCoord[0];
    varying float tt = 1 - i_uvCoord[1];
    
    if (ISUVDEFINED(ss, tt))
    {
    """
    
    rslpost = \
    """
        colorBalance(o_outColor, 
            o_outAlpha,
            i_alphaIsLuminance,
            i_alphaGain,
            i_alphaOffset,
            i_colorGain,
            i_colorOffset,
            i_invert);
    }
    else
    {
        o_outColor = i_defaultColor;
        o_outAlpha = luminance( o_outColor );
    }
    
    o_outTransparency = color(1 - o_outAlpha, 1 - o_outAlpha, 1 - o_outAlpha);   
    """


class Texture3D(ShadingNode):
    classification = 'rendernode/3delight/texture/3d:texture/3d'
    includes = ['texture3d.h','utils.h']         
    
    defaultColor = Color(default=(.5,.5,.5))
    colorGain    = Color(default=(1,1,1))
    colorOffset  = Color(default=(0,0,0))
    alphaGain   = Float(default=1)
    alphaOffset = Float(default=0)     
    alphaIsLuminance = Boolean(default=False)
    
    colorBalance = Group([defaultColor,colorGain,colorOffset,alphaGain,alphaOffset,alphaIsLuminance])
    
    blend = Float(storage='uniform')
    local = Boolean(storage='uniform')
    wrap = Boolean(default=True,storage='uniform')    
    placementMatrix = Matrix(notemplate=True)
    invert = Boolean(default=False)
    effects = Group([blend,local,wrap,invert])
     
    Pref = Point(message=True, storage='varying')
     
    outColor = Color(output=True)
    outAlpha = Float(output=True)
    outTransparency = Color(output=True, default=0)
    
    rsl = \
    """
    float edgeDist;
    float outside;  
    varying point pp = transformP(i_blend, 
        i_local, 
        i_placementMatrix, 
        i_wrap, edgeDist, 
        outside);
    if(outside < 1)
    {   
    """
    
    rslpost = \
    """
    colorBalance(o_outColor, 
            o_outAlpha, 
            i_alphaIsLuminance, 
            i_alphaGain, 
            i_alphaOffset, 
            i_colorGain, 
            i_colorOffset, 
            i_invert);

        if(i_blend > 0 && edgeDist >= 0)
        {
            o_outColor = blendDefaultColor(i_blend, i_defaultColor, edgeDist, o_outColor);
        }
    }
    else
    {
        o_outColor = i_defaultColor;
        o_outAlpha = 0;
    } 
    o_outTransparency = color(1 - o_outAlpha, 1 - o_outAlpha, 1 - o_outAlpha);  
    """

class Extern(ShadingCodeNode):
    classification = 'rendernode/3delight/utility:utility/general'
    description = "Create an extern shader parameter"
     
    parameterName = String(norsl=True)
    
    #
    def getParameterName(self):
        thisObj = self.thisMObject()
        paramName = OpenMaya.MPlug(thisObj, self.parameterName.obj).asString()
        paramName.strip(' ')
        if paramName == '':
            connectedTo = OpenMaya.MPlugArray()
            OpenMaya.MPlug(self.thisMObject(), self.outputValue.obj).connectedTo(connectedTo, False, True)
            if connectedTo.length():
                paramName = connectedTo[0].name().replace('.', '_')
            else:
                paramName = OpenMaya.MFnDependencyNode(thisObj).name()
                 
        return paramName
   
    #
    def getExternName(self):
        return self.inputValue.getDelight().replace(self.inputValue._name, self.getParameterName())
    
    #
    def getShadingCode(self):
        shadingCode = 'extern %s;\n'%self.getExternName()
        shadingCode = 'outputValue = %s;\n'%self.getParameterName()
        return shadingCode
    
    #
    def getShadingParameters(self):
        data = self._forceCache()
        valueStr = str(self.inputValue.getRSLValue(self.inputValue.getValue(data)))
        shadingParameters = 'shader_input %s=%s\n'%(self.getExternName(), valueStr)
        shadingParameters += ShadingCodeNode.getShadingParameters(self)
        return shadingParameters
    
    rsl = '//\n'

class AttributeNode(ShadingNode):
    classification = 'rendernode/3delight/utility:utility/general'
    description = "Query attributes"
     
    attributeName = String(default='user:')
    attributeExists = Float(output=True)
    
    rsl = """
    o_attributeExists = attribute(i_attributeName, o_outputValue);
    if(o_attributeExists == 0){ 
        o_outputValue = i_inputValue;
    }
    """    
