import re
import sys
import textwrap

from maya.OpenMaya import *
from maya.OpenMayaMPx import *

import pymel.core as pm

from .items import Item, CallCustom 
from .containers import Container
from . import components
from .utils import ArrayDataHandleIterator

class Attribute(Item):
    length = 1
    rsllength = 1
    dltype = None
    rsltype = None

    __defaultArgs = {'longname': None,
                     'shortname': None,
                     'storage': None,
                     'default': None,
                     'output': False,
                     'array': None,
                     'hidden': None,
                     'internal': None,
                     'indexmatters': None,
                     'keyable': True,
                     'connectable': None,
                     'storable': None,
                     'readable': None,
                     'writable': None,
                     'dynamic': None,
                     'init': None,
                     'aov': False,
                     'norsl': False,
                     'nomaya': False,
                     'affect': True,
                     'obj': None,
                     'parent': None,
                     'message': False,
                     'messagetype': None,
                     'sourceshapename': False,
                     'texture': False,
                     'prepare': False,
                     'help': None,
                     'nooptimize': False,
                     'label': None,
                     'suppress': False,
                     'utility':False,
                     'external':False,
                     'multi':True,
                     'callcustom': None}

    def __init__(self, *args, **kwargs):
        self.setDefaults(Attribute.__defaultArgs)
        super(Attribute, self).__init__(*args, **kwargs)

        if self.aov:
            self.storage = 'varying'

        
    def isArray(self):
        if self.array:
            return True
        else:
            try:
                 return self.parent.isArray()
            except:
                 return False

    def getDelightName(self):
        try:
            return self.parent.getDelightName() + '.' + self.longname
        except:
            if self.array :
                return self.longname + '[]'
            else:
                return self.longname

    def validate(self):
        # validate parameters
        if not self.aov and not isinstance(self.shortname, str):
            raise TypeError('%s: shortname must be a string' % self.longname)
        
#        if self.init != None and (not isinstance(self.init, (tuple, list)) or not all([isinstance(i, str) for i in self.init])):
#            raise TypeError('%s: init must be a tuple or list of strings' % self.longname)
        
        if self.storage not in (None, 'uniform', 'varying'):
            raise TypeError('%s: storage must be None, uniform or varying' % self.longname) 

        if not self.aov and not self.isValid(self.default):
            raise TypeError('%s: invalid default value %s' % (self.longname, str(self.default)))
        
    def getDelight(self):
        if self.dltype and not self.norsl:
            args = []
            
            if self.init:
                args.append('init={%s}' % self.init)
                
            if self.sourceshapename:
                args.append('sourceshapename')
                
            if self.texture:
                args.append('texture')
            
            if self.prepare:
                args.append('prepare')
                    
            if self.storage and not self.sourceshapename and not self.texture and not self.prepare:
                args.append(self.storage)

            if self.isArray():
                args.append(self.dltype + '[]')
            else:
                args.append(self.dltype)
    
            args.append(self.getDelightName())

            return ' '.join(args)
        else:
            return None

    def getRSL(self):
        if self.rsltype and not self.norsl:
            args = []
            
            if self.output or self.aov:
                args.append('output')
            
            if self.storage:
                args.append(self.storage)
            
            args.append(self.rsltype)
    
            if self.aov or self.message:
                prefix = ''
            else:
                if self.output:
                    prefix = 'o_'
                else:
                    prefix = 'i_'
    
            array = self.isArray()
            
            if self.rsllength > 1:
                arraydecl = '[%d]' % self.rsllength
            elif array:
                arraydecl = '[]'
            else:
                arraydecl = ''
            
            args.append('%s%s%s' % (prefix, self.longname, arraydecl))
            
            if self.aov:
                args.append('=')
                args.append(repr(self.rsldefault))
            
            return ' '.join(args)
        else:
            return None

    def getRSLValue(self, value):
        raise NotImplementedError()

    def setAttributeFlags(self, attr):
        if self.output:
            attr.setStorable(False)
            attr.setWritable(False)
            attr.setKeyable(False)
        else:
            if self.storable != None:
                attr.setStorable(self.storable)
            if self.writable != None:
                attr.setWritable(self.writable)
            if self.keyable != None:
                attr.setKeyable(self.keyable)
        if self.connectable != None:
                attr.setConnectable(self.connectable)
        if self.readable != None:
            attr.setReadable(self.readable)
        if self.hidden != None:
            attr.setHidden(self.hidden)
        if self.array != None :
            attr.setArray(self.array and self.multi)
            if self.indexmatters != None:
                attr.setIndexMatters(self.indexmatters)
        if self.dynamic != None:
            attr.setDynamic(self.dynamic)
        if  self.internal != None:
            attr.setInternal(self.internal)

    def addAttributes(self):
        if not self.aov and not self.message and not self.nomaya:
            try:
                MPxNode.addAttribute(self.obj)
            except Exception, e:
                raise RuntimeError(str(e) + ' (%s, %s)' % (self.longname, self.shortname))

    def getTemplate(self):
        template = ''
        if not self.hidden and not self.notemplate and not self.output and not self.aov and not self.message and not self.suppress:
            if self.nooptimize:
                template += """
                    editorTemplate -beginNoOptimize;\n"""
            template += """
                    editorTemplate"""
            if self.label != None:
                template += ' -label "%s"' % self.label 
            if self.help != None:
                template += ' -annotation "%s"' % self.getAnnotation()
            template += ' -addControl "%s"' % self.longname
            template += ';\n'
            if self.nooptimize:
                template += """                
                    editorTemplate -endNoOptimize;\n"""
        elif self.notemplate:
            template += """                
                    editorTemplate -suppress "%s";\n""" % self.longname 

        return template

    def getAnnotation(self):
        # reformat the help
        annotation = re.sub(r'\s+', ' ', self.help)
        annotation = textwrap.fill(annotation, 50)
        # escape quotes and newlines
        annotation = annotation.replace('"', r'\"')
        annotation = annotation.replace('\n', r'\n')
        return annotation

    def getHelpers(self):
        return None

    @staticmethod
    def getShortnameFromLongname(longname):
        # following formula:
        #   input1D -> i1
        #   inputX -> ix
        #   someVariableName -> svn
        buf = longname[1:].replace('1D', '1').replace('2D', '2').replace('3D', '3').replace('4D', '4')
        return longname[0].lower() + ''.join([c.lower() for c in buf if c.isupper() or c.isdigit()])

    def getLongname(self):
        return self.__dict__['longname']
    def setLongname(self, longname):
        self.__dict__['longname'] = longname
        # if the short name hasn't been set, approximate one
        if self.shortname == None:
            self.shortname = self.getShortnameFromLongname(longname)
    longname = property(getLongname, setLongname)

    def getShortname(self):
        return self.__dict__['shortname']
    def setShortname(self, shortname):
        self.__dict__['shortname'] = shortname
    shortname = property(getShortname, setShortname)

    def getData(self, data):
        if isinstance(data, MDataBlock):
            if self.array and self.multi:
                if self.output:
                    return ArrayDataHandleIterator(data.outputArrayValue(self.obj), self.output)
                else:
                    return ArrayDataHandleIterator(data.inputArrayValue(self.obj), self.output)
            else:
                if self.output:
                    return data.outputValue(self.obj)
                else:
                    return data.inputValue(self.obj)
        else:
            return data

    def getValue(self, data):
        dataHandle = self.getData(data)
        return self.cast(dataHandle)

    def getChildValue(self, data):
        dataHandle = self.getData(data).child(self.obj)
        return self.cast(dataHandle)
    
    def setValue(self, data, value):
        dataHandle = self.getData(data) 
        self.set(dataHandle, value)
        dataHandle.setClean()
        
    def setChildValue(self, data, value):
        dataHandle = self.getData(data).child(self.obj)
        self.set(dataHandle, value)
        dataHandle.setClean()


class Float(Attribute):
    rsltype = 'float'
    dltype = 'float'

    __defaultArgs = {'min': None,
                     'max': None,
                     'softmin': 0,
                     'softmax': 1,
                     'default': 0,
                     'rsldefault': 0}

    def __init__(self, **kwargs): 
        self.setDefaults(Float.__defaultArgs)
        super(Float, self).__init__(**kwargs)

    def isValid(self, value):
        return isinstance(value, (int, float))

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnNumericData.kFloat, self.sanitize(self.default))
            self.setAttributeFlags(attr)
            self.setAttributeMinMax(attr)

    def setAttributeMinMax(self, attr):
        if self.min != None:
            attr.setMin(self.sanitize(self.min))
        if self.max != None:
            attr.setMax(self.sanitize(self.max))
        if self.softmin != None:
            attr.setSoftMin(self.sanitize(self.softmin))
        if self.softmax != None:
            attr.setSoftMax(self.sanitize(self.softmax))
        
    def sanitize(self, value):
        return float(value)

    def cast(self, dataHandle):
        return dataHandle.asFloat()        

    def set(self, dataHandle, value):
        dataHandle.setFloat(value)

    def getRSLValue(self, value):
        return float(value)

class Enum(Float):
    __defaultArgs = {'choices': None,
                     'softmin': None,
                     'softmax': None,
                     'storage': 'uniform'}
#                     'addbuttonlabel':"Add LABEL"}
    
    def __init__(self, **kwargs): 
        self.setDefaults(Enum.__defaultArgs)
        super(Enum, self).__init__(**kwargs)
    
#    def getHelpers(self):
#        # copied from AEfileTemplate.mel
#        helpers = \
#        r"""
#            
#            source AEnewNonNumericMulti;
#           
#            global proc AETEMPLATE_LONGNAME_MultiEnumNew (string $attr)
#            {
#                setUITemplate -pst attributeEditorTemplate;
#                columnLayout -adj 1;
#                    frameLayout -l "LABEL";
#                        columnLayout -adj 1;
#                            button -l "ADDBUTTONLABEL" AETEMPLATE_LONGNAME_multiEnumAddButton;
#                            columnLayout -adj 1 AETEMPLATE_LONGNAME_multiEnumLayout;
#                            setParent ..;
#                        setParent ..;
#                    setParent ..;
#                setParent ..;
#                setUITemplate -ppt;
#                
#                AETEMPLATE_LONGNAME_MultiEnumReplace $attr;
#            }
#            
#            global proc AETEMPLATE_LONGNAME_MultiEnumReplace (string $attr)
#            {
#                string $nodeattr[];
#                tokenize($attr, ".", $nodeattr);
#                string $command = "AEnewNonNumericMultiAddNewItem " + $nodeattr[0] + " "+ $nodeattr[1];
#            
#                button -e -c $command AETEMPLATE_LONGNAME_multiEnumAddButton;
#                
#                string $old[] = `columnLayout -q -ca AETEMPLATE_LONGNAME_multiEnumLayout`;
#                if(size($old))
#                    deleteUI($old);
#                    
#                string $multi[] = `listAttr -multi $attr`;
#                for($a in $multi){
#                    string $plugName = ($nodeattr[0] + "." + $a);
#                    rowLayout -nc 2 -adj 1 -cw 2 24 -p AETEMPLATE_LONGNAME_multiEnumLayout;
#                    attrControlGrp -attribute $plugName;
#                    symbolButton
#                    -image "smallTrash.xpm" 
#                    -command ("AEremoveMultiElement " + $plugName);
#                }
#            }
#            
#            
#        """.replace('LONGNAME', self.longname)
#        if self.addbuttonlabel != None:
#            helpers = helpers.replace('ADDBUTTONLABEL', self.addbuttonlabel)
#        else:
#            helpers = helpers.replace('ADDBUTTONLABEL', '')  
#                    
#        if self.help != None:
#           helpers = helpers.replace('HELP', self.getAnnotation())
#        else:
#            helpers = helpers.replace('HELP', '')
#        if self.label != None:
#            helpers = helpers.replace('LABEL', self.label)
#        else:
#            helpers = helpers.replace('LABEL', '')
#          
#        return helpers
#            
#    def getTemplate(self):
#        if not self.hidden and not self.notemplate and self.output != True and self.array:
#            return (r"""
#                editorTemplate -callCustom "AETEMPLATE_LONGNAME_MultiEnumNew" 
#                                           "AETEMPLATE_LONGNAME_MultiEnumReplace" 
#                                           "%s";
#            """ % self.longname).replace('LONGNAME', self.longname)
#        else:
#            return ''
        
    def validate(self):
        super(Enum, self).validate()
        if not isinstance(self.choices, list) or \
           not all([isinstance(i, str) for i in self.choices]):
            raise TypeError('%s: choices must be a list of strings' % self.longname)
        
    def isValid(self, value):
        return value in self.choices

    def sanitize(self, value):
        return value
        
    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnEnumAttribute()
            self.obj = attr.create(self.longname, self.shortname, self.choices.index(self.sanitize(self.default)))
            self.setAttributeFlags(attr)
            for v in self.choices:
                attr.addField(v, self.choices.index(self.sanitize(v)))

    def cast(self, dataHandle):
        return dataHandle.asInt()        

    def set(self, dataHandle, value):
        dataHandle.setInt(value)

    
class Boolean(Float):
    __defaultArgs = {'default': False,
                     'softmin': None,
                     'softmax': None,
                     'storage': 'uniform',
                     'nooptimize': True}
    
    def __init__(self, **kwargs): 
        self.setDefaults(Boolean.__defaultArgs)
        super(Boolean, self).__init__(**kwargs)
    
    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnNumericData.kBoolean, self.sanitize(self.default))
            self.setAttributeFlags(attr)

    def isValid(self, value):
        return isinstance(value, bool)

    def cast(self, dataHandle):
        return dataHandle.asBool()        

    def set(self, dataHandle, value):
        dataHandle.setBool(value)


class Integer(Float):
    __defaultArgs = {'softmin': 0,
                     'softmax': 100,
                     'storage': 'uniform'}
    
    def __init__(self, **kwargs): 
        self.setDefaults(Integer.__defaultArgs)
        super(Integer, self).__init__(**kwargs)

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnNumericData.kLong, self.sanitize(self.default))
            self.setAttributeFlags(attr)

    def isValid(self, value):
        return isinstance(value, int)

    def cast(self, dataHandle):
        return dataHandle.asInt()        

    def set(self, dataHandle, value):
        dataHandle.setInt(value)


class IntArray(Attribute):
    
    __defaultArgs = {'default':[]}

    def __init__(self, **kwargs): 
        self.setDefaults(IntArray.__defaultArgs)
        super(IntArray, self).__init__(**kwargs)
        
    def isValid(self, value):
        return isinstance(value, (tuple, list))
    
    def sanitize(self, value):
        asIntArray = MIntArray()
        if isinstance(value, (tuple, list)):
            for item in value:
                asIntArray.append(item)
        return asIntArray

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnTypedAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnData.kIntArray)
            self.setAttributeFlags(attr)            
            defaultObj = MFnIntArrayData().create(self.sanitize(self.default))
            attr.setDefault(defaultObj)
            
class StringArray(Attribute):
    __defaultArgs = {'default':[]}
    def __init__(self, **kwargs): 
        self.setDefaults(StringArray.__defaultArgs)
        super(StringArray, self).__init__(**kwargs)
        
    def isValid(self, value):
        return isinstance(value, (tuple, list))
    
    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnTypedAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnData.kStringArray)
            self.setAttributeFlags(attr)            
                        

class ColorArray(Attribute):
        
    dltype = 'color'
    rsltype = 'color'
    
    __defaultArgs = {'default':[],
                     'array':True,
                     'multi':False
                    }
    def __init__(self, **kwargs): 
        self.setDefaults(ColorArray.__defaultArgs)
        super(ColorArray, self).__init__(**kwargs)
        
    def isValid(self, value):
        return isinstance(value, (tuple, list))
    
    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnTypedAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnData.kVectorArray)
            self.setAttributeFlags(attr)            
                       
class FloatArray(Attribute):
        
    dltype = 'float'
    rsltype = 'float'
    
    __defaultArgs = {'default':[],
                     'array':True,
                     'multi':False
                    }
    def __init__(self, **kwargs): 
        self.setDefaults(FloatArray.__defaultArgs)
        super(FloatArray, self).__init__(**kwargs)
        
    def isValid(self, value):
        return isinstance(value, (tuple, list))
    
    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnNumericData.kFloat)
            self.setAttributeFlags(attr)    
            
class FloatN(Float):
    length = None
    rsllength = None
    mayatype = MFnNumericData.kFloat
    __defaultArgs = {'longnames': None,
                     'shortnames': None}

    def __init__(self, **kwargs): 
        self.setDefaults(FloatN.__defaultArgs)
        super(FloatN, self).__init__(**kwargs)
        if isinstance(self.default, (float, int)):
            self.default = [self.default for i in range(0, self.length)]

    def isValid(self, value):
        return isinstance(value, (float, int)) or \
            (isinstance(value, (tuple, list)) and len(value) == self.length and \
             all([isinstance(i, (float, int)) for i in value]))

    def sanitize(self, value):
        if isinstance(value, (tuple, list)):
            return map(lambda i: float(i), value)
        else:
            return [float(value) for i in range(0, self.length)]

    def getChildSuffix(self, index):
        return str(index+1)

    # override the property set method
    def setLongname(self, longname):
        super(FloatN, self).setLongname(longname)
        if self.longnames == None:
            self.longnames = [self.longname + self.getChildSuffix(i) for i in range(0, self.length)]
    longname = property(Float.getLongname, setLongname)

    def setShortname(self, shortname):
        super(FloatN, self).setShortname(shortname)
        if self.shortnames == None:
            self.shortnames = [self.shortname + self.getChildSuffix(i)[0].lower() for i in range(0, self.length)]
    shortname = property(Float.getShortname, setShortname)

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
    
            default = self.sanitize(self.default)
    
            cattrs = [None]*self.length
            cobjs = [None]*self.length
            for i in range(0, self.length):
                cattrs[i] = MFnNumericAttribute()
                cobjs[i] = cattrs[i].create(self.longnames[i], self.shortnames[i], self.mayatype, default[i])
                self.setAttributeMinMax(cattrs[i], i)
    
            self.obj = attr.create(self.longname, self.shortname, *cobjs)
            self.setAttributeFlags(attr)

    def setAttributeMinMax(self, attr, index):
        if self.min != None:
            attr.setMin(self.sanitize(self.min)[index])
        if self.max != None:
            attr.setMax(self.sanitize(self.max)[index])
        if self.softmin != None:
            attr.setSoftMin(self.sanitize(self.softmin)[index])
        if self.softmax != None:
            attr.setSoftMax(self.sanitize(self.softmax)[index])

class Float2(FloatN):
    length = 2
    rsllength = 2
    dltype = 'float2'

    def cast(self, dataHandle):
        return dataHandle.asFloat2()        

    def set(self, dataHandle, value):
        dataHandle.set2Float(value[0], value[1])


class UV(Float2):
    __defaultArgs = { 'init': 'ss,tt' }

    def __init__(self, **kwargs): 
        self.setDefaults(UV.__defaultArgs)
        super(UV, self).__init__(**kwargs)

    def getChildSuffix(self, index):
        return ('U', 'V')[index]
        

class Float3(FloatN):
    length = 3
    rsllength = 3
    dltype = 'float3'

    def cast(self, dataHandle):
        return dataHandle.asFloat3()        

    def set(self, dataHandle, value):
        dataHandle.set3Float(value.x, value.y, value.z)


class Color(Float3):
    rsllength = 1
    dltype = 'color'
    rsltype = 'color'
    __defaultArgs = {'default': 1}

    def __init__(self, **kwargs): 
        self.setDefaults(Color.__defaultArgs)
        super(Color, self).__init__(**kwargs)

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.createColor(self.longname, self.shortname)
            self.setAttributeFlags(attr)
            default = self.sanitize(self.default)
            attr.setDefault(default[0], default[1], default[2])

    def set(self, dataHandle, value):
        dataHandle.set3Float(value.r, value.g, value.b)

    def getRSLValue(self, value):
        return 'color ('+', '.join([str(comp) for comp in value])+')'

class PointLike(Float3):
    rsllength = 1
    __defaultArgs = {'default': 0}

    def __init__(self, **kwargs): 
        self.setDefaults(PointLike.__defaultArgs)
        super(PointLike, self).__init__(**kwargs)

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.createPoint(self.longname, self.shortname)
            self.setAttributeFlags(attr)
            default = self.sanitize(self.default)
            attr.setDefault(default[0], default[1], default[2])

    def getChildSuffix(self, index):
        return ('X', 'Y', 'Z')[index]


class Point(PointLike):
    dltype = 'point'
    rsltype = 'point'

    def set(self, dataHandle, value):
        dataHandle.set3Float(value.x, value.y, value.z)

    def getRSLValue(self, value):
        return 'point ('+', '.join([str(comp) for comp in value])+')'


class Vector(PointLike):
    dltype = 'vector'
    rsltype = 'vector'

    def set(self, dataHandle, value):
        dataHandle.set3Float(value.x, value.y, value.z)

    def getRSLValue(self, value):
        return 'vector ('+', '.join([str(comp) for comp in value])+')'


class Normal(Vector):
    dltype = 'normal'
    rsltype = 'normal'

    def getRSLValue(self, value):
        return 'normal ('+', '.join([str(comp) for comp in value])+')'


class Matrix(Attribute):
    rsltype = 'matrix'
    dltype = 'matrix'
    __defaultArgs = {'default': 1}
    
    def __init__(self, **kwargs): 
        self.setDefaults(Matrix.__defaultArgs)
        super(Matrix, self).__init__(**kwargs)

    def isValid(self, value):
        return isinstance(value, (float, int)) or \
            isinstance(value, (tuple, list)) and len(value) == 4 and \
            all([isinstance(j, (tuple, list)) and len(j) == 4 for j in value]) and \
            all([isinstance(i, (float, int)) for i in j for j in value])

    def sanitize(self, value):
        if isinstance(value, (tuple, list)):
            return map(lambda i: map(lambda j: float(j), i), value)
        else:
            return [[float(value), 0.0, 0.0, 0.0],
                    [0.0, float(value), 0.0, 0.0],
                    [0.0, 0.0, float(value), 0.0],
                    [0.0, 0.0, 0.0, float(value)]]

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnMatrixAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnMatrixAttribute.kFloat)
            self.setAttributeFlags(attr)
            default = self.sanitize(self.default)
            # TODO: no apparent way to set matrix values in the Python API?
            # this doesn't work
            #if isinstance(default, float):
            #    attr.setDefault(MFloatMatrix([[default, 0.0, 0.0, 0.0],
            #                                       [0.0, default, 0.0, 0.0],
            #                                       [0.0, 0.0, default, 0.0],
            #                                       [0.0, 0.0, 0.0, default]])
            #else:
            #    attr.setDefault(MFloatMatrix(default))

    def cast(self, dataHandle):
        return dataHandle.asFloatMatrix()        

    def set(self, dataHandle, value):
        dataHandle.setMFloatMatrix(value)


class String(Attribute):
    rsltype = 'string'
    dltype = 'string'
    __defaultArgs = {'default': '',
                     'keyable': False,
                     'rsldefault': '',
                     'storage': 'uniform'}

    def __init__(self, **kwargs): 
        self.setDefaults(String.__defaultArgs)
        super(String, self).__init__(**kwargs)

    def isValid(self, value):
        return isinstance(value, str)

    def sanitize(self, value):
        return value

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnTypedAttribute()
            self.obj = attr.create(self.longname, self.shortname, MFnData.kString)
            self.setAttributeFlags(attr)
            strdata = MFnStringData()
            strdataobj = strdata.create()
            strdata.set(self.default)
            attr.setDefault(strdataobj)

    def cast(self, dataHandle):
        return OpenMaya.MFnStringData(dataHandle.data()).string()

    def set(self, dataHandle, value):
        dataHandle.setString(value)

    def getRSLValue(self, value):
        return '"'+value+'"'


class File(String):
    
    def getHelpers(self):
        # copied from AEfileTemplate.mel
        helpers = \
        r"""
            global proc int AETEMPLATE_LONGNAME_AssignTextureCB( string $fileAttribute,
                                                 string $filename,
                                                 string $fileType )
            {
                //
                // Description:
                //    This procedure is called when the user changes the file texture name in
                //    the edit box in the file texture attribute editor (whether by manually
                //    typing it in, or by using the file browser to choose a new file).
                //
                //    This procedure updates the file texture node file name attribute and
                //    calls AETEMPLATE_LONGNAME_TextureNameChanged to do some special case handling for 
                //    files with alpha channels. 
                //
            
                setAttr $fileAttribute -type "string" $filename;
            
                string $currentDir = `workspace -q -dir`;
                retainWorkingDirectory ($currentDir);
            
                // Extract the name of the node from the node.attribute name
                //
                string $tokenArray[];
                tokenize($fileAttribute, ".", $tokenArray);
            
                string $fileNode = $tokenArray[0];
            
                return true;
            }
            
            global proc AETEMPLATE_LONGNAME_TextureBrowser( string $cmd )
            {
                string  $workspace = `workspace -q -fn`;
                setWorkingDirectory $workspace "image" "sourceImages";
                
                fileBrowser ($cmd, "Open", "", 0);
            }
            
            global proc AETEMPLATE_LONGNAME_TextureNameNew (string $fileAttribute)
            {
                setUITemplate -pst attributeEditorTemplate;
                rowLayout -nc 3 AETEMPLATE_LONGNAME_textureNameLayout;
                    string $label = "LABEL";
                    if (size($label) == 0)
                        $label = interToUI("LONGNAME");
                    text -l $label -ann "HELP";
                    textField -ann "HELP" AETEMPLATE_LONGNAME_textureNameField;
                    symbolButton -ann "HELP" -image "navButtonBrowse.xpm" AETEMPLATE_LONGNAME_textureBrowserButton;
                setParent ..;
                setUITemplate -ppt;
                
                AETEMPLATE_LONGNAME_TextureNameReplace $fileAttribute;
            }
            
            global proc AETEMPLATE_LONGNAME_TextureNameReplace (string $fileAttribute)
            {
                connectControl -index 2 -fileName AETEMPLATE_LONGNAME_textureNameField $fileAttribute;
            
                string $command = "AETEMPLATE_LONGNAME_AssignTextureCB "+" "+$fileAttribute;
            
                button -e -c
                    ("AETEMPLATE_LONGNAME_TextureBrowser \"" + $command + "\"" ) AETEMPLATE_LONGNAME_textureBrowserButton;
            }
            
        """.replace('LONGNAME', self.longname)
        if self.help != None:
           helpers = helpers.replace('HELP', self.getAnnotation())
        else:
            helpers = helpers.replace('HELP', '')
        if self.label != None:
            helpers = helpers.replace('LABEL', self.label)
        else:
            helpers = helpers.replace('LABEL', '')
        return helpers
            
    def getTemplate(self):
        if not self.hidden and not self.notemplate and self.output != True:
            return (r"""
                editorTemplate -callCustom "AETEMPLATE_LONGNAME_TextureNameNew" 
                                           "AETEMPLATE_LONGNAME_TextureNameReplace" 
                                           "%s";
            """ % self.longname).replace('LONGNAME', self.longname)
        else:
            return ''
            
    def buildTemplate(self):
        if not self.hidden and not self.notemplate and not self.output:
            pass
            
class Image(File):
    __defaultArgs = {'texture': True}
    
    def __init__(self, **kwargs): 
        self.setDefaults(Image.__defaultArgs)
        super(Image, self).__init__(**kwargs)


class Message(String):
    rsltype = 'string'
    dltype = 'string'
    __defaultArgs = {'sourceshapename': True,
                     'rsldefault': None,
                     'storage': 'uniform',
                     'connectable': True}

    def __init__(self, **kwargs):
        self.setDefaults(Message.__defaultArgs)
        super(Message, self).__init__(**kwargs)

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnMessageAttribute()
            self.obj = attr.create(self.longname, self.shortname)
            self.setAttributeFlags(attr)

class CoordinateSystem(String):
    class CoordinateSystemCallCustom(CallCustom):
        def new(self, plug):
            plug = pm.Attribute(plug)
            with pm.ui.UITemplate("attributeEditorTemplate"):
                with pm.rowLayout(numberOfColumns=3, adjustableColumn=2) as self._coordsysLayout:
                    if not self.attr.label:
                        label = pm.interToUI(self.attr.longname)
                    else:
                        label = self.attr.label
                    pm.text(label=label, annotation=self.attr.help)
                    self._coordsys = pm.textField(annotation=help)
                    self._browserButton = pm.symbolButton(image="coordsys.png", annotation=self.attr.help)
                    self._popupMenu = pm.popupMenu(parent=self._browserButton, button=1)
            
            self.replace(str(plug))
        
        def replace(self, plug):
            plug = pm.Attribute(plug)
            pm.connectControl(self._coordsys.name(), plug, index=2)
            
            # populate the popup menu with coordinate systems
            self._popupMenu.deleteAllItems()
            
            with self._popupMenu:
                objects = []
                
                # include the default, if any
                if self.attr.default:
                    objects.append(self.attr.default)
                
                # add 3delight coordinate systems
                objects.extend(pm.ls(type="delightCoordinateSystem"))
                
                # TODO: add maya cameras
                
                for obj in objects:
                    pm.menuItem(label=str(obj), command=lambda arg, plug=plug, coordsys=obj: plug.set(coordsys))

                if objects:
                    pm.menuItem(divider=True)

                pm.menuItem(label="Create New Coordinate System", boldFont=True,
                            command=lambda arg, plug=plug: plug.set(self._createCoordsys()))
    
        @staticmethod
        def _createCoordsys():
            new_node = pm.createNode("delightCoordinateSystem", name="delightCoordinateSystemShape1", skipSelect=True)
            pm.mel.DL_setVersionAttr(new_node)
            pm.mel.DCS_init(new_node)
            return new_node
    
    __defaultArgs = {'callcustom': CoordinateSystemCallCustom}
    
    def __init__(self, **kwargs):
        self.setDefaults(CoordinateSystem.__defaultArgs)
        super(CoordinateSystem, self).__init__(**kwargs)
        
    def getTemplate(self):
        if not self.hidden and not self.notemplate and self.output != True:
            return (r"""
                editorTemplate -callCustom "AETEMPLATE_LONGNAME_New" 
                                           "AETEMPLATE_LONGNAME_Replace" 
                                           "%s";
            """ % self.longname).replace('LONGNAME', self.longname)
        else:
            return ''

class Address(Attribute):
    def isValid(self, value):
        return True

    def sanitize(self, value):
        return value

    def createAttributes(self):
        if not self.aov and not self.message:
            attr = MFnNumericAttribute()
            self.obj = attr.createAddr(self.longname, self.shortname)
            self.setAttributeFlags(attr)

    
class Compound(Attribute, Container):
    __defaultArgs = {'keyable': False,
                     'affect': False}
    
    def __init__(self, children, **kwargs):
        self.setDefaults(Compound.__defaultArgs)
        super(Compound, self).__init__(children, **kwargs)

    def validate(self):
        super(Compound, self).validate()

    def isValid(self, value):
        return True

    def getRSL(self):
        return None

    def getDelight(self):
        return None

    def createAttributes(self):
        if not self.aov and not self.message:
            for child in self.children:
                child.createAttributes()
    
            attr = MFnCompoundAttribute()
            self.obj = attr.create(self.longname, self.shortname)
            self.setAttributeFlags(attr)
            
            for child in self.children:
                attr.addChild(child.obj)

    def getHelpers(self):
        if not self.hidden and not self.notemplate and not self.output and isinstance(self.callcustom, basestring):
            helpers = self.callcustom
        else:
            return ''
             
        return helpers.replace('LONGNAME', self.longname)
    
    def getTemplate(self):
        if self.label == None:
            name = '(interToUI(\"%s\"))' % self.longname
        else:
            name = '("%s")' % self.label
        if not self.hidden and not self.notemplate and not self.output and self.callcustom != None:
            template = r"""
                editorTemplate -beginLayout %s  -collapse 1;
                editorTemplate -callCustom "AETEMPLATE_LONGNAME_New"
                                           "AETEMPLATE_LONGNAME_Replace"
                                           "LONGNAME";
                editorTemplate -endLayout;
                editorTemplate -suppress "LONGNAME";
                """ % name
            for attr in self.children:
                template += '                editorTemplate -suppress "%s";\n' % attr.longname
            return template.replace('LONGNAME', self.longname)
        else:
            return super(Compound, self).getTemplate()

class Ramp(Compound):
    __interpChoices = ['None', 'Linear', 'Smooth', 'Spline']
    
    def __init__(self, **kwargs):
        super(Ramp, self).__init__([], array=True, **kwargs)

        default = self.sanitize(self.default)

        self.positionAttribute = Float(suffix='_Position',
                                        shortname=self.shortname + 'p',
                                        default=default[0])
        self.valueAttribute = self.createValueAttribute(default[1])
        self.interpAttribute = Enum(suffix='_Interp',
                                     shortname=self.shortname + 'i',
                                     default=default[2],
                                     choices=self.__interpChoices)
        self.children = [self.positionAttribute, self.valueAttribute, self.interpAttribute]
    
    def createValueAttribute(self):
        raise NotImplementedError
        
    def isValidValue(self, value):
        raise NotImplementedError
    
    def isValid(self, value):
        return isinstance(value, (tuple, list)) and \
                len(value) == 3 and \
                isinstance(value[0], (int, float)) and \
                self.isValidValue(value[1]) and \
                value[2] in self.__interpChoices

    def sanitizeValue(self, value):
        raise NotImplementedError
        
    def sanitize(self, value):
        return [float(value[0]), 
                self.sanitizeValue(value[1]),
                value[2]]

    def getTemplate(self):
        if not self.hidden and not self.notemplate and self.output != True:
            return r"""
                AEaddRampControl ($node + ".%s");
            """ % self.longname
        else:
            return ''

    # override the property set method
    def setLongname(self, longname):
        super(Ramp, self).setLongname(longname)
        for child in self.children:
            child.longname = self.longname + child.suffix
    longname = property(Compound.getLongname, setLongname)


class FloatRamp(Ramp):
    def createValueAttribute(self, default):
        return Float(suffix='_FloatValue',
                          shortname=self.shortname + 'fv',
                          default=default)
        
    def isValidValue(self, value):
        return isinstance(value, (float, int))
        
    def sanitizeValue(self, value):
        return float(value)
 
    
class ColorRamp(Ramp):
    def createValueAttribute(self, default):
        return Color(suffix='_Color',
                     shortname=self.shortname + 'c',
                     default=default)
        
    def isValidValue(self, value):
        return isinstance(value, (float, int)) or \
            (isinstance(value, (tuple, list)) and len(value) == 3 and \
             all([isinstance(i, (float, int)) for i in value]))

    def sanitizeValue(self, value):
        if isinstance(value, (tuple, list)):
            return map(lambda i: float(i), value)
        else:
            return [float(value), float(value), float(value)]


class LightData(Compound):
    __defaultArgs = {'lightDirection': None,
                     'lightIntensity': None,
                     'lightAmbient': None,
                     'lightDiffuse': None,
                     'lightSpecular': None,
                     'lightShadowFraction': None,
                     'preShadowIntensity': None,
                     'lightBlindData': None}
    
    def __init__(self, **kwargs): 
        self.setDefaults(LightData.__defaultArgs)
        super(LightData, self).__init__([kwargs['lightDirection'],
                                              kwargs['lightIntensity'],
                                              kwargs['lightAmbient'],
                                              kwargs['lightDiffuse'],
                                              kwargs['lightSpecular'],
                                              kwargs['lightShadowFraction'],
                                              kwargs['preShadowIntensity'],
                                              kwargs['lightBlindData']], **kwargs)
        
    def validate(self):
        super(LightData, self).validate()
        if not isinstance(self.lightDirection, Vector) or \
           not isinstance(self.lightIntensity, Color) or \
           not isinstance(self.lightAmbient, Boolean) or \
           not isinstance(self.lightDiffuse, Boolean) or \
           not isinstance(self.lightSpecular, Boolean) or \
           not isinstance(self.lightShadowFraction, Float) or \
           not isinstance(self.preShadowIntensity, Float) or \
           not isinstance(self.lightBlindData, Address):
            raise TypeError('%s: missing additional lighting parameters' % self.longname)

    def isValid(self, value):
        return True

    def sanitize(self, value):
        return value

    def createAttributes(self):
        if not self.aov and not self.message:
            for child in self.children:
                child.createAttributes()
    
            attr = MFnLightDataAttribute()
            self.obj = attr.create(self.longname, self.shortname,
                                   self.lightDirection.obj,
                                   self.lightIntensity.obj,
                                   self.lightAmbient.obj,
                                   self.lightDiffuse.obj,
                                   self.lightSpecular.obj,
                                   self.lightShadowFraction.obj,
                                   self.preShadowIntensity.obj,
                                   self.lightBlindData.obj)
            self.setAttributeFlags(attr)

    def getTemplate(self):
        return ''

    def getDelight(self):
        return None
    
    def getRSL(self):
        return None


class ComponentData(Compound):
    
    rsltype = 'void'
    dltype = 'void'
    
    channels = filter(lambda channel: channel.component, components.channels)
    
    __defaultArgs = {}
    
    def getRSL(self):
        # HUMMM: Overriding Compound override
        return Attribute.getRSL(self)
#    
    def getDelight(self):
        # HUMMM: Overriding Compound override
        return Attribute.getDelight(self)
    
    def __init__(self, **kwargs):
        self.setDefaults(ComponentData.__defaultArgs)
        super(ComponentData, self).__init__(**kwargs)    
 
