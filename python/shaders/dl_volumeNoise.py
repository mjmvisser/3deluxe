import delight

class dl_volumeNoise(delight.Texture3D):
    typeid = 0x00300339
    includes = ["volumeNoise_utils.h"]
    
    # u float 
    frequencyIncrement = delight.Float(shortname="fd", default=.5, storage="uniform")
    threshold = delight.Float(shortname="th", default=0, storage="uniform")
    amplitude = delight.Float(shortname="am", default=1, storage="uniform")
    ratio = delight.Float(shortname="ra", default=.707, storage="uniform")
    frequencyRatio = delight.Float(shortname="fr", default=2, storage="uniform")
    depthMax = delight.Float(shortname="dm", default=3, storage="uniform")
    inflection = delight.Boolean(shortname="in", default=False, storage="uniform")
    time = delight.Float(shortname="ti", default=0, storage="uniform")
    frequency = delight.Float(shortname="fq", default=8)
    
    # u point
    scale = delight.Point(shortname="sc", default=1, storage="uniform")
    origin = delight.Point(shortname="or", default=0, storage="uniform")
    
    # float
    implode = delight.Float(shortname="im", default=0)
    
    # point
    implodeCenter = delight.Point(shortname="ic", default=0)
    
    # u float
    noiseType = delight.Enum(shortname="nt", default="Billow",
        choices=["Perlin Noise", "Billow", "Volume Wave", "Wispy", "SpaceTime"], storage="uniform")
    
    # float
    density = delight.Float(shortname="de", default=1)
    spottyness = delight.Float(shortname="sp", default=.1)
    sizeRand = delight.Float(shortname="sr", default=0)
    randomness = delight.Float(shortname="rn", default=1)
    falloff = delight.Enum(shortname="fa", default="Fast", choices=["Linear", "Smooth", "Fast", "Bubble"])
    
    # float
    numWaves = delight.Float(shortname="nw", default=5)
    
    
    
    rsl = \
    """

    void nsVaryFq (
        uniform float i_frequencyIncrement;
        uniform float i_threshold, i_amplitude, i_ratio, i_frequencyRatio;
        uniform float i_depthMax;
        uniform float i_inflection;
        uniform float i_time;
        float i_frequency;
        uniform point i_scale, i_origin;
        float i_implode;
        point i_implodeCenter;

        /* 0 = perlin, 1=bilow, 2=volume wave, 3=wispy, 4=spacetime */
        uniform float i_noiseType;

        /* Billow noise attributes */ 
        float i_density, i_spottyness, i_sizeRand, i_randomness, i_falloff;

        /* Wispy attribute */
        float i_numWaves;
     
        /* "Color Balance" related parameters */
        color i_defaultColor, i_colorGain, i_colorOffset;
        float i_alphaGain, i_alphaOffset;
        uniform float i_alphaIsLuminance;

        /* "Effects" related parameters */
        uniform float i_invert;
        float i_local;
        float i_wrap;
        float i_blend;

        /* geomtric inputs */
        matrix i_placementMatrix;

        // Outputs
        //
        output float o_outAlpha;
        output color o_outColor;
    ) {
        float fqByDivs = i_frequency/i_frequencyIncrement;
        float fqByDivsFloor = floor(fqByDivs);
        float fqByDivsCeil = ceil(fqByDivs);
        float nsPrevFq = fqByDivsFloor*i_frequencyIncrement;
        float nsNextFq = fqByDivsCeil*i_frequencyIncrement;
        float mixer = smoothstep(0, 1, fqByDivs - fqByDivsFloor);
        //float nsPrev = noise(nsPrevFq*p + 100 * (vector cellnoise(fqByDivsFloor + .5)));
        //float nsNext = noise(nsNextFq*p + 100 * (vector cellnoise(fqByDivsCeil + .5)));
        point nsPrevOrigin = i_origin + 100 * (vector cellnoise(fqByDivsFloor + .5));
        point nsNextOrigin = i_origin + 100 * (vector cellnoise(fqByDivsCeil + .5));

        color nsPrev = 0;
        color nsNext = 0;

        dl_maya_volumeNoise(
            /* "volumeNoise" related parameters */
            i_threshold, i_amplitude, i_ratio, i_frequencyRatio,
            i_depthMax,
            i_inflection,
            i_time, nsPrevFq,
            i_scale, nsPrevOrigin,
            i_implode,
            i_implodeCenter,

            /* 0 = perlin, 1=bilow, 2=volume wave, 3=wispy, 4=spacetime */
            i_noiseType,

            /* Billow noise attributes */ 
            i_density, i_spottyness, i_sizeRand, i_randomness, i_falloff,

            /* Wispy attribute */
            i_numWaves,
         
            /* "Color Balance" related parameters */
            i_defaultColor, i_colorGain, i_colorOffset,
            i_alphaGain, i_alphaOffset,
            i_alphaIsLuminance,

            /* "Effects" related parameters */
            i_invert,
            i_local,
            i_wrap,
            i_blend,

            /* geomtric inputs */
            i_placementMatrix,

            // Outputs
            //
            o_outAlpha,
            nsPrev);

        dl_maya_volumeNoise(
            /* "volumeNoise" related parameters */
            i_threshold, i_amplitude, i_ratio, i_frequencyRatio,
            i_depthMax,
            i_inflection,
            i_time, nsNextFq,
            i_scale, nsNextOrigin,
            i_implode,
            i_implodeCenter,

            /* 0 = perlin, 1=bilow, 2=volume wave, 3=wispy, 4=spacetime */
            i_noiseType,

            /* Billow noise attributes */ 
            i_density, i_spottyness, i_sizeRand, i_randomness, i_falloff,

            /* Wispy attribute */
            i_numWaves,
         
            /* "Color Balance" related parameters */
            i_defaultColor, i_colorGain, i_colorOffset,
            i_alphaGain, i_alphaOffset,
            i_alphaIsLuminance,

            /* "Effects" related parameters */
            i_invert,
            i_local,
            i_wrap,
            i_blend,

            /* geomtric inputs */
            i_placementMatrix,

            // Outputs
            //
            o_outAlpha,
            nsNext);
    
        o_outColor = mix(nsPrev, nsNext, mixer);
    }

    nsVaryFq(
        i_frequencyIncrement,
        i_threshold, i_amplitude, i_ratio, i_frequencyRatio,
        i_depthMax,
        i_inflection,
        i_time, i_frequency,
        i_scale, i_origin,
        i_implode,
        i_implodeCenter,

        /* 0 = perlin, 1=bilow, 2=volume wave, 3=wispy, 4=spacetime */
        i_noiseType,

        /* Billow noise attributes */ 
        i_density, i_spottyness, i_sizeRand, i_randomness, i_falloff,

        /* Wispy attribute */
        i_numWaves,
     
        /* "Color Balance" related parameters */
        i_defaultColor, i_colorGain, i_colorOffset,
        i_alphaGain, i_alphaOffset,
        i_alphaIsLuminance,

        /* "Effects" related parameters */
        i_invert,
        i_local,
        i_wrap,
        i_blend,

        /* geomtric inputs */
        i_placementMatrix,

        // Outputs
        //
        o_outAlpha,
        o_outColor
        );
    """


def initializePlugin(obj):
    dl_volumeNoise.register(obj)

def uninitializePlugin(obj):
    dl_volumeNoise.deregister(obj)
