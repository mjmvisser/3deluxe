import delight

class dl_fresnel(delight.ShadingComponent):
    typeid = 0x00300004
    description = "Weights an interior and an exterior shadingcomponent based upon a fresnel calculation "
    
    indexOfRefraction = delight.Float(default=1.5, softmax=3, storage='uniform',
                                      help="(Relative) index of refraction of material to use for weighting the two components. The index of refraction from air to glass is 1.5. Air to water is 1.33.")
    amount = delight.Float(default=1, storage='uniform', help="Amount of fresnel weighting")
    interior = delight.ShadingComponent.generateComponents('int')
    exterior = delight.ShadingComponent.generateComponents('ext')

    rsl = \
"""
#ifndef SHADER_TYPE_light
    extern vector I;
    
    vector In = normalize(I);
    normal Nn = normalize(i_normalCamera);
    normal Nf = ShadingNormal(Nn);
    vector V = -In;

    // calculate weights
    float k_int, k_ext;
    float eta = (V.Nf >= 0) ? (1/i_indexOfRefraction) : i_indexOfRefraction;
    fresnel(-V, Nf, eta, k_ext, k_int);
    k_int = k_int * i_amount + (1-i_amount);
    k_ext = k_ext * i_amount + (1-i_amount);
    o_dlOutColor = k_int * intColor + k_ext * extColor;
    o_dlOutTransparency = k_int * intTransparency + k_ext * extTransparency; 
    o_dlOutSurfaceColor = k_int * i_intSurfaceColor + k_ext * i_extSurfaceColor;
    o_dlOutIncandescence = k_int * i_intIncandescence + k_ext * i_extIncandescence;
    o_dlOutAmbient = k_int * i_intAmbient + k_ext * i_extAmbient;
    o_dlOutIndirect = k_int * i_intIndirect + k_ext * i_extIndirect;
    o_dlOutDiffuse = k_int * i_intDiffuse + k_ext * i_extDiffuse;
    o_dlOutThinTranslucence = k_int * i_intThinTranslucence + k_ext * i_extThinTranslucence;
    o_dlOutSubsurfaceScattering = k_int * i_intSubsurfaceScattering + k_ext * i_extSubsurfaceScattering;
    o_dlOutBackScattering = k_int * i_intBackScattering + k_ext * i_extBackScattering;
    o_dlOutSpecular = k_int * i_intSpecular + k_ext * i_extSpecular;
    o_dlOutRim = k_int * i_intRim + k_ext * i_extRim;
    o_dlOutReflection = k_int * i_intReflection + k_ext * i_extReflection;
    o_dlOutRefraction = k_int * i_intRefraction + k_ext * i_extRefraction;
    o_dlOutShadow = max(i_intShadow, i_extShadow);
    o_outColor = o_dlOutColor;
    o_outTransparency = o_dlOutTransparency;
#endif
"""


def initializePlugin(obj):
    dl_fresnel.register(obj)

def uninitializePlugin(obj):
    dl_fresnel.deregister(obj)
