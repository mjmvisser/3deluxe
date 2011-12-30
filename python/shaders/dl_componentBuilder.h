#ifndef __dl_componentBuilder_h
#define __dl_componentBuilder_h

/*
begin inputs
	uniform float mute
	uniform float contribution
	float intensity
	color color
	uniform float shadeCurves
	uniform float lightSetIndex
	color beauty
	color light
	color diffuse_unocc
	color diffuse_shad
	color specular_unocc
	color specular_shad
	color translucence_unocc
	color translucence_shad
	color diffuse_unocc_sc
	color diffuse_shad_sc
	color specular_unocc_sc
	color specular_shad_sc
	color translucence_unocc_sc
	color translucence_shad_sc
	color diffuse_surf
	color specular_surf
	color incandescence
	color ambient
	color indirect_unocc
	color indirect_shad
	color indirect_unocc_sc
	color indirect_shad_sc
	color reflection_env
	color occlusion
	color bentnormal
	color reflection
	color reflection_depth
	color refraction
	color subsurface
	color collect_direct_shad
	color collect_indirect_shad
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

void
maya_dl_componentBuilder(
	// Inputs
	//
	uniform float i_mute;
	uniform float i_contribution;
	float i_intensity;
	color i_color;
	uniform float i_shadeCurves;
	uniform float i_lightSetIndex;
	color i_beauty;
	color i_light;
	color i_diffuse_unocc;
	color i_diffuse_shad;
	color i_specular_unocc;
	color i_specular_shad;
	color i_translucence_unocc;
	color i_translucence_shad;
	color i_diffuse_unocc_sc;
	color i_diffuse_shad_sc;
	color i_specular_unocc_sc;
	color i_specular_shad_sc;
	color i_translucence_unocc_sc;
	color i_translucence_shad_sc;
	color i_diffuse_surf;
	color i_specular_surf;
	color i_incandescence;
	color i_ambient;
	color i_indirect_unocc;
	color i_indirect_shad;
	color i_indirect_unocc_sc;
	color i_indirect_shad_sc;
	color i_reflection_env;
	color i_occlusion;
	color i_bentnormal;
	color i_reflection;
	color i_reflection_depth;
	color i_refraction;
	color i_subsurface;
	color i_collect_direct_shad;
	color i_collect_indirect_shad;
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
    
	o_output_beauty = i_beauty * globalIntensity * i_color;
	o_output_light[i_lightSetIndex] = i_light * globalIntensity * i_color;
	o_output_diffuse_unocc[i_lightSetIndex] = i_diffuse_unocc * globalIntensity * i_color;
	o_output_diffuse_shad[i_lightSetIndex] = i_diffuse_shad * globalIntensity * i_color;
	o_output_specular_unocc[i_lightSetIndex] = i_specular_unocc * globalIntensity * i_color;
	o_output_specular_shad[i_lightSetIndex] = i_specular_shad * globalIntensity * i_color;
	o_output_translucence_unocc[i_lightSetIndex] = i_translucence_unocc * globalIntensity * i_color;
	o_output_translucence_shad[i_lightSetIndex] = i_translucence_shad * globalIntensity * i_color;
	o_output_diffuse_unocc_sc[i_lightSetIndex] = i_diffuse_unocc_sc * globalIntensity * i_color;
	o_output_diffuse_shad_sc[i_lightSetIndex] = i_diffuse_shad_sc * globalIntensity * i_color;
	o_output_specular_unocc_sc[i_lightSetIndex] = i_specular_unocc_sc * globalIntensity * i_color;
	o_output_specular_shad_sc[i_lightSetIndex] = i_specular_shad_sc * globalIntensity * i_color;
	o_output_translucence_unocc_sc[i_lightSetIndex] = i_translucence_unocc_sc * globalIntensity * i_color;
	o_output_translucence_shad_sc[i_lightSetIndex] = i_translucence_shad_sc * globalIntensity * i_color;
	o_output_diffuse_surf = i_diffuse_surf * globalIntensity * i_color;
	o_output_specular_surf = i_specular_surf * globalIntensity * i_color;
	o_output_incandescence = i_incandescence * globalIntensity * i_color;
	o_output_ambient = i_ambient * globalIntensity * i_color;
	o_output_indirect_unocc = i_indirect_unocc * globalIntensity * i_color;
	o_output_indirect_shad = i_indirect_shad * globalIntensity * i_color;
	o_output_indirect_unocc_sc = i_indirect_unocc_sc * globalIntensity * i_color;
	o_output_indirect_shad_sc = i_indirect_shad_sc * globalIntensity * i_color;
	o_output_reflection_env = i_reflection_env * globalIntensity * i_color;
	o_output_occlusion = i_occlusion * globalIntensity * i_color;
	o_output_bentnormal = i_bentnormal * globalIntensity * i_color;
	o_output_reflection = i_reflection * globalIntensity * i_color;
	o_output_reflection_depth = i_reflection_depth * globalIntensity * i_color;
	o_output_refraction = i_refraction * globalIntensity * i_color;
	o_output_subsurface = i_subsurface * globalIntensity * i_color;
	o_output_collect_direct_shad[i_lightSetIndex] = i_collect_direct_shad * globalIntensity * i_color;
	o_output_collect_indirect_shad = i_collect_indirect_shad * globalIntensity * i_color;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_componentBuilder_h */
