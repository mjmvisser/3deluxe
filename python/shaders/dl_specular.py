import deluxe

class dl_specular(deluxe.ShadingComponent, deluxe.EnvironmentMapBase):
    typeid = 0x00300002
    description = "The specular component simulates the reflection of light sources. Samples all incoming lights along the specular direction of the surface."
    includes = ["env_utils.h"]
    
    model = deluxe.Enum(default='3Delight',
                         choices=['3Delight', 'Standard', 'Phong', 'Cook-Torrance', 'Glossy', 'Anisotropic', 'Kajiya'],
                         storage='uniform',
                         help="""Specular model to use. 3Delight, Standard and Phong all model traditional specularity. 
                                 Cook-Torrance is for metallic surfaces, Glossy is for highly glossy surfaces, and
                                 Kajiya assumes the surface is a hair-like thin tube.""")
    roughness = deluxe.Float(min=0, softmax=0.2, default=0.05, 
                              help="Size or roughness of highlight")
    sharpness = deluxe.Float(min=0, softmax=1, default=0.2,
                              help="(Glossy) Sharpness of highlight. 1 is infinitely sharp, 0 is very dull.")
    indexOfRefraction = deluxe.Float(default=0, min=0, softmax=50,
                                      help="Index of refraction of the material")
    uRoughness = deluxe.Float(min=0, softmax=1, default=0.2, help="(Anisotropic) Size of highlight in the U direction ")
    vRoughness = deluxe.Float(min=0, softmax=1, default=0.9, help="(Anisotropic) Size of highlight in the V direction ")
    useEnvironment = deluxe.Boolean(default=False,
                             help="Whether to respond to traditional CG lights only or also include lighting from the environment. ")

    rsl = \
    """
    
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
    """


def initializePlugin(obj):
    dl_specular.register(obj)

def uninitializePlugin(obj):
    dl_specular.deregister(obj)
