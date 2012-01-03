import delight

import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math, sys

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

class dl_uberLightShape(delight.Light):
    typeid = 0x00310000
    includes = ["uberlight_utils.h", "shadow_utils.h", "utils.h"]

    lightType = delight.Enum(default='Spot', choices=['Spot', 'Point', 'Distant'])

    # falloff
    falloff = delight.Enum(default='None',
                           choices=['None', 'Linear', 'Quadratic'])
    falloffDistance = delight.Float(default=1, storage='uniform',
                                    help="""The distance at which the incident energy is actually
                                            equal to intensity*reflcolor.  In other words, the intensity
                                            is actually given by:   I = (falloffdist / distance) ^ falloff""")
    maxIntensity = delight.Float(default=1, storage='uniform',
                                 help="""To prevent the light from becoming unboundedly
                                         large when the distance < falloffdist, the intensity is
                                         smoothly clamped to this maximum value.""");

    # cone shaping
    coneAngle = delight.Float(min=0, max=180, default=40, storage='uniform')
    penumbraAngle = delight.Float(min=0, max=90, default=10, storage='uniform')

    beamDistribution = delight.Float(default=0, min=0, softmax=2, storage='uniform',
                                     help="""Controls intensity falloff due to angle.
                                             A value of 0 (the default) means no angle falloff.  A value
                                             of 1 is roughly physically correct for a spotlight, and
                                             corresponds to a cosine falloff.
                                             This parameter has no effect on point lights.""")
    SpotPoint = delight.Group([falloff, falloffDistance, maxIntensity],
        label='Spot/Point Light', collapse=False)

    Spot = delight.Group([coneAngle, penumbraAngle, beamDistribution],
        label='Spot Light', collapse=False)

    # component contributions
    contributeDiffuse = delight.Float(shortname='cnd',
                                      min=0, max=1,
                                      default=1,
                                      storage='uniform',
                                      help='Controls whether or not this light contributes to the diffuse component.')
    contributeSpecular = delight.Float(shortname='cnsp',
                                       min=0, max=1,
                                       default=1,
                                       storage='uniform',
                                       help='Controls whether or not this light contributes to the specular component.')
    contributeTranslucence = delight.Float(shortname='cnt',
                                           min=0, max=1,
                                           default=1,
                                           storage='uniform',
                                           help='Controls whether or not this light contributes to the translucence component.')


    Contributions = delight.Group([contributeDiffuse, contributeSpecular, contributeTranslucence], label='Component Contributions')

    # gobo
    gbTex = delight.Image ( label='Gobo Texture', default="")
    gbBlur = delight.Float ( label='Blur', shortname='blr', default=0, min=0, max=1)
    gbInfl = delight.Float ( label='Influence', shortname='infl', default=1, min=0, max=1)
    gbSoffset = delight.Float ( label='sOffset', shortname='sofs', default=0, softmin=-1, softmax=1)
    gbToffset = delight.Float ( label='tOffset', shortname='tofs', default=0, softmin=-1, softmax=1)
    gbSscale = delight.Float ( label='sScale', shortname='sscale', default=1, softmin=0, softmax=2)
    gbTscale = delight.Float ( label='tScale', shortname='tscale', default=1, softmin=0, softmax=2)
    gbRotate = delight.Float ( label='rotate', default=0, softmin=-.5, softmax=.5)
    outOfRangeMode = delight.Enum ( default='Tile', choices=['Tile', 'Hold', 'Black'])
    gobo = delight.Group([gbTex, gbBlur, gbInfl, gbSoffset, gbToffset, gbSscale, gbTscale, gbRotate, outOfRangeMode])

 
    # blockers
    blockerParms = \
"""
bkNNCoordsys = delight.String (shortname='bkNNcs', label = 'coordinateSystem', default="")
bkNNTint = delight.Color(shortname='bkNNtn', label = 'tint', storage='uniform')
bkNNTex = delight.Image (shortname='bkNNtx', label = 'texture', default="")
bkNNChannel = delight.Enum (shortname='bkNNch', label = 'channel', default='rgb', choices=['rgb', 'r', 'g', 'b', 'a', 'luminance'])
bkNNBlur = delight.Float (shortname='bkNNbl', label='Blur', default=0, min=0, max=1)
bkNNInfl = delight.Float (shortname='bkNNin', label='Influence', default=1, min=0, max=1)
bkNNHedge = delight.Float(shortname='bkNNhe', label = 'vert edge', min=0, softmax=.5, default=0, storage='uniform')
bkNNWedge = delight.Float(mshortname='bkNNwe', label = 'horiz edge', min=0, softmax=.5, default=0, storage='uniform') 

blockerNN = delight.Group([ bkNNCoordsys, bkNNInfl, bkNNTint, bkNNTex, bkNNChannel, bkNNBlur, bkNNHedge, bkNNWedge])
"""
    lmBlockersStr = "lmBlockers = delight.Group(["

    nBlockers = 10

    for i in range(1, nBlockers + 1):
        num = '%02d' % i
        parmBlock = blockerParms.replace('NN', num)
        exec parmBlock
        lmBlockersStr += "blocker" + num
        if (i == nBlockers):
            lmBlockersStr += """
], label = 'Blockers (lumiere)')
"""
        else:
            lmBlockersStr += ", "

    exec lmBlockersStr


    # cut on/off
    cutOn = delight.Float(shortname='cn', min=0, softmax=10, default=0.01, storage='uniform')
    cutOnEdge = delight.Float(shortname='cne', min=0, softmax=10, default=0, storage='uniform')
    cutOnShape = delight.Float(shortname='cns', min=0, softmax=5, default=1, storage='uniform')
    cutOff = delight.Float(shortname='coff', min=0, softmax=10, default=1.0e6, storage='uniform')
    cutOffEdge = delight.Float(min=0, softmax=10, default=0, storage='uniform')
    cutOffShape = delight.Float(min=0, softmax=5, default=1, storage='uniform')

    zShaping = delight.Group([cutOn, cutOnEdge, cutOnShape, cutOff, cutOffEdge, cutOffShape],
                             label='Cut On/Off')

    # barn doors
    barnDoorLeftAngle = delight.Float(default=90, min=0, max=90, storage='uniform')
    barnDoorLeftEdge = delight.Float(default=5, min=0, softmax=20, storage='uniform')
    barnDoorLeftLength = delight.Float(hidden=1, default=0, min=0, softmax=5, storage='uniform')
    barnDoorLeftRoll = delight.Float(default=0, min=-90, max=90, storage='uniform')

    barnDoorRightAngle = delight.Float(default=90, min=0, max=90, storage='uniform')
    barnDoorRightEdge = delight.Float(default=5, min=0, softmax=20, storage='uniform')
    barnDoorRightLength = delight.Float(hidden=1, default=0, min=0, softmax=5, storage='uniform')
    barnDoorRightRoll = delight.Float(default=0, min=-90, max=90, storage='uniform')

    barnDoorTopAngle = delight.Float(default=90, min=0, max=90, storage='uniform')
    barnDoorTopEdge = delight.Float(default=5, min=0, softmax=20, storage='uniform')
    barnDoorTopLength = delight.Float(hidden=1, default=0, min=0, softmax=5, storage='uniform')
    barnDoorTopRoll = delight.Float(default=0, min=-90, max=90, storage='uniform')

    barnDoorBottomAngle = delight.Float(default=90, min=0, max=90, storage='uniform')
    barnDoorBottomEdge = delight.Float(default=5, min=0, softmax=20, storage='uniform')
    barnDoorBottomLength = delight.Float(hidden=1, default=0, min=0, softmax=5, storage='uniform')
    barnDoorBottomRoll = delight.Float(default=0, min=-90, max=90, storage='uniform')

    barnDoors = delight.Group([barnDoorLeftAngle, barnDoorLeftEdge, barnDoorLeftRoll,
                               barnDoorRightAngle, barnDoorRightEdge, barnDoorRightRoll,
                               barnDoorTopAngle, barnDoorTopEdge, barnDoorTopRoll,
                               barnDoorBottomAngle, barnDoorBottomEdge, barnDoorBottomRoll])

    # Noisy light
    noiseAmplitude = delight.Float()
    noiseFrequency = delight.Float(default=4)
    noiseOffset = delight.Float3(default=(0,0,0))
    noise = delight.Group([noiseAmplitude, noiseFrequency, noiseOffset])

    shadowColor = delight.Color(default=0, help="Color to tint the shadow.")
    shadowIntensity = delight.Float(default=1, help="Intensity of shadow.")
    useAmbientOcclusion = delight.Float(default=0, help="Mix ambient occlusion with cast shadows.",
                                storage="uniform", softmax=1)

    orthoShadow = delight.Boolean(default=False)
    shadowType = delight.Enum(default='None', 
                              choices=['None', 'Mapped', 'Ray-Traced'],
                              help="""If you are using "Mapped", you MUST assign a 3delight light attribute to this light.""")
    # mapped shadows
    shadowBlur = delight.Float(label='Blur',
                               shortname='bl', default=0.01, min=0, softmax=0.2, storage='uniform',
                               help="""Amount to blur the shadow. A value of 1.0 would
                                       request that the entire texture be blurred in the result.""")
    shadowFilterType = delight.Enum(label='Filter Type',
                                    default='Gaussian',
                                    choices=['Box','Triangle','Gaussian']);
    shadowBias = delight.Float(label='Bias',
                               shortname='bi', default=0.225, min=0, softmax=5, storage='uniform',
                               help="Used to prevent self-shadowing. If set to 0, the global bias is used.")
    shadowSamples = delight.Integer(label='Samples',
                                    default=16, min=0, softmax=16)
    
    useSoftShadowDecay = delight.Boolean(default=False,
                                         help="Turns on soft shadows that decay with distance.")
    shadowMinimumRadius = delight.Float(label='Minimum Radius',
                                        shortname='mnr', default=0.001, min=0, softmax=0.2, storage='uniform')
    shadowMaximumRadius = delight.Float(label='Maximum Radius',
                                        shortname='mxr', default=0.1, min=0, softmax=0.2, storage='uniform')
    selfShadowReduce = delight.Float(default=2, min=0, softmax=5, storage='uniform')
    shadowDecay = delight.Float(label='Decay',
                                default=0, min=0, softmax=5, storage='uniform')
    shadowDecayCutOn = delight.Float(label='Decay Cut-On',
                                     shortname='sdcon', default=10, min=0, max=1000, storage='uniform')
    shadowDecayCutOff = delight.Float(label='Decay Cut-Off',
                                      shortname='sdcoff', default=10, min=0, max=1000, storage='uniform')
    
    softShadowDecay = delight.Group([useSoftShadowDecay,
                                     shadowMinimumRadius, shadowMaximumRadius,
                                     selfShadowReduce, shadowDecay,
                                     shadowDecayCutOn, shadowDecayCutOff])

    useShadowMapsSets = delight.Boolean(default=True)
    shadowMapsSetIndex = delight.Integer(default=-1)
    
    mappedShadows = delight.Group([useShadowMapsSets, shadowMapsSetIndex, shadowBlur, shadowFilterType, 
                                   shadowBias, shadowSamples,
                                   softShadowDecay])

    # raytraced shadows
    traceSampleCone = delight.Float(min=0, max=90, default=0, storage='uniform',
                                    help="""Specifies an angle that describes a cone in which rays will
                                            be sampled. Larger cones means softer results.""")
    traceSamples = delight.Integer(shortname='tsam',
                                   min=0, default=4, storage='uniform',
                                   help="""Specifies the number of samples to use to. Higher sample counts are needed
                                           if anti-aliasing is to be performed or the sample cone is greater than 0.""")
    traceSubset = delight.String(shortname='tsub', storage='uniform',
                                 help="""Specifies a subset of objects which are included in ray tracing computations.""")
    traceBias = delight.Float(default=-1, softmin=0, softmax=10, storage='uniform',
                              help="""Specifies a bias for ray's starting point to avoid potentially erroneous intersections
                                      with the emitting surface. A value of `-1' forces 3DELIGHT to take the default value
                                      as specified by Attribute "trace" "bias".""")
    tracedShadows = delight.Group([traceSampleCone, traceSamples, traceSubset, traceBias],
                                  label='Ray-Traced Shadows')

    digidoubleShadowType = delight.Enum(default='Ray-Traced', 
                              choices=['None', 'Mapped', 'Ray-Traced'], help="""
                                Select shadow type for digidouble shadow.  The digidouble MUST be part of the
                                set specified in digidoubleSubset for either Mapped OR Ray-Traced shadows.
                                Objects in this set will cast shadows on other surfaces but NOT on themselves,
                                and will receive shadows from other surfaces EXCEPT where they are \"blocked\"
                                by digidouble surfaces.""")

    digidoubleSubset = delight.String(default='digidouble', help="""Subset containing digidoubles.  This MUST
                                be specified whether digidoubleShadowType = Mapped OR Ray-Traced.""")

    digidoubleShadowMap = delight.String(default='', help="""Shadowmap containing digidouble, only used if digidoubleShadowMap = Mapped.""")

    digidoubleShadows = delight.Group([digidoubleShadowType, digidoubleSubset, digidoubleShadowMap])

    shadows = delight.Group([shadowColor, shadowIntensity, useAmbientOcclusion, orthoShadow, shadowType, mappedShadows, tracedShadows, digidoubleShadows])

    blockerProcs = r"""
    proc addNewBlocker(string $blockers)
    {
        string $node  = plugNode($blockers);

        string $new_node = `shadingNode -asUtility "dl_shadowBlocker"`;

        // new name should be like this:
        // blahblah1 -> blahblahAmbientSC1
        // blahblah -> blahblahAmbientSC

        string $number = `match "[0-9]*$" $node`;
        string $bareNode = `substitute "[0-9]*$" $node ""`;

        string $newName = ($bareNode + "Blocker" + $number);
        $new_node = `rename $new_node $newName`;

        int $new_index = dl_dgPlugArrayAddNew($blockers);               
        string $plugName = $blockers + "[" + $new_index + "]";

        connectAttr -f ($new_node+".outColor") ($plugName +".blockerColor");
        connectAttr -f ($new_node+".outAlpha") ($plugName +".blockerValue");

        string $p3tname = `shadingNode -asUtility place3dTexture`;
        string $manipName = $new_node +"Manip";
        string $manip  = `rename $p3tname $manipName`;
        setAttr ($manip+".scaleZ") 0;
        setAttr ($manip+".rotateX") 90;
        connectAttr -f  ($manip +".worldInverseMatrix") ($new_node+".placementMatrix");
        
        // TODO: do this via the prepare hook
        connectAttr -f  ($node +".cutOn") ($new_node+".cutOn");
	
        select -r $node;

    }

    proc string getPlugFromSelection(string $blockers)
    {
        int $selidxlist[] = `textScrollList -q -selectIndexedItem blockerList`;
        int $selindex =  $selidxlist[0];        
        if ($selindex)
        {
            $selindex--;
            int $indexList[] = dl_dgPlugArrayGetIndices($blockers);           
            int $index =  $indexList[$selindex];            
            string $plug = ($blockers+"["+$index+"]");           
            return $plug;                        
        }
        else
        {
            return "";
        }        
    }

    proc string  getSourceFromPlug(string $plug)
    {
        string $input = $plug+".blockerColor" ;
        string $sources[] = `listConnections -source 1 -destination 0 $input`;

        return $sources[0];
    }

    proc deleteBlocker(string $blockers)
    {    
        string $plug = getPlugFromSelection($blockers);
        if (size($plug))
        {            
            string $source = getSourceFromPlug($plug);
            removeMultiInstance -b true $plug ;
            delete $source;
            delete ($source +"Manip");                        
        }        
    }

    proc selectBlocker(string $blockers)
    {
        string $plug = getPlugFromSelection($blockers);
        if (size($plug))
        {     
            string $source = getSourceFromPlug($plug);
            select -r $source;
        } 
    } 

    proc renameBlockers(string $blockers)
    {
        string $node  = plugNode($blockers);
        int $indexList[] = dl_dgPlugArrayGetIndices($blockers);
        int $i;
        for ($i in $indexList)
        {           
            string $source = getSourceFromPlug ($blockers +  "[" + $i + "]");
            string $nt = `nodeType $source`;             
            string $number = `match "[0-9]*$" $node`;
            string $bareNode = `substitute "[0-9]*$" $node ""`;
            string $bareNt = `substitute "^dl_blocker" $nt ""`;            
            string $newName = ($bareNode + $bareNt + $number);
            rename $source $newName;
        }        
    }

    global proc AETEMPLATE_LONGNAME_New(string $blockers)
    {
        string $plugNode = plugNode($blockers);
        print ("\n\n ------------ JEREMY plugNode = " + $plugNode);
        columnLayout;
            rowLayout -nc 2;
                text -l " ";
                rowLayout -nc 2 -columnWidth2 75 75;
                    button -ann "Add and connect a new blocker." -l "Add"  -align "center" blockerAddButton;
                    button -ann "Delete the selected blocker"  -l "Delete" -align "center" blockerDeleteButton;
                setParent ..;
            setParent ..;
            rowLayout -nc 2;
                text -ann "List of blocker nodes." -l "blockers";
                textScrollList -ann "List of blocker nodes." -height 150 blockerList;
            setParent ..;
            separator -st "none" -h 4;
            rowLayout -nc 2;
                text -l " ";
                button -ann "Rename blocker nodes using this node's name as a prefix." -l "Rename Nodes" -align "center" renameNodesButton;
            setParent ..;
        setParent ..;        
        separator -st "none" -h 4;
        AETEMPLATE_LONGNAME_Replace($blockers);
    }

    global proc AETEMPLATE_LONGNAME_Replace(string $blockers)
    {
        button -edit -command ("addNewBlocker "+$blockers) blockerAddButton;
        button -edit -command ("deleteBlocker "+$blockers) blockerDeleteButton;
        textScrollList -edit -removeAll blockerList;
        int $indexList[] = dl_dgPlugArrayGetIndices($blockers);
        int $i;
        for ($i in $indexList)
        {           
            string $source = getSourceFromPlug ($blockers +  "[" + $i + "]");
            textScrollList -edit -append $source blockerList;
        }
        textScrollList -edit -doubleClickCommand ("selectBlocker " + $blockers) blockerList;
        button -edit -command ("renameBlockers "+$blockers) renameNodesButton;         
    }
    """
    
    blockerColor = delight.Color(shortname='shdc', notemplate=True)
    blockerValue = delight.Float(shortname='shdv', notemplate=True)
    blockers = delight.Compound([blockerColor, blockerValue], array=True, callcustom=blockerProcs)

    blockerGroup = delight.Group([blockers], label='Blockers', hidden=True)

    # Gobos
    goboColor = delight.Color(shortname='gbc', notemplate=True)
    gobos = delight.Compound([goboColor], array=True)
    
    goboGroup = delight.Group([gobos], hidden=True, label='Gobos')

    # display stuff...
    displayPenumbraAngle = delight.Boolean(default=False)
    displayLightLimits = delight.Boolean(default=False)
    displayBarnDoors = delight.Boolean(default=False)
    displayFalloff = delight.Boolean(default=False)
    iconSize = delight.Float(default=1, min=0.01, storage='uniform')
    display = delight.Group([displayPenumbraAngle, displayLightLimits, displayBarnDoors, displayFalloff, iconSize])

    __occluded = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    __occlusionColor = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    __unoccludedCl = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    __contribTranslucence = delight.Float(default=False, output=True, message=True, messagetype='lightsource')
    __useAmbientOcclusion = delight.Float(default=0, output=True, message=True, messagetype='lightsource')

    # category
    __category = delight.String(default='', message=True, messagetype='lightsource')

    rsl = \
    """
       
        extern color __occluded;
        extern color __occlusionColor;
        extern color __unoccludedCl;
        extern float __contribTranslucence;
        extern float __useAmbientOcclusion;

        __nonspecular = 1 - i_contributeSpecular;
        __nondiffuse = 1 - i_contributeDiffuse;
        __contribTranslucence = i_contributeTranslucence;
        __useAmbientOcclusion = i_useAmbientOcclusion;

        /* For simplicity, assume that the light is at the origin of shader
         * space, and aimed in the +z direction.  So to move or orient the
         * light, you transform coordinate system in the RIB stream, prior
         * to instancing the light shader.  But that sure simplifies the
         * internals of the light shader!  Anyway, let PL be the position of
         * the surface point we're shading, expressed in the local light
         * shader coordinates.
         */


        point PL = transform ("shader", Ps);
        uniform point from = point "shader" (0, 0, 0);
        point fromShad = from;
        uniform point to = point "shader" (0, 0, 1);
        uniform vector axis = (to - from) / length(to - from);

        uniform float angle;

        uniform float coneAngle_tan = abs(tan(radians(i_coneAngle/2)));
        uniform float penumbraAngle_tan = abs(tan(radians(i_coneAngle/2 + i_penumbraAngle)));

        // TODO:  We should have a wrapper function like this for all texture lookups.
        void getTexture(string tex; float ss, tt, channel, blur; output color clr) {
            uniform float num_channels;
            if (tex != "" && textureinfo(tex, "exists", 0) == 1) {
                textureinfo( tex, "channels", num_channels );
                // Treat as if channel == 1 (red) if there only is one channel.
                uniform float channelToUse = num_channels == 1 ? 1 : channel;
                if (channelToUse == 0 || channelToUse == 5) {
                    clr = texture(tex, ss, tt, "blur", blur);
                    if (channelToUse == 5) {
                        clr = luminance(clr);
                    } else if (num_channels == 2) {
                        clr = (clr[0] + clr[1])/2;
                    }
                } else {
                    clr = float texture(tex[channelToUse - 1], ss, tt, "blur", blur);
                }
            }
        }

        void applyBlocker(
            string bkCoordsys;
            color bkTint;
            string bkTex;
            float bkChannel;
            float bkBlur;
            float bkInfl;
            float bkHedge;
            float bkWedge;
            output color lcol;
            ) {

            extern vector L;
            extern point Ps;

            if (bkCoordsys != "")
            {
                vector sAx = normalize(vtransform(bkCoordsys, "current", vector (1, 0, 0)));
                vector tAx = normalize(vtransform(bkCoordsys, "current", vector (0, 1, 0)));
                point cOrg = transform(bkCoordsys, "current", point (0, 0, 0));

                vector cOrgToP =  Ps - cOrg;
                float projOnPlaneS = sAx.cOrgToP;
                float projOnPlaneT = tAx.cOrgToP;
                point projOnPlane = cOrg + projOnPlaneS * sAx + projOnPlaneT * tAx;
                vector toProjOnPlane = projOnPlane - Ps;
                vector Ln = normalize(L);
                float cs = normalize(toProjOnPlane).Ln;
                point Pint = Ps + Ln * length(toProjOnPlane)/cs;
                vector cOrgToPint = Pint - cOrg;
                //float sBk = cOrgToPint.sAx;
                //float tBk = cOrgToPint.tAx;
                point PintCs = transform(bkCoordsys, Pint);
                float sBk = (1+PintCs[0])/2;
                float tBk = 1-(1+PintCs[1])/2;

                //lcol = (sBk, tBk, .5);
                float inBlocker = 
                          smoothstep (0, bkWedge, sBk)
                        * (1-smoothstep (1-bkWedge, 1, sBk))
                        * smoothstep (0, bkHedge, tBk)
                        * (1-smoothstep (1-bkHedge, 1, tBk));
                inBlocker *= filterstep(depth(Pint), depth(Ps));
                
                color bkClr = 1;
                getTexture(bkTex, sBk, tBk, bkChannel, bkBlur, bkClr);
                bkClr *= bkTint;
                lcol *= mix(color 1, bkClr, inBlocker * bkInfl);
            }
        }






        if (i_lightType == 0) 
        {
            /* Spot light or area light */
            uniform float maxradius = 1.4142136 * (coneAngle_tan + penumbraAngle_tan);
            angle = atan(maxradius);
        }
        else
        {
            /* Point light */
            angle = PI;
        }

        illuminate (from, axis, angle)
        {
            if (i_lightType == 2)
                L = axis * length(Ps-from); // Parallel rays.
            if (i_orthoShadow == 1)
                fromShad = Ps - normalize(axis) * 9999999;

            /* Accumulate attenuation of the light as it is affected by various
             * blockers and whatnot.  Start with no attenuation (i.e. a 
             * multiplicitive attenuation of 1.
             */
            float atten = 1.0;
            color lcol = i_lightColor * i_intensity;

            if (i_lightType == 0) { // Only for spotlight.
                atten *= getLightConeVolume(PL, i_lightType, from, axis,
                                           i_cutOn, i_cutOff,
                                           i_cutOnEdge, i_cutOffEdge, 
                                           i_cutOnShape, i_cutOffShape,
                                           coneAngle_tan, penumbraAngle_tan);

                atten *= getAngleFalloff(PL, i_beamDistribution, radians(i_coneAngle/2 + i_penumbraAngle));
                atten *=  getBarnDoors(PL,
                                   i_barnDoorLeftAngle, i_barnDoorRightAngle, i_barnDoorTopAngle, i_barnDoorBottomAngle,
                                   i_barnDoorLeftEdge, i_barnDoorRightEdge, i_barnDoorTopEdge, i_barnDoorBottomEdge,
                                   i_barnDoorLeftLength, i_barnDoorRightLength, i_barnDoorTopLength, i_barnDoorBottomLength,
                                   i_barnDoorLeftRoll, i_barnDoorRightRoll, i_barnDoorTopRoll, i_barnDoorBottomRoll);

            }
            if (i_lightType != 2) { // Not for distant light.
                atten *= getDistanceFalloff(PL, i_falloff, i_falloffDistance,
                                        i_maxIntensity/i_intensity);

            }

            /* If the volume says we aren't being lit, skip the remaining tests */
            if (atten > 0)
            {
                /* Apply OUR gobo (which works) */
                if ((i_gbTex != "") && i_gbInfl > 0 && textureinfo(i_gbTex, "exists", 0) == 1) {
                    float totalConeAngFromAxis = i_coneAngle/2 + i_penumbraAngle;
                    float m = 45/totalConeAngFromAxis;
                    float ss = PL[0]/PL[2]*m;
                    float tt = PL[1]/PL[2]*m;
                    float ang = atan(tt, ss);
                    float dist = sqrt(ss*ss + tt*tt);
                    ang += i_gbRotate;
                    ss = cos(ang)*dist;
                    tt = sin(ang)*dist;
                    ss = .5 + .5 * ss / i_gbSscale;
                    tt = .5 + .5 * tt / i_gbTscale;
                    ss += i_gbSoffset;
                    tt += i_gbToffset;
                    if (i_outOfRangeMode == 1) {
                        ss = clamp(ss, 0, 1);
                        tt = clamp(tt, 0, 1);
                    } else if (i_outOfRangeMode == 2 &&
                        (ss > 1 || ss < 0 || tt > 1 || tt < 0)) {
                        // Using filterstep for this provides a cleaner edge
                        // but causes artifacts at the edge of the light cone.
                        lcol = 0;
                    }

                    color gbClr = 1;
                    if (i_gbInfl > 0) {
                        getTexture(i_gbTex, ss, tt, 0, i_gbBlur, gbClr);
                    }
                    lcol *= mix(color 1, gbClr, i_gbInfl);
                }

                /* Apply THEIR gobos (which don't work) */
                uniform float num_gobos = arraylength(i_goboColor);
                float gobo_index;
                for (gobo_index = 0; gobo_index < num_gobos; gobo_index += 1)
                {
                    lcol *= i_goboColor[gobo_index];
                }

                /* Apply OUR blockers (which allow textures) */
#define APPLYBLOCKER(N) applyBlocker( i_bk##N##Coordsys, i_bk##N##Tint, i_bk##N##Tex, i_bk##N##Channel, i_bk##N##Blur, i_bk##N##Infl, i_bk##N##Hedge, i_bk##N##Wedge, lcol);

APPLYBLOCKER(01)
APPLYBLOCKER(02)
APPLYBLOCKER(03)
APPLYBLOCKER(04)
APPLYBLOCKER(05)
APPLYBLOCKER(06)
APPLYBLOCKER(07)
APPLYBLOCKER(08)
APPLYBLOCKER(09)
APPLYBLOCKER(10)

                /* Apply noise */
                if (i_noiseAmplitude > 0)
                {
                    float n = noise (i_noiseFrequency * (PL+vector "shader" (i_noiseOffset[0], i_noiseOffset[1], i_noiseOffset[2])) * point(1,1,0));
                    n = smoothstep (0, 1, 0.5 + i_noiseAmplitude * (n-0.5));
                    atten *= n;
                }

                /* Apply shadows */

                color unoccluded = 1;

                if (i_shadowType == 1)
                {
                    // mapped shadows
                    // map name is automatically supplied as a shader parameter by 3delight as "shadowmapname"
                    
                    
                    extern uniform string shadowmapname;

                    color shadow_total = 0;
                    // 
                    if(shadowmapname != "")
                        shadow_total += 1-color getShadowMapContribution(Ps,
                                                                    shadowmapname,
                                                                    i_shadowBlur,
                                                                    i_shadowFilterType,
                                                                    i_shadowBias,
                                                                    i_shadowSamples,
                                                                    i_useSoftShadowDecay,
                                                                    i_shadowMinimumRadius,
                                                                    i_shadowMaximumRadius,
                                                                    i_selfShadowReduce,
                                                                    i_shadowDecay,
                                                                    i_shadowDecayCutOn,
                                                                    i_shadowDecayCutOff);

                        
                    //    
                    if(i_useShadowMapsSets == 1){
                    
                        string shdCat = "shadowmap";
                        if(i_shadowMapsSetIndex != -1)
                            shdCat = format("shadowmap_%d", i_shadowMapsSetIndex);
                            
                        shader shdLights[] = getlights("category", shdCat);
                        uniform float i;
                        uniform float shdLightsSize = arraylength(shdLights);
                        for(i = 0; i <  shdLightsSize; i+=1){
                            if(shdLights[i]->shadowmapname != ""){
                                string shdmap = shdLights[i]->shadowmapname;
                                shadow_total += 1 - color getShadowMapContribution(Ps,
                                                                                    shdmap,
                                                                                    i_shadowBlur,
                                                                                    i_shadowFilterType,
                                                                                    i_shadowBias,
                                                                                    i_shadowSamples,
                                                                                    i_useSoftShadowDecay,
                                                                                    i_shadowMinimumRadius,
                                                                                    i_shadowMaximumRadius,
                                                                                    i_selfShadowReduce,
                                                                                    i_shadowDecay,
                                                                                    i_shadowDecayCutOn,
                                                                                    i_shadowDecayCutOff);
                            }
                        }
                    }

                    unoccluded = 1 - shadow_total;
                }
                else if (i_shadowType == 2)
                {
                    // ray-traced shadows
                    unoccluded = getTracedShadowContribution(Ps, fromShad,
                                                             i_traceSampleCone,
                                                             i_traceSamples,
                                                             i_traceSubset,
                                                             i_traceBias);
                }

                // Get digidouble shadows.
                if (i_digidoubleShadowType != 0)
                {
                    float digidoubleShd = 1;

                    if (i_digidoubleShadowType == 1) {
                        if (i_digidoubleShadowMap != "" &&
                                textureinfo(i_digidoubleShadowMap, "exists", 0) == 1) {
                            digidoubleShd = getShadowMapContribution(Ps,
                                                            i_digidoubleShadowMap,
                                                            i_shadowBlur,
                                                            i_shadowFilterType,
                                                            i_shadowBias,
                                                            i_shadowSamples,
                                                            i_useSoftShadowDecay,
                                                            i_shadowMinimumRadius,
                                                            i_shadowMaximumRadius,
                                                            i_selfShadowReduce,
                                                            i_shadowDecay,
                                                            i_shadowDecayCutOn,
                                                            i_shadowDecayCutOff);
                        }
                    } else {
                        color digidoubleShdClr = getTracedShadowContribution(Ps, fromShad,
                                                                 i_traceSampleCone,
                                                                 i_traceSamples,
                                                                 i_digidoubleSubset, //i_traceSubset,
                                                                 i_traceBias);
                        digidoubleShd = luminance(digidoubleShdClr);
                    }

                    string attr = "grouping:membership";
                    string membership = "";
                    attribute(attr, membership);

                    // This is how I was able get a match if digidoubleSubset = "thisSet"
                    // and membership = "thisSet", "otherSet,thisSet", "thisSet,otherSet",
                    // or "otherSet,thisSet,yetOtherSet", but NOT "suffix_thisSet".
                    // ("\<thisSet\>" syntax doesn't work).
                    float inSubset =
                        match (concat("^", i_digidoubleSubset, "$"), membership) == 1 ||
                        match (concat("^", i_digidoubleSubset, ","), membership) == 1 ||
                        match (concat(",", i_digidoubleSubset, "$"), membership) == 1 ||
                        match (concat(",", i_digidoubleSubset, ","), membership) == 1 ? 1 : 0;

                    if (inSubset > .5) {
                        // If this is a digidouble, remove digidouble shadows from other shadows.
                        unoccluded = 1-(1-unoccluded) * digidoubleShd;
                    } else {
                        // If this is NOT a digidouble, comp digidouble shadows on other shadows normally (multiply).
                        unoccluded *= digidoubleShd;
                    }

                }


                // start with shadow color
                color shadow_color = i_shadowColor;
                
                // apply shadow intensity
                unoccluded = 1 - ((1 - unoccluded) * i_shadowIntensity);
    
                /* Apply blockers */
                
                uniform float num_blockers = arraylength(i_blockerColor);
                float blocker_index;
                for (blocker_index = 0; blocker_index < num_blockers; blocker_index += 1)
                {
                    unoccluded *= i_blockerValue[blocker_index];
                    shadow_color *= i_blockerColor[blocker_index];
                }

                __unoccludedCl = lcol;
                lcol = mix(shadow_color, lcol, unoccluded);
                
                //__nonspecular = 1 - luminance(unoccluded) * (1 - __nonspecular);

                __occluded = 1 - unoccluded;
                __occlusionColor = shadow_color;
            }

            __unoccludedCl *= atten;
            Cl = lcol * atten;
        }
    """

    def draw(self, view, path, style, status):
        thisNode = self.thisMObject()
     
        fnThisNode = OpenMaya.MFnDependencyNode(thisNode)
        # light attributes
        cA = fnThisNode.attribute("coneAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        coneAngle = plug.asDouble()
        cA = fnThisNode.attribute("penumbraAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        penumbraAngle = plug.asDouble()
        cA = fnThisNode.attribute("lightType")
        plug = OpenMaya.MPlug(thisNode, cA)
        lightType = plug.asShort()
        cA = fnThisNode.attribute("cutOnEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        cutOnEdge = plug.asDouble()
        cA = fnThisNode.attribute("cutOn")
        plug = OpenMaya.MPlug(thisNode, cA)
        cutOn = plug.asDouble()
        cA = fnThisNode.attribute("cutOff")
        plug = OpenMaya.MPlug(thisNode, cA)
        cutOff = plug.asDouble()
        cA = fnThisNode.attribute("cutOffEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        cutOffEdge = plug.asDouble()
        # viewport display attributes
        cA = fnThisNode.attribute("displayLightLimits")
        plug = OpenMaya.MPlug(thisNode, cA)
        displayLightLimits = plug.asBool()
        cA = fnThisNode.attribute("displayPenumbraAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        displayPenumbraAngle = plug.asBool()
        cA = fnThisNode.attribute("iconSize")
        plug = OpenMaya.MPlug(thisNode, cA)
        iconSize = plug.asDouble()
        cA = fnThisNode.attribute("displayFalloff")
        plug = OpenMaya.MPlug(thisNode, cA)
        displayFalloff = plug.asBool()
        cA = fnThisNode.attribute("falloff")
        plug = OpenMaya.MPlug(thisNode, cA)
        falloffType = plug.asShort()
        
        #Barn doors.
        cA = fnThisNode.attribute("displayBarnDoors")
        plug = OpenMaya.MPlug(thisNode, cA)
        displayBarnDoors = plug.asBool()
        cA = fnThisNode.attribute("barnDoorLeftAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnLang = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorLeftEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnLedge = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorLeftLength")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnLlength = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorLeftRoll")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnLroll = plug.asDouble()

        cA = fnThisNode.attribute("barnDoorRightAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnRang = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorRightEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnRedge = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorRightLength")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnRlength = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorRightRoll")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnRroll = plug.asDouble()

        cA = fnThisNode.attribute("barnDoorTopAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnTang = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorTopEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnTedge = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorTopLength")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnTlength = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorTopRoll")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnTroll = plug.asDouble()

        cA = fnThisNode.attribute("barnDoorBottomAngle")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnBang = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorBottomEdge")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnBedge = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorBottomLength")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnBlength = plug.asDouble()
        cA = fnThisNode.attribute("barnDoorBottomRoll")
        plug = OpenMaya.MPlug(thisNode, cA)
        barnBroll = plug.asDouble()
        
        coneHeight = 1.0
        divs = 30

        if (cutOnEdge > cutOn):
            cutOnEdge = cutOn;
        coneRadius = coneHeight * math.tan(math.pi * (coneAngle / 2) / 180)
        falloffRadius = coneHeight * math.tan(math.pi * (coneAngle / 2 + penumbraAngle) / 180)
        cutOnRadius = cutOn * math.tan(math.pi * (coneAngle / 2) / 180)
        cutOnEdgeRadius = (cutOn - cutOnEdge) * math.tan(math.pi * (coneAngle / 2) / 180)
        cutOffRadius = cutOff * math.tan(math.pi * (coneAngle / 2) / 180)
        cutOffEdgeRadius = (cutOff + cutOffEdge) * math.tan(math.pi * (coneAngle / 2) / 180)
        cutOffRadiusEdge = cutOff * math.tan(math.pi * (coneAngle / 2 + penumbraAngle) / 180)
        
        view.beginGL()
        
        glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        # Color of main light cone ui.
        def dormantColor(clrNum):
            if status == OpenMayaUI.M3dView.kDormant:
                view.setDrawColor(clrNum, OpenMayaUI.M3dView.kActiveColors)
            
        dormantColor(11)
        # Colours: 
        # 0 = black, 1 = mid grey, 2 = light grey, 3 = burgundy, 4 = dark blue,
        # 5 = mid blue, 6 = dark green, 7 = dark purple, 8 = pink, 9 = burgundy again,
        # 11 = burgundy again, 12 = red, 13 = green, 14 = blue, 15 = white, 16 = yellow

        
        if(lightType == 0):
            # draw light cone base
            glFT.glPushMatrix()
            glFT.glScalef(iconSize, iconSize, iconSize)
            glFT.glPushMatrix()
            glFT.glTranslated(0, 0, - coneHeight)
            glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
            for i in range(0, divs, 1):
                angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                glFT.glVertex3f(math.cos(angle) * coneRadius, math.sin(angle) * coneRadius, 0.0)
            glFT.glEnd()
            # draw light cone edge
            if displayPenumbraAngle:
                if (iconSize < cutOff):
                    glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
                    dormantColor(14)
                    glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                    for i in range(0, divs, 1):
                        angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                        glFT.glVertex3f(math.cos(angle) * falloffRadius, math.sin(angle) * falloffRadius, 0.0)
                    glFT.glEnd()
                    glFT.glPopAttrib()
            glFT.glPopMatrix()
            # draw center arrow
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0, 0, 0)
            glFT.glVertex3f(-coneRadius, 0, - coneHeight)
            glFT.glVertex3f(0, 0, 0)
            glFT.glVertex3f(coneRadius, 0, - coneHeight)
            glFT.glVertex3f(0, 0, 0)
            glFT.glVertex3f(0, - coneRadius, - coneHeight)
            glFT.glVertex3f(0, 0, 0)
            glFT.glVertex3f(0, coneRadius, - coneHeight)
            glFT.glVertex3f(0, 0, 0)
            glFT.glVertex3f(0, 0, - (coneHeight + 0.5))
            glFT.glVertex3f(0, 0, - (coneHeight + 0.5))
            glFT.glVertex3f(0, 0.06, - (coneHeight + 0.2))
            glFT.glVertex3f(0, 0, - (coneHeight + 0.5))
            glFT.glVertex3f(0, - 0.06, - (coneHeight + 0.2))
            glFT.glVertex3f(0, 0.06, - (coneHeight + 0.2))
            glFT.glVertex3f(0, - 0.06, - (coneHeight + 0.2))
            glFT.glVertex3f(0, 0, - (coneHeight + 0.5))
            glFT.glVertex3f(0.06, 0, - (coneHeight + 0.2))
            glFT.glVertex3f(0, 0, - (coneHeight + 0.5))
            glFT.glVertex3f(-0.06, 0, - (coneHeight + 0.2))
            glFT.glVertex3f(0.06, 0, - (coneHeight + 0.2))
            glFT.glVertex3f(-0.06, 0, - (coneHeight + 0.2))
            glFT.glEnd()
        
                
            if displayLightLimits:
                # draw cut on edge
                if (cutOnEdge > 0):
                    glFT.glPushMatrix()
                    glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
                    glFT.glLineWidth(2.0)
                    dormantColor(6)
                    glFT.glTranslated(0, 0, cutOnEdge - cutOn)
                    glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                    for i in range(0, divs, 1):
                        angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                        glFT.glVertex3f(math.cos(angle) * cutOnEdgeRadius, math.sin(angle) * cutOnEdgeRadius, 0.0)
                    glFT.glEnd()
                    glFT.glPopAttrib()
                    glFT.glPopMatrix()
                # draw cut on
                glFT.glPushMatrix()
                glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
                glFT.glLineWidth(2.0)
                if (cutOn >= cutOff):
                    cutOn = cutOff
                    cutOnRadius = cutOn * math.tan(math.pi * (coneAngle / 2) / 180)
                    dormantColor(12)
                else:
                    dormantColor(16)
                glFT.glTranslated(0, 0, - cutOn)
                glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                for i in range(0, divs, 1):
                    angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                    glFT.glVertex3f(math.cos(angle) * cutOnRadius, math.sin(angle) * cutOnRadius, 0.0)
                glFT.glEnd()
                glFT.glPopMatrix()
                # draw cut off
                glFT.glPushMatrix()
                glFT.glTranslated(0, 0, - cutOff)
                glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                for i in range(0, divs, 1):
                    angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                    glFT.glVertex3f(math.cos(angle) * cutOffRadius, math.sin(angle) * cutOffRadius, 0.0)
                glFT.glEnd()
                glFT.glPopAttrib()
                if displayPenumbraAngle:
                    glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
                    dormantColor(14)
                    glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                    for i in range(0, divs, 1):
                        angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                        glFT.glVertex3f(math.cos(angle) * cutOffRadiusEdge, math.sin(angle) * cutOffRadiusEdge, 0.0)
                    glFT.glEnd()
                    glFT.glPopAttrib()
                glFT.glPopMatrix()
                # draw cut off edge
                if (cutOffEdge > 0):
                    glFT.glPushMatrix()
                    glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
                    glFT.glLineWidth(2.0)
                    dormantColor(6)
                    glFT.glTranslated(0, 0, -cutOffEdge - cutOff)
                    glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
                    for i in range(0, divs, 1):
                        angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
                        glFT.glVertex3f(math.cos(angle) * cutOffEdgeRadius, math.sin(angle) * cutOffEdgeRadius, 0.0)
                    glFT.glEnd()
                    glFT.glPopAttrib()
                    glFT.glPopMatrix()
		
		if displayFalloff:
			phiRadius = 0.4
			phiLine = 0.45
			glFT.glHint(OpenMayaRender.MGL_LINE_SMOOTH_HINT, OpenMayaRender.MGL_NICEST);
			glFT.glEnable(OpenMayaRender.MGL_BLEND)
			glFT.glEnable(OpenMayaRender.MGL_LINE_SMOOTH)
			glFT.glBlendFunc (OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
			if (falloffType == 0):
				glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
				glFT.glLineWidth(2.0)
				dormantColor(3)
				glFT.glPushMatrix()
				glFT.glTranslated(0, 0, - cutOff)
				glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
				for i in range(0, divs, 1):
					angle = (i * 360.0 / divs) * 3.1415926535898 / 180.0
					glFT.glVertex3f(math.cos(angle) * phiRadius, math.sin(angle) * phiRadius, 0.0)
				glFT.glEnd()
				glFT.glBegin(OpenMayaRender.MGL_LINES)
				glFT.glVertex3f( phiLine,  phiLine, 0)
				glFT.glVertex3f(-phiLine, -phiLine, 0)
				glFT.glEnd()
				glFT.glPopMatrix()
				glFT.glPopAttrib()
			if (falloffType == 1):
				glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
				glFT.glLineWidth(2.0)
				dormantColor(3)
				glFT.glPushMatrix()
				glFT.glTranslated(0, 0, - cutOff)
				glFT.glBegin(OpenMayaRender.MGL_LINES)
				glFT.glVertex3f(-phiLine, phiLine * 0.75, 0)
				glFT.glVertex3f( phiLine, phiLine * 0.75, 0)
				glFT.glVertex3f(-phiLine, 0, 0)
				glFT.glVertex3f( phiLine, 0, 0)
				glFT.glVertex3f(-phiLine,-phiLine * 0.75, 0)
				glFT.glVertex3f( phiLine,-phiLine * 0.75, 0)
				glFT.glEnd()
				glFT.glPopMatrix()
				glFT.glPopAttrib()
			if (falloffType == 2):
				glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
				glFT.glLineWidth(2.0)
				dormantColor(3)
				glFT.glPushMatrix()
				glFT.glTranslated(0, 0, - cutOff)
				glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
				glFT.glVertex3f(-phiLine, phiLine, 0)
				glFT.glVertex3f( phiLine, phiLine, 0)
				glFT.glVertex3f( phiLine,-phiLine, 0)
				glFT.glVertex3f(-phiLine,-phiLine, 0)
				glFT.glEnd()
				glFT.glPopMatrix()
				glFT.glPopAttrib()
			glFT.glDisable(OpenMayaRender.MGL_LINE_SMOOTH)
			glFT.glDisable(OpenMayaRender.MGL_BLEND)

        if(displayBarnDoors == 1):

            def sum2d2d(a1, a2):
                return [a1[0] + a2[0], a1[1] + a2[1]]

            def multF2d(f, a):
                return [f*a[0], f*a[1]]

            def sub2d2d(a1, a2):
                return sum2d2d(a1, multF2d(-1, a2))

            def lineIntersect(P1, P2, P3, P4):
                # from http://ozviz.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
                # The intersection is where
                # P1 + ua * (P2 - P1) = 
                # P3 + ub * (P4 - P3)
                # solve for ua or ub
                x1 = P1[0]
                y1 = P1[1]
                x2 = P2[0]
                y2 = P2[1]
                x3 = P3[0]
                y3 = P3[1]
                x4 = P4[0]
                y4 = P4[1]
                ans = [0, 0]

                denom = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
                if (denom !=0):
                    ua = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/denom
                    ans = sum2d2d(P1, multF2d(ua, sub2d2d(P2, P1)))

                return ans

            def rot2d(P, ang):
                x = P[0]
                y = P[1]
                xx = x
                yy = y
                dist = math.sqrt(x*x + y*y)
                if (dist > 0):
                    newAng = math.acos(y/dist) + ang
                    xx = math.sin(newAng)*dist
                    yy = math.cos(newAng)*dist
                return [xx, yy]

               
            z = -max(coneHeight, cutOn);

            barnRattrs = [barnRang, barnRroll, barnRedge, barnRlength, [], []]
            barnBattrs = [barnBang, barnBroll, barnBedge, barnBlength, [], []]
            barnLattrs = [barnLang, barnLroll, barnLedge, barnLlength, [], []]
            barnTattrs = [barnTang, barnTroll, barnTedge, barnTlength, [], []]

            # Store the left and right neighbour's parms in the last
            # 2 cells (would be nice if we knew how to link...)
            barnRattrs[4] = barnBattrs
            barnBattrs[4] = barnLattrs
            barnLattrs[4] = barnTattrs
            barnTattrs[4] = barnRattrs

            barnBattrs[5] = barnRattrs
            barnLattrs[5] = barnBattrs
            barnTattrs[5] = barnLattrs
            barnRattrs[5] = barnTattrs

            # Make multidimensional list: 2 layers (inner + outer) X 4 corners X 2 coordinates.
            coords = [[[[] for inner in range(2)] for outer in range(4)] for inner in range(2)]

            innerBdClr = 8
            outerBdClr = 7
            allattrs = [barnBattrs, barnLattrs, barnTattrs, barnRattrs]


            # Find all 16 coordinates.
            for outer in [0, 1]:
                corner = 0
                if (outer == 0):
                    dormantColor(innerBdClr)
                else:
                    dormantColor(outerBdClr)

                for attrs in allattrs:
                    thisAng = math.radians(attrs[0])
                    thisRoll = math.radians(attrs[1])
                    thisEdge = math.radians(attrs[2])
                    nbrAng = math.radians(attrs[4][0])
                    nbrRoll = math.radians(attrs[4][1])
                    nbrEdge = math.radians(attrs[4][2])

                    dist = math.tan(min(thisAng + thisEdge*outer, math.pi*.49)) * z
                    nbrdist = math.tan(min(nbrAng + nbrEdge*outer, math.pi*.49))* z

                    thisP0 = rot2d([0, dist], -thisRoll)
                    thisP1 = rot2d([1, dist], -thisRoll)
                    nbrP0 = rot2d([0, nbrdist], -nbrRoll + math.pi/2)
                    nbrP1 = rot2d([1, nbrdist], -nbrRoll + math.pi/2)
                    int = lineIntersect(thisP0, thisP1, nbrP0, nbrP1)
                    xx = int[0]
                    yy = int[1]

                
                    # Simplistic 90 degree rotation.
                    if (corner == 0):
                        xxx = xx
                        yyy = yy
                    elif (corner == 1):
                        xxx = yy
                        yyy = -xx
                    elif (corner == 2):
                        xxx = -xx
                        yyy = -yy
                    else:
                        xxx = -yy
                        yyy = xx
                    coords[outer][corner][0] = xxx
                    coords[outer][corner][1] = yyy
                    corner += 1
            
            # Draw outer rectangle, inner rectangle and lines connecting them.
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            for prev in range(4):
                corner = prev + 1
                if (corner == 4):
                    corner = 0
                next = corner + 1
                if (next == 4):
                    next = 0
                #it appears that allattrs[corner][5] = allattrs[prevNbr][4] = allattrs[prev]

                thisAng = allattrs[corner][0]
                prevAng = allattrs[prev][0]
                thisEdge = allattrs[corner][2]
                # Only draw this edge if its ang < 90

                if (thisAng < 90):
                    # Draw inner line.
                    dormantColor(innerBdClr)
                    dimension = (prev + 1) % 2
                    glFT.glVertex3f(coords[0][prev][0], coords[0][prev][1], z)
                    glFT.glVertex3f(coords[0][corner][0], coords[0][corner][1], z)
                    # Draw connecting line (only if neighbour's ang is also < 90)
                    glFT.glVertex3f(coords[0][prev][0], coords[0][prev][1], z)
                    dormantColor(outerBdClr)
                    glFT.glVertex3f(coords[1][prev][0], coords[1][prev][1], z)

                    if (thisEdge > 0):
                        # Draw outer line (only if edge is > 0)
                        dormantColor(outerBdClr)
                        start = coords[1][corner][dimension]/(coords[1][corner][dimension]-coords[1][prev][dimension])
                        glFT.glVertex3f(coords[1][prev][0], coords[1][prev][1], z)
                        glFT.glVertex3f(coords[1][corner][0], coords[1][corner][1], z)
            glFT.glEnd()

        
        if(lightType == 1):
            pointRadius = 0.1
            pointRayLength = 0.1
            pointDivs = 16
            
            glFT.glPushMatrix()
            glFT.glScalef(iconSize, iconSize, iconSize)
            glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
            glFT.glLineWidth(2.0)
            glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
            for i in range(0, pointDivs, 1):
                angle = (i * 360.0 / pointDivs) * 3.1415926535898 / 180.0
                glFT.glVertex3f(math.cos(angle) * pointRadius, math.sin(angle) * pointRadius, 0.0)
            glFT.glEnd()
            glFT.glPopAttrib()
            glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
            glFT.glLineWidth(1.0)
            glFT.glPushMatrix()
            glFT.glTranslatef(0.0, pointRadius, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(0.0, pointRayLength, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(0.0, - pointRadius, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(0.0, - pointRayLength, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(pointRadius, 0.0, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(pointRayLength, 0.0, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(-pointRadius, 0.0, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(-pointRayLength, 0.0, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glRotatef(45.0, 0.0, 0.0, 1.0)
            glFT.glPushMatrix()
            glFT.glTranslatef(0.0, pointRadius, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(0.0, pointRayLength, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(0.0, - pointRadius, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(0.0, - pointRayLength, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(pointRadius, 0.0, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(pointRayLength, 0.0, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPushMatrix()
            glFT.glTranslatef(-pointRadius, 0.0, 0.0)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            glFT.glVertex3f(0.0, 0.0, 0.0)
            glFT.glVertex3f(-pointRayLength, 0.0, 0.0)
            glFT.glEnd()
            glFT.glPopMatrix()
            glFT.glPopMatrix()
            glFT.glPopAttrib()
            glFT.glPopMatrix()
        
        if(lightType == 2):
            glFT.glPushMatrix()
            glFT.glScalef(iconSize, iconSize, iconSize)
            glFT.glBegin(OpenMayaRender.MGL_LINES)
            spacing = .3
            len = 1.5
            halflen = len/2.0
            headlen = .2
            xpos = -spacing
            for i in range(0, 3):
                ydisp = -.2
                if (i == 1):
                    ydisp = -ydisp
                glFT.glVertex3f(xpos, ydisp, halflen)
                glFT.glVertex3f(xpos, ydisp, - halflen)
                glFT.glVertex3f(xpos, ydisp, - halflen)
                glFT.glVertex3f(xpos, ydisp + 0.04,  -halflen + headlen)
                glFT.glVertex3f(xpos, ydisp + 0, 0. - halflen)
                glFT.glVertex3f(xpos, ydisp - 0.04,  -halflen + headlen)
                glFT.glVertex3f(xpos, ydisp + 0.04,  -halflen + headlen)
                glFT.glVertex3f(xpos, ydisp - 0.04,  -halflen + headlen)
                glFT.glVertex3f(xpos, ydisp, - halflen)
                glFT.glVertex3f(xpos+0.04, ydisp,  -halflen + headlen)
                glFT.glVertex3f(xpos, ydisp, 0. - halflen)
                glFT.glVertex3f(xpos-0.04, ydisp,  -halflen + headlen)
                glFT.glVertex3f(xpos+0.04, ydisp,  -halflen + headlen)
                glFT.glVertex3f(xpos-0.04, ydisp,  -halflen + headlen)
                xpos += spacing
            glFT.glEnd()
            glFT.glPopMatrix()
        
        glFT.glPopAttrib()
        
        view.endGL()

def initializePlugin(obj):
	dl_uberLightShape.register(obj)

def uninitializePlugin(obj):
	dl_uberLightShape.deregister(obj)
