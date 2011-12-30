#ifndef __dl_envLightShape_h
#define __dl_envLightShape_h

/*
begin inputs
	uniform float envMethod
	texture string envMap
	sourceshapename string envSpace
	vector physkySunLightRotation
	uniform float physkyJustSun
	texture string physkyCloudTex
	texture string physkyGroundTex
	float physkyTextureBlur
	float physkyProceduralSamples
	float physkyProceduralBlur
	float physkyMultiplier
	float3 physkyRgbUnitConversion
	float physkyHaze
	float physkyRedBlueShift
	float physkySaturation
	float physkyHorizonHeight
	float physkyHorizonBlur
	float physkyFakeSkyBlur
	float physkyFakeSkyBlurUpBias
	color physkyGroundColour
	color physkyNightColour
	float physkySunDiskIntensity
	float physkySunDiskScale
	float physkySunGlowIntensity
	float physkySunMaxIntensity
	uniform float physkyYIsUp
	uniform string physkyCoordsys
	uniform float physkyBakeSkyMap
	uniform string physkyBakeSkyMapFile
	uniform float envExposure
	uniform float envGamma
	uniform float envOffset
	uniform float occMethod
	uniform string occPtcFile
	uniform float occMaxSolidAngle
	uniform float occClamp
	float occSampleBase
	uniform float occHitSides
	uniform float occSamples
	uniform float occAdaptiveSampling
	float occRayBias
	uniform float occMaxDistance
	uniform float occConeAngle
	uniform float occFalloffMode
	float occFalloff
	uniform float occIntensity
	uniform color occColor
	uniform float occBias
	uniform float occGain
	uniform float traceSamplesMult
	uniform float intensity
	uniform color lightColor
end inputs

begin shader_extra_parameters lightsource
	uniform float __occSamplesMult = 1.0;
	uniform float __occConeAngleMult = 1.0;
	uniform float __physkyBlur = 0.0;
	uniform float __physkySamps = 1.0;
	varying vector __envDir = vector (12345, 12345, 12345);
	output uniform string __map = "";
	output uniform string __coordsys = "";
	output varying float __occlusion = 0.0;
	output varying color __occlusionColor = color (0, 0, 0);
	output uniform float __traceSamplesMult = 1.0;
	output uniform float __exposure = 1.0;
	output uniform float __gamma = 0.5;
	output uniform float __offset = 0.5;
	output uniform float __useAmbientOcclusion = 0.0;
	uniform string __category = "environment";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

#include "remap_utils.h"
#include "physicalsky_utils.h"
#include "env_utils.h"

void
maya_dl_envLightShape(
	// Inputs
	//
	uniform float i_envMethod;
	uniform string i_envMap;
	uniform string i_envSpace;
	vector i_physkySunLightRotation;
	uniform float i_physkyJustSun;
	uniform string i_physkyCloudTex;
	uniform string i_physkyGroundTex;
	float i_physkyTextureBlur;
	float i_physkyProceduralSamples;
	float i_physkyProceduralBlur;
	float i_physkyMultiplier;
	float i_physkyRgbUnitConversion[3];
	float i_physkyHaze;
	float i_physkyRedBlueShift;
	float i_physkySaturation;
	float i_physkyHorizonHeight;
	float i_physkyHorizonBlur;
	float i_physkyFakeSkyBlur;
	float i_physkyFakeSkyBlurUpBias;
	color i_physkyGroundColour;
	color i_physkyNightColour;
	float i_physkySunDiskIntensity;
	float i_physkySunDiskScale;
	float i_physkySunGlowIntensity;
	float i_physkySunMaxIntensity;
	uniform float i_physkyYIsUp;
	uniform string i_physkyCoordsys;
	uniform float i_physkyBakeSkyMap;
	uniform string i_physkyBakeSkyMapFile;
	uniform float i_envExposure;
	uniform float i_envGamma;
	uniform float i_envOffset;
	uniform float i_occMethod;
	uniform string i_occPtcFile;
	uniform float i_occMaxSolidAngle;
	uniform float i_occClamp;
	float i_occSampleBase;
	uniform float i_occHitSides;
	uniform float i_occSamples;
	uniform float i_occAdaptiveSampling;
	float i_occRayBias;
	uniform float i_occMaxDistance;
	uniform float i_occConeAngle;
	uniform float i_occFalloffMode;
	float i_occFalloff;
	uniform float i_occIntensity;
	uniform color i_occColor;
	uniform float i_occBias;
	uniform float i_occGain;
	uniform float i_traceSamplesMult;
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
        

        extern string __map;
        extern string __coordsys;
        extern float __occlusion;
        extern color __occlusionColor;
        extern uniform float __traceSamplesMult;
        extern float __exposure;
        extern float __gamma;
        extern float __offset;
        extern float __occSamplesMult;
        extern float __occConeAngleMult;
        extern float __useAmbientOcclusion;
        extern float __physkyBlur;
        extern float __physkySamps;
        extern vector __envDir;

        point origin = Ps;
        normal dir = Ns;

        uniform float traceDisplacements = 0;
        attribute("trace:displacements", traceDisplacements);
        if (traceDisplacements == 0)
        {
            // get the undisplaced surface point and normal from the displacement shader
            displacement("__Porig", origin);
            displacement("__Norig", dir);
        }

        dir = normalize(dir);
        normal dirf = faceforward(dir, I);

        normal Nf = faceforward(normalize(Ns), I);
        vector In = normalize(I);
        
        // reflection vector
        float almostEq(vector a, b; float error) {
            float result = 0;
            if (abs(a[0] - b[0]) < error && abs(a[1] - b[1]) < error && abs(a[2] - b[2]) < error)
                result = 1;
            return result;
        }
        vector R = almostEq(__envDir, vector 12345, .001) == 1 ? reflect(In, dirf) : __envDir;
        
        // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
        illuminate(Ps + Nf)
        {
            float coneangle = radians(__occConeAngleMult * i_occConeAngle);
        
            float occluded_reflection = 0;

            // compute occlusion
            
            if (i_occMethod == 1)
                // Ray Tracing
            {
                float samples = __occSamplesMult * i_occSamples;
                
                if (i_envMethod == 1) {
                    // use i_envMap.for "distribution" (?)
                    occluded_reflection = occlusion(origin, R, samples,
                                                    "coneangle", coneangle,
                                                    "maxdist", i_occMaxDistance,
                                                    "adaptive", i_occAdaptiveSampling,
                                                    "bias", i_occRayBias,
                                                    "falloffmode", i_occFalloffMode,
                                                    "falloff", i_occFalloff,
                                                    "distribution", i_envMap);
                } else if (i_envMethod == 2) {
                    occluded_reflection = occlusion(origin, R, samples,
                                                    "coneangle", coneangle,
                                                    "maxdist", i_occMaxDistance,
                                                    "adaptive", i_occAdaptiveSampling,
                                                    "bias", i_occRayBias,
                                                    "falloffmode", i_occFalloffMode,
                                                    "falloff", i_occFalloff);
                }
            }
            else if (i_occMethod == 2)
            {
                string occPtcFiles[];
                if( getPointCloudFiles("ReflectionOcclusion", i_occPtcFile, occPtcFiles) > 0){
                    
                    uniform string occHitSides = "";
                    if (i_occHitSides == 0)
                        occHitSides = "front";
                    else if (i_occHitSides == 1)
                        occHitSides = "back";
                    else if (i_occHitSides == 2)
                        occHitSides = "both";
                
                    // Point Cloud
                    if (i_envMethod == 1) {
                        // use i_envMap.for "distribution" (?)
                        occluded_reflection = occlusion(Ps, R, 0,
                                                        "coneangle", coneangle,
                                                        "filenames", occPtcFiles,
                                                        "pointbased", 1,
                                                        "hitsides", occHitSides,
                                                        "samplebase", i_occSampleBase,
                                                        "bias", i_occRayBias,
                                                        "falloffmode", i_occFalloffMode,
                                                        "falloff", i_occFalloff,
                                                        "maxdist", i_occMaxDistance,
                                                        "maxsolidangle", i_occMaxSolidAngle,
                                                        "clamp", i_occClamp,
                                                        "distribution", i_envMap);
                    } else {
                        occluded_reflection = occlusion(Ps, R, 0,
                                                        "coneangle", coneangle,
                                                        "filenames", occPtcFiles,
                                                        "pointbased", 1,
                                                        "hitsides", occHitSides,
                                                        "samplebase", i_occSampleBase,
                                                        "bias", i_occRayBias,
                                                        "falloffmode", i_occFalloffMode,
                                                        "falloff", i_occFalloff,
                                                        "maxdist", i_occMaxDistance,
                                                        "maxsolidangle", i_occMaxSolidAngle,
                                                        "clamp", i_occClamp);
                    }
                }
            } 
            else if (i_occMethod == 3) // Tell the surface shader to use ambient occlusion for reflection occlusion.
            {
                __useAmbientOcclusion = 1;
            }

            // parameters are just returned via message passing
            // the actual environment map lookup happens in env_utils.h
            // ADDED IN dltools2.3: if i_envMethod == 2 (physical sky),
            // __map is set to "" so env_utils does nothing; instead,
            // the sky colour is multiplied into Cl.

            if (i_envMethod == 2) {
                float blurToUse = __physkyBlur < 0 ? i_physkyProceduralBlur : __physkyBlur;
                float sampsToUse = __physkySamps < 0 ? i_physkyProceduralSamples : __physkySamps;
                color skyClr = getPhysicalSky (
                    vtransform("world", R),
                    i_physkySunLightRotation,
                    sampsToUse,
                    blurToUse,
                    i_physkyHaze,
                    i_physkySaturation,
                    i_physkyYIsUp,
                    i_physkyHorizonHeight,
                    i_physkyHorizonBlur,
                    i_physkySunDiskIntensity,
                    i_physkySunDiskScale,
                    i_physkySunGlowIntensity,
                    i_physkySunMaxIntensity,
                    i_physkyGroundColour,
                    i_physkyRgbUnitConversion,
                    i_physkyMultiplier,
                    i_physkyRedBlueShift,
                    i_physkyNightColour,
                    i_physkyGroundTex,
                    i_physkyCloudTex,
                    i_physkyTextureBlur,
                    i_physkyJustSun,
                    i_physkyFakeSkyBlur,
                    i_physkyFakeSkyBlurUpBias
                    );
			    skyClr = remapHDRI(i_envExposure, i_envGamma, i_envOffset, skyClr);
                __map = "";
                Cl = i_intensity * i_lightColor * skyClr;;
            } else if (i_envMethod == 1){
                __map = i_envMap;
                Cl = i_intensity * i_lightColor;
            }
            __coordsys = i_envSpace;
            __occlusion = remapOcclusion(i_occIntensity, i_occBias, i_occGain, occluded_reflection);
            __occlusionColor = i_occColor;
            __traceSamplesMult = i_traceSamplesMult;
            __exposure = i_envExposure;
            __gamma = i_envGamma;
            __offset = i_envOffset;

        }
}

#endif /* __dl_envLightShape_h */
