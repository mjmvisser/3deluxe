#ifndef __dl_refraction_h
#define __dl_refraction_h

/*
begin inputs
	uniform float mute
	uniform float contribution
	float intensity
	color color
	uniform float shadeCurves
	uniform float mapContribution
	float mapBlur
	float mapBlurS
	float mapBlurT
	uniform float mapFilter
	uniform float physicalSkySamples
	uniform float calculationMethod
	uniform float rayMethod
	uniform float raySamples
	float rayBlur
	uniform string raySubset
	uniform float rayMaxDistance
	uniform float rayBias
	uniform float rayFalloff
	color rayFalloffColor
	uniform string ptcFile
	float ptcIntensity
	float ptcBlur
	float ptcBias
	float ptcMaxDist
	uniform float ptcClamp
	uniform float ptcSortBleeding
	float ptcMaxSolidAngle
	float ptcSampleBase
	uniform float indexOfRefraction
	uniform float maxIntensity
	normal normalCamera
end inputs

begin outputs
	void outputComponent
	color outputComponent.output_beauty
	color[] outputComponent.output_light
	color[] outputComponent.output_diffuse_unocc
	color[] outputComponent.output_diffuse_shad
	color[] outputComponent.output_specular_unocc
	color[] outputComponent.output_specular_shad
	color[] outputComponent.output_translucence_unocc
	color[] outputComponent.output_translucence_shad
	color[] outputComponent.output_diffuse_unocc_sc
	color[] outputComponent.output_diffuse_shad_sc
	color[] outputComponent.output_specular_unocc_sc
	color[] outputComponent.output_specular_shad_sc
	color[] outputComponent.output_translucence_unocc_sc
	color[] outputComponent.output_translucence_shad_sc
	color outputComponent.output_diffuse_surf
	color outputComponent.output_specular_surf
	color outputComponent.output_incandescence
	color outputComponent.output_ambient
	color outputComponent.output_indirect_unocc
	color outputComponent.output_indirect_shad
	color outputComponent.output_indirect_unocc_sc
	color outputComponent.output_indirect_shad_sc
	color outputComponent.output_reflection_env
	color outputComponent.output_occlusion
	color outputComponent.output_bentnormal
	color outputComponent.output_reflection
	color outputComponent.output_reflection_depth
	color outputComponent.output_refraction
	color outputComponent.output_subsurface
	color[] outputComponent.output_collect_direct_shad
	color outputComponent.output_collect_indirect_shad
	color outColor
	color outTransparency
end outputs

*/

#include "utils.h"
#include "component_utils.h"
#include "ray_utils.h"
#include "env_utils.h"

void
maya_dl_refraction(
	// Inputs
	//
	uniform float i_mute;
	uniform float i_contribution;
	float i_intensity;
	color i_color;
	uniform float i_shadeCurves;
	uniform float i_mapContribution;
	float i_mapBlur;
	float i_mapBlurS;
	float i_mapBlurT;
	uniform float i_mapFilter;
	uniform float i_physicalSkySamples;
	uniform float i_calculationMethod;
	uniform float i_rayMethod;
	uniform float i_raySamples;
	float i_rayBlur;
	uniform string i_raySubset;
	uniform float i_rayMaxDistance;
	uniform float i_rayBias;
	uniform float i_rayFalloff;
	color i_rayFalloffColor;
	uniform string i_ptcFile;
	float i_ptcIntensity;
	float i_ptcBlur;
	float i_ptcBias;
	float i_ptcMaxDist;
	uniform float i_ptcClamp;
	uniform float i_ptcSortBleeding;
	float i_ptcMaxSolidAngle;
	float i_ptcSampleBase;
	uniform float i_indexOfRefraction;
	uniform float i_maxIntensity;
	normal i_normalCamera;
	// Outputs
	//
	output color o_output_beauty;
	output color o_output_light[];
	output color o_output_diffuse_unocc[];
	output color o_output_diffuse_shad[];
	output color o_output_specular_unocc[];
	output color o_output_specular_shad[];
	output color o_output_translucence_unocc[];
	output color o_output_translucence_shad[];
	output color o_output_diffuse_unocc_sc[];
	output color o_output_diffuse_shad_sc[];
	output color o_output_specular_unocc_sc[];
	output color o_output_specular_shad_sc[];
	output color o_output_translucence_unocc_sc[];
	output color o_output_translucence_shad_sc[];
	output color o_output_diffuse_surf;
	output color o_output_specular_surf;
	output color o_output_incandescence;
	output color o_output_ambient;
	output color o_output_indirect_unocc;
	output color o_output_indirect_shad;
	output color o_output_indirect_unocc_sc;
	output color o_output_indirect_shad_sc;
	output color o_output_reflection_env;
	output color o_output_occlusion;
	output color o_output_bentnormal;
	output color o_output_reflection;
	output color o_output_reflection_depth;
	output color o_output_refraction;
	output color o_output_subsurface;
	output color o_output_collect_direct_shad[];
	output color o_output_collect_indirect_shad;
	output color o_outColor;
	output color o_outTransparency;
	)
{

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
    

    uniform string envFilter;
    if (i_mapFilter == 0)
        envFilter = "gaussian";
    else if (i_mapFilter == 1)
        envFilter = "triangle";
    else
        envFilter = "box";
    
    color envColor = 0;

    color ptcColor = 0;
    float ptcAlpha = 0;
    string ptcFiles[];

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


    // Refract vector
	float eta = (V.dir >= 0) ? (1/i_indexOfRefraction) : i_indexOfRefraction;
	vector R = refract(In, dir, eta);

    // Get map 
    if (i_mapContribution > 0) {
        getEnvironmentReflection(origin, Nf, R, i_mapBlur, i_mapBlurS, i_mapBlurT, envFilter, i_physicalSkySamples, envColor);
        envColor *= i_mapContribution;
    }
    
    // Ray Tracing
	if (i_calculationMethod == 0) {
	    color rayTransmission = 1;
	    getTraceOrGather(P, R, "refraction", i_rayMethod, i_rayMaxDistance, i_raySamples, i_rayBias, i_rayBlur, i_raySubset, o_output_refraction, rayDist, rayTransmission);
	    if(rayTransmission == 1)
	        o_output_refraction = envColor;
    }
	else if (i_calculationMethod == 1 && isBakingRadiosity() < 1) { // Point Cloud
	    if(getPointCloudFiles("Refraction", i_ptcFile, ptcFiles)){
            ptcColor = indirectdiffuse(P, normalize(R), 0, "pointbased", 1, "filenames", ptcFiles,  "maxdist", i_ptcMaxDist, "samplebase", i_ptcSampleBase, "bias", i_ptcBias,
                "occlusion", ptcAlpha, "sortbleeding", i_ptcSortBleeding, "clamp", i_ptcClamp, "maxsolidangle", i_ptcMaxSolidAngle, "coneangle", max(0.01, i_ptcBlur*PI/2));
            ptcColor *= i_ptcIntensity;
            ptcAlpha *= i_ptcIntensity;
	    }
        
        // Mix object on top of env
        o_output_refraction = mix(envColor, ptcColor, ptcAlpha);
	}
    else{
        o_output_refraction = envColor;
    }
    
    // TODO: SORT THIS OUT
    // handle falloff
    /* THIS IS FROM dl_reflection, BUT I DON'T UNDERSTAND IT. (falloffDistance parm required).
    if (i_falloff != 0) {
        if (rayDist < 1e30) {
            if (rayDist > i_falloffDistance) {
                o_output_refraction *= pow(i_falloffDistance/rayDist, i_falloff);
            }
            else {
                uniform float ss = log(1/i_maxIntensity);
                uniform float beta = -i_falloff / ss;
                o_output_refraction *= (i_maxIntensity * exp(ss * pow(rayDist/i_falloffDistance, beta)));
            }
        }
    }

    if (i_falloff != 0)
        o_output_refraction = mix(i_falloffColor, o_output_refraction, pow(max(0, 1-(rayDist/i_rayMaxDistance)), i_falloff));
    
    if (i_maxIntensity >= 0) 
        clampToMaxIntens(i_maxIntensity, i_maxIntensity*.1, o_output_refraction);
    */

	o_output_refraction *= surfaceColor * globalIntensity;
    o_output_beauty = o_output_refraction;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_refraction_h */
