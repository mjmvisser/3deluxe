#ifndef __dl_projectionLightShape_h
#define __dl_projectionLightShape_h

/*
begin inputs
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
	prepare color color
	varying color transparency
	uniform float compositeMode
	uniform string projLightSubset
	uniform float intensity
	uniform color lightColor
end inputs

begin shader_extra_parameters lightsource
	output varying float __compositeMode = 0.0;
	output varying float __alpha = 1.0;
	output uniform string __projLightSubset = "";
	uniform string __category = "texture";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

#include "shadow_utils.h"
#include "utils.h"

void
prepare_maya_dl_projectionLightShape(
	// Inputs
	//
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
	varying color i_color;
	varying color i_transparency;
	uniform float i_compositeMode;
	uniform string i_projLightSubset;
	uniform float i_intensity;
	uniform color i_lightColor;
	)
{

    extern float ss;
    extern float tt;
    extern point Ps;
    point Pl = transform("shader", Ps);
    ss = (Pl[0] + 1)/2;
    tt = (Pl[1] + 1)/2;
}

void
end_maya_dl_projectionLightShape(
	// Inputs
	//
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
	varying color i_color;
	varying color i_transparency;
	uniform float i_compositeMode;
	uniform string i_projLightSubset;
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
        


        extern color Cl;
        extern vector L;
        extern point Ps;
        extern normal Ns;
        extern vector I;
        
        extern float __compositeMode;
        extern float __alpha;
        extern string __projLightSubset;

        point Pl = transform("shader", Ps);
        float ss = Pl[0];
        float tt = Pl[1];

        __compositeMode = i_compositeMode;
        float unshadowedAlpha = luminance(1-i_transparency);
        __projLightSubset = i_projLightSubset;

        illuminate(Ps)
        {
            extern uniform string shadowmapname;
            color unoccluded = color getShadowMapContribution(Ps,
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
            __alpha = unshadowedAlpha * luminance(unoccluded);
            Cl = i_color * unoccluded;
        }
}

#endif /* __dl_projectionLightShape_h */
