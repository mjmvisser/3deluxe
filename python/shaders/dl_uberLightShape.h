#ifndef __dl_uberLightShape_h
#define __dl_uberLightShape_h

/*
begin inputs
	uniform float lightType
	uniform float intensity
	uniform color lightColor
	uniform float falloff
	uniform float falloffDistance
	uniform float maxIntensity
	uniform float coneAngle
	uniform float penumbraAngle
	uniform float beamDistribution
	uniform float contributeDiffuse
	uniform float contributeSpecular
	uniform float contributeTranslucence
	prepare color goboColor
	prepare float goboAlpha
	uniform float cutOn
	uniform float cutOnEdge
	uniform float cutOnShape
	uniform float cutOff
	uniform float cutOffEdge
	uniform float cutOffShape
	uniform float barnDoorLeftAngle
	uniform float barnDoorLeftEdge
	uniform float barnDoorLeftLength
	uniform float barnDoorLeftRoll
	uniform float barnDoorRightAngle
	uniform float barnDoorRightEdge
	uniform float barnDoorRightLength
	uniform float barnDoorRightRoll
	uniform float barnDoorTopAngle
	uniform float barnDoorTopEdge
	uniform float barnDoorTopLength
	uniform float barnDoorTopRoll
	uniform float barnDoorBottomAngle
	uniform float barnDoorBottomEdge
	uniform float barnDoorBottomLength
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
	color[] blockers[].blockerColor
	float[] blockers[].blockerValue
	uniform float digidoubleShadowType
	uniform string digidoubleSubset
	uniform string digidoubleShadowMap
	uniform float displayPenumbraAngle
	uniform float displayLightLimits
	uniform float displayBarnDoors
	uniform float displayFalloff
	uniform float iconSize
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
prepare_maya_dl_uberLightShape(
	// Inputs
	//
	uniform float i_lightType;
	uniform float i_intensity;
	uniform color i_lightColor;
	uniform float i_falloff;
	uniform float i_falloffDistance;
	uniform float i_maxIntensity;
	uniform float i_coneAngle;
	uniform float i_penumbraAngle;
	uniform float i_beamDistribution;
	uniform float i_contributeDiffuse;
	uniform float i_contributeSpecular;
	uniform float i_contributeTranslucence;
	color i_goboColor;
	float i_goboAlpha;
	uniform float i_cutOn;
	uniform float i_cutOnEdge;
	uniform float i_cutOnShape;
	uniform float i_cutOff;
	uniform float i_cutOffEdge;
	uniform float i_cutOffShape;
	uniform float i_barnDoorLeftAngle;
	uniform float i_barnDoorLeftEdge;
	uniform float i_barnDoorLeftLength;
	uniform float i_barnDoorLeftRoll;
	uniform float i_barnDoorRightAngle;
	uniform float i_barnDoorRightEdge;
	uniform float i_barnDoorRightLength;
	uniform float i_barnDoorRightRoll;
	uniform float i_barnDoorTopAngle;
	uniform float i_barnDoorTopEdge;
	uniform float i_barnDoorTopLength;
	uniform float i_barnDoorTopRoll;
	uniform float i_barnDoorBottomAngle;
	uniform float i_barnDoorBottomEdge;
	uniform float i_barnDoorBottomLength;
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
	color i_blockerColor[];
	float i_blockerValue[];
	uniform float i_digidoubleShadowType;
	uniform string i_digidoubleSubset;
	uniform string i_digidoubleShadowMap;
	uniform float i_displayPenumbraAngle;
	uniform float i_displayLightLimits;
	uniform float i_displayBarnDoors;
	uniform float i_displayFalloff;
	uniform float i_iconSize;
	)
{

        uniform point from = point "shader" (0,0,0);
        uniform point to = point "shader" (0,0,1);

        extern vector L;
        extern float ss, tt;

        float coneangle = radians(i_coneAngle);
        float penumbraangle = radians(i_penumbraAngle);
        float max_angle = coneangle / 2;
        if( penumbraangle > 0.0 )
                max_angle += penumbraangle;


        uniform vector A = (to - from)/length(to-from);
        uniform vector xaxis = A ^ vector "shader" (1,0,0);
        if (length(xaxis) == 0)
                xaxis = A ^ vector "shader" (0,1,0);

        uniform vector yaxis = normalize(A ^ xaxis);

        illuminate( from, A, max_angle )
        {
                float anglex = atan(L.xaxis, L.A);
                float angley = atan(L.yaxis, L.A);

                tt = 1 - ((tan(anglex) / tan(max_angle)) * 0.5 + 0.5);
                ss = (tan(angley) / tan(max_angle)) * 0.5 + 0.5;
        }
}

void
end_maya_dl_uberLightShape(
	// Inputs
	//
	uniform float i_lightType;
	uniform float i_intensity;
	uniform color i_lightColor;
	uniform float i_falloff;
	uniform float i_falloffDistance;
	uniform float i_maxIntensity;
	uniform float i_coneAngle;
	uniform float i_penumbraAngle;
	uniform float i_beamDistribution;
	uniform float i_contributeDiffuse;
	uniform float i_contributeSpecular;
	uniform float i_contributeTranslucence;
	color i_goboColor;
	float i_goboAlpha;
	uniform float i_cutOn;
	uniform float i_cutOnEdge;
	uniform float i_cutOnShape;
	uniform float i_cutOff;
	uniform float i_cutOffEdge;
	uniform float i_cutOffShape;
	uniform float i_barnDoorLeftAngle;
	uniform float i_barnDoorLeftEdge;
	uniform float i_barnDoorLeftLength;
	uniform float i_barnDoorLeftRoll;
	uniform float i_barnDoorRightAngle;
	uniform float i_barnDoorRightEdge;
	uniform float i_barnDoorRightLength;
	uniform float i_barnDoorRightRoll;
	uniform float i_barnDoorTopAngle;
	uniform float i_barnDoorTopEdge;
	uniform float i_barnDoorTopLength;
	uniform float i_barnDoorTopRoll;
	uniform float i_barnDoorBottomAngle;
	uniform float i_barnDoorBottomEdge;
	uniform float i_barnDoorBottomLength;
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
	color i_blockerColor[];
	float i_blockerValue[];
	uniform float i_digidoubleShadowType;
	uniform string i_digidoubleSubset;
	uniform string i_digidoubleShadowMap;
	uniform float i_displayPenumbraAngle;
	uniform float i_displayLightLimits;
	uniform float i_displayBarnDoors;
	uniform float i_displayFalloff;
	uniform float i_iconSize;
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
                lcol *= i_goboColor * i_goboAlpha;

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
