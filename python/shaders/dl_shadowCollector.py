import delight

class dl_shadowCollector(delight.DiffuseBase, delight.ShadingComponent):
    typeid = 0x00300012
    description = """Shading component for collecting shadows from lights.
        Direct shadows (affecting diff, spec and rim) go in aov_direct_shadow,
        whereas indirect shadows (affecting indirect lighting) go in aov_indirect_shadow.
        The beauty pass is not meant to be used, it's just for visualization."""
    
    beautyModes = [ 'r=Direct, g=Indirect, b=Hemisphere Falloff',
                    'Direct + Indirect (white)',
                    'Direct (white)', 'Indirect (white)',
                    'For slapcomp: rgb = shadowColor * shadowOpacity, (alpha = Direct + Indirect)*shadowOpacity']
    
    beautyMode = delight.Enum(default=beautyModes[0], choices=beautyModes, storage='varying',
                              help="What to show in the beauty. ")
    
    diffuseFalloff = delight.Float(shortname='dfo', default=1,
        help="Make shadows fade as normal points away from light.")

    useLightColor = delight.Enum(shortname='ulc', default="Direct & Indirect", storage='varying',
        choices=["Direct & Indirect", "Direct", "Indirect", "None"])

    shadowColor = delight.Color(shortname='shc',default=0, help="""
        Color of shadow, ONLY USED WHEN showInBty == 'rgb = shadowColor * shadowOpacity, alpha = (Direct + Indirect)*shadowOpacity'
        """)
    
    shadowOpacity = delight.Float(shortname='sho', default=1, help="Opacity/intensity of shadows.")
    
    hemispheres = delight.Float(default=.9, max=2,
                help="""How much of the hemisphere around the normal to search for direct shadows.
                    To include self-shadowing, use 2 (search whole sphere).
                    To not include self-shadowing, use < 1 (search less than hemisphere).""")
    
    hemisphereFalloff = delight.Float(default=0.05, max=1, help="How far from the searched hemisphere to fade direct shadows.")

    advanced = delight.Group([shadowColor, shadowOpacity, hemispheres, hemisphereFalloff])


    rsl = \
    """
    
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
    """


def initializePlugin(obj):
    dl_shadowCollector.register(obj)

def uninitializePlugin(obj):
    dl_shadowCollector.deregister(obj)
