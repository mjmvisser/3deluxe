surface dl__shadowCollector(
	uniform float shaderid = 0;
#ifndef rendermanCodeShaderParam_beautyMode
#define rendermanCodeShaderParam_beautyMode
	 float beautyMode = 0.0;
#endif
#ifndef rendermanCodeShaderParam_diffuseFalloff
#define rendermanCodeShaderParam_diffuseFalloff
	 float diffuseFalloff = 1.0;
#endif
#ifndef rendermanCodeShaderParam_useLightColor
#define rendermanCodeShaderParam_useLightColor
	 float useLightColor = 0.0;
#endif
#ifndef rendermanCodeShaderParam_shadowColor
#define rendermanCodeShaderParam_shadowColor
	 color shadowColor = color (0.0, 0.0, 0.0);
#endif
#ifndef rendermanCodeShaderParam_shadowOpacity
#define rendermanCodeShaderParam_shadowOpacity
	 float shadowOpacity = 1.0;
#endif
#ifndef rendermanCodeShaderParam_hemispheres
#define rendermanCodeShaderParam_hemispheres
	 float hemispheres = 0.899999976158;
#endif
#ifndef rendermanCodeShaderParam_hemisphereFalloff
#define rendermanCodeShaderParam_hemisphereFalloff
	 float hemisphereFalloff = 0.0500000007451;
#endif
#ifndef rendermanCodeShaderParam_opacity
#define rendermanCodeShaderParam_opacity
	output varying color opacity = 0;
#endif
#ifndef rendermanCodeShaderParam_beauty
#define rendermanCodeShaderParam_beauty
	output varying color beauty = 0;
#endif
#ifndef rendermanCodeShaderParam_light
#define rendermanCodeShaderParam_light
	output varying color light = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls0
#define rendermanCodeShaderParam_light_ls0
	output varying color light_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls1
#define rendermanCodeShaderParam_light_ls1
	output varying color light_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls2
#define rendermanCodeShaderParam_light_ls2
	output varying color light_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls3
#define rendermanCodeShaderParam_light_ls3
	output varying color light_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls4
#define rendermanCodeShaderParam_light_ls4
	output varying color light_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_light_ls5
#define rendermanCodeShaderParam_light_ls5
	output varying color light_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc
#define rendermanCodeShaderParam_diffuse_unocc
	output varying color diffuse_unocc = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls0
#define rendermanCodeShaderParam_diffuse_unocc_ls0
	output varying color diffuse_unocc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls1
#define rendermanCodeShaderParam_diffuse_unocc_ls1
	output varying color diffuse_unocc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls2
#define rendermanCodeShaderParam_diffuse_unocc_ls2
	output varying color diffuse_unocc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls3
#define rendermanCodeShaderParam_diffuse_unocc_ls3
	output varying color diffuse_unocc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls4
#define rendermanCodeShaderParam_diffuse_unocc_ls4
	output varying color diffuse_unocc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_ls5
#define rendermanCodeShaderParam_diffuse_unocc_ls5
	output varying color diffuse_unocc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad
#define rendermanCodeShaderParam_diffuse_shad
	output varying color diffuse_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls0
#define rendermanCodeShaderParam_diffuse_shad_ls0
	output varying color diffuse_shad_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls1
#define rendermanCodeShaderParam_diffuse_shad_ls1
	output varying color diffuse_shad_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls2
#define rendermanCodeShaderParam_diffuse_shad_ls2
	output varying color diffuse_shad_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls3
#define rendermanCodeShaderParam_diffuse_shad_ls3
	output varying color diffuse_shad_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls4
#define rendermanCodeShaderParam_diffuse_shad_ls4
	output varying color diffuse_shad_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_ls5
#define rendermanCodeShaderParam_diffuse_shad_ls5
	output varying color diffuse_shad_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc
#define rendermanCodeShaderParam_specular_unocc
	output varying color specular_unocc = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls0
#define rendermanCodeShaderParam_specular_unocc_ls0
	output varying color specular_unocc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls1
#define rendermanCodeShaderParam_specular_unocc_ls1
	output varying color specular_unocc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls2
#define rendermanCodeShaderParam_specular_unocc_ls2
	output varying color specular_unocc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls3
#define rendermanCodeShaderParam_specular_unocc_ls3
	output varying color specular_unocc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls4
#define rendermanCodeShaderParam_specular_unocc_ls4
	output varying color specular_unocc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_ls5
#define rendermanCodeShaderParam_specular_unocc_ls5
	output varying color specular_unocc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad
#define rendermanCodeShaderParam_specular_shad
	output varying color specular_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls0
#define rendermanCodeShaderParam_specular_shad_ls0
	output varying color specular_shad_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls1
#define rendermanCodeShaderParam_specular_shad_ls1
	output varying color specular_shad_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls2
#define rendermanCodeShaderParam_specular_shad_ls2
	output varying color specular_shad_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls3
#define rendermanCodeShaderParam_specular_shad_ls3
	output varying color specular_shad_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls4
#define rendermanCodeShaderParam_specular_shad_ls4
	output varying color specular_shad_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_ls5
#define rendermanCodeShaderParam_specular_shad_ls5
	output varying color specular_shad_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc
#define rendermanCodeShaderParam_translucence_unocc
	output varying color translucence_unocc = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls0
#define rendermanCodeShaderParam_translucence_unocc_ls0
	output varying color translucence_unocc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls1
#define rendermanCodeShaderParam_translucence_unocc_ls1
	output varying color translucence_unocc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls2
#define rendermanCodeShaderParam_translucence_unocc_ls2
	output varying color translucence_unocc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls3
#define rendermanCodeShaderParam_translucence_unocc_ls3
	output varying color translucence_unocc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls4
#define rendermanCodeShaderParam_translucence_unocc_ls4
	output varying color translucence_unocc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_ls5
#define rendermanCodeShaderParam_translucence_unocc_ls5
	output varying color translucence_unocc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad
#define rendermanCodeShaderParam_translucence_shad
	output varying color translucence_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls0
#define rendermanCodeShaderParam_translucence_shad_ls0
	output varying color translucence_shad_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls1
#define rendermanCodeShaderParam_translucence_shad_ls1
	output varying color translucence_shad_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls2
#define rendermanCodeShaderParam_translucence_shad_ls2
	output varying color translucence_shad_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls3
#define rendermanCodeShaderParam_translucence_shad_ls3
	output varying color translucence_shad_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls4
#define rendermanCodeShaderParam_translucence_shad_ls4
	output varying color translucence_shad_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_ls5
#define rendermanCodeShaderParam_translucence_shad_ls5
	output varying color translucence_shad_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc
#define rendermanCodeShaderParam_diffuse_unocc_sc
	output varying color diffuse_unocc_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls0
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls0
	output varying color diffuse_unocc_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls1
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls1
	output varying color diffuse_unocc_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls2
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls2
	output varying color diffuse_unocc_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls3
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls3
	output varying color diffuse_unocc_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls4
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls4
	output varying color diffuse_unocc_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_unocc_sc_ls5
#define rendermanCodeShaderParam_diffuse_unocc_sc_ls5
	output varying color diffuse_unocc_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc
#define rendermanCodeShaderParam_diffuse_shad_sc
	output varying color diffuse_shad_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls0
#define rendermanCodeShaderParam_diffuse_shad_sc_ls0
	output varying color diffuse_shad_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls1
#define rendermanCodeShaderParam_diffuse_shad_sc_ls1
	output varying color diffuse_shad_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls2
#define rendermanCodeShaderParam_diffuse_shad_sc_ls2
	output varying color diffuse_shad_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls3
#define rendermanCodeShaderParam_diffuse_shad_sc_ls3
	output varying color diffuse_shad_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls4
#define rendermanCodeShaderParam_diffuse_shad_sc_ls4
	output varying color diffuse_shad_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_shad_sc_ls5
#define rendermanCodeShaderParam_diffuse_shad_sc_ls5
	output varying color diffuse_shad_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc
#define rendermanCodeShaderParam_specular_unocc_sc
	output varying color specular_unocc_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls0
#define rendermanCodeShaderParam_specular_unocc_sc_ls0
	output varying color specular_unocc_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls1
#define rendermanCodeShaderParam_specular_unocc_sc_ls1
	output varying color specular_unocc_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls2
#define rendermanCodeShaderParam_specular_unocc_sc_ls2
	output varying color specular_unocc_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls3
#define rendermanCodeShaderParam_specular_unocc_sc_ls3
	output varying color specular_unocc_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls4
#define rendermanCodeShaderParam_specular_unocc_sc_ls4
	output varying color specular_unocc_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_unocc_sc_ls5
#define rendermanCodeShaderParam_specular_unocc_sc_ls5
	output varying color specular_unocc_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc
#define rendermanCodeShaderParam_specular_shad_sc
	output varying color specular_shad_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls0
#define rendermanCodeShaderParam_specular_shad_sc_ls0
	output varying color specular_shad_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls1
#define rendermanCodeShaderParam_specular_shad_sc_ls1
	output varying color specular_shad_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls2
#define rendermanCodeShaderParam_specular_shad_sc_ls2
	output varying color specular_shad_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls3
#define rendermanCodeShaderParam_specular_shad_sc_ls3
	output varying color specular_shad_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls4
#define rendermanCodeShaderParam_specular_shad_sc_ls4
	output varying color specular_shad_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_shad_sc_ls5
#define rendermanCodeShaderParam_specular_shad_sc_ls5
	output varying color specular_shad_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc
#define rendermanCodeShaderParam_translucence_unocc_sc
	output varying color translucence_unocc_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls0
#define rendermanCodeShaderParam_translucence_unocc_sc_ls0
	output varying color translucence_unocc_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls1
#define rendermanCodeShaderParam_translucence_unocc_sc_ls1
	output varying color translucence_unocc_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls2
#define rendermanCodeShaderParam_translucence_unocc_sc_ls2
	output varying color translucence_unocc_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls3
#define rendermanCodeShaderParam_translucence_unocc_sc_ls3
	output varying color translucence_unocc_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls4
#define rendermanCodeShaderParam_translucence_unocc_sc_ls4
	output varying color translucence_unocc_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_unocc_sc_ls5
#define rendermanCodeShaderParam_translucence_unocc_sc_ls5
	output varying color translucence_unocc_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc
#define rendermanCodeShaderParam_translucence_shad_sc
	output varying color translucence_shad_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls0
#define rendermanCodeShaderParam_translucence_shad_sc_ls0
	output varying color translucence_shad_sc_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls1
#define rendermanCodeShaderParam_translucence_shad_sc_ls1
	output varying color translucence_shad_sc_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls2
#define rendermanCodeShaderParam_translucence_shad_sc_ls2
	output varying color translucence_shad_sc_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls3
#define rendermanCodeShaderParam_translucence_shad_sc_ls3
	output varying color translucence_shad_sc_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls4
#define rendermanCodeShaderParam_translucence_shad_sc_ls4
	output varying color translucence_shad_sc_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_translucence_shad_sc_ls5
#define rendermanCodeShaderParam_translucence_shad_sc_ls5
	output varying color translucence_shad_sc_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_diffuse_surf
#define rendermanCodeShaderParam_diffuse_surf
	output varying color diffuse_surf = 0;
#endif
#ifndef rendermanCodeShaderParam_specular_surf
#define rendermanCodeShaderParam_specular_surf
	output varying color specular_surf = 0;
#endif
#ifndef rendermanCodeShaderParam_incandescence
#define rendermanCodeShaderParam_incandescence
	output varying color incandescence = 0;
#endif
#ifndef rendermanCodeShaderParam_ambient
#define rendermanCodeShaderParam_ambient
	output varying color ambient = 0;
#endif
#ifndef rendermanCodeShaderParam_indirect_unocc
#define rendermanCodeShaderParam_indirect_unocc
	output varying color indirect_unocc = 0;
#endif
#ifndef rendermanCodeShaderParam_indirect_shad
#define rendermanCodeShaderParam_indirect_shad
	output varying color indirect_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_indirect_unocc_sc
#define rendermanCodeShaderParam_indirect_unocc_sc
	output varying color indirect_unocc_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_indirect_shad_sc
#define rendermanCodeShaderParam_indirect_shad_sc
	output varying color indirect_shad_sc = 0;
#endif
#ifndef rendermanCodeShaderParam_reflection_env
#define rendermanCodeShaderParam_reflection_env
	output varying color reflection_env = 0;
#endif
#ifndef rendermanCodeShaderParam_occlusion
#define rendermanCodeShaderParam_occlusion
	output varying color occlusion = 0;
#endif
#ifndef rendermanCodeShaderParam_bentnormal
#define rendermanCodeShaderParam_bentnormal
	output varying color bentnormal = 0;
#endif
#ifndef rendermanCodeShaderParam_reflection
#define rendermanCodeShaderParam_reflection
	output varying color reflection = 0;
#endif
#ifndef rendermanCodeShaderParam_reflection_depth
#define rendermanCodeShaderParam_reflection_depth
	output varying color reflection_depth = 0;
#endif
#ifndef rendermanCodeShaderParam_refraction
#define rendermanCodeShaderParam_refraction
	output varying color refraction = 0;
#endif
#ifndef rendermanCodeShaderParam_subsurface
#define rendermanCodeShaderParam_subsurface
	output varying color subsurface = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad
#define rendermanCodeShaderParam_collect_direct_shad
	output varying color collect_direct_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls0
#define rendermanCodeShaderParam_collect_direct_shad_ls0
	output varying color collect_direct_shad_ls0 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls1
#define rendermanCodeShaderParam_collect_direct_shad_ls1
	output varying color collect_direct_shad_ls1 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls2
#define rendermanCodeShaderParam_collect_direct_shad_ls2
	output varying color collect_direct_shad_ls2 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls3
#define rendermanCodeShaderParam_collect_direct_shad_ls3
	output varying color collect_direct_shad_ls3 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls4
#define rendermanCodeShaderParam_collect_direct_shad_ls4
	output varying color collect_direct_shad_ls4 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_direct_shad_ls5
#define rendermanCodeShaderParam_collect_direct_shad_ls5
	output varying color collect_direct_shad_ls5 = 0;
#endif
#ifndef rendermanCodeShaderParam_collect_indirect_shad
#define rendermanCodeShaderParam_collect_indirect_shad
	output varying color collect_indirect_shad = 0;
#endif
#ifndef rendermanCodeShaderParam_facing_ratio
#define rendermanCodeShaderParam_facing_ratio
	output varying color facing_ratio = 0;
#endif
#ifndef rendermanCodeShaderParam_z_depth
#define rendermanCodeShaderParam_z_depth
	output varying color z_depth = 0;
#endif
#ifndef rendermanCodeShaderParam_xyz_camera
#define rendermanCodeShaderParam_xyz_camera
	output varying color xyz_camera = 0;
#endif
#ifndef rendermanCodeShaderParam_xyz_world
#define rendermanCodeShaderParam_xyz_world
	output varying color xyz_world = 0;
#endif
#ifndef rendermanCodeShaderParam_xyz_object
#define rendermanCodeShaderParam_xyz_object
	output varying color xyz_object = 0;
#endif
#ifndef rendermanCodeShaderParam_uv_coord
#define rendermanCodeShaderParam_uv_coord
	output varying color uv_coord = 0;
#endif
#ifndef rendermanCodeShaderParam_normal_world
#define rendermanCodeShaderParam_normal_world
	output varying color normal_world = 0;
#endif
#ifndef rendermanCodeShaderParam_lod_id
#define rendermanCodeShaderParam_lod_id
	output varying color lod_id = 0;
#endif
#ifndef rendermanCodeShaderParam_puzzle_1
#define rendermanCodeShaderParam_puzzle_1
	output varying color puzzle_1 = 0;
#endif
#ifndef rendermanCodeShaderParam_puzzle_2
#define rendermanCodeShaderParam_puzzle_2
	output varying color puzzle_2 = 0;
#endif
#ifndef rendermanCodeShaderParam_puzzle_3
#define rendermanCodeShaderParam_puzzle_3
	output varying color puzzle_3 = 0;
#endif
#ifndef rendermanCodeShaderParam_puzzle_id
#define rendermanCodeShaderParam_puzzle_id
	output varying color puzzle_id = 0;
#endif
#ifndef rendermanCodeShaderParam_layer_id
#define rendermanCodeShaderParam_layer_id
	output varying color layer_id = 0;
#endif
)
{
	// Common variables declarations
	//
	float ss = s;
	float tt = 1 - t;

	// Dummy variable declarations
	//
	float floatDummy = 0.0;
	float float2Dummy[2] = {0.0, 0.0};
	float floatsDummy[] = {};
	color colorDummy = color(0,0,0);
	color colorsDummy[] = {};
	matrix matrixDummy = 1;
	normal normalDummy = normal(0,0,0);
	point pointDummy = point(0,0,0);
	vector vectorDummy = vector(0,0,0);
	string stringDummy;

	// Variable to keep track of transparency for AOVs if multiple shaders are used
	color __transparency = 1;

	// Include statements
	//
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat5(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float beautyMode;
		outputValue = beautyMode;
	}
	
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat4(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float diffuseFalloff;
		outputValue = diffuseFalloff;
	}
	
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat7(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float useLightColor;
		outputValue = useLightColor;
	}
	
	#include <dl_externColor.h>
	void maya_rendermanCode_dl_externColor1(
		 color inputValue;
		output  color outputValue;
		)
	{
		extern  color shadowColor;
		outputValue = shadowColor;
	}
	
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat1(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float shadowOpacity;
		outputValue = shadowOpacity;
	}
	
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat2(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float hemispheres;
		outputValue = hemispheres;
	}
	
	#include <dl_externFloat.h>
	void maya_rendermanCode_dl_externFloat3(
		 float inputValue;
		output  float outputValue;
		)
	{
		extern  float hemisphereFalloff;
		outputValue = hemisphereFalloff;
	}
	
	#include <dl_layer.h>
	void maya_rendermanCode_dl_shadowCollector(
		 normal normalCamera;
		 color puzzle1;
		 color puzzle2;
		 color puzzle3;
		 color globalOpacity;
		 float displacementGlobalScale;
		 float displacementGlobalOffset;
		uniform float displacementCompensateScale;
		uniform float premultAux;
		uniform float collapseComponents;
		uniform float collapseDisplacements;
		 color layers0_layer_opacity;
		uniform float layers0_layer_mode;
		 float layers0_layer_premult;
		 color layers0_layer_components0_component_beauty;
		 color layers0_layer_components0_component_light[];
		 color layers0_layer_components0_component_diffuse_unocc[];
		 color layers0_layer_components0_component_diffuse_shad[];
		 color layers0_layer_components0_component_specular_unocc[];
		 color layers0_layer_components0_component_specular_shad[];
		 color layers0_layer_components0_component_translucence_unocc[];
		 color layers0_layer_components0_component_translucence_shad[];
		 color layers0_layer_components0_component_diffuse_unocc_sc[];
		 color layers0_layer_components0_component_diffuse_shad_sc[];
		 color layers0_layer_components0_component_specular_unocc_sc[];
		 color layers0_layer_components0_component_specular_shad_sc[];
		 color layers0_layer_components0_component_translucence_unocc_sc[];
		 color layers0_layer_components0_component_translucence_shad_sc[];
		 color layers0_layer_components0_component_diffuse_surf;
		 color layers0_layer_components0_component_specular_surf;
		 color layers0_layer_components0_component_incandescence;
		 color layers0_layer_components0_component_ambient;
		 color layers0_layer_components0_component_indirect_unocc;
		 color layers0_layer_components0_component_indirect_shad;
		 color layers0_layer_components0_component_indirect_unocc_sc;
		 color layers0_layer_components0_component_indirect_shad_sc;
		 color layers0_layer_components0_component_reflection_env;
		 color layers0_layer_components0_component_occlusion;
		 color layers0_layer_components0_component_bentnormal;
		 color layers0_layer_components0_component_reflection;
		 color layers0_layer_components0_component_reflection_depth;
		 color layers0_layer_components0_component_refraction;
		 color layers0_layer_components0_component_subsurface;
		 color layers0_layer_components0_component_collect_direct_shad[];
		 color layers0_layer_components0_component_collect_indirect_shad;
		 float customFloat[];
		 color customColor[];
		output  color outputComponent_output_beauty;
		output  color outputComponent_output_light[];
		output  color outputComponent_output_diffuse_unocc[];
		output  color outputComponent_output_diffuse_shad[];
		output  color outputComponent_output_specular_unocc[];
		output  color outputComponent_output_specular_shad[];
		output  color outputComponent_output_translucence_unocc[];
		output  color outputComponent_output_translucence_shad[];
		output  color outputComponent_output_diffuse_unocc_sc[];
		output  color outputComponent_output_diffuse_shad_sc[];
		output  color outputComponent_output_specular_unocc_sc[];
		output  color outputComponent_output_specular_shad_sc[];
		output  color outputComponent_output_translucence_unocc_sc[];
		output  color outputComponent_output_translucence_shad_sc[];
		output  color outputComponent_output_diffuse_surf;
		output  color outputComponent_output_specular_surf;
		output  color outputComponent_output_incandescence;
		output  color outputComponent_output_ambient;
		output  color outputComponent_output_indirect_unocc;
		output  color outputComponent_output_indirect_shad;
		output  color outputComponent_output_indirect_unocc_sc;
		output  color outputComponent_output_indirect_shad_sc;
		output  color outputComponent_output_reflection_env;
		output  color outputComponent_output_occlusion;
		output  color outputComponent_output_bentnormal;
		output  color outputComponent_output_reflection;
		output  color outputComponent_output_reflection_depth;
		output  color outputComponent_output_refraction;
		output  color outputComponent_output_subsurface;
		output  color outputComponent_output_collect_direct_shad[];
		output  color outputComponent_output_collect_indirect_shad;
		output  color outColor;
		output  color outTransparency;
		output  float displacement;
		)
	{
		extern varying color opacity;
		extern varying color beauty;
		extern varying color light;
		extern varying color light_ls0;
		extern varying color light_ls1;
		extern varying color light_ls2;
		extern varying color light_ls3;
		extern varying color light_ls4;
		extern varying color light_ls5;
		extern varying color diffuse_unocc;
		extern varying color diffuse_unocc_ls0;
		extern varying color diffuse_unocc_ls1;
		extern varying color diffuse_unocc_ls2;
		extern varying color diffuse_unocc_ls3;
		extern varying color diffuse_unocc_ls4;
		extern varying color diffuse_unocc_ls5;
		extern varying color diffuse_shad;
		extern varying color diffuse_shad_ls0;
		extern varying color diffuse_shad_ls1;
		extern varying color diffuse_shad_ls2;
		extern varying color diffuse_shad_ls3;
		extern varying color diffuse_shad_ls4;
		extern varying color diffuse_shad_ls5;
		extern varying color specular_unocc;
		extern varying color specular_unocc_ls0;
		extern varying color specular_unocc_ls1;
		extern varying color specular_unocc_ls2;
		extern varying color specular_unocc_ls3;
		extern varying color specular_unocc_ls4;
		extern varying color specular_unocc_ls5;
		extern varying color specular_shad;
		extern varying color specular_shad_ls0;
		extern varying color specular_shad_ls1;
		extern varying color specular_shad_ls2;
		extern varying color specular_shad_ls3;
		extern varying color specular_shad_ls4;
		extern varying color specular_shad_ls5;
		extern varying color translucence_unocc;
		extern varying color translucence_unocc_ls0;
		extern varying color translucence_unocc_ls1;
		extern varying color translucence_unocc_ls2;
		extern varying color translucence_unocc_ls3;
		extern varying color translucence_unocc_ls4;
		extern varying color translucence_unocc_ls5;
		extern varying color translucence_shad;
		extern varying color translucence_shad_ls0;
		extern varying color translucence_shad_ls1;
		extern varying color translucence_shad_ls2;
		extern varying color translucence_shad_ls3;
		extern varying color translucence_shad_ls4;
		extern varying color translucence_shad_ls5;
		extern varying color diffuse_unocc_sc;
		extern varying color diffuse_unocc_sc_ls0;
		extern varying color diffuse_unocc_sc_ls1;
		extern varying color diffuse_unocc_sc_ls2;
		extern varying color diffuse_unocc_sc_ls3;
		extern varying color diffuse_unocc_sc_ls4;
		extern varying color diffuse_unocc_sc_ls5;
		extern varying color diffuse_shad_sc;
		extern varying color diffuse_shad_sc_ls0;
		extern varying color diffuse_shad_sc_ls1;
		extern varying color diffuse_shad_sc_ls2;
		extern varying color diffuse_shad_sc_ls3;
		extern varying color diffuse_shad_sc_ls4;
		extern varying color diffuse_shad_sc_ls5;
		extern varying color specular_unocc_sc;
		extern varying color specular_unocc_sc_ls0;
		extern varying color specular_unocc_sc_ls1;
		extern varying color specular_unocc_sc_ls2;
		extern varying color specular_unocc_sc_ls3;
		extern varying color specular_unocc_sc_ls4;
		extern varying color specular_unocc_sc_ls5;
		extern varying color specular_shad_sc;
		extern varying color specular_shad_sc_ls0;
		extern varying color specular_shad_sc_ls1;
		extern varying color specular_shad_sc_ls2;
		extern varying color specular_shad_sc_ls3;
		extern varying color specular_shad_sc_ls4;
		extern varying color specular_shad_sc_ls5;
		extern varying color translucence_unocc_sc;
		extern varying color translucence_unocc_sc_ls0;
		extern varying color translucence_unocc_sc_ls1;
		extern varying color translucence_unocc_sc_ls2;
		extern varying color translucence_unocc_sc_ls3;
		extern varying color translucence_unocc_sc_ls4;
		extern varying color translucence_unocc_sc_ls5;
		extern varying color translucence_shad_sc;
		extern varying color translucence_shad_sc_ls0;
		extern varying color translucence_shad_sc_ls1;
		extern varying color translucence_shad_sc_ls2;
		extern varying color translucence_shad_sc_ls3;
		extern varying color translucence_shad_sc_ls4;
		extern varying color translucence_shad_sc_ls5;
		extern varying color diffuse_surf;
		extern varying color specular_surf;
		extern varying color incandescence;
		extern varying color ambient;
		extern varying color indirect_unocc;
		extern varying color indirect_shad;
		extern varying color indirect_unocc_sc;
		extern varying color indirect_shad_sc;
		extern varying color reflection_env;
		extern varying color occlusion;
		extern varying color bentnormal;
		extern varying color reflection;
		extern varying color reflection_depth;
		extern varying color refraction;
		extern varying color subsurface;
		extern varying color collect_direct_shad;
		extern varying color collect_direct_shad_ls0;
		extern varying color collect_direct_shad_ls1;
		extern varying color collect_direct_shad_ls2;
		extern varying color collect_direct_shad_ls3;
		extern varying color collect_direct_shad_ls4;
		extern varying color collect_direct_shad_ls5;
		extern varying color collect_indirect_shad;
		extern varying color facing_ratio;
		extern varying color z_depth;
		extern varying color xyz_camera;
		extern varying color xyz_world;
		extern varying color xyz_object;
		extern varying color uv_coord;
		extern varying color normal_world;
		extern varying color lod_id;
		extern varying color puzzle_1;
		extern varying color puzzle_2;
		extern varying color puzzle_3;
		extern varying color puzzle_id;
		extern varying color layer_id;
		#include "dl_layer.h"
		color resultColor, resultOpacity;
		color layer0_opacity = layers0_layer_opacity;
		blend(layers0_layer_mode, 1, layer0_opacity, 1, opacity, resultColor, opacity);
		beauty = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_beauty, layer0_opacity, beauty, opacity);
		diffuse_surf = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_diffuse_surf, layer0_opacity, diffuse_surf, opacity);
		specular_surf = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_specular_surf, layer0_opacity, specular_surf, opacity);
		incandescence = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_incandescence, layer0_opacity, incandescence, opacity);
		ambient = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_ambient, layer0_opacity, ambient, opacity);
		indirect_unocc = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_indirect_unocc, layer0_opacity, indirect_unocc, opacity);
		indirect_shad = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_indirect_shad, layer0_opacity, indirect_shad, opacity);
		indirect_unocc_sc = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_indirect_unocc_sc, layer0_opacity, indirect_unocc_sc, opacity);
		indirect_shad_sc = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_indirect_shad_sc, layer0_opacity, indirect_shad_sc, opacity);
		reflection_env = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_reflection_env, layer0_opacity, reflection_env, opacity);
		occlusion = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_occlusion, layer0_opacity, occlusion, opacity);
		bentnormal = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_bentnormal, layer0_opacity, bentnormal, opacity);
		reflection = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_reflection, layer0_opacity, reflection, opacity);
		reflection_depth = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_reflection_depth, layer0_opacity, reflection_depth, opacity);
		refraction = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_refraction, layer0_opacity, refraction, opacity);
		subsurface = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_subsurface, layer0_opacity, subsurface, opacity);
		collect_indirect_shad = blendColors(layers0_layer_mode, layers0_layer_premult, layers0_layer_components0_component_collect_indirect_shad, layer0_opacity, collect_indirect_shad, opacity);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[0],
			layers0_layer_components0_component_diffuse_unocc[0],
			layers0_layer_components0_component_diffuse_shad[0],
			layers0_layer_components0_component_specular_unocc[0],
			layers0_layer_components0_component_specular_shad[0],
			layers0_layer_components0_component_translucence_unocc[0],
			layers0_layer_components0_component_translucence_shad[0],
			layers0_layer_components0_component_diffuse_unocc_sc[0],
			layers0_layer_components0_component_diffuse_shad_sc[0],
			layers0_layer_components0_component_specular_unocc_sc[0],
			layers0_layer_components0_component_specular_shad_sc[0],
			layers0_layer_components0_component_translucence_unocc_sc[0],
			layers0_layer_components0_component_translucence_shad_sc[0],
			layers0_layer_components0_component_collect_direct_shad[0],
			opacity,
			light_ls0,
			diffuse_unocc_ls0,
			diffuse_shad_ls0,
			specular_unocc_ls0,
			specular_shad_ls0,
			translucence_unocc_ls0,
			translucence_shad_ls0,
			diffuse_unocc_sc_ls0,
			diffuse_shad_sc_ls0,
			specular_unocc_sc_ls0,
			specular_shad_sc_ls0,
			translucence_unocc_sc_ls0,
			translucence_shad_sc_ls0,
			collect_direct_shad_ls0,
			light_ls0,
			diffuse_unocc_ls0,
			diffuse_shad_ls0,
			specular_unocc_ls0,
			specular_shad_ls0,
			translucence_unocc_ls0,
			translucence_shad_ls0,
			diffuse_unocc_sc_ls0,
			diffuse_shad_sc_ls0,
			specular_unocc_sc_ls0,
			specular_shad_sc_ls0,
			translucence_unocc_sc_ls0,
			translucence_shad_sc_ls0,
			collect_direct_shad_ls0);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[1],
			layers0_layer_components0_component_diffuse_unocc[1],
			layers0_layer_components0_component_diffuse_shad[1],
			layers0_layer_components0_component_specular_unocc[1],
			layers0_layer_components0_component_specular_shad[1],
			layers0_layer_components0_component_translucence_unocc[1],
			layers0_layer_components0_component_translucence_shad[1],
			layers0_layer_components0_component_diffuse_unocc_sc[1],
			layers0_layer_components0_component_diffuse_shad_sc[1],
			layers0_layer_components0_component_specular_unocc_sc[1],
			layers0_layer_components0_component_specular_shad_sc[1],
			layers0_layer_components0_component_translucence_unocc_sc[1],
			layers0_layer_components0_component_translucence_shad_sc[1],
			layers0_layer_components0_component_collect_direct_shad[1],
			opacity,
			light_ls1,
			diffuse_unocc_ls1,
			diffuse_shad_ls1,
			specular_unocc_ls1,
			specular_shad_ls1,
			translucence_unocc_ls1,
			translucence_shad_ls1,
			diffuse_unocc_sc_ls1,
			diffuse_shad_sc_ls1,
			specular_unocc_sc_ls1,
			specular_shad_sc_ls1,
			translucence_unocc_sc_ls1,
			translucence_shad_sc_ls1,
			collect_direct_shad_ls1,
			light_ls1,
			diffuse_unocc_ls1,
			diffuse_shad_ls1,
			specular_unocc_ls1,
			specular_shad_ls1,
			translucence_unocc_ls1,
			translucence_shad_ls1,
			diffuse_unocc_sc_ls1,
			diffuse_shad_sc_ls1,
			specular_unocc_sc_ls1,
			specular_shad_sc_ls1,
			translucence_unocc_sc_ls1,
			translucence_shad_sc_ls1,
			collect_direct_shad_ls1);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[2],
			layers0_layer_components0_component_diffuse_unocc[2],
			layers0_layer_components0_component_diffuse_shad[2],
			layers0_layer_components0_component_specular_unocc[2],
			layers0_layer_components0_component_specular_shad[2],
			layers0_layer_components0_component_translucence_unocc[2],
			layers0_layer_components0_component_translucence_shad[2],
			layers0_layer_components0_component_diffuse_unocc_sc[2],
			layers0_layer_components0_component_diffuse_shad_sc[2],
			layers0_layer_components0_component_specular_unocc_sc[2],
			layers0_layer_components0_component_specular_shad_sc[2],
			layers0_layer_components0_component_translucence_unocc_sc[2],
			layers0_layer_components0_component_translucence_shad_sc[2],
			layers0_layer_components0_component_collect_direct_shad[2],
			opacity,
			light_ls2,
			diffuse_unocc_ls2,
			diffuse_shad_ls2,
			specular_unocc_ls2,
			specular_shad_ls2,
			translucence_unocc_ls2,
			translucence_shad_ls2,
			diffuse_unocc_sc_ls2,
			diffuse_shad_sc_ls2,
			specular_unocc_sc_ls2,
			specular_shad_sc_ls2,
			translucence_unocc_sc_ls2,
			translucence_shad_sc_ls2,
			collect_direct_shad_ls2,
			light_ls2,
			diffuse_unocc_ls2,
			diffuse_shad_ls2,
			specular_unocc_ls2,
			specular_shad_ls2,
			translucence_unocc_ls2,
			translucence_shad_ls2,
			diffuse_unocc_sc_ls2,
			diffuse_shad_sc_ls2,
			specular_unocc_sc_ls2,
			specular_shad_sc_ls2,
			translucence_unocc_sc_ls2,
			translucence_shad_sc_ls2,
			collect_direct_shad_ls2);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[3],
			layers0_layer_components0_component_diffuse_unocc[3],
			layers0_layer_components0_component_diffuse_shad[3],
			layers0_layer_components0_component_specular_unocc[3],
			layers0_layer_components0_component_specular_shad[3],
			layers0_layer_components0_component_translucence_unocc[3],
			layers0_layer_components0_component_translucence_shad[3],
			layers0_layer_components0_component_diffuse_unocc_sc[3],
			layers0_layer_components0_component_diffuse_shad_sc[3],
			layers0_layer_components0_component_specular_unocc_sc[3],
			layers0_layer_components0_component_specular_shad_sc[3],
			layers0_layer_components0_component_translucence_unocc_sc[3],
			layers0_layer_components0_component_translucence_shad_sc[3],
			layers0_layer_components0_component_collect_direct_shad[3],
			opacity,
			light_ls3,
			diffuse_unocc_ls3,
			diffuse_shad_ls3,
			specular_unocc_ls3,
			specular_shad_ls3,
			translucence_unocc_ls3,
			translucence_shad_ls3,
			diffuse_unocc_sc_ls3,
			diffuse_shad_sc_ls3,
			specular_unocc_sc_ls3,
			specular_shad_sc_ls3,
			translucence_unocc_sc_ls3,
			translucence_shad_sc_ls3,
			collect_direct_shad_ls3,
			light_ls3,
			diffuse_unocc_ls3,
			diffuse_shad_ls3,
			specular_unocc_ls3,
			specular_shad_ls3,
			translucence_unocc_ls3,
			translucence_shad_ls3,
			diffuse_unocc_sc_ls3,
			diffuse_shad_sc_ls3,
			specular_unocc_sc_ls3,
			specular_shad_sc_ls3,
			translucence_unocc_sc_ls3,
			translucence_shad_sc_ls3,
			collect_direct_shad_ls3);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[4],
			layers0_layer_components0_component_diffuse_unocc[4],
			layers0_layer_components0_component_diffuse_shad[4],
			layers0_layer_components0_component_specular_unocc[4],
			layers0_layer_components0_component_specular_shad[4],
			layers0_layer_components0_component_translucence_unocc[4],
			layers0_layer_components0_component_translucence_shad[4],
			layers0_layer_components0_component_diffuse_unocc_sc[4],
			layers0_layer_components0_component_diffuse_shad_sc[4],
			layers0_layer_components0_component_specular_unocc_sc[4],
			layers0_layer_components0_component_specular_shad_sc[4],
			layers0_layer_components0_component_translucence_unocc_sc[4],
			layers0_layer_components0_component_translucence_shad_sc[4],
			layers0_layer_components0_component_collect_direct_shad[4],
			opacity,
			light_ls4,
			diffuse_unocc_ls4,
			diffuse_shad_ls4,
			specular_unocc_ls4,
			specular_shad_ls4,
			translucence_unocc_ls4,
			translucence_shad_ls4,
			diffuse_unocc_sc_ls4,
			diffuse_shad_sc_ls4,
			specular_unocc_sc_ls4,
			specular_shad_sc_ls4,
			translucence_unocc_sc_ls4,
			translucence_shad_sc_ls4,
			collect_direct_shad_ls4,
			light_ls4,
			diffuse_unocc_ls4,
			diffuse_shad_ls4,
			specular_unocc_ls4,
			specular_shad_ls4,
			translucence_unocc_ls4,
			translucence_shad_ls4,
			diffuse_unocc_sc_ls4,
			diffuse_shad_sc_ls4,
			specular_unocc_sc_ls4,
			specular_shad_sc_ls4,
			translucence_unocc_sc_ls4,
			translucence_shad_sc_ls4,
			collect_direct_shad_ls4);
		blendLightsets(
			layers0_layer_mode,
			layers0_layer_premult,
			layer0_opacity,
			layers0_layer_components0_component_light[5],
			layers0_layer_components0_component_diffuse_unocc[5],
			layers0_layer_components0_component_diffuse_shad[5],
			layers0_layer_components0_component_specular_unocc[5],
			layers0_layer_components0_component_specular_shad[5],
			layers0_layer_components0_component_translucence_unocc[5],
			layers0_layer_components0_component_translucence_shad[5],
			layers0_layer_components0_component_diffuse_unocc_sc[5],
			layers0_layer_components0_component_diffuse_shad_sc[5],
			layers0_layer_components0_component_specular_unocc_sc[5],
			layers0_layer_components0_component_specular_shad_sc[5],
			layers0_layer_components0_component_translucence_unocc_sc[5],
			layers0_layer_components0_component_translucence_shad_sc[5],
			layers0_layer_components0_component_collect_direct_shad[5],
			opacity,
			light_ls5,
			diffuse_unocc_ls5,
			diffuse_shad_ls5,
			specular_unocc_ls5,
			specular_shad_ls5,
			translucence_unocc_ls5,
			translucence_shad_ls5,
			diffuse_unocc_sc_ls5,
			diffuse_shad_sc_ls5,
			specular_unocc_sc_ls5,
			specular_shad_sc_ls5,
			translucence_unocc_sc_ls5,
			translucence_shad_sc_ls5,
			collect_direct_shad_ls5,
			light_ls5,
			diffuse_unocc_ls5,
			diffuse_shad_ls5,
			specular_unocc_ls5,
			specular_shad_ls5,
			translucence_unocc_ls5,
			translucence_shad_ls5,
			diffuse_unocc_sc_ls5,
			diffuse_shad_sc_ls5,
			specular_unocc_sc_ls5,
			specular_shad_sc_ls5,
			translucence_unocc_sc_ls5,
			translucence_shad_sc_ls5,
			collect_direct_shad_ls5);
		opacity *= globalOpacity;
		beauty *= globalOpacity;
		light_ls0 *= globalOpacity;
		light_ls1 *= globalOpacity;
		light_ls2 *= globalOpacity;
		light_ls3 *= globalOpacity;
		light_ls4 *= globalOpacity;
		light_ls5 *= globalOpacity;
		color light_lightsets[] = {light_ls0, light_ls1, light_ls2, light_ls3, light_ls4, light_ls5};
		light = accumulateColors(light_lightsets);
		diffuse_unocc_ls0 *= globalOpacity;
		diffuse_unocc_ls1 *= globalOpacity;
		diffuse_unocc_ls2 *= globalOpacity;
		diffuse_unocc_ls3 *= globalOpacity;
		diffuse_unocc_ls4 *= globalOpacity;
		diffuse_unocc_ls5 *= globalOpacity;
		color diffuse_unocc_lightsets[] = {diffuse_unocc_ls0, diffuse_unocc_ls1, diffuse_unocc_ls2, diffuse_unocc_ls3, diffuse_unocc_ls4, diffuse_unocc_ls5};
		diffuse_unocc = accumulateColors(diffuse_unocc_lightsets);
		diffuse_shad_ls0 *= globalOpacity;
		diffuse_shad_ls1 *= globalOpacity;
		diffuse_shad_ls2 *= globalOpacity;
		diffuse_shad_ls3 *= globalOpacity;
		diffuse_shad_ls4 *= globalOpacity;
		diffuse_shad_ls5 *= globalOpacity;
		color diffuse_shad_lightsets[] = {diffuse_shad_ls0, diffuse_shad_ls1, diffuse_shad_ls2, diffuse_shad_ls3, diffuse_shad_ls4, diffuse_shad_ls5};
		diffuse_shad = accumulateColors(diffuse_shad_lightsets);
		specular_unocc_ls0 *= globalOpacity;
		specular_unocc_ls1 *= globalOpacity;
		specular_unocc_ls2 *= globalOpacity;
		specular_unocc_ls3 *= globalOpacity;
		specular_unocc_ls4 *= globalOpacity;
		specular_unocc_ls5 *= globalOpacity;
		color specular_unocc_lightsets[] = {specular_unocc_ls0, specular_unocc_ls1, specular_unocc_ls2, specular_unocc_ls3, specular_unocc_ls4, specular_unocc_ls5};
		specular_unocc = accumulateColors(specular_unocc_lightsets);
		specular_shad_ls0 *= globalOpacity;
		specular_shad_ls1 *= globalOpacity;
		specular_shad_ls2 *= globalOpacity;
		specular_shad_ls3 *= globalOpacity;
		specular_shad_ls4 *= globalOpacity;
		specular_shad_ls5 *= globalOpacity;
		color specular_shad_lightsets[] = {specular_shad_ls0, specular_shad_ls1, specular_shad_ls2, specular_shad_ls3, specular_shad_ls4, specular_shad_ls5};
		specular_shad = accumulateColors(specular_shad_lightsets);
		translucence_unocc_ls0 *= globalOpacity;
		translucence_unocc_ls1 *= globalOpacity;
		translucence_unocc_ls2 *= globalOpacity;
		translucence_unocc_ls3 *= globalOpacity;
		translucence_unocc_ls4 *= globalOpacity;
		translucence_unocc_ls5 *= globalOpacity;
		color translucence_unocc_lightsets[] = {translucence_unocc_ls0, translucence_unocc_ls1, translucence_unocc_ls2, translucence_unocc_ls3, translucence_unocc_ls4, translucence_unocc_ls5};
		translucence_unocc = accumulateColors(translucence_unocc_lightsets);
		translucence_shad_ls0 *= globalOpacity;
		translucence_shad_ls1 *= globalOpacity;
		translucence_shad_ls2 *= globalOpacity;
		translucence_shad_ls3 *= globalOpacity;
		translucence_shad_ls4 *= globalOpacity;
		translucence_shad_ls5 *= globalOpacity;
		color translucence_shad_lightsets[] = {translucence_shad_ls0, translucence_shad_ls1, translucence_shad_ls2, translucence_shad_ls3, translucence_shad_ls4, translucence_shad_ls5};
		translucence_shad = accumulateColors(translucence_shad_lightsets);
		diffuse_unocc_sc_ls0 *= globalOpacity;
		diffuse_unocc_sc_ls1 *= globalOpacity;
		diffuse_unocc_sc_ls2 *= globalOpacity;
		diffuse_unocc_sc_ls3 *= globalOpacity;
		diffuse_unocc_sc_ls4 *= globalOpacity;
		diffuse_unocc_sc_ls5 *= globalOpacity;
		color diffuse_unocc_sc_lightsets[] = {diffuse_unocc_sc_ls0, diffuse_unocc_sc_ls1, diffuse_unocc_sc_ls2, diffuse_unocc_sc_ls3, diffuse_unocc_sc_ls4, diffuse_unocc_sc_ls5};
		diffuse_unocc_sc = accumulateColors(diffuse_unocc_sc_lightsets);
		diffuse_shad_sc_ls0 *= globalOpacity;
		diffuse_shad_sc_ls1 *= globalOpacity;
		diffuse_shad_sc_ls2 *= globalOpacity;
		diffuse_shad_sc_ls3 *= globalOpacity;
		diffuse_shad_sc_ls4 *= globalOpacity;
		diffuse_shad_sc_ls5 *= globalOpacity;
		color diffuse_shad_sc_lightsets[] = {diffuse_shad_sc_ls0, diffuse_shad_sc_ls1, diffuse_shad_sc_ls2, diffuse_shad_sc_ls3, diffuse_shad_sc_ls4, diffuse_shad_sc_ls5};
		diffuse_shad_sc = accumulateColors(diffuse_shad_sc_lightsets);
		specular_unocc_sc_ls0 *= globalOpacity;
		specular_unocc_sc_ls1 *= globalOpacity;
		specular_unocc_sc_ls2 *= globalOpacity;
		specular_unocc_sc_ls3 *= globalOpacity;
		specular_unocc_sc_ls4 *= globalOpacity;
		specular_unocc_sc_ls5 *= globalOpacity;
		color specular_unocc_sc_lightsets[] = {specular_unocc_sc_ls0, specular_unocc_sc_ls1, specular_unocc_sc_ls2, specular_unocc_sc_ls3, specular_unocc_sc_ls4, specular_unocc_sc_ls5};
		specular_unocc_sc = accumulateColors(specular_unocc_sc_lightsets);
		specular_shad_sc_ls0 *= globalOpacity;
		specular_shad_sc_ls1 *= globalOpacity;
		specular_shad_sc_ls2 *= globalOpacity;
		specular_shad_sc_ls3 *= globalOpacity;
		specular_shad_sc_ls4 *= globalOpacity;
		specular_shad_sc_ls5 *= globalOpacity;
		color specular_shad_sc_lightsets[] = {specular_shad_sc_ls0, specular_shad_sc_ls1, specular_shad_sc_ls2, specular_shad_sc_ls3, specular_shad_sc_ls4, specular_shad_sc_ls5};
		specular_shad_sc = accumulateColors(specular_shad_sc_lightsets);
		translucence_unocc_sc_ls0 *= globalOpacity;
		translucence_unocc_sc_ls1 *= globalOpacity;
		translucence_unocc_sc_ls2 *= globalOpacity;
		translucence_unocc_sc_ls3 *= globalOpacity;
		translucence_unocc_sc_ls4 *= globalOpacity;
		translucence_unocc_sc_ls5 *= globalOpacity;
		color translucence_unocc_sc_lightsets[] = {translucence_unocc_sc_ls0, translucence_unocc_sc_ls1, translucence_unocc_sc_ls2, translucence_unocc_sc_ls3, translucence_unocc_sc_ls4, translucence_unocc_sc_ls5};
		translucence_unocc_sc = accumulateColors(translucence_unocc_sc_lightsets);
		translucence_shad_sc_ls0 *= globalOpacity;
		translucence_shad_sc_ls1 *= globalOpacity;
		translucence_shad_sc_ls2 *= globalOpacity;
		translucence_shad_sc_ls3 *= globalOpacity;
		translucence_shad_sc_ls4 *= globalOpacity;
		translucence_shad_sc_ls5 *= globalOpacity;
		color translucence_shad_sc_lightsets[] = {translucence_shad_sc_ls0, translucence_shad_sc_ls1, translucence_shad_sc_ls2, translucence_shad_sc_ls3, translucence_shad_sc_ls4, translucence_shad_sc_ls5};
		translucence_shad_sc = accumulateColors(translucence_shad_sc_lightsets);
		diffuse_surf *= globalOpacity;
		specular_surf *= globalOpacity;
		incandescence *= globalOpacity;
		ambient *= globalOpacity;
		indirect_unocc *= globalOpacity;
		indirect_shad *= globalOpacity;
		indirect_unocc_sc *= globalOpacity;
		indirect_shad_sc *= globalOpacity;
		reflection_env *= globalOpacity;
		occlusion *= globalOpacity;
		bentnormal *= globalOpacity;
		reflection *= globalOpacity;
		reflection_depth *= globalOpacity;
		refraction *= globalOpacity;
		subsurface *= globalOpacity;
		collect_direct_shad_ls0 *= globalOpacity;
		collect_direct_shad_ls1 *= globalOpacity;
		collect_direct_shad_ls2 *= globalOpacity;
		collect_direct_shad_ls3 *= globalOpacity;
		collect_direct_shad_ls4 *= globalOpacity;
		collect_direct_shad_ls5 *= globalOpacity;
		color collect_direct_shad_lightsets[] = {collect_direct_shad_ls0, collect_direct_shad_ls1, collect_direct_shad_ls2, collect_direct_shad_ls3, collect_direct_shad_ls4, collect_direct_shad_ls5};
		collect_direct_shad = accumulateColors(collect_direct_shad_lightsets);
		collect_indirect_shad *= globalOpacity;
		color layerOpacities[] = {layer0_opacity};
		string layerNames[] = {"layer0"};
		calculateAuxiliaries(opacity, premultAux, layerOpacities, layerNames, puzzle1, puzzle2, puzzle3);
		outColor = beauty;
		outTransparency = 1 - opacity;
	}
	
	#include <dl_shadowCollector.h>

	// Output variable declarations
	//
	float dl__externFloat5_outputValue_local = 0;
	float dl__externFloat4_outputValue_local = 0;
	float dl__externFloat7_outputValue_local = 0;
	color dl__externColor1_outputValue_local = color(0,0,0);
	float dl__externFloat1_outputValue_local = 0;
	float dl__externFloat2_outputValue_local = 0;
	float dl__externFloat3_outputValue_local = 0;
	color dl__shadowCollectorComponent_outputComponent_output__beauty_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__light_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__diffuse__shad_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__specular__unocc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__specular__shad_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__translucence__unocc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__translucence__shad_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__diffuse__shad__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__specular__unocc__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__specular__shad__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__translucence__unocc__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__translucence__shad__sc_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__diffuse__surf_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__specular__surf_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__incandescence_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__ambient_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__indirect__unocc_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__indirect__shad_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__indirect__unocc__sc_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__indirect__shad__sc_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__reflection__env_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__occlusion_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__bentnormal_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__reflection_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__reflection__depth_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__refraction_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__subsurface_local = color(0,0,0);
color dl__shadowCollectorComponent_outputComponent_output__collect__direct__shad_local[] = { color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0), color(0,0,0) };
color dl__shadowCollectorComponent_outputComponent_output__collect__indirect__shad_local = color(0,0,0);
	color dl__shadowCollector_outColor_local = color(0,0,0);
	color dl__shadowCollector_outTransparency_local = color(0,0,0);

	// Compute call string for dl_externFloat5
	//
	maya_rendermanCode_dl_externFloat5(
		0, // inputValue
		dl__externFloat5_outputValue_local
		);

	// Compute call string for dl_externFloat4
	//
	maya_rendermanCode_dl_externFloat4(
		1, // inputValue
		dl__externFloat4_outputValue_local
		);

	// Compute call string for dl_externFloat7
	//
	maya_rendermanCode_dl_externFloat7(
		0, // inputValue
		dl__externFloat7_outputValue_local
		);

	// Compute call string for dl_externColor1
	//
	maya_rendermanCode_dl_externColor1(
		color(0, 0, 0), // inputValue
		dl__externColor1_outputValue_local
		);

	// Compute call string for dl_externFloat1
	//
	maya_rendermanCode_dl_externFloat1(
		1, // inputValue
		dl__externFloat1_outputValue_local
		);

	// Compute call string for dl_externFloat2
	//
	maya_rendermanCode_dl_externFloat2(
		0.8999999762, // inputValue
		dl__externFloat2_outputValue_local
		);

	// Compute call string for dl_externFloat3
	//
	maya_rendermanCode_dl_externFloat3(
		0.05000000075, // inputValue
		dl__externFloat3_outputValue_local
		);

	// Compute call string for dl_shadowCollectorComponent
	//
	maya_dl_shadowCollector(
		0, // mute
		1, // contribution
		1, // intensity
		color(1, 1, 1), // color
		0, // shadeCurves
		dl__externFloat5_outputValue_local, // beautyMode
		dl__externFloat4_outputValue_local, // diffuseFalloff
		dl__externFloat7_outputValue_local, // useLightColor
		0, // lightType
		N, // normalCamera
		dl__externColor1_outputValue_local, // shadowColor
		dl__externFloat1_outputValue_local, // shadowOpacity
		dl__externFloat2_outputValue_local, // hemispheres
		dl__externFloat3_outputValue_local, // hemisphereFalloff
		dl__shadowCollectorComponent_outputComponent_output__beauty_local,
		dl__shadowCollectorComponent_outputComponent_output__light_local,
		dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc_local,
		dl__shadowCollectorComponent_outputComponent_output__diffuse__shad_local,
		dl__shadowCollectorComponent_outputComponent_output__specular__unocc_local,
		dl__shadowCollectorComponent_outputComponent_output__specular__shad_local,
		dl__shadowCollectorComponent_outputComponent_output__translucence__unocc_local,
		dl__shadowCollectorComponent_outputComponent_output__translucence__shad_local,
		dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__diffuse__shad__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__specular__unocc__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__specular__shad__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__translucence__unocc__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__translucence__shad__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__diffuse__surf_local,
		dl__shadowCollectorComponent_outputComponent_output__specular__surf_local,
		dl__shadowCollectorComponent_outputComponent_output__incandescence_local,
		dl__shadowCollectorComponent_outputComponent_output__ambient_local,
		dl__shadowCollectorComponent_outputComponent_output__indirect__unocc_local,
		dl__shadowCollectorComponent_outputComponent_output__indirect__shad_local,
		dl__shadowCollectorComponent_outputComponent_output__indirect__unocc__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__indirect__shad__sc_local,
		dl__shadowCollectorComponent_outputComponent_output__reflection__env_local,
		dl__shadowCollectorComponent_outputComponent_output__occlusion_local,
		dl__shadowCollectorComponent_outputComponent_output__bentnormal_local,
		dl__shadowCollectorComponent_outputComponent_output__reflection_local,
		dl__shadowCollectorComponent_outputComponent_output__reflection__depth_local,
		dl__shadowCollectorComponent_outputComponent_output__refraction_local,
		dl__shadowCollectorComponent_outputComponent_output__subsurface_local,
		dl__shadowCollectorComponent_outputComponent_output__collect__direct__shad_local,
		dl__shadowCollectorComponent_outputComponent_output__collect__indirect__shad_local,
		colorDummy, // receiving dl_shadowCollectorComponent.outColor
		colorDummy // receiving dl_shadowCollectorComponent.outTransparency
		);

	// Compute call string for dl_shadowCollector
	//
	float dl__shadowCollector_customFloat_local[] = {  };
	color dl__shadowCollector_customColor_local[] = {  };

	maya_rendermanCode_dl_shadowCollector(
		N, // normalCamera
		color(1, 0, 0), // puzzle1
		color(0, 1, 0), // puzzle2
		color(0, 0, 1), // puzzle3
		color(1, 1, 1), // globalOpacity
		1, // displacementGlobalScale
		0, // displacementGlobalOffset
		0, // displacementCompensateScale
		1, // premultAux
		0, // collapseComponents
		0, // collapseDisplacements
		color(1, 1, 1), // layers[0].layer_opacity
		0, // layers[0].layer_mode
		1, // layers[0].layer_premult
		dl__shadowCollectorComponent_outputComponent_output__beauty_local, // layers[0].layer_components[0].component_beauty
		dl__shadowCollectorComponent_outputComponent_output__light_local, // layers[0].layer_components[0].component_light
		dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc_local, // layers[0].layer_components[0].component_diffuse_unocc
		dl__shadowCollectorComponent_outputComponent_output__diffuse__shad_local, // layers[0].layer_components[0].component_diffuse_shad
		dl__shadowCollectorComponent_outputComponent_output__specular__unocc_local, // layers[0].layer_components[0].component_specular_unocc
		dl__shadowCollectorComponent_outputComponent_output__specular__shad_local, // layers[0].layer_components[0].component_specular_shad
		dl__shadowCollectorComponent_outputComponent_output__translucence__unocc_local, // layers[0].layer_components[0].component_translucence_unocc
		dl__shadowCollectorComponent_outputComponent_output__translucence__shad_local, // layers[0].layer_components[0].component_translucence_shad
		dl__shadowCollectorComponent_outputComponent_output__diffuse__unocc__sc_local, // layers[0].layer_components[0].component_diffuse_unocc_sc
		dl__shadowCollectorComponent_outputComponent_output__diffuse__shad__sc_local, // layers[0].layer_components[0].component_diffuse_shad_sc
		dl__shadowCollectorComponent_outputComponent_output__specular__unocc__sc_local, // layers[0].layer_components[0].component_specular_unocc_sc
		dl__shadowCollectorComponent_outputComponent_output__specular__shad__sc_local, // layers[0].layer_components[0].component_specular_shad_sc
		dl__shadowCollectorComponent_outputComponent_output__translucence__unocc__sc_local, // layers[0].layer_components[0].component_translucence_unocc_sc
		dl__shadowCollectorComponent_outputComponent_output__translucence__shad__sc_local, // layers[0].layer_components[0].component_translucence_shad_sc
		dl__shadowCollectorComponent_outputComponent_output__diffuse__surf_local, // layers[0].layer_components[0].component_diffuse_surf
		dl__shadowCollectorComponent_outputComponent_output__specular__surf_local, // layers[0].layer_components[0].component_specular_surf
		dl__shadowCollectorComponent_outputComponent_output__incandescence_local, // layers[0].layer_components[0].component_incandescence
		dl__shadowCollectorComponent_outputComponent_output__ambient_local, // layers[0].layer_components[0].component_ambient
		dl__shadowCollectorComponent_outputComponent_output__indirect__unocc_local, // layers[0].layer_components[0].component_indirect_unocc
		dl__shadowCollectorComponent_outputComponent_output__indirect__shad_local, // layers[0].layer_components[0].component_indirect_shad
		dl__shadowCollectorComponent_outputComponent_output__indirect__unocc__sc_local, // layers[0].layer_components[0].component_indirect_unocc_sc
		dl__shadowCollectorComponent_outputComponent_output__indirect__shad__sc_local, // layers[0].layer_components[0].component_indirect_shad_sc
		dl__shadowCollectorComponent_outputComponent_output__reflection__env_local, // layers[0].layer_components[0].component_reflection_env
		dl__shadowCollectorComponent_outputComponent_output__occlusion_local, // layers[0].layer_components[0].component_occlusion
		dl__shadowCollectorComponent_outputComponent_output__bentnormal_local, // layers[0].layer_components[0].component_bentnormal
		dl__shadowCollectorComponent_outputComponent_output__reflection_local, // layers[0].layer_components[0].component_reflection
		dl__shadowCollectorComponent_outputComponent_output__reflection__depth_local, // layers[0].layer_components[0].component_reflection_depth
		dl__shadowCollectorComponent_outputComponent_output__refraction_local, // layers[0].layer_components[0].component_refraction
		dl__shadowCollectorComponent_outputComponent_output__subsurface_local, // layers[0].layer_components[0].component_subsurface
		dl__shadowCollectorComponent_outputComponent_output__collect__direct__shad_local, // layers[0].layer_components[0].component_collect_direct_shad
		dl__shadowCollectorComponent_outputComponent_output__collect__indirect__shad_local, // layers[0].layer_components[0].component_collect_indirect_shad
		dl__shadowCollector_customFloat_local, // customFloat[]
		dl__shadowCollector_customColor_local, // customColor[]
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_beauty
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_light
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_diffuse_unocc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_diffuse_shad
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_specular_unocc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_specular_shad
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_translucence_unocc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_translucence_shad
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_diffuse_unocc_sc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_diffuse_shad_sc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_specular_unocc_sc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_specular_shad_sc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_translucence_unocc_sc
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_translucence_shad_sc
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_diffuse_surf
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_specular_surf
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_incandescence
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_ambient
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_indirect_unocc
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_indirect_shad
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_indirect_unocc_sc
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_indirect_shad_sc
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_reflection_env
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_occlusion
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_bentnormal
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_reflection
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_reflection_depth
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_refraction
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_subsurface
		colorsDummy, // receiving dl_shadowCollector.outputComponent.output_collect_direct_shad
		colorDummy, // receiving dl_shadowCollector.outputComponent.output_collect_indirect_shad
		dl__shadowCollector_outColor_local,
		dl__shadowCollector_outTransparency_local,
		floatDummy // receiving dl_shadowCollector.displacement
		);

	// Assign final output variables to state variables.
	//
	Oi = Os * (1.0 - dl__shadowCollector_outTransparency_local);
	Ci = dl__shadowCollector_outColor_local * Os;

	illuminance( "bakelight", P, "send:light:do_bake", 1 )
	{
	}
}
// Shader code generated by DL_translateMayaToSl.
// Total time: 0.35s.
// Time per node: 0.03888888889s.
