#ifndef __dl_uberLightShape_h
#define __dl_uberLightShape_h

/*
begin inputs
	uniform float falloff
	uniform float falloffDistance
	uniform float maxIntensity
	uniform float coneAngle
	uniform float penumbraAngle
	uniform float beamDistribution
	uniform float contributeDiffuse
	uniform float contributeSpecular
	uniform float contributeTranslucence
	texture string gbTex
	float gbBlur
	float gbInfl
	float gbSoffset
	float gbToffset
	float gbSscale
	float gbTscale
	float gbRotate
	uniform float outOfRangeMode
	uniform string bk01Coordsys
	float bk01Infl
	uniform color bk01Tint
	texture string bk01Tex
	uniform float bk01Channel
	float bk01Blur
	uniform float bk01Hedge
	uniform float bk01Wedge
	uniform string bk02Coordsys
	float bk02Infl
	uniform color bk02Tint
	texture string bk02Tex
	uniform float bk02Channel
	float bk02Blur
	uniform float bk02Hedge
	uniform float bk02Wedge
	uniform string bk03Coordsys
	float bk03Infl
	uniform color bk03Tint
	texture string bk03Tex
	uniform float bk03Channel
	float bk03Blur
	uniform float bk03Hedge
	uniform float bk03Wedge
	uniform string bk04Coordsys
	float bk04Infl
	uniform color bk04Tint
	texture string bk04Tex
	uniform float bk04Channel
	float bk04Blur
	uniform float bk04Hedge
	uniform float bk04Wedge
	uniform string bk05Coordsys
	float bk05Infl
	uniform color bk05Tint
	texture string bk05Tex
	uniform float bk05Channel
	float bk05Blur
	uniform float bk05Hedge
	uniform float bk05Wedge
	uniform string bk06Coordsys
	float bk06Infl
	uniform color bk06Tint
	texture string bk06Tex
	uniform float bk06Channel
	float bk06Blur
	uniform float bk06Hedge
	uniform float bk06Wedge
	uniform string bk07Coordsys
	float bk07Infl
	uniform color bk07Tint
	texture string bk07Tex
	uniform float bk07Channel
	float bk07Blur
	uniform float bk07Hedge
	uniform float bk07Wedge
	uniform string bk08Coordsys
	float bk08Infl
	uniform color bk08Tint
	texture string bk08Tex
	uniform float bk08Channel
	float bk08Blur
	uniform float bk08Hedge
	uniform float bk08Wedge
	uniform string bk09Coordsys
	float bk09Infl
	uniform color bk09Tint
	texture string bk09Tex
	uniform float bk09Channel
	float bk09Blur
	uniform float bk09Hedge
	uniform float bk09Wedge
	uniform string bk10Coordsys
	float bk10Infl
	uniform color bk10Tint
	texture string bk10Tex
	uniform float bk10Channel
	float bk10Blur
	uniform float bk10Hedge
	uniform float bk10Wedge
	uniform float cutOn
	uniform float cutOnEdge
	uniform float cutOnShape
	uniform float cutOff
	uniform float cutOffEdge
	uniform float cutOffShape
	uniform float barnDoorLeftAngle
	uniform float barnDoorLeftEdge
	uniform float barnDoorLeftRoll
	uniform float barnDoorRightAngle
	uniform float barnDoorRightEdge
	uniform float barnDoorRightRoll
	uniform float barnDoorTopAngle
	uniform float barnDoorTopEdge
	uniform float barnDoorTopRoll
	uniform float barnDoorBottomAngle
	uniform float barnDoorBottomEdge
	uniform float barnDoorBottomRoll
	float noiseAmplitude
	float noiseFrequency
	float3 noiseOffset
	color shadowColor
	float shadowIntensity
	uniform float useAmbientOcclusion
	uniform float orthoShadow
	uniform float shadowType
	uniform float useShadowMapsSets
	uniform float shadowMapsSetIndex
	uniform float shadowBlur
	uniform float shadowFilterType
	uniform float shadowBias
	uniform float shadowSamples
	uniform float useSoftShadowDecay
	uniform float shadowMinimumRadius
	uniform float shadowMaximumRadius
	uniform float selfShadowReduce
	uniform float shadowDecay
	uniform float shadowDecayCutOn
	uniform float shadowDecayCutOff
	uniform float traceSampleCone
	uniform float traceSamples
	uniform string traceSubset
	uniform float traceBias
	uniform float digidoubleShadowType
	uniform string digidoubleSubset
	uniform string digidoubleShadowMap
	color[] blockers[].blockerColor
	float[] blockers[].blockerValue
	color[] gobos[].goboColor
	uniform float displayPenumbraAngle
	uniform float displayLightLimits
	uniform float displayBarnDoors
	uniform float displayFalloff
	uniform float iconSize
	uniform float lightType
	uniform float barnDoorLeftLength
	uniform float barnDoorRightLength
	uniform float barnDoorTopLength
	uniform float barnDoorBottomLength
	uniform float intensity
	uniform color lightColor
end inputs

begin shader_extra_parameters lightsource
	output varying color __occluded = color (0, 0, 0);
	output varying color __occlusionColor = color (0, 0, 0);
	output varying color __unoccludedCl = color (0, 0, 0);
	output float __contribTranslucence = 0.0;
	output float __useAmbientOcclusion = 0.0;
	uniform string __category = "";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

#include "uberlight_utils.h"
#include "shadow_utils.h"
#include "utils.h"

void
maya_dl_uberLightShape(
	// Inputs
	//
	uniform float i_falloff;
	uniform float i_falloffDistance;
	uniform float i_maxIntensity;
	uniform float i_coneAngle;
	uniform float i_penumbraAngle;
	uniform float i_beamDistribution;
	uniform float i_contributeDiffuse;
	uniform float i_contributeSpecular;
	uniform float i_contributeTranslucence;
	uniform string i_gbTex;
	float i_gbBlur;
	float i_gbInfl;
	float i_gbSoffset;
	float i_gbToffset;
	float i_gbSscale;
	float i_gbTscale;
	float i_gbRotate;
	uniform float i_outOfRangeMode;
	uniform string i_bk01Coordsys;
	float i_bk01Infl;
	uniform color i_bk01Tint;
	uniform string i_bk01Tex;
	uniform float i_bk01Channel;
	float i_bk01Blur;
	uniform float i_bk01Hedge;
	uniform float i_bk01Wedge;
	uniform string i_bk02Coordsys;
	float i_bk02Infl;
	uniform color i_bk02Tint;
	uniform string i_bk02Tex;
	uniform float i_bk02Channel;
	float i_bk02Blur;
	uniform float i_bk02Hedge;
	uniform float i_bk02Wedge;
	uniform string i_bk03Coordsys;
	float i_bk03Infl;
	uniform color i_bk03Tint;
	uniform string i_bk03Tex;
	uniform float i_bk03Channel;
	float i_bk03Blur;
	uniform float i_bk03Hedge;
	uniform float i_bk03Wedge;
	uniform string i_bk04Coordsys;
	float i_bk04Infl;
	uniform color i_bk04Tint;
	uniform string i_bk04Tex;
	uniform float i_bk04Channel;
	float i_bk04Blur;
	uniform float i_bk04Hedge;
	uniform float i_bk04Wedge;
	uniform string i_bk05Coordsys;
	float i_bk05Infl;
	uniform color i_bk05Tint;
	uniform string i_bk05Tex;
	uniform float i_bk05Channel;
	float i_bk05Blur;
	uniform float i_bk05Hedge;
	uniform float i_bk05Wedge;
	uniform string i_bk06Coordsys;
	float i_bk06Infl;
	uniform color i_bk06Tint;
	uniform string i_bk06Tex;
	uniform float i_bk06Channel;
	float i_bk06Blur;
	uniform float i_bk06Hedge;
	uniform float i_bk06Wedge;
	uniform string i_bk07Coordsys;
	float i_bk07Infl;
	uniform color i_bk07Tint;
	uniform string i_bk07Tex;
	uniform float i_bk07Channel;
	float i_bk07Blur;
	uniform float i_bk07Hedge;
	uniform float i_bk07Wedge;
	uniform string i_bk08Coordsys;
	float i_bk08Infl;
	uniform color i_bk08Tint;
	uniform string i_bk08Tex;
	uniform float i_bk08Channel;
	float i_bk08Blur;
	uniform float i_bk08Hedge;
	uniform float i_bk08Wedge;
	uniform string i_bk09Coordsys;
	float i_bk09Infl;
	uniform color i_bk09Tint;
	uniform string i_bk09Tex;
	uniform float i_bk09Channel;
	float i_bk09Blur;
	uniform float i_bk09Hedge;
	uniform float i_bk09Wedge;
	uniform string i_bk10Coordsys;
	float i_bk10Infl;
	uniform color i_bk10Tint;
	uniform string i_bk10Tex;
	uniform float i_bk10Channel;
	float i_bk10Blur;
	uniform float i_bk10Hedge;
	uniform float i_bk10Wedge;
	uniform float i_cutOn;
	uniform float i_cutOnEdge;
	uniform float i_cutOnShape;
	uniform float i_cutOff;
	uniform float i_cutOffEdge;
	uniform float i_cutOffShape;
	uniform float i_barnDoorLeftAngle;
	uniform float i_barnDoorLeftEdge;
	uniform float i_barnDoorLeftRoll;
	uniform float i_barnDoorRightAngle;
	uniform float i_barnDoorRightEdge;
	uniform float i_barnDoorRightRoll;
	uniform float i_barnDoorTopAngle;
	uniform float i_barnDoorTopEdge;
	uniform float i_barnDoorTopRoll;
	uniform float i_barnDoorBottomAngle;
	uniform float i_barnDoorBottomEdge;
	uniform float i_barnDoorBottomRoll;
	float i_noiseAmplitude;
	float i_noiseFrequency;
	float i_noiseOffset[3];
	color i_shadowColor;
	float i_shadowIntensity;
	uniform float i_useAmbientOcclusion;
	uniform float i_orthoShadow;
	uniform float i_shadowType;
	uniform float i_useShadowMapsSets;
	uniform float i_shadowMapsSetIndex;
	uniform float i_shadowBlur;
	uniform float i_shadowFilterType;
	uniform float i_shadowBias;
	uniform float i_shadowSamples;
	uniform float i_useSoftShadowDecay;
	uniform float i_shadowMinimumRadius;
	uniform float i_shadowMaximumRadius;
	uniform float i_selfShadowReduce;
	uniform float i_shadowDecay;
	uniform float i_shadowDecayCutOn;
	uniform float i_shadowDecayCutOff;
	uniform float i_traceSampleCone;
	uniform float i_traceSamples;
	uniform string i_traceSubset;
	uniform float i_traceBias;
	uniform float i_digidoubleShadowType;
	uniform string i_digidoubleSubset;
	uniform string i_digidoubleShadowMap;
	color i_blockerColor[];
	float i_blockerValue[];
	color i_goboColor[];
	uniform float i_displayPenumbraAngle;
	uniform float i_displayLightLimits;
	uniform float i_displayBarnDoors;
	uniform float i_displayFalloff;
	uniform float i_iconSize;
	uniform float i_lightType;
	uniform float i_barnDoorLeftLength;
	uniform float i_barnDoorRightLength;
	uniform float i_barnDoorTopLength;
	uniform float i_barnDoorBottomLength;
	uniform float i_intensity;
	uniform color i_lightColor;
	)
{

    extern color Cl;
    extern vector L;
    extern point Ps;
    extern point P;
    extern normal N;
    extern normal Ns;
    extern vector I;
    extern float __nonspecular;
    extern float __nondiffuse;
        

       
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
}

#endif /* __dl_uberLightShape_h */
