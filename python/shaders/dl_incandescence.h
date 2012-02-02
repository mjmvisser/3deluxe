#ifndef __dl_incandescence_h
#define __dl_incandescence_h

/*
begin inputs
	uniform float bakeIncomingColor
	uniform string bakeFile
	uniform float method
	uniform float shape
	normal normalCamera
	uniform float mute
	uniform float contribution
	float intensity
	color color
	uniform float shadeCurves
end inputs

begin outputs
	color outColor
	color outTransparency
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
end outputs

*/

#include "utils.h"
#include "component_utils.h"

void
maya_dl_incandescence(
	// Inputs
	//
	uniform float i_bakeIncomingColor;
	uniform string i_bakeFile;
	uniform float i_method;
	uniform float i_shape;
	normal i_normalCamera;
	uniform float i_mute;
	uniform float i_contribution;
	float i_intensity;
	color i_color;
	uniform float i_shadeCurves;
	// Outputs
	//
	output color o_outColor;
	output color o_outTransparency;
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
    

    
    extern float s;
    extern float t;
        
    // bake incoming color.
    if (i_bakeIncomingColor > 0) {
        if (i_bakeIncomingColor == 1) {
            bake(i_bakeFile, s, t, i_color);
        } else {
            float lum = luminance(i_color);
            bake(i_bakeFile, s, t, lum);
        }
    }
        
    color col = surfaceColor * globalIntensity;

    if( i_method != 3 ) {
    	if( i_method != 0 ) {
    	    float facing = max(Nf.V, 0);
    	    if( i_method == 2 ) {
        		facing = sqrt(1 - facing*facing);
    	    }
    	    col *= pow(facing, i_shape);
    	}
    }
    else {
    	float lum = 0;
    	uniform vector vec = (.3,.59,.11);
    	illuminance("-environment&-indirect&-bakelight", P, Nf, PI/2,
            	    "lightcache", "reuse") {
    	    lum += vec.vector(Cl);
    	}
    	col *= lum;
    }
    
    o_output_incandescence = col;
    o_output_beauty = col;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_incandescence_h */
