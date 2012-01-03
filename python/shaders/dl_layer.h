#ifndef __dl_layer_h
#define __dl_layer_h


#include "utils.h"
#include "component_utils.h"
#include "blend_utils.h"
#include "displacement_utils.h"

float
blendFloats(
	// Inputs
	//
	uniform float i_mode;
	float i_premult;
	float i_fg;
	color i_fga;
	float i_bg;
	color i_bga;
	)
{
	color resultColor, resultOpacity;
	float premult = mix(1, luminance(i_fga), i_premult);
	blend(i_mode, color(i_fg) * premult, i_fga, color(i_bg), i_bga, resultColor, resultOpacity);
	return comp(resultColor, 0);
}

float
accumulateFloats(
	// Inputs
	//
	float i_inputs[];
	)
{
    uniform float size = arraylength(i_inputs);
    uniform float i;
    float total = 0;
    for(i = 0; i < size; i+= 1)
    {
        total += i_inputs[i];
    }
    return total;
    
}

void
copyFloats(
	// Inputs
	//
	float i_inputs[];
	// Outputs
	//
	output float o_outputs[];
	)
{
    uniform float isize = arraylength(i_inputs);
    uniform float osize = arraylength(o_outputs);
    uniform float i;
    for(i = 0; i < isize &&  i < osize ; i += 1)
    {
        o_outputs[i] = i_inputs[i];
    }
    
}

color
blendColors(
	// Inputs
	//
	uniform float i_mode;
	float i_premult;
	color i_fg;
	color i_fga;
	color i_bg;
	color i_bga;
	)
{
	color resultColor, resultOpacity;
	color premult = mix(color 1, i_fga, i_premult);
	blend(i_mode, i_fg * premult, i_fga, i_bg, i_bga, resultColor, resultOpacity);
	return resultColor;
}

color
accumulateColors(
	// Inputs
	//
	color i_inputs[];
	)
{
    uniform float size = arraylength(i_inputs);
    uniform float i;
    color total = 0;
    for(i = 0; i < size; i+= 1)
    {
        total += i_inputs[i];
    }
    return total;
    
}

void
copyColors(
	// Inputs
	//
	color i_inputs[];
	// Outputs
	//
	output color o_outputs[];
	)
{
    uniform float isize = arraylength(i_inputs);
    uniform float osize = arraylength(o_outputs);
    uniform float i;
    for(i = 0; i < isize &&  i < osize ; i += 1)
    {
        o_outputs[i] = i_inputs[i];
    }
    
}

void
blendLightsets(
	// Inputs
	//
	uniform float i_mode;
	float i_premult;
	color i_fg_opacity;
	color i_fg_light;
	color i_fg_diffuse_unocc;
	color i_fg_diffuse_shad;
	color i_fg_specular_unocc;
	color i_fg_specular_shad;
	color i_fg_translucence_unocc;
	color i_fg_translucence_shad;
	color i_fg_diffuse_unocc_sc;
	color i_fg_diffuse_shad_sc;
	color i_fg_specular_unocc_sc;
	color i_fg_specular_shad_sc;
	color i_fg_translucence_unocc_sc;
	color i_fg_translucence_shad_sc;
	color i_fg_collect_direct_shad;
	color i_bg_opacity;
	color i_bg_light;
	color i_bg_diffuse_unocc;
	color i_bg_diffuse_shad;
	color i_bg_specular_unocc;
	color i_bg_specular_shad;
	color i_bg_translucence_unocc;
	color i_bg_translucence_shad;
	color i_bg_diffuse_unocc_sc;
	color i_bg_diffuse_shad_sc;
	color i_bg_specular_unocc_sc;
	color i_bg_specular_shad_sc;
	color i_bg_translucence_unocc_sc;
	color i_bg_translucence_shad_sc;
	color i_bg_collect_direct_shad;
	// Outputs
	//
	output color o_light;
	output color o_diffuse_unocc;
	output color o_diffuse_shad;
	output color o_specular_unocc;
	output color o_specular_shad;
	output color o_translucence_unocc;
	output color o_translucence_shad;
	output color o_diffuse_unocc_sc;
	output color o_diffuse_shad_sc;
	output color o_specular_unocc_sc;
	output color o_specular_shad_sc;
	output color o_translucence_unocc_sc;
	output color o_translucence_shad_sc;
	output color o_collect_direct_shad;
	)
{
	o_light = blendColors(i_mode, i_premult, i_fg_light, i_fg_opacity, i_bg_light, i_bg_opacity);
	o_diffuse_unocc = blendColors(i_mode, i_premult, i_fg_diffuse_unocc, i_fg_opacity, i_bg_diffuse_unocc, i_bg_opacity);
	o_diffuse_shad = blendColors(i_mode, i_premult, i_fg_diffuse_shad, i_fg_opacity, i_bg_diffuse_shad, i_bg_opacity);
	o_specular_unocc = blendColors(i_mode, i_premult, i_fg_specular_unocc, i_fg_opacity, i_bg_specular_unocc, i_bg_opacity);
	o_specular_shad = blendColors(i_mode, i_premult, i_fg_specular_shad, i_fg_opacity, i_bg_specular_shad, i_bg_opacity);
	o_translucence_unocc = blendColors(i_mode, i_premult, i_fg_translucence_unocc, i_fg_opacity, i_bg_translucence_unocc, i_bg_opacity);
	o_translucence_shad = blendColors(i_mode, i_premult, i_fg_translucence_shad, i_fg_opacity, i_bg_translucence_shad, i_bg_opacity);
	o_diffuse_unocc_sc = blendColors(i_mode, i_premult, i_fg_diffuse_unocc_sc, i_fg_opacity, i_bg_diffuse_unocc_sc, i_bg_opacity);
	o_diffuse_shad_sc = blendColors(i_mode, i_premult, i_fg_diffuse_shad_sc, i_fg_opacity, i_bg_diffuse_shad_sc, i_bg_opacity);
	o_specular_unocc_sc = blendColors(i_mode, i_premult, i_fg_specular_unocc_sc, i_fg_opacity, i_bg_specular_unocc_sc, i_bg_opacity);
	o_specular_shad_sc = blendColors(i_mode, i_premult, i_fg_specular_shad_sc, i_fg_opacity, i_bg_specular_shad_sc, i_bg_opacity);
	o_translucence_unocc_sc = blendColors(i_mode, i_premult, i_fg_translucence_unocc_sc, i_fg_opacity, i_bg_translucence_unocc_sc, i_bg_opacity);
	o_translucence_shad_sc = blendColors(i_mode, i_premult, i_fg_translucence_shad_sc, i_fg_opacity, i_bg_translucence_shad_sc, i_bg_opacity);
	o_collect_direct_shad = blendColors(i_mode, i_premult, i_fg_collect_direct_shad, i_fg_opacity, i_bg_collect_direct_shad, i_bg_opacity);

}

void
calculateAuxiliaries(
	// Inputs
	//
	color i_opacity;
	float i_premult;
	color i_layerOpacities[];
	uniform string i_layerNames[];
	color i_puzzle1;
	color i_puzzle2;
	color i_puzzle3;
	)
{

    extern point P;
    extern normal N;
    extern vector I;
    extern float u, v;
    extern float s, t;
    
    vector In = normalize(I);
    normal Nn = normalize(N);
    
     color premult = mix(color 1, i_opacity, i_premult);

	extern color facing_ratio;
	facing_ratio = -In.ShadingNormal(Nn) * premult;

	extern color z_depth;
	z_depth = depth(P) * premult;

	extern color xyz_camera;
	xyz_camera = color(comp(P, 0), comp(P, 1), comp(P, 2)) * premult;

	extern color xyz_world;
	xyz_world = color(transform("world", P)) * premult;

	extern color xyz_object;
	xyz_object = color(transform("object", P)) * premult;

	extern color uv_coord;
	uv_coord = color(s, t, 0) * premult;

	extern color normal_world;
	normal_world = color(normalize(ntransform("world", N))) * premult;

	extern color lod_id;
	lod_id = color(0);attribute("user:lod_id", lod_id);lod_id *= premult;

	extern color puzzle_1;
	puzzle_1 = i_puzzle1; attribute("user:puzzle_1", puzzle_1);puzzle_1 *= premult;

	extern color puzzle_2;
	puzzle_2 = i_puzzle2; attribute("user:puzzle_2", puzzle_2);puzzle_2 *= premult;

	extern color puzzle_3;
	puzzle_3 = i_puzzle3; attribute("user:puzzle_3", puzzle_3);puzzle_3 *= premult;

	extern color puzzle_id;
	puzzle_id = color(0);
    //string hashString = "";
    //attribute("user:delight_shortest_unique_name", hashString);
    //attribute("user:puzzle_id_set", hashString);
    //float hash = dl_hash(hashString);
    //puzzle_id = cellnoise(hash) * premult;;

	extern color layer_id;
	layer_id = 0;
    //float i;
    //for (i=0; i<arraylength(i_layerNames); i += 1) {
    //    color op = i_layerOpacities[i];
    //    float tolerance = .0001;
    //    if (op[0] > tolerance || op[1] > tolerance || op[2] > tolerance) {
    //        string layerName = i_layerNames[i];
    //        float hash = dl_hash(layerName);
    //        layer_id = cellnoise(hash);;
    //    }
    //};

}


#endif /* __dl_layer_h */
