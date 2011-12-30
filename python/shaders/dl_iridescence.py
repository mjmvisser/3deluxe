import delight

class dl_iridescence(delight.Utility):
    typeid = 0x00370010
    includes = ["noise_utils.h", "env_utils.h", "component_utils.h"]
    description = "iridescence function"
    
    facingColour = delight.Color(shortname="fc", default=[0, 0, 1], help="""
        The color where the surface is facing the camera.  As the normal turns away from the camera,
        the hue changes, but the value and saturation remain the same.""")
    hueShift = delight.Float(shortname="sh", storage='uniform', default=2, help="""
        How much the hue shifts as the normal goes from facing the camera to perpendicular, eg. if
        hueShift = 2, the hue will do two complete rainbows from the center to edge of a sphere.""")
    noise = delight.Float(shortname="nsy", storage='uniform', default=1, help="""
        How much swirly (domain-distorted) noise is added to hue shift.  """)
    noiseFrequency = delight.Float(shortname="nf", storage='uniform', default=1, help="""
        Frequency of the hue shift noise.""")
    noiseOctaves = delight.Float(shortname="no", storage='uniform', default=3, help="""
        How many octaves of noise to do.""")
    noiseWarp = delight.Float(shortname="nw", storage='uniform', default=.5, help="""
        How how swirly (domain-distorted) the noise should be.""")
    noiseSpeed = delight.Float(shortname="ns", storage='uniform', default=.1, help="""
        Speed at which the noise morphs and moves downward relative to the frame number.
        """)
    ior = delight.Float(shortname="ior", storage='uniform', default=1.3, help="""
        THIS ONLY AFFACTS outAlpha, NOT outColor.  To create semi-transparent surfaces
        eg.  bubbles, plug outAlpha into dl_ultra's opacity parameter.  ior sets the
        index of refraction, which determines how much the opacity is reduced where the
        normal faces the camera (higher value = more opaque).
        """)
    outColor = delight.Color(shortname="oc", output=True)
    outAlpha = delight.Float(shortname="oa", output=True)


              
    rsl = \
    """    
    extern float time;
    extern point P;
    extern vector I;
    extern normal N;
    normal Nn = normalize(N);
    normal Nf = ShadingNormal(Nn);
    vector In = normalize(I);
    vector R, T;
    float Kr, Kt;
    fresnel (In, Nn, 1/i_ior,  Kr, Kt, R, T);
    float facing = Nn.In;

    point Pw = transform("world", P);

    

    // Hardcode some good noise parameters.
    uniform float initialAmplitude = 1;
    uniform float lacunarity = 1;
    uniform float frequencyRatio = 2;
    uniform float ratio = .5;
    uniform float ripples[3] = {1, 1, 1};  // not exactly sure what this is for....

    uniform float oct[2] = {i_noiseOctaves, i_noiseOctaves};

    vector Vns = vfBm((Pw + vector(0, time*i_noiseSpeed, 0))*i_noiseFrequency, oct, lacunarity, ratio, ripples);

    point Pnoise = Pw*i_noiseFrequency + i_noiseWarp * Vns * i_noise;

    //float ns =  fBm( point Vns, time*i_noiseSpeed,
    float ns =  fBm( Pnoise, time*i_noiseSpeed,
        initialAmplitude, oct, lacunarity, frequencyRatio, ratio);

    facing += i_noise * ns;
    color cHsv = ctransform("rgb", "hsv", i_facingColour);
    cHsv[0] = mod(cHsv[0] + (1-facing)*i_hueShift, 1);

    o_outColor = ctransform("hsv", "rgb", cHsv);
    o_outAlpha =  Kr;
    """
    
       
def initializePlugin(obj):
    dl_iridescence.register(obj)

def uninitializePlugin(obj):
    dl_iridescence.deregister(obj)
