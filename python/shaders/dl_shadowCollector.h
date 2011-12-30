#ifndef __dl_shadowCollector_h
#define __dl_shadowCollector_h

/*
begin inputs
	uniform float mute
	uniform float contribution
	float intensity
	color color
	uniform float shadeCurves
	color shadowColor
	float shadowOpacity
	float hemispheres
	float hemisphereFalloff
	varying float beautyMode
	float diffuseFalloff
	varying float useLightColor
	uniform float lightType
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
maya_dl_shadowCollector(
	// Inputs
	//
	uniform float i_mute;
	uniform float i_contribution;
	float i_intensity;
	color i_color;
	uniform float i_shadeCurves;
	color i_shadowColor;
	float i_shadowOpacity;
	float i_hemispheres;
	float i_hemisphereFalloff;
	varying float i_beautyMode;
	float i_diffuseFalloff;
	varying float i_useLightColor;
	uniform float i_lightType;
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

    
    o_output_beauty = 0;
    
    color o_opacity = 0;
    
    color indirectShad = 0;
    color directShad = 0;

    // 
    Nf = Nn;

    // Indirect
    color indirectCol = 1;
    color occlusionColor = 0;
    if (useIndirect > 0) {
        color indOccluded = 0;
        illuminance("indirect", P,// Nf, PI/2,
                    "lightcache", "reuse") {
            // Each surface should not be illuminated by more than one
            // indirect light, so no need to sum these.
            lightsource("__occluded", indOccluded);
            lightsource("__occlusionColor", occlusionColor);
            indirectCol = Cl;
        }
        indirectShad = indOccluded * i_intensity;
        if (i_useLightColor == 0 || i_useLightColor == 2) indirectShad *= indirectCol * (1-occlusionColor);
    }

    // Direct 

    float hemisphereFalloff = 0;
    if (useDirect) {
        float nLights = 0;
        BEGIN_LIGHTSET_LOOP(o_output_diffuse_unocc)

        color dirOccluded = 0;
        string category = format("diffuse&-indirect%s", LIGHTSET_CATEGORY);
        illuminance(category, P, Nf, i_hemispheres*PI/2,
                    "lightcache", "reuse") {
            lightsource("__occluded", dirOccluded);
            lightsource("__occlusionColor", occlusionColor);
            float NdotL= normalize(L).Nf;
            float ang = acos(NdotL);
            ang = ang/PI;
            float falloff = 1-smoothstep(i_hemispheres-i_hemisphereFalloff, i_hemispheres, 2*ang);

            color thisDirectShad = falloff*dirOccluded * i_intensity * (1-occlusionColor);
            if (i_useLightColor == 0 || i_useLightColor == 1) {
                color unoccludedCl = Cl;
                lightsource("__unoccludedCl", unoccludedCl);
                thisDirectShad *= unoccludedCl;
            }
            thisDirectShad *= mix(1, max(0, NdotL), i_diffuseFalloff);
            o_output_collect_direct_shad[LIGHTSET_INDEX] += thisDirectShad;
            directShad += thisDirectShad;
            // This allows us to visualize the i_hemispheres of multiple lights.
            //hemisphereFalloff = mix(hemisphereFalloff, 1, falloff*.5);
            hemisphereFalloff += falloff;

        }

        shader directLights[] = getlights("category", category); 
        nLights += arraylength(directLights);
        END_LIGHTSET_LOOP
        hemisphereFalloff/= nLights;
    }
    

    // Add directShad and indirectShad because they are subtracted in dl_ultra.
    color bty;
    if (i_beautyMode == 4 ) {
        // If i_beautyMode == 4, rgb = 0, alpha = Direct + Indirect:  shadows are in alpha.
        bty = directShad + indirectShad + i_shadowColor;
        o_opacity = (directShad + indirectShad) * i_shadowOpacity;
    } else {
        bty = 
        (i_beautyMode == 0 ?
            (luminance(directShad), luminance(indirectShad), hemisphereFalloff):
        i_beautyMode == 1 ? directShad + indirectShad :
        i_beautyMode == 2 ? directShad : indirectShad
        ) * (i_shadowOpacity, i_shadowOpacity, 1);
        o_opacity = 1;
    }
    //bty = directShad;

    bty *= i_contribution;
    
    o_output_beauty = bty;
    //o_output_collect_direct_shad = directShad * i_contribution;
    o_output_collect_indirect_shad = indirectShad * i_contribution;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_shadowCollector_h */
