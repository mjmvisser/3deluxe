import string

from maya.OpenMaya import *

import deluxe
 
class dl_layer(deluxe.ShadingCodeComponent):
    typeid = 0x00310010
    classification = "rendernode/3delight/material:shader/surface"
    description = "Generic layered shader."
    
    # 
    includes = ["blend_utils.h",  "displacement_utils.h"]    
    
    # Used for easy code generation replacement
    _codetokens = {}
   
    # Utility functions parameters (in dl_layer.h)
    blendLightsetsFgInputs = [deluxe.Color(longname='fg_opacity')]
    blendLightsetsBgInputs = [deluxe.Color(longname='bg_opacity')]
    blendLightsetsOutputs = []
    
    # Input and output component compound attributes children
    layerComponentChildren = []
    
    # Shading component channels, build compound attributes children and utility functions parameters
    channels = deluxe.ComponentData.channels
    for channel in channels:
        inmsg='component_%s'%channel.longname
        if channel.array:
            exec 'blendLightsetsFgInputs.append(deluxe.%s(longname="fg_%s", utility=True))'%(channel.apitype, channel.longname)
            exec 'blendLightsetsBgInputs.append(deluxe.%s(longname="bg_%s", utility=True))'%(channel.apitype, channel.longname)
            exec 'blendLightsetsOutputs.append(deluxe.%s(longname="%s", output=True, utility=True))'%(channel.apitype, channel.longname)
        exec '%s = deluxe.%s(shortname="l%s", norsl=True)'%(inmsg, channel.type, channel.shortname)
        exec 'layerComponentChildren.append(%s)'%inmsg

    
    # UTILITY FUNCTIONS
    utilfuncs = []
    for type in ['Float', 'Color']:
        
        blendBase = 'blend%ss'%type
        blendFunc = '%sFunc'%blendBase
        blendCode = '\tcolor resultColor, resultOpacity;\n'
        if type == 'Float':
            blendCode += '\tfloat premult = mix(1, luminance(i_fga), i_premult);\n'
            blendCode += '\tblend(i_mode, color(i_fg) * premult, i_fga, color(i_bg), i_bga, resultColor, resultOpacity);\n'
            blendCode += '\treturn comp(resultColor, 0);'
        else:
            blendCode += '\tcolor premult = mix(color 1, i_fga, i_premult);\n'
            blendCode += '\tblend(i_mode, i_fg * premult, i_fga, i_bg, i_bga, resultColor, resultOpacity);\n'
            blendCode += '\treturn resultColor;'

        exec "%s = deluxe.Function(name='%s', type='%s', inputs=[deluxe.Float(longname='mode', storage='uniform'), deluxe.Float(longname='premult'), deluxe.%s(longname='fg'), deluxe.Color(longname='fga'), deluxe.%s(longname='bg'), deluxe.Color(longname='bga')])"%(blendFunc, blendBase, type.lower(), type, type)
        exec "%s.rsl = blendCode"%blendFunc
        exec "utilfuncs.append(%s)"%blendFunc
        
        
        accumBase = 'accumulate%ss'%type
        accumFunc = '%sFunc'%accumBase
        accumCode = """\
    uniform float size = arraylength(i_inputs);
    uniform float i;
    %s total = 0;
    for(i = 0; i < size; i+= 1)
    {
        total += i_inputs[i];
    }
    return total;
    """%type.lower()
    
        exec "%s = deluxe.Function(name='%s', type='%s', inputs=[deluxe.%s(longname='inputs', array=True)])"%(accumFunc, accumBase, type.lower(), type)
        exec "%s.rsl = accumCode"%accumFunc
        exec "utilfuncs.append(%s)"%accumFunc
        
        
        copyBase = 'copy%ss'%type
        copyFunc = '%sFunc'%copyBase
        copyCode = """\
    uniform float isize = arraylength(i_inputs);
    uniform float osize = arraylength(o_outputs);
    uniform float i;
    for(i = 0; i < isize &&  i < osize ; i += 1)
    {
        o_outputs[i] = i_inputs[i];
    }
    """
        exec "%s = deluxe.Function(name='%s', inputs=[deluxe.%s(longname='inputs', array=True)], outputs=[deluxe.%s(longname='outputs', array=True, output=True)])"%(copyFunc, copyBase, type, type )
        exec "%s.rsl = copyCode"%copyFunc
        exec "utilfuncs.append(%s)"%copyFunc

    #
    blendLightsetsInputs = [deluxe.Float(longname='mode', storage='uniform'), deluxe.Float(longname='premult')]
    blendLightsetsInputs.extend(blendLightsetsFgInputs)
    blendLightsetsInputs.extend(blendLightsetsBgInputs)
    blendLightsetsFunc = deluxe.Function(name='blendLightsets', inputs=blendLightsetsInputs, outputs=blendLightsetsOutputs)
    for channel in filter(lambda msg: msg.array, channels):
        blendLightsetsFunc.rsl += '\to_%s = blend%ss(i_mode, i_premult, i_fg_%s, i_fg_opacity, i_bg_%s, i_bg_opacity);\n'%(channel.longname, channel.apitype, channel.longname, channel.longname)
                        
    utilfuncs.append(blendLightsetsFunc)    
     
     
    puzzleAuxInputs = []
    puzzleDefaults = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for i in range(0, len(puzzleDefaults)):
        id = i + 1
        baseName = 'puzzle%d'%id
        exec '%s = deluxe.Color(shortname="pz%d", default=%s)'%(baseName, id, str(puzzleDefaults[i]))
        exec 'puzzleAuxInputs.append(%s)'%baseName
        
    calculateAuxiliariesInputs = [deluxe.Color(longname='opacity'), deluxe.Float(longname='premult'), deluxe.Color(longname='layerOpacities', array=True), deluxe.String(longname='layerNames',array=True)]
    calculateAuxiliariesInputs.extend(puzzleAuxInputs)
    calculateAuxiliariesFunc = deluxe.Function(name='calculateAuxiliaries', inputs=calculateAuxiliariesInputs)
    calculateAuxiliariesFunc.rsl = """
    extern point P;
    extern normal N;
    extern vector I;
    extern float u, v;
    extern float s, t;
    
    vector In = normalize(I);
    normal Nn = normalize(N);
    
     color premult = mix(color 1, i_opacity, i_premult);
"""

    auxAOVs = filter(lambda channel: channel.auxiliary, deluxe.components.channels)
    
    for aov in auxAOVs:
        calculateAuxiliariesFunc.rsl += '\n\textern %s %s;\n'%(aov.rsltype, aov.longname)
        calculateAuxiliariesFunc.rsl += '\t%s = %s;\n'%(aov.longname, aov.code)
    
    
    utilfuncs.append(calculateAuxiliariesFunc)
    
    
    # ATTRIBUTES

    #
    displayOpacity = deluxe.Color(shortname='do', norsl=True)
    displayColor = deluxe.Color(shortname='dc', norsl=True)
    
    
     # A global opacity multiplier
    globalOpacity = deluxe.Color(shortname='go', default=1.0, affect=False)
    
    # Global displacement scale 
    displacementGlobalScale = deluxe.Float(shortname='dsc', default=1.0, affect=False)
    
    # Global displacement offset 
    displacementGlobalOffset = deluxe.Float(shortname='dof', default=0.0, affect=False)
    
    #  
    displacementCompensateScale = deluxe.Boolean(shortname='dcs', default=False, affect=False)
    #   
#    displacementUseNormalMap = deluxe.Boolean(default=False, storage='uniform',
#        help="If on, the normal is set by an input to the normalMap parameter, typically a texture.")
    
    #
#    displacementNormalMap = deluxe.Color(default=0, storage='varying',
#        help="""If the useNormalMap parameter is on, this sets the normal.
#        Typically you would input a colour texture of a worldspace normal map.
#        """)
    
    # Arbitrary max lightset count
    lightSetsCount = deluxe.Integer(shortname='lsc', norsl=True, default=1, min=1, max=16, affect=False)
    
    # Layers blend order
    order = deluxe.IntArray(shortname='ord', affect=False, norsl=True)
    actualOrder = deluxe.IntArray(shortname='aord', output=True, internal=True, norsl=True)
    
    # Layer compound attribute children
    # Layer name, mostly used as a label but could be used to name per layer AOVs if we decide to output them
    layer_name = deluxe.String(shortname='lnm', utility=True, affect=False)
    
    #
    blendModes=['Over', 'Under', 'In', 'Out', 'Atop', 'Xor', 'Cover', 'Add', 'Subtract', 'Multiply', 'Difference', 'Lighten', 'Darken', 'Saturate', 'Desaturate', 'Illuminate', 'None']
    # From blend function in blend_utils.h, Over=0, ...Illuminate=15
    layer_mode = deluxe.Enum(shortname='lmde', choices=blendModes, default=blendModes[0], utility=True, affect=False)
    
    # Blend opacity
    layer_opacity = deluxe.Color(shortname='lo', default=1.0, utility=True, affect=False)
    
    #
    layer_premult = deluxe.Float(shortname='lpm', default=1.0, utility=True, affect=False, hidden=True)
    
    #
    layer_blendOpacity = deluxe.Boolean(shortname='lbo', default=True, utility=True, affect=False)
    
    # When turned off, no code is generated for this layer, don't use this to dynamically turn layer on and off, use layer_opacity
    layer_enable = deluxe.Boolean(shortname='len', default=True, norsl=True, affect=False)
    
    # Layer input components   
    layer_components = deluxe.ComponentData(shortname='lcmp', children=layerComponentChildren, array=True, norsl=True, affect=False)    
    
    #
    layer_displacement_name = deluxe.String(shortname='ldn', norsl=True, affect=False)
    layer_displacement_enable = deluxe.Boolean(shortname='lde', default=True, norsl=True, affect=False)
    layer_displacement_amount = deluxe.Float(shortname='lda', default=0.0, norsl=True, utility=True, affect=False)
    layer_displacement_scale = deluxe.Float(shortname='ldsc', default=1.0, softmin=-1, softmax=1, norsl=True, utility=True, affect=False)
    layer_displacement_alpha = deluxe.Float(shortname='ldal', default=1.0, min=0, max=1, norsl=True, utility=True, affect=False)
    layer_displacement_offset = deluxe.Float(shortname='ldo', default=0.0, softmin=-1, softmax=1, norsl=True, utility=True, affect=False)
    layer_displacement_type = deluxe.Enum(shortname='ldty', choices=['Bump', 'Displace'], default='Displace', utility=True, affect=False)
    layer_displacement_recalcNorm = deluxe.Boolean(shortname='ldrn', default=True, norsl=True, utility=True, affect=False)
    layer_displacement_useShadNorm = deluxe.Boolean(shortname='ldun', default=False, norsl=True, utility=True, affect=False)
    layer_displacement_useNormMap = deluxe.Boolean(shortname='ldum', default=False, norsl=True, utility=True, affect=False)
    layer_displacement_normMap = deluxe.Color(shortname='ldnm', default=False, norsl=True, utility=True, affect=False)
    layer_displacement_lip = deluxe.Float(shortname='ldl', min=0, max=1, default=0.0, norsl=True, utility=True, affect=False)
    layer_displacement_lipRim = deluxe.Float(shortname='ldls', min=0, max=1, norsl=True, utility=True, affect=False)
    
    
    layer_displacement_children = [ layer_displacement_name, 
                                    layer_displacement_enable, 
                                    layer_displacement_amount,
                                    layer_displacement_scale,
                                    layer_displacement_alpha,
                                    layer_displacement_offset,
                                    layer_displacement_type,
                                    layer_displacement_recalcNorm,
                                    layer_displacement_useShadNorm,
                                    layer_displacement_useNormMap,
                                    layer_displacement_normMap,
                                    layer_displacement_lip,
                                    layer_displacement_lipRim,
                                    ]
    #    
    layer_displacements = deluxe.Compound(layer_displacement_children, shortname='lds', array=True, utility=True, affect=False)
    layer_displacement_mode = deluxe.Enum(shortname='ldmo', choices=['Add', 'Over'], default='Add', utility=True, affect=False)
    layer_displacement_layerScale = deluxe.Float(shortname='ldlc', default=1.0, utility=True, affect=False)
    layer_displacement_layerOffset = deluxe.Float(shortname='ldlo', default=0.0, utility=True, affect=False)
    
    layer_displacements_order = deluxe.IntArray(shortname='ldor', affect=False, norsl=True)
    layer_displacements_actualOrder = deluxe.IntArray(shortname='ldao', output=True, internal=True, affect=False, norsl=True)
    
    # Layers
    layers = deluxe.Compound([layer_name, layer_enable, layer_mode, layer_opacity, layer_premult, layer_blendOpacity, layer_components, layer_displacement_mode, layer_displacement_layerScale, layer_displacement_layerOffset, layer_displacements, layer_displacements_order, layer_displacements_actualOrder], array=True, utility=True, affect=False)
    
    #
    primaryModes = [msg.longname for msg in channels] +  [aov.longname for aov in auxAOVs]
    
    # The primary display output, should always be color unless for debugging or when someone know what he's doing... 
    primaryMode = deluxe.Enum(shortname='pmo', choices=primaryModes, default='beauty', affect=False, norsl=True)
    
    # The primary display lightset index is used for debugging, it should stay to -1 (disabled) otherwise
    primaryLightSetIndex = deluxe.Integer(shortname='pls', default=-1, min=-1, max=16, affect=False, norsl=True)
    
    #
    premultAux = deluxe.Boolean(shortname='pma', default=True)
    
    # Values of custom float AOVs  
    customFloat = deluxe.Float(array=True, utility=True, affect=False)
    
    # Names of custom float AOVs  
    customFloatName = deluxe.String(array=True, utility=True, affect=False)
    
    # Values of custom color AOVs  
    customColor = deluxe.Color(default=0, array=True, utility=True, affect=False)
    
    # Names of custom color AOVs  
    customColorName = deluxe.String(array=True, utility=True, affect=False)

    #
    collapseComponents = deluxe.Boolean(shortname='clc', hidden=True, default=False, affect=False)
    collapseDisplacements = deluxe.Boolean(shortname='cld', hidden=True, default=False, affect=False)

    #
    displacement=deluxe.Float(output=True, shortname='od')
    
    # Used to initialise stupid attrFieldSliderGrp to get map button!
    phonyFloat = deluxe.Float(hidden=True, utility=True, affect=False)
    
    
    @classmethod
    def setCodeToken(cls, key, value):
        cls._codetokens[key] = value
    
    @classmethod
    def getCode(cls, code):
        result = code
        for key in cls._codetokens.keys():
            result = result.replace(key, cls._codetokens[key])
        return result
    
    @classmethod
    def getLine(cls, code):
        return '%s;\n'%cls.getCode(code)
        
    @classmethod
    def cleanupParamName(cls, name):
        cleanname = ''
        for c in name:
            if c in map(chr, range(48, 58) + range(65, 91) + range(97, 123) + [95]):
                cleanname += c
        return cleanname
    
    @classmethod
    def getLayerId(cls, layer):
        return 'layers%d'%layer.logicalIndex()
    
    @classmethod
    def getLayerName(cls, layer):
        layerName = cls.cleanupParamName(layer.child(cls.layer_name.obj).asString())
        if len(layerName):
            return layerName
        return cls.getLayerId(layer)   
    
    @classmethod
    def getLayerAttr(cls, layer):
        return 'layers[%d]'%layer.logicalIndex()
           
    @classmethod
    def setLayer(cls, layer):
        cls.setCodeToken('LAYERID', cls.getLayerId(layer))
        cls.setCodeToken('LAYERNAME', cls.getLayerName(layer))
        cls.setCodeToken('LAYERATTR', cls.getLayerAttr(layer))

    @classmethod
    def setChannel(cls, channel, lightsetindex=None):
        cls.setCodeToken('CHANNELDECLARE', channel.rsltype + ['', '[]'][channel.array != None and channel.array])
        cls.setCodeToken('CHANNELAOVTYPE', channel.rsltype)
        cls.setCodeToken('CHANNELNAME', channel.longname)
        cls.setCodeToken('CHANNELLIGHTSET', channel.getLightsetSuffix(lightsetindex))

    @classmethod
    def setVarPrefix(cls, varprefix):
        cls.setCodeToken('VARPREFIX', varprefix)
        
    def isSurfaceShader(self):
        
        # HUMM VERY VERY HACKY
        # Using this MEL global variable (from $DELIGHT/maya/scripts/DL_translateMayaToSl.mel) to know if this node is the actual shader or just an utility
        try:
            result = []
            MGlobal.executeCommand('$dl_layer_bogus = $g_final_color_plug;', result)
            plugnode = result[0].split('.')[0]
            return plugnode == MFnDependencyNode(self.thisMObject()).name()
        except:
            pass
        
        return True
    
    def isDisplacementShader(self):
        
        # HUMM VERY VERY HACKY
        # Using this MEL global variable (from $DELIGHT/maya/scripts/DL_translateMayaToSl.mel) to know if this node is the actual shader or just an utility
        result = []
        MGlobal.executeCommand('string $dl_layer_bogus_array[]; $dl_layer_bogus_array = $g_src_plugs;', result)
        node, attr = result[0].split('.')
        return attr == 'displacement' and node == MFnDependencyNode(self.thisMObject()).name()
    
    
    def getPlugArray(self, plug, order=[], connectedOnly=False, checkChildren=False):
        
        # get existing
        idxs = MIntArray()
        plug.getExistingArrayAttributeIndices(idxs)
        
        # try to use order to sort existing idxs
        sortedIdxs=[]
        for idx in order:
            if idx in idxs:
                sortedIdxs.append(idx)
        
        for idx in idxs:
            if idx not in sortedIdxs:
                sortedIdxs.append(idx)

        plugs=[]        
        for idx in sortedIdxs:
            idxplug = plug.elementByLogicalIndex(idx)
            if connectedOnly:
                incommingPlugs = MPlugArray()
                
                if checkChildren:
                    hasConnectedChild=False
                    for i in range(0, idxplug.numChildren()):
                        childplug = idxplug.child(i)
                        if childplug.connectedTo(incommingPlugs, 1, 0):
                            hasConnectedChild = True
                            break
                    if not hasConnectedChild:
                        continue
                else:    
                    if not idxplug.connectedTo(incommingPlugs, 1, 0):
                        continue
                
            plugs.append(idxplug)
            
        return plugs
    
    def getLayers(self, enabled=True):
        thisObj = self.thisMObject()
        order = MFnIntArrayData(MPlug(thisObj, self.order.obj).asMObject()).array()
        allLayers = self.getPlugArray(MPlug(thisObj, self.layers.obj), order)
        layers = []
        for layer in allLayers:
            if layer.child(self.layer_enable.obj).asBool() or not enabled:
                layers.append(layer)
                
        return layers
    
    
    def getDisplacements(self, layerPlug, enabled=True):
        order = MFnIntArrayData(layerPlug.child(self.layer_displacements_order.obj).asMObject()).array()
        allDisplacements = self.getPlugArray(layerPlug.child(self.layer_displacements.obj), order)
        displacements = []
        for displacement in allDisplacements:
            if displacement.child(self.layer_displacement_enable.obj).asBool() or not enabled:
                displacements.append(displacement)
                
        return displacements
    
    
    #
    def getCustoms(self, type, allCustomParams, code=False, shaderOutput=True):
        customStr = ''
        attrName='custom%s'%type.capitalize()
        
        if not code:
            customStr += '%s[] %s[]\n'%(type, attrName)
        
        idx = 0
        namePlug = MPlug(self.thisMObject(), getattr(self.__class__, '%sName'%attrName).obj)
        for plug in self.getPlugArray(namePlug):
            paramName = self.cleanupParamName(plug.asString())
            if len(paramName) and paramName not in allCustomParams:
                if code:
                    mult = 'opacity'
                    if type == 'float':
                        mult = 'luminance(%s)'%mult

                    customStr += '%s = %s[%d] * %s;\n'%(paramName, attrName, idx, mult)
                elif shaderOutput:
                    customStr += 'shader_output varying %s %s\n'%(type, paramName)
                allCustomParams.append(paramName)
                idx += 1
                
        return customStr
    
    
    # Override from ShadingCodeComponent
    def getShadingCode(self):
        
        #
        shadingCode=''
        
        # Include this class file for utility functions
        shadingCode += '#include "%s.h"\n'%self.__class__.__name__
            
            
        thisObj = self.thisMObject()
        
        #
        if self.isDisplacementShader():
            shadingCode += """
extern point P;
extern normal N;
extern normal Ng;
extern point __Porig;
extern normal __Norig;
// save P and N for use when raytracing without displacements
__Porig = P;
__Norig = N;
normal Nn = normalize(N);
normal deltaN = Nn - normalize(Ng);
point Pnew = P + Nn * displacementGlobalOffset;
normal Nnew = Nn;

float scaleComp = 1.0;
if(displacementCompensateScale){ 
    vector v0 = vtransform("object", vector(1, 0, 0));
    vector v1 = vtransform("object", vector(0, 1, 0));
    vector v2 = vtransform("object", vector(0, 0, 1));
    float compensate = (length(v0) + length(v1) + length(v2)) / 3;
    if(compensate)
        scaleComp = scaleComp / compensate;
}

float amount = 0;
"""
            layers = self.getLayers()
            
            for layer in reversed(layers):
                
                substractOverLayers = ''
                for toplayer in layers[layer.logicalIndex()+1:]:
                    if toplayer.child(self.layer_displacement_mode.obj).asShort() == 1:
                        self.setLayer(toplayer)
                        substractOverLayers += self.getCode(' - LAYERID_alpha')
                self.setLayer(layer)
                shadingCode += self.getLine('float LAYERID_alpha = clamp(luminance(LAYERID_layer_opacity)%s, 0, 1)'%(substractOverLayers))
                
            for layer in layers:
                self.setLayer(layer)
                for displacement in self.getDisplacements(layer):
                    varbase='LAYERID_layer_displacements%i_layer_displacement'%displacement.logicalIndex()
                    shadingCode += self.getLine('amount = getLip(%s_lip, %s_lipRim, %s_amount)'%(varbase, varbase, varbase))
                    shadingCode += self.getLine('amount = (amount * scaleComp * %s_scale * LAYERID_layer_displacement_layerScale * displacementGlobalScale + ((%s_offset + LAYERID_layer_displacement_layerOffset) * scaleComp)) * LAYERID_alpha * clamp(%s_alpha, 0, 1)'%(varbase, varbase, varbase))
                
                    if displacement.child(self.layer_displacement_useNormMap.obj).asShort():
                        shadingCode += self.getLine('Nnew += ntransform("object", "current", normal(%s_normMap))'%(varbase))
                    shadingCode += self.getLine('getDisplacement(amount, %s_type, %s_recalcNorm, %s_useShadNorm, Pnew, normalize(Nnew), deltaN, Pnew, Nnew)'%(varbase, varbase, varbase))
                    
            shadingCode += """
    
P = Pnew;
N = Nnew;
"""
        else:
            
            #        
            shadingCode += self.getLine('color resultColor, resultOpacity')
        
            # Add one cause lightset arrays are actually one based since index 0 is reserved for default lightset i.e. no lightset
            lightSetsCount = MPlug(thisObj, self.lightSetsCount.obj).asInt()
            if lightSetsCount < 1:
                lightSetsCount = 1
            
            # If this node is used as an actual shader we need the AOVs
            isSurfaceShader = self.isSurfaceShader()
            if isSurfaceShader:
                self.setVarPrefix('')
            else:
                
                # If not we declare local vars
                self.setVarPrefix('local_')
                shadingCode += self.getLine('color VARPREFIXopacity = 0')
                for channel in self.channels:
                    self.setChannel(channel)
                    if channel.array:
                        for i in range(0, lightSetsCount):
                            self.setChannel(channel, i)
                            shadingCode += self.getLine('color VARPREFIXCHANNELNAMECHANNELLIGHTSET = 0')    
                    else:
                        shadingCode += self.getLine('color VARPREFIXCHANNELNAME = 0')    
                            
            # Loop into enabled layers
            for layer in self.getLayers():
    
                # Get all connected components to this layer
                components = self.getPlugArray(layer.child(self.layer_components.obj), connectedOnly=True)
                
                self.setLayer(layer)
    
                # Mult layer opacity
                shadingCode += self.getLine('color LAYERNAME_opacity = LAYERID_layer_opacity')
                
                if not len(components):
                    continue
                
                # Blend opacity
                if layer.child(self.layer_blendOpacity.obj).asBool():
                    shadingCode += self.getLine('blend(LAYERID_layer_mode, 1, LAYERNAME_opacity, 1, VARPREFIXopacity, resultColor, VARPREFIXopacity)')
    
                #
                for channel in filter(lambda msg: not msg.array, self.channels):
                    self.setChannel(channel)
                    componentList = ['LAYERID_layer_components%d_component_CHANNELNAME'%(comp.logicalIndex()) for comp in components]                
                    shadingCode += self.getLine('VARPREFIXCHANNELNAME = blend%ss(LAYERID_layer_mode, LAYERID_layer_premult, %s, LAYERNAME_opacity, VARPREFIXCHANNELNAME, VARPREFIXopacity)'%(channel.apitype, string.join(componentList, ' + ')))
                    
                # Blend all lightsets separatly
                for i in range(0, lightSetsCount):
                    
                    # Build blendLightsets parameter list
                    blendFgInputs = [self.getCode('LAYERNAME_opacity')]
                    for channel in filter(lambda msg: msg.array, self.channels):
                        self.setChannel(channel)
                        
                        # Add up all components 
                        componentList = ['LAYERID_layer_components%d_component_CHANNELNAME[%d]'%(comp.logicalIndex(), i) for comp in components]
                        blendFgInputs.append(self.getCode(string.join(componentList, ' + ')))
                        
                    blendBgInputs = [self.getCode('VARPREFIXopacity')]
                    blendOutputs = []
                    for channel in filter(lambda msg: msg.array, self.channels):
                        self.setChannel(channel, i)
                        blendBgInputs.append(self.getCode('VARPREFIXCHANNELNAMECHANNELLIGHTSET'))                        
                        blendOutputs.append(self.getCode('VARPREFIXCHANNELNAMECHANNELLIGHTSET'))                  
                    
                    #
                    blendParams = [self.getCode('LAYERID_layer_mode'), self.getCode('LAYERID_layer_premult')] + blendFgInputs + blendBgInputs + blendOutputs
                    shadingCode += 'blendLightsets(\n\t%s);\n'%string.join(blendParams, ',\n\t')
            
            #
            shadingCode += self.getLine('VARPREFIXopacity *= globalOpacity')
            
            # Add (or substract) all channels to out color per light set
            for channel in self.channels:
                self.setChannel(channel)
                
                if channel.array:
                    accum_lightsets = []
                    for i in range(0, lightSetsCount):
                        self.setChannel(channel, i)
                        
                        shadingCode += self.getLine('VARPREFIXCHANNELNAMECHANNELLIGHTSET *= globalOpacity')
                        accum_lightsets.append(self.getCode('VARPREFIXCHANNELNAMECHANNELLIGHTSET'))
                        
                    shadingCode += self.getLine('color CHANNELNAME_lightsets[] = {%s}'%string.join(accum_lightsets, ', '))
                    
                    if isSurfaceShader:            
                        shadingCode += self.getLine('VARPREFIXCHANNELNAME = accumulateColors(CHANNELNAME_lightsets)')
                    else:
                        shadingCode += self.getLine('copyColors(CHANNELNAME_lightsets, outputComponent_output_CHANNELNAME)')
                else:
                    shadingCode += self.getLine('VARPREFIXCHANNELNAME *= globalOpacity')
                    if not isSurfaceShader:
                        shadingCode += self.getLine('outputComponent_output_CHANNELNAME = local_CHANNELNAME')
            
            if isSurfaceShader:
                
                layernames=[]
                layeropacs=[]
                for layer in self.getLayers():
                    self.setLayer(layer)
                    layernames.append(self.getCode('LAYERNAME'))
                    layeropacs.append(self.getCode('LAYERNAME_opacity'))


                puzzleParamStr = string.join([p.longname for p in self.puzzleAuxInputs], ', ')
                shadingCode += self.getLine('color layerOpacities[] = {%s}'%string.join(layeropacs, ','))
                shadingCode += self.getLine('string layerNames[] = {"%s"}'%string.join(layernames, '", "'))
                shadingCode += self.getLine('calculateAuxiliaries(opacity, premultAux, layerOpacities, layerNames, %s)'%puzzleParamStr)
            
                allCustomParams = []
                shadingCode += self.getCustoms('float', allCustomParams, code=True)
                shadingCode += self.getCustoms('color', allCustomParams, code=True)
            
            #
            primaryModeIdx = MPlug(thisObj, self.primaryMode.obj).asShort()
            primaryMode = self.primaryModes[primaryModeIdx]
            primaryLightSetIndex = MPlug(thisObj, self.primaryLightSetIndex.obj).asInt()
            if primaryLightSetIndex >= 0 and primaryMode not in [obj.longname for obj in self.auxAOVs]:
                primaryMode += '_ls%d'%primaryLightSetIndex
            
            shadingCode += self.getLine('outColor = VARPREFIX%s'%primaryMode)
            shadingCode += self.getLine('outTransparency = 1 - VARPREFIXopacity')
        
        return shadingCode
    
    # Override from ShadingCodeComponent
    def getShadingParameters(self):
        
        shadingParameters = '' 
        thisObj = self.thisMObject()
        
        lightSetsCount = MPlug(thisObj, self.lightSetsCount.obj).asInt()
        if lightSetsCount < 1:
            lightSetsCount = 1
                    
        isSurfaceShader = self.isSurfaceShader()        
        isDisplacementShader = self.isDisplacementShader()        
                            
        #
        if isDisplacementShader:
            for attr in self.getShadingParametersAttributes():
                if not attr.output and attr.longname.startswith('displacement'):
                    shadingParameters += '%s %s\n'%(attr.rsltype, attr.longname)
        else: 
            shadingParameters += super(dl_layer, self).getShadingParameters()
        
        #
        for layer in self.getLayers():
            
            self.setLayer(layer)
            shadingParameters += self.getCode('color LAYERATTR.layer_opacity\n')
            if isDisplacementShader:
                shadingParameters += self.getCode('float LAYERATTR.layer_displacement_layerScale\n')
                shadingParameters += self.getCode('float LAYERATTR.layer_displacement_layerOffset\n')
            else:
                shadingParameters += self.getCode('uniform float LAYERATTR.layer_mode\n')
            
            if isDisplacementShader:
                for displacement in self.getDisplacements(layer):
                    displacementIndex = displacement.logicalIndex()
                    for child in self.layer_displacement_children:
                        if child.utility:
                            shadingParameters += self.getCode('%s LAYERATTR.layer_displacements[%d].%s\n'%(child.rsltype, displacementIndex, child.longname))
            else:
                shadingParameters += self.getCode('float LAYERATTR.layer_premult\n')
                for component in self.getPlugArray(layer.child(self.layer_components.obj), connectedOnly=True):
                    componentIndex = component.logicalIndex()
                    shadingParameters += self.getCode('void%d LAYERATTR.layer_components[%d]\n'%(lightSetsCount, componentIndex))
                    for channel in self.channels:
                        self.setChannel(channel)
                        shadingParameters += self.getCode('CHANNELDECLARE LAYERATTR.layer_components[%d].component_CHANNELNAME\n'%componentIndex)
            
        
        if isSurfaceShader:
        
            shadingParameters += self.getCode('shader_output varying color opacity\n')
            
            for channel in self.channels:
                self.setChannel(channel)
                shadingParameters += self.getCode('shader_output varying CHANNELAOVTYPE CHANNELNAME\n')
                if channel.array:
                    for i in range(0, lightSetsCount):
                        self.setChannel(channel, i)
                        shadingParameters += self.getCode('shader_output varying CHANNELAOVTYPE CHANNELNAMECHANNELLIGHTSET\n')
                
            for auxAOV in self.auxAOVs:
                shadingParameters += self.getCode('shader_output varying %s %s\n'%(auxAOV.rsltype, auxAOV.longname))
        
        if isDisplacementShader:
            shadingParameters += 'shader_output varying point __Porig\n'
            shadingParameters += 'shader_output varying normal __Norig\n'

        #
        if not isDisplacementShader:
                        
            allCustomParams = []
            shadingParameters += self.getCustoms('float', allCustomParams, shaderOutput=isSurfaceShader)
            shadingParameters += self.getCustoms('color', allCustomParams, shaderOutput=isSurfaceShader)    
            
        return shadingParameters

        
    def getInternalValueInContext(self, plug, dataHandle, ctx):
        
        if plug.attribute() == self.__class__.actualOrder.obj:
            layers = self.getLayers(enabled=False)
            order = MIntArray()
            for layer in layers:
                order.append(layer.logicalIndex())
            dataHandle.setMObject(MFnIntArrayData().create(order))
            return True
        elif plug.attribute() == self.__class__.layer_displacements_actualOrder.obj:
            displacements = self.getDisplacements(plug.parent(), enabled=False)
            order = MIntArray()
            for displacement in displacements:
                order.append(displacement.logicalIndex())
            dataHandle.setMObject(MFnIntArrayData().create(order))
            return True
            
        return super(dl_layer, self).getInternalValueInContext(plug, dataHandle, ctx)

    def compute(self, plug, data):        
        
        if plug == self.outColor.obj:
            r, g, b = data.inputValue(self.displayColor.obj).asFloat3()
            data.outputValue(plug).set3Float(r, g, b)
            return data.setClean(plug)
        elif plug == self.outTransparency.obj:
            r, g, b = data.inputValue(self.displayOpacity.obj).asFloat3()
            data.outputValue(plug).set3Float(1.0 - r, 1.0 - g, 1.0 - b )
            return data.setClean(plug)
        
        return super(dl_layer, self).compute(plug, data)
        
    def postConstructor(self):
        
        # We always have at least one layer
        # TODO: maybe make this less systematic
        layerPlug = MPlug(self.thisMObject(), self.layers.obj)
        layer0Plug = layerPlug.elementByLogicalIndex(0)
        layerNamePlug = layer0Plug.child(self.layer_name.obj)
        layerNamePlug.setMObject(MFnStringData().create('layer0'))
        
        super(dl_layer, self).postConstructor()
    
    template = 'source dl_layer'

    
def initializePlugin(obj):
    dl_layer.register(obj)
    
def uninitializePlugin(obj):
    dl_layer.deregister(obj)
