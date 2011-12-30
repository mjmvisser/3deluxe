import delight

class dl_fur(delight.DiffuseBase, delight.ShadingComponent):
    typeid = 0x00300014
    description = "Fur shader."
    includes = ["ray_utils.h", "env_utils.h"]
     
    basecolorTint = delight.Color(default=1, help="""
        Tint the color near the hair base (root).  Multiplies the incoming primvar 'basecolor'.  """)
    tipcolorTint = delight.Color(default=1, help="""
        Tint the color near the hair tip.  Multiplies the incoming primvar 'tipcolor'.  """)
    tipBias = delight.Float(default=0, min=-1, max=1, help=
        """<0 uses more basecolor, >0 use more tipcolor.  Use values between -1 and 1.""")
    specRoughness = delight.Float(default=.1, min=0, max=1, help="Same roughness used for spec1 and spec2.")
    spec1tint = delight.Color(default=.02, help="Tint first, simple spec hilight.")
    spec1shiftToRoot = delight.Float(default=1, help="How much to shift first spec hilight towards root")
    spec2tint = delight.Color(default=1, help="""
        Tint second spec hilight, reflected from inside hair and so multiplied by hair surface color.""")
    spec2shiftToTip = delight.Float(default=1, help="How much to shift first spec hilight towards root")
    diffTint = delight.Color(default=.5, help="Multiplies diffuse.")
    diffFalloff = delight.Float(default=.5, help="""
        If 1, regular normal-dependent falloff is used.
        If 0, normal has no effect, eg. even back-facing surfaces are fully illuminated""")
    indirectIntensity = delight.Color(help="Multiplies indirect diffuse.")

    #Reflection
#    indexOfRefraction = delight.Float(default=0, softmax=3, storage='uniform',
#                                      help="(Relative) index of refraction of material. The index of refraction from air to glass is 1.5. Air to water is 1.33. ")
#    falloff = delight.Enum(default='None',
#                           choices=['None', 'Linear', 'Quadratic'],
#                           help="How reflections from objects fall off with distance.")
#    falloffDistance = delight.Float(default=1, storage='uniform',
#                                    help="""The distance at which the reflected energy is actually
#                                            equal to intensity*reflcolor.  In other words, the intensity
#                                            is actually given by: I = (falloffdist / distance) ^ falloff""")
#    maxIntensity = delight.Float(default=1, storage='uniform',
#                                 help="""To prevent the reflection intensity from becoming unboundedly
#                                         large when the distance < falloffdist, it is
#                                         smoothly clamped to this maximum value.""");
#    
#    occIntensityMult = delight.Float(storage='uniform', default=1, softmin=0, softmax=2,
#                         help="Intensity multiplier for raytraced reflection occlusion.")
#    occSamplesMult = delight.Float(shortname='os', storage='uniform', default=1, softmin=0, softmax=2,
#                         help="Samples multiplier for raytraced reflection occlusion.")
#    occConeAngleMult = delight.Float(storage='uniform', default=1, softmin=0, softmax=2,
#                         help="Cone angle multiplier for raytraced reflection occlusion.")
#
#    reflectionOcclusion = delight.Group([occIntensityMult, occSamplesMult, occConeAngleMult], collapse=False)
#
#    ptcEnable = delight.Enum(default='Off',
#                           choices=['Off', 'In front of raytracing', 'Behind raytracing'],
#                           help="Where to insert pointcloud reflections, if at all.")
#    ptcFile = delight.File(default='', label='Point Cloud File', help="""The point cloud of objects to reflect.""")
#
#    ptcIntensity = delight.Float(default=1, help="""Intensity of pointcloud reflections.""")
#
#    ptcBlur = delight.Float(default=0, help="""
#        How much to blur the pointcloud reflections (clamped to >= .01 to avoid artifacts).""")
#
#    pointcloudReflection = delight.Group([ptcEnable, ptcFile, ptcIntensity, ptcBlur], collapse=False)
#
#    reflection = delight.Group([indexOfRefraction, falloff, falloffDistance, maxIntensity, reflectionOcclusion, pointcloudReflection])

    # Primvars.
    surfacenormal = delight.Normal(shortname="sn", default=-12345, message=True)
    basecolor = delight.Color(shortname="bc", default=1, message=True)
    tipcolor = delight.Color(shortname="tc", default=1, message=True)

    rsl = \
    """    
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

    """

def initializePlugin(obj):
    dl_fur.register(obj)

def uninitializePlugin(obj):
    dl_fur.deregister(obj)
