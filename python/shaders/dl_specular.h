#ifndef __dl_specular_h
#define __dl_specular_h

/*
begin inputs
	uniform float model
	float roughness
	float sharpness
	float indexOfRefraction
	float uRoughness
	float vRoughness
	uniform float useEnvironment
	normal normalCamera
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
#include "env_utils.h"

void
maya_dl_specular(
	// Inputs
	//
	uniform float i_model;
	float i_roughness;
	float i_sharpness;
	float i_indexOfRefraction;
	float i_uRoughness;
	float i_vRoughness;
	uniform float i_useEnvironment;
	normal i_normalCamera;
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

    uniform string envFilter;
    if (i_mapFilter == 0)
        envFilter = "gaussian";
    else if (i_mapFilter == 1)
        envFilter = "triangle";
    else
        envFilter = "box";
    
    color envColor = 0;

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
    

    
    if(isBakingRadiosity() > 0)
        return;
    
    extern vector dPdu;
    extern vector dPdv;
        
    vector uVec = normalize(dPdu);
    vector vVec = normalize(dPdv);

    o_output_beauty = 0;

    // pre-compute some values for the A/S model
    float Nu=0, Nv=0, nunvScale=0;
    if (i_model == 5) {
        // convert the user-friendly roughness parameters
        // into the terms defined by A/S:
        Nu = 10 * pow(10,3*(1-i_uRoughness));
        Nv = 10 * pow(10,3*(1-i_vRoughness));
        
        // this is not light-dependent so we can calculate
        // outside the illuminance loop
        nunvScale = sqrt((Nu+1)*(Nv+1)) / (8*PI);
    }

    // pre-compute some values for the Kajiya model
    float cosbeta=0, beta=0, sinbeta=0;
    if (i_model == 6) {
        cosbeta = vVec.V;
        beta = acos(cosbeta);
        sinbeta = sin(beta);
    }

    // pre-compute coefficient for fresnel
    float Kr = 1;
    if (i_indexOfRefraction > 0) {
        float eta = (V.Nn >= 0) ? (1/i_indexOfRefraction) : i_indexOfRefraction;
        float Kt;
        fresnel(V, Nn, eta, Kr, Kt);
    }

    BEGIN_LIGHTSET_LOOP(o_output_specular_unocc);
    
        color col = 0;
        color unoccludedCol = 0;
        if (globalIntensity <= 0)
            continue;
        
        // Get indirectOcclusion.
        color indirectOcclusion = 0;
        illuminance("indirect", P, Nf, PI/2,
                    "lightcache", "reuse") {
            lightsource("__occluded", indirectOcclusion);
        }

        string category = format("-environment&-indirect&-bakelight%s", LIGHTSET_CATEGORY);
		illuminance(category, P, Nf, PI/2,
		            "lightcache", "reuse") {
		    float nonspec = 0;
		    lightsource("__nonspecular", nonspec);
		    if (nonspec < 1) {
		        vector Ln = normalize(L);
                color attenClr;
		        
		        if (i_model == 0) {
                    // default 3Delight
        			attenClr = (1-nonspec) * Kr * specularbrdf(Ln, Nf, V, i_roughness);
    			}
    			else if (i_model == 1) {
    			    // Standard
    			    vector Hn = normalize(Ln+V);
    			    attenClr = (1-nonspec) * Kr * pow(max(0, Nf.Hn), 1/i_roughness);
    			}
    			else if (i_model == 2) {
    			    // Phongtastic
                    vector R = reflect(In, Nf);
    			    attenClr = (1-nonspec) * Kr * pow(max(0, R.V), 1/i_roughness);
    			}
    			else if (i_model == 3) {
    			    // Cook-Torrance
                    vector Hn = normalize(Ln+V);
                    float t = Hn.Nn;
                    float t2 = t*t;
                    float v = V.Nn;
                    float vp = Ln.Nn;
                    float u = Hn.V;
                    float m2 = i_roughness*i_roughness;
                    
                    float D = 0.5/(m2*t2*t2) * exp((t2-1)/(m2*t2));
                    float G = min(1, 2*min(t*v/u, t*vp/u));

                    attenClr = (1-nonspec) * (Kr * D * G / (vp*v)) * Nn.Ln;
    			}
    			else if (i_model == 4) {
    			    // Glossy from Larry Gritz's locillum.h
    			    float w = .18 * (1-i_sharpness);
                    vector Hn = normalize(Ln+V);
                    attenClr = (1-nonspec) * Kr * smoothstep(.72-w, .72+w,
                                                              pow(max(0,Nn.Hn), 1/i_roughness));
    			}
    			else if (i_model == 5) {
                    // Ashikhmin / Shirley anisotropic phong light reflection model
                    vector Hn = normalize(Ln+V);
                
                    float t = Hn.Nf;
                    float hu = Hn.uVec;
                    float hv = Hn.vVec;
                
                    float exp, strength;
                    exp = (Nu*hu*hu + Nv*hv*hv) / (1 - t*t);
                    strength = pow(t, exp);
                
                    float spec = nunvScale * strength;
                
                    attenClr = (1-nonspec) * Kr * spec;
                    
    			}
    			else if (i_model == 6) {
    			    // Kajiya/Kay for thin curves
                    float cosalpha = vVec.Ln;
                    float alpha = acos(cosalpha);
                    float sinalpha = sin(alpha);
                    float kajiya = cosalpha * cosbeta + 
                                   sinalpha * sinbeta;
                    attenClr = (1-nonspec) * Kr * pow(kajiya, 1/i_roughness); 
    			}

                attenClr = max(0, attenClr);
                color unoccludedCl = Cl;
                lightsource("__unoccludedCl", unoccludedCl);
                unoccludedCol += unoccludedCl * attenClr;
                float useAmbientOcclusion = 0;
                lightsource("__useAmbientOcclusion", useAmbientOcclusion);
                col += mix(Cl, mix(Cl, color 0, indirectOcclusion), useAmbientOcclusion) * attenClr;
    		}
        }

        //
        if (i_useEnvironment == 1 && i_mapContribution > 0) {
            // color the highlight with the environment reflection
            color envColor = 0;
            vector R = reflect(In, Nf);
            getEnvironmentReflection(P, Nf, R, i_mapBlur, i_mapBlurS, i_mapBlurT, envFilter, i_physicalSkySamples, envColor);
            surfaceColor = mix(i_color, envColor, i_mapContribution);
            surfaceColor *= Cs;
        }
        
        col *= globalIntensity;
        unoccludedCol *= globalIntensity;
        
        //
        o_output_specular_unocc[LIGHTSET_INDEX] = unoccludedCol;
        o_output_specular_shad[LIGHTSET_INDEX] = unoccludedCol - col;
        o_output_specular_unocc_sc[LIGHTSET_INDEX] = o_output_specular_unocc[LIGHTSET_INDEX] * surfaceColor;
        o_output_specular_shad_sc[LIGHTSET_INDEX] = o_output_specular_shad[LIGHTSET_INDEX] * surfaceColor;
        o_output_light[LIGHTSET_INDEX] += o_output_specular_unocc[LIGHTSET_INDEX] * surfaceColor;
        o_output_light[LIGHTSET_INDEX] -= o_output_specular_shad[LIGHTSET_INDEX] * surfaceColor;
        o_output_beauty += o_output_specular_unocc[LIGHTSET_INDEX] * surfaceColor;
        o_output_beauty -= o_output_specular_shad[LIGHTSET_INDEX] * surfaceColor;
        
    END_LIGHTSET_LOOP
    
    o_output_specular_surf = surfaceColor;

    #endif // SHADER_TYPE_light
}

#endif /* __dl_specular_h */
