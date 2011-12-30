#ifndef __dl_indirectLightShape_h
#define __dl_indirectLightShape_h

/*
begin inputs
	uniform float envMethod
	float envIntensity
	color envColor
	texture string envMap
	sourceshapename string envSpace
	uniform float envConvolveMode
	uniform float envBlur
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
	uniform float indirectMethod
	float indirectIntensity
	uniform string indirectPtcFile
	uniform float occPtcFileIsDirectory
	uniform float indirectMaxSolidAngle
	uniform float indirectClamp
	float indirectSampleBase
	uniform float indirectHitSides
	uniform float indirectSamples
	uniform float indirectAdaptiveSampling
	float indirectRayBias
	uniform float indirectMaxDistance
	uniform float indirectFalloffMode
	float indirectFalloff
	uniform float intensity
	uniform color lightColor
end inputs

begin shader_extra_parameters lightsource
	float __computeOcclusion = 1.0;
	output varying color __occluded = color (0, 0, 0);
	output color __occlusionColor = color (0, 0, 0);
	output varying color __indirect_color = color (0, 0, 0);
	output varying color __bentnormal = color (0, 0, 0);
	uniform string __category = "indirect";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

#include "remap_utils.h"
#include "component_utils.h"
#include "physicalsky_utils.h"
#include "env_utils.h"

void
maya_dl_indirectLightShape(
	// Inputs
	//
	uniform float i_envMethod;
	float i_envIntensity;
	color i_envColor;
	uniform string i_envMap;
	uniform string i_envSpace;
	uniform float i_envConvolveMode;
	uniform float i_envBlur;
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
	uniform float i_indirectMethod;
	float i_indirectIntensity;
	uniform string i_indirectPtcFile;
	uniform float i_occPtcFileIsDirectory;
	uniform float i_indirectMaxSolidAngle;
	uniform float i_indirectClamp;
	float i_indirectSampleBase;
	uniform float i_indirectHitSides;
	uniform float i_indirectSamples;
	uniform float i_indirectAdaptiveSampling;
	float i_indirectRayBias;
	uniform float i_indirectMaxDistance;
	uniform float i_indirectFalloffMode;
	float i_indirectFalloff;
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
        extern color __indirect_color;
        extern color __bentnormal;
        extern float __computeOcclusion;

        point origin = Ps;
        normal dir = Ns;
        vector dirW = transform("world", dir);

        uniform float traceDisplacements = 0;
        attribute("trace:displacements", traceDisplacements);
        if (traceDisplacements == 0)
        {
            // get the undisplaced surface point and normal from the displacement shader
            displacement("__Porig", origin);
            displacement("__Norig", dir);
        }

        dir = normalize(dir);
        normal dirf = ShadingNormal(dir);

        normal Nn = normalize(Ns);
        normal Nf = ShadingNormal(Nn);

        uniform string envspace = "world";
        if (i_envSpace != "")
            envspace = i_envSpace;

        // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
        illuminate(Ps + Nf)
        {
            // compute occlusion
            
            float occluded = 0;
            vector bentnormal = vector Nf;

            if (__computeOcclusion != 0)
            {
                if (i_occMethod == 1)
                    // Ray Tracing
                {
                    if (i_envMethod == 1) {
                        // use i_envMap.for "distribution" (?)
                        occluded = occlusion(origin, dirf, i_occSamples,
                                         "coneangle", radians(i_occConeAngle),
                                         "maxdist", i_occMaxDistance,
                                         "adaptive", i_occAdaptiveSampling,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "distribution", i_envMap,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    } else if (i_envMethod == 2) {
                        occluded = occlusion(origin, dirf, i_occSamples,
                                         "coneangle", radians(i_occConeAngle),
                                         "maxdist", i_occMaxDistance,
                                         "adaptive", i_occAdaptiveSampling,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    }
                }
                else if (i_occMethod == 2)
                {
                    uniform string occHitSides = "";
                    if (i_occHitSides == 0)
                        occHitSides = "front";
                    else if (i_occHitSides == 1)
                        occHitSides = "back";
                    else if (i_occHitSides == 2)
                        occHitSides = "both";
                
                    // Point Cloud
                    //if( textureinfo(i_occPtcFile, "exists", 0) )
                    string occPtcFile = i_occPtcFile;
                    if (i_occPtcFileIsDirectory) {
                        string objName = "";
                        attribute("user:delight_shortest_unique_name", objName);
                        occPtcFile = concat(occPtcFile, "/", objName, ".ptc");
                    }
                    
                    string occPtcFiles[];
                    if( getPointCloudFiles("AmbientOcclusion", occPtcFile, occPtcFiles) > 0)
                    {
                        occluded = occlusion(Ps, dirf, 0,
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
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    }
                    /*
                    
                    // TODO MAKE THIS CLEANER
                    float selfOcclude = 1;
                    attribute("user:selfOcclude", selfOcclude);
                    if( selfOcclude == 1 && i_occPtcFileNoSelfOcclude != "")
                    {
                        float thisOcc = occlusion(Ps, dirf, 0,
                                         "filename", i_occPtcFileNoSelfOcclude,
                                         "pointbased", 1,
                                         "hitsides", occHitSides,
                                         "samplebase", i_occSampleBase,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "maxdist", i_occMaxDistance,
                                         "maxsolidangle", i_occMaxSolidAngle,
                                         "clamp", i_occClamp,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                        // This is based on opacity compositing + is an inaccurate approximation of merging 2 pointclouds. 
                        occluded = 1 - (1-occluded) * (1-thisOcc); 
                    }
                    */
                    // markv: This statement doesn't compile
                    // from docs:  "environmentdir"      output varying vector      If specified, it is set to the
                    //             average un-occluded direction, which is the average of all sampled directions 
                    //             that do not hit any geometry. Note that this vector is defined in `current' space,
                    //             so it is necessary to transform it to `world' space if an environment() lookup is intended.  
                    //bentnormal = vtransform("world", "current", bentnormal);
                    //
                    // jeremye: When using pointclouds, environmentdir seems to be in world space, in spite
                    // of what the docs say.  I've sent a message to support@3delight.com to address this.
                    // In the meantime, the hack below effectively transforms bentnormal from world to
                    // current space without generating an error (warning really).
                    // UPDATE: This will be fixed soon, at which point REMOVE BELOW (and test).
                    //
                    // marcantoinep: not yet fixed , keeping code

                    vector tmp = vtransform("world", bentnormal);
                    tmp[0] = bentnormal[0]; tmp[1] = bentnormal[1]; tmp[2] = bentnormal[2];
                    bentnormal = vtransform("world", "current", tmp);
                }
            }
            bentnormal = vtransform(envspace, bentnormal);
            
            // compute indirect diffuse lighting

            color indirect_color = 0;
    
            if (i_envMethod == 1) {
                color envColor = 1;
                if( textureinfo(i_envMap, "exists", 0) ) {
                    vector envdir = normalize(bentnormal);
                    if (i_envConvolveMode == 0) 
                        envColor = environment(i_envMap, envdir, "blur", i_envBlur);
                    else
                        envColor = indirectdiffuse(i_envMap, envdir);
                }
                indirect_color += envColor * i_envColor * i_envIntensity;
            } else if (i_envMethod == 2) {
                // Lookup physical sky.
                indirect_color += getPhysicalSky (
                    dirW,
                    i_physkySunLightRotation,
                    i_physkyProceduralSamples,
                    i_physkyProceduralBlur,
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
                    i_physkyFakeSkyBlurUpBias);
                if (i_physkyBakeSkyMap == 1) {
                    float ss = 0, tt = 0;
                    normal Nw = normalize(ntransform("world", Ns));
                    stFromV(vector Nw, ss, tt);
                    bake(i_physkyBakeSkyMapFile, ss, tt, indirect_color);
                }
            }
        
            color indirectColor = 0;
            
            if (i_indirectMethod == 1)
            {
                // Ray Tracing
                if (i_envMethod == 1) {
                    // Missed rays lookup i_envMap.
                    indirectColor += indirectdiffuse(origin, dir, i_indirectSamples,
                                                 "maxdist", i_indirectMaxDistance,
                                                 "adaptive", i_indirectAdaptiveSampling,
                                                 "bias", i_indirectRayBias,
                                                 "falloffmode", i_indirectFalloffMode,
                                                 "falloff", i_indirectFalloff,
                                                 "environmentmap", i_envMap,
                                                 "environmentspace", envspace);
                } else if (i_envMethod == 2){
                    // Missed rays lookup physical sky.
                    indirectColor += indirectdiffuse(origin, dir, i_indirectSamples,
                                                 "maxdist", i_indirectMaxDistance,
                                                 "adaptive", i_indirectAdaptiveSampling,
                                                 "bias", i_indirectRayBias,
                                                 "falloffmode", i_indirectFalloffMode,
                                                 "falloff", i_indirectFalloff,
                                                 "environmentspace", envspace);
                    color skyClr = getPhysicalSky (
                        dirW,
                        i_physkySunLightRotation,
                        i_physkyProceduralSamples,
                        i_physkyProceduralBlur,
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
                        i_physkyFakeSkyBlurUpBias);
                    indirectColor += skyClr *(1-occluded);//mix(skyClr, indirectColor, occluded);
                }
            }
            else if (i_indirectMethod == 2)
            {
                uniform string indirectHitSides = "";
                if (i_indirectHitSides == 0)
                    indirectHitSides = "front";
                else if (i_indirectHitSides == 1)
                    indirectHitSides = "back";
                else if (i_indirectHitSides == 2)
                    indirectHitSides = "both";

                // Point Cloud
                string indirectPtcFiles[];
                if( getPointCloudFiles("ColorBleeding", i_indirectPtcFile, indirectPtcFiles) > 0){
                    indirectColor += indirectdiffuse(Ps, Nn, 0,
                                                     "filenames", indirectPtcFiles,
                                                     "pointbased", 1,
                                                     "hitsides", indirectHitSides,
                                                     "samplebase", i_indirectSampleBase,
                                                     "bias", i_indirectRayBias,
                                                     "falloffmode", i_indirectFalloffMode,
                                                     "falloff", i_indirectFalloff,
                                                     "maxdist", i_indirectMaxDistance,
                                                     "maxsolidangle", i_indirectMaxSolidAngle,
                                                     "clamp", i_indirectClamp);
                }
            }
            
            indirect_color += indirectColor * i_indirectIntensity;
            
            indirect_color = remapHDRI(i_envExposure, i_envGamma, i_envOffset, indirect_color);
            occluded = remapOcclusion(i_occIntensity, i_occBias, i_occGain, occluded);
            
            Cl = i_intensity * indirect_color * i_lightColor;
            
            // output occlusion to the surface
            __occluded = color occluded;
            __occlusionColor = i_occColor;
            __indirect_color = indirect_color;
            __bentnormal = color bentnormal;
        }

}

#endif /* __dl_indirectLightShape_h */
