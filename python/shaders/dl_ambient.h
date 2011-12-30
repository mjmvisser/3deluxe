#ifndef __dl_ambient_h
#define __dl_ambient_h

/*
begin inputs
	uniform float mute
	uniform float contribution
	float intensity
	color color
	uniform float shadeCurves
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
#include "env_utils.h"

void
maya_dl_ambient(
	// Inputs
	//
	uniform float i_mute;
	uniform float i_contribution;
	float i_intensity;
	color i_color;
	uniform float i_shadeCurves;
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
    

    
    color col = 0;
    illuminance( "ambient", P ) {
        if( L == 0 ) {
            col += Cl;
        }
    }
    col *= globalIntensity * surfaceColor;
    o_output_ambient = col;
    o_output_beauty = col;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_ambient_h */
