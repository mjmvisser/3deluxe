import deluxe

class dl_diffuse(deluxe.DiffuseBase, deluxe.ShadingComponent):
    typeid = 0x00300001
    description = "Returns the result of the diffuse shading operator."
    includes = ["env_utils.h"]
    
    roughness = deluxe.Float(default=0, min=0, max=1, help="Values greater than 0 cause the illuminated area to be more uniformly lit and darker, and create a sharper falloff between illuminated and non-illuminated areas.")
    wrap = deluxe.Float(default=0, min=-1, max=1, help='Allows diffuse illumination to "wrap around" to surfaces where the normal is pointing away from the light.')

    diffuseIntensity = deluxe.Color(help="Multiply direct diffuse - direct lighting multiplied by this AND the \"color\" parameter.")
    indirectIntensity = deluxe.Color(help="Multiply indirect diffuse - indirect lighting multiplied by this AND the \"color\" parameter.")
    
    #Direct = deluxe.Group([roughness, wrap], collapse=False)
    #Indirect = deluxe.Group([indirectIntensity], collapse=False)

    translucenceIntensity = deluxe.Color(help="Multiply translucence - translucence lighting multiplied by this AND the \"color\" parameter.", default=0)
    
    modes = ['Normal', 'Thin']
    mode = deluxe.Enum(default=modes[0], choices=modes, help="")
    
    focus = deluxe.Float(min=0, max=1, default=0.5, help="Translucence focus")
    
    normalAttributes = deluxe.Group([focus], collapse=False)
   
    subsurfaceWeight = deluxe.Float(shortname='ssw' )
    subsurfaceIntensity = deluxe.Color(shortname='ssi')
    subsurfaceScale = deluxe.Float(shortname='sssc', default=0.1)
    subsurfaceSmooth = deluxe.Float(shortname='sssm', default=0, storage='uniform', label="Smooth")
    subsurfaceIndexOfRefraction = deluxe.Float(shortname='ssior', default=1.5, label='Index Of Refraction')
    subsurfacePtcFile = deluxe.String(default='', label='Point Cloud File',
                                help="""(Point-Based) The point cloud file in which baked radiance is stored.""")
    subsurfaceModes = ['Scattering / Absortion', 'Albedo / Mean Free Path']
    subsurfaceMode = deluxe.Enum(default=subsurfaceModes[0], choices=subsurfaceModes, help="")
    subsurfaceScattering = deluxe.Color(shortname='ssc', default=[0.5, 0.5, 0.5], label='Scattering' )
    subsurfaceAbsorption = deluxe.Color(shortname='sssa', default=[0.05, 0.05, 0.05], label='Absorption' )
    subsurfaceAlbedo = deluxe.Color(shortname='ssa', default=[0.3,0.3, 0.3], label='Albedo' )
    subsurfaceDiffuseMeanFreePath = deluxe.Color(shortname='dmfp', default=[3, 3, 3], label='Mean Free Path' )
        
    #subsurfaceScatteringAttributes = deluxe.Group([subsurfaceWeight, subsurfaceIntensity, subsurfaceScale, subsurfaceSmooth, subsurfaceIndexOfRefraction, subsurfaceScattering, subsurfaceAbsorption, subsurfaceAlbedo, subsurfaceDiffuseMeanFreePath, subsurfacePtcFile], collapse=False)
    subsurfaceScatteringAttributes = deluxe.Group([subsurfaceWeight, subsurfaceIntensity, subsurfaceScale, subsurfaceSmooth, subsurfaceIndexOfRefraction, subsurfaceMode, subsurfaceScattering, subsurfaceAbsorption, subsurfaceAlbedo, subsurfaceDiffuseMeanFreePath, subsurfacePtcFile], collapse=False)
    
 
    creep = deluxe.Float(shortname='cre', help="Degree to which light creeps to the front")
    backIllumination = deluxe.Boolean(default=True,
                                       storage='uniform',
                                       help="Calculate illumination for the back side of the object. This is the typical use and is accomplished by reversing the surface normal.")
     
    thinAttributes = deluxe.Group([creep, backIllumination], collapse=False)
    translucenceAttributes = deluxe.Group([translucenceIntensity, mode, normalAttributes, thinAttributes], collapse=False)

        
    bakeDistUnderSurf = deluxe.Boolean(shortname='bdus', default=False)
    bakeDistUnderSurfFile = deluxe.String(shortname='bdusf', default="/tmp/dist.#.bake")
    bakeDistUnderSurfScale = deluxe.Float(shortname='bduss', default=1)
    
    bakingAttributes = deluxe.Group([bakeDistUnderSurf, bakeDistUnderSurfFile, bakeDistUnderSurfScale])
        
    
    rsl = \
    """    
    
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
    """

def initializePlugin(obj):
    dl_diffuse.register(obj)

def uninitializePlugin(obj):
    dl_diffuse.deregister(obj)
