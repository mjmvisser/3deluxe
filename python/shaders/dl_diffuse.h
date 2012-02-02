#ifndef __dl_diffuse_h
#define __dl_diffuse_h

/*
begin inputs
	float roughness
	float wrap
	color diffuseIntensity
	color indirectIntensity
	uniform float lightType
	normal normalCamera
	float subsurfaceWeight
	color subsurfaceIntensity
	float subsurfaceScale
	uniform float subsurfaceSmooth
	float subsurfaceIndexOfRefraction
	uniform float subsurfaceMode
	color subsurfaceScattering
	color subsurfaceAbsorption
	color subsurfaceAlbedo
	color subsurfaceDiffuseMeanFreePath
	uniform string subsurfacePtcFile
	color translucenceIntensity
	uniform float mode
	float focus
	float creep
	uniform float backIllumination
	uniform float bakeDistUnderSurf
	uniform string bakeDistUnderSurfFile
	float bakeDistUnderSurfScale
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
#include "env_utils.h"

void
maya_dl_diffuse(
	// Inputs
	//
	float i_roughness;
	float i_wrap;
	color i_diffuseIntensity;
	color i_indirectIntensity;
	uniform float i_lightType;
	normal i_normalCamera;
	float i_subsurfaceWeight;
	color i_subsurfaceIntensity;
	float i_subsurfaceScale;
	uniform float i_subsurfaceSmooth;
	float i_subsurfaceIndexOfRefraction;
	uniform float i_subsurfaceMode;
	color i_subsurfaceScattering;
	color i_subsurfaceAbsorption;
	color i_subsurfaceAlbedo;
	color i_subsurfaceDiffuseMeanFreePath;
	uniform string i_subsurfacePtcFile;
	color i_translucenceIntensity;
	uniform float i_mode;
	float i_focus;
	float i_creep;
	uniform float i_backIllumination;
	uniform float i_bakeDistUnderSurf;
	uniform string i_bakeDistUnderSurfFile;
	float i_bakeDistUnderSurfScale;
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
    
    
    o_output_beauty = 0;
    
  float bake = isBakingRadiosity();
    float diffuseWeight = mix(1-i_subsurfaceWeight, 1, bake);

    // Indirect
    color indirectCol = 0;
    color occluded = 0;
    color occlusionColor = 0;
    color bentnormal = 0;
    if (useIndirect > 0) {
        illuminance("indirect", P, Nf, PI/2,
                    "lightcache", "reuse") {
            // Each surface should not be illuminated by more than one
            // indirect light, so no need to sum these.
            lightsource("__occluded", occluded);
            lightsource("__occlusionColor", occlusionColor);
            lightsource("__bentnormal", bentnormal);
            indirectCol = Cl;
        }
        indirectCol *= i_indirectIntensity * globalIntensity * diffuseWeight;
    }
    
    // subsurface
    //
    string ptcFiles[];
    if(bake < 1 && i_subsurfaceWeight > 0 && 
        getPointCloudFiles("Subsurface", i_subsurfacePtcFile, ptcFiles) > 0){
        if(i_subsurfaceMode == 0){
            o_output_subsurface = subsurface(  P, Nn,
                                  "filenames", ptcFiles,
                                  "smooth", i_subsurfaceSmooth, 
                                  "scattering", i_subsurfaceScattering + color(0.001), 
                                  "absorption", i_subsurfaceAbsorption + color(0.001), 
                                  "scale", i_subsurfaceScale, 
                                  "ior", i_subsurfaceIndexOfRefraction );
        }
        else{
            o_output_subsurface = subsurface(  P, Nn,
                                  "filenames", ptcFiles,
                                  "smooth", i_subsurfaceSmooth, 
                                  "diffusemeanfreepath", i_subsurfaceDiffuseMeanFreePath + color(0.001), 
                                  "albedo", i_subsurfaceAlbedo + color(0.001),
                                  "scale", i_subsurfaceScale, 
                                  "ior", i_subsurfaceIndexOfRefraction );
        }
        o_output_subsurface *= i_subsurfaceIntensity * i_subsurfaceWeight;
    }
    
    
    // Oren Nayar constants
    float sigma2, A, B, theta_r;
    vector V_perp_N;
    if (i_roughness > 0) {
        sigma2 = i_roughness*i_roughness;
        A = 1 - 0.5 * sigma2 / (sigma2+0.33);
        B = 0.45 * sigma2 / (sigma2 + 0.09);
        theta_r = acos(V.Nn);
        V_perp_N = normalize(V - Nf * (V.Nf));
    }

    
    // 
    BEGIN_LIGHTSET_LOOP(o_output_diffuse_unocc)
    
    // Direct 
    color diff = 0;
    color unoccludedDiff = 0;
    color tran = 0;
    color unoccludedTran = 0;

    // translucence of 1 causes a division by zero
    float focus = min(i_focus, 0.99999);
    
    normal Nback = Nf;
    if (i_backIllumination > 0)
    {
        Nback = -Nback;
    }

    if (useDirect) {
    
        string category = format("diffuse&-indirect%s", LIGHTSET_CATEGORY);
        illuminance(category, P, // Search whole sphere for translucence.
                    "lightcache", "reuse") {
            float nondiff = 0;
            lightsource("__nondiffuse", nondiff);

            // Diffuse.
            if (nondiff < 1) {
                vector Ln = normalize(L);
                float atten;
                if (i_roughness > 0) {
                    float cos_theta_i = max(0, (Ln.Nf + i_wrap)/(1 + i_wrap));
                    float cos_phi_diff = V_perp_N . normalize(Ln - Nf*cos_theta_i);
                    float theta_i = acos(cos_theta_i);
                    float alpha = max(theta_i, theta_r);
                    float beta = min(theta_i, theta_r);
                    atten = (1-nondiff) * cos_theta_i * (A + B * max(0, cos_phi_diff) * sin(alpha) * tan(beta));
                }
                else {
                    // Lambertian diffuse
                    atten = (1-nondiff) * max(0, (Ln.Nf + i_wrap)/(1 + i_wrap));
                }
                color unoccludedCl = Cl;
                lightsource("__unoccludedCl", unoccludedCl);
                unoccludedDiff += unoccludedCl * atten;
                float useAmbientOcclusion = 0;
                lightsource("__useAmbientOcclusion", useAmbientOcclusion);
                diff += mix(Cl, mix(Cl, color 0, occluded), useAmbientOcclusion) * atten;
            }

            // Translucence.
    	    float ktrans = 1;
    	    lightsource("__contribTranslucence", ktrans);
    
            if (ktrans > 0 && nondiff < 1) {
            
                float atten;
            
                if (i_mode == 0){
                    vector Ln = normalize(L);
                    float costheta = Ln.In;
                    float a = (1 + costheta) * 0.5;
                    float trs = pow(pow(a, focus), 1/(1-focus));
                    atten = ktrans * (1-nondiff) * trs;
                }
                else{
                    float ndl = normalize(L).Nback;
                    float thin = (ndl + i_creep) / (1 + i_creep);
                    atten = ktrans * (1-nondiff) * max(thin, 0);
                }
                
                tran += Cl * atten;
                
                color unoccludedCl = Cl;
                lightsource("__unoccludedCl", unoccludedCl);
                unoccludedTran += unoccludedCl * atten;
    	    }
        }
        
        diff *= i_diffuseIntensity * globalIntensity * diffuseWeight;
        unoccludedDiff *= i_diffuseIntensity * globalIntensity * diffuseWeight;
        
        tran *= i_translucenceIntensity * globalIntensity;
        unoccludedTran *= i_translucenceIntensity * globalIntensity;
    }
    
    
    // 
    o_output_diffuse_unocc[LIGHTSET_INDEX] = unoccludedDiff;
    o_output_diffuse_shad[LIGHTSET_INDEX] = unoccludedDiff - diff;
    o_output_diffuse_unocc_sc[LIGHTSET_INDEX] = o_output_diffuse_unocc[LIGHTSET_INDEX]  * surfaceColor;
    o_output_diffuse_shad_sc[LIGHTSET_INDEX] = o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;
    
    o_output_light[LIGHTSET_INDEX] +=  o_output_diffuse_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] -=  o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;
    
    o_output_beauty += o_output_diffuse_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_beauty -= o_output_diffuse_shad[LIGHTSET_INDEX] * surfaceColor;

    o_output_translucence_unocc[LIGHTSET_INDEX] = unoccludedTran;
    o_output_translucence_shad[LIGHTSET_INDEX] = unoccludedTran - tran;
    o_output_translucence_unocc_sc[LIGHTSET_INDEX] = o_output_translucence_unocc[LIGHTSET_INDEX]  * surfaceColor;
    o_output_translucence_shad_sc[LIGHTSET_INDEX] = o_output_translucence_shad[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] +=  o_output_translucence_unocc[LIGHTSET_INDEX] * surfaceColor;
    o_output_light[LIGHTSET_INDEX] -=  o_output_translucence_shad[LIGHTSET_INDEX] * surfaceColor;        
        
    o_output_beauty += o_output_translucence_unocc_sc[LIGHTSET_INDEX] ;
    o_output_beauty -= o_output_translucence_shad_sc[LIGHTSET_INDEX];
    
    
    o_output_beauty += o_output_subsurface;
    
    END_LIGHTSET_LOOP
    
    //
    o_output_indirect_unocc = indirectCol;
    o_output_indirect_shad = indirectCol - mix(indirectCol, occlusionColor, occluded);
    o_output_indirect_unocc_sc = o_output_indirect_unocc  * surfaceColor;
    o_output_indirect_shad_sc = o_output_indirect_shad * surfaceColor;
    o_output_occlusion = luminance(occluded);        
    o_output_bentnormal = bentnormal;
    
    //
    o_output_beauty += o_output_indirect_unocc * surfaceColor;
    o_output_beauty -= o_output_indirect_shad * surfaceColor;
    
    o_output_diffuse_surf = surfaceColor;
    
    if (i_bakeDistUnderSurf == 1) {
        extern float s;
        extern float t;
        extern normal N;
        float dist = trace(P, -N);
        if (dist > 1000000) dist = 0;
        bake(i_bakeDistUnderSurfFile, s, t, dist*i_bakeDistUnderSurfScale);
    }

    #endif // SHADER_TYPE_light
}

#endif /* __dl_diffuse_h */
