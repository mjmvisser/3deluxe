#ifndef __dl_fur_h
#define __dl_fur_h

/*
begin inputs
	color basecolorTint
	color tipcolorTint
	float tipBias
	float specRoughness
	color spec1tint
	float spec1shiftToRoot
	color spec2tint
	float spec2shiftToTip
	color diffTint
	float diffFalloff
	color indirectIntensity
	uniform float lightType
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

begin shader_extra_parameters surfacenormal
	normal surfacenormal = normal (-12345, -12345, -12345);
	color basecolor = color (1, 1, 1);
	color tipcolor = color (1, 1, 1);
end shader_extra_parameters

*/

#include "utils.h"
#include "component_utils.h"
#include "ray_utils.h"
#include "env_utils.h"

void
maya_dl_fur(
	// Inputs
	//
	color i_basecolorTint;
	color i_tipcolorTint;
	float i_tipBias;
	float i_specRoughness;
	color i_spec1tint;
	float i_spec1shiftToRoot;
	color i_spec2tint;
	float i_spec2shiftToTip;
	color i_diffTint;
	float i_diffFalloff;
	color i_indirectIntensity;
	uniform float i_lightType;
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
    

    uniform string baseCategory = "";
    if (i_lightType == 0)
        baseCategory = "diffuse&-indirect";
    else if (i_lightType == 1)
        baseCategory = "indirect";
    else if (i_lightType == 2)
        baseCategory = "diffuse";
            
    float useDirect = 0;
    if (i_lightType == 0 || i_lightType == 2)
        useDirect = 1;
        
    float useIndirect = 0;
    if (i_lightType == 1 || i_lightType == 2)
        useIndirect = 1;
    
float luminance(color c) {
    return (c[0] + c[1] + c[2])/3;
}

float getSpecMultiplier (vector Ln; normal Nn; vector Vn; float roughness) {
    vector H = normalize(Ln+Vn);
    return pow(max(0.0, Nn.H), 1/roughness);
}
    extern float v;
    extern vector dPdv;

    // Primvars.
    extern color basecolor;
    extern color tipcolor;
    extern normal surfacenormal;

    float debug = 0;
    color baseclrToUse = (1, 0, 0);
    color tipclrToUse = (0, 1, 0);
    color spec1tintToUse = (0, 0, 1);
    if (debug < 1) {
        baseclrToUse = basecolor * i_basecolorTint;
        tipclrToUse = tipcolor * i_tipcolorTint;
        spec1tintToUse = i_spec1tint;
    }

    vector w1 = vector "world" (1, 0, 0);
    float unitLen = length(vector "world" (1, 0, 0));
    vector lenDir = normalize(dPdv) * unitLen;
    
    if (surfacenormal != -12345) Nn = normalize(surfacenormal);

    // Indirect
    color indirectCol = 0;
    color occluded = 0;
    color occlusionColor = 0;
    color bentnormal = 0;
    if (useIndirect > 0) {
        illuminance("indirect", P, Nn, PI/2,
                    "lightcache", "reuse") {
            // Each surface should not be illuminated by more than one
            // indirect light, so no need to sum these.
            lightsource("__occluded", occluded);
            lightsource("__occlusionColor", occlusionColor);
            lightsource("__bentnormal", bentnormal);
            indirectCol = Cl;
        }
        indirectCol *= i_indirectIntensity * globalIntensity;
    }

    color mixBias(color a, b; float bias, v) {
        float aWt, bWt;
        float biasRemap = (bias + 1)/2;
        if (biasRemap <= 0) {
            aWt = 1;
            bWt = 0;
        } else if (biasRemap >= 1) {
            aWt = 0;
            bWt = 1;
        } else {
            aWt = (1-v)*.5/biasRemap;
            bWt = v*.5/(1-biasRemap);
        }
        return (a * aWt + b * bWt)/(aWt + bWt);
    }

    //color diffClr = mix(baseclrToUse, tipclrToUse, v);
    color diffClr = mixBias(baseclrToUse, tipclrToUse, i_tipBias, v);

    // surfaceColor is already set to i_color * Cs.  We don't want to use Cs.
    surfaceColor = i_color*diffClr;


    o_output_beauty = 0;

    BEGIN_LIGHTSET_LOOP(o_output_diffuse_unocc)

    color diff = 0;
    color unoccludedDiff = 0;
    color spec = 0;
    color unoccludedSpec = 0;
    //string category = format("diffuse&-indirect%s", LIGHTSET_CATEGORY);
    string category = "diffuse&-indirect";
    illuminance(category, P, // Search whole sphere for translucence.
                    "lightcache", "reuse") {
        extern point E;
        vector Ln = normalize(L);
        // First spec component from the surface.
        // The shaded point should be shifted along lengthDir toward root due to
        // serrated surface.  This moves spec toward root.

        point Pspec1 = P + i_spec1shiftToRoot * lenDir;
        vector Vspec1 = normalize(E - Pspec1);
        color spec1 = getSpecMultiplier (Ln, Nn, Vspec1, i_specRoughness );

        // Second spec component is reflected from the opposite, inner side of the hair.
        // The shaded point should be shifted along lengthDir toward tip due to
        // serrated surface.  This moves spec toward root.
        point Pspec2 = P - i_spec2shiftToTip * lenDir;

        // The shaded point should also be shifted along the surface toward the light because
        // that is where the ray would have entered the hair in order to come out at P.
        vector Vspec2 = normalize(E - Pspec2);
        color spec2 = specularbrdf (Ln, Nn, Vspec2, i_specRoughness );

        color diffMult = mix(1, max(0, Ln.Nn), i_diffFalloff) * i_diffTint;
        color specMult = (spec1tintToUse * spec1 + (i_spec2tint * spec2) * surfaceColor);

        color unoccludedCl = Cl;
        lightsource("__unoccludedCl", unoccludedCl);

        unoccludedDiff += unoccludedCl * diffMult * globalIntensity;
        diff += diffMult * Cl * globalIntensity;

        unoccludedSpec += unoccludedCl * specMult * globalIntensity;
        spec += specMult * Cl * globalIntensity;
    }

    o_output_diffuse_unocc[LIGHTSET_INDEX] = unoccludedDiff;
    o_output_diffuse_shad[LIGHTSET_INDEX] = unoccludedDiff - diff;
    o_output_diffuse_unocc_sc[LIGHTSET_INDEX] = o_output_diffuse_unocc[LIGHTSET_INDEX]  * surfaceColor;
    o_output_diffuse_shad_sc[LIGHTSET_INDEX] = o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] += o_output_diffuse_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] -= o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;
    o_output_beauty += o_output_diffuse_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_beauty -= o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;

    o_output_specular_unocc[LIGHTSET_INDEX] = unoccludedSpec;
    o_output_specular_shad[LIGHTSET_INDEX] = unoccludedSpec - spec;
    o_output_specular_unocc_sc[LIGHTSET_INDEX] = o_output_specular_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_specular_shad_sc[LIGHTSET_INDEX] = o_output_specular_shad[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] += o_output_specular_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] -= o_output_specular_shad[LIGHTSET_INDEX] * surfaceColor;    
    o_output_beauty += o_output_specular_unocc[LIGHTSET_INDEX];
    o_output_beauty -= o_output_specular_shad[LIGHTSET_INDEX];

    END_LIGHTSET_LOOP

    o_output_diffuse_surf = surfaceColor;

    // Spec1 and spec2 have different "surface" colours, so we just incoporate them into
    // specular_unocc and specular_shad (in the illuminance loop) and set specular_surf to 1.
    o_output_specular_surf = 1;

    o_output_indirect_unocc = indirectCol;
    o_output_indirect_shad = indirectCol - mix(indirectCol, occlusionColor, occluded);
    o_output_indirect_unocc_sc = o_output_indirect_unocc  * surfaceColor;
    o_output_indirect_shad_sc = o_output_indirect_shad * surfaceColor;    
    o_output_beauty += (o_output_indirect_unocc - o_output_indirect_shad)
                        * o_output_diffuse_surf * surfaceColor;
    // TODO: ADD o_output_bentnormal


    #endif // SHADER_TYPE_light
}

#endif /* __dl_fur_h */
