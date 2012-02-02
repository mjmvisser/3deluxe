import deluxe

class dl_reflection(deluxe.ReflectionRefractionComponent):
    typeid = 0x00300005
    description = "Calculates reflections "
    
    deluxe.ReflectionRefractionComponent.indexOfRefraction.default = 0;
    
    occIntensityMult = deluxe.Float(storage='uniform', default=1, softmin=0, softmax=2,
                         help="Intensity multiplier for raytraced reflection occlusion.")
    occSamplesMult = deluxe.Float(shortname='os', storage='uniform', default=1, softmin=0, softmax=2,
                         help="Samples multiplier for raytraced reflection occlusion.")
    occConeAngleMult = deluxe.Float(storage='uniform', default=1, softmin=0, softmax=2,
                         help="Cone angle multiplier for raytraced reflection occlusion.")

    reflectionOcclusion = deluxe.Group([occIntensityMult, occSamplesMult, occConeAngleMult])

    rsl = \
    """
    
    // reflect vector
    vector R;
    float kr;
    if (i_indexOfRefraction > 0) {
        float eta = (V.Nf >= 0) ? (1/i_indexOfRefraction) : i_indexOfRefraction;
        float kt;
        vector T;
        fresnel(In, dir, eta, kr, kt, R, T);
    }
    else {
        R = reflect(In, dir);
        kr = 1;
    }
    
    if (i_mapContribution > 0) {
        getEnvironmentReflection(origin, Nf, R, i_mapBlur, i_mapBlurS, i_mapBlurT, envFilter, i_physicalSkySamples, i_occConeAngleMult, i_occSamplesMult, envColor);
        envColor *= i_mapContribution;
    }
        
    color rayTransmission = 1;
    if (i_calculationMethod == 0) {
        getTraceOrGather(P, R, "reflection", i_rayMethod, i_rayMaxDistance, i_raySamples, i_rayBias, i_rayBlur, i_raySubset, o_output_reflection, rayDist, rayTransmission);
        if(rayTransmission == 1){
            o_output_reflection_env = envColor;
        }
        else if (i_rayFalloff != 0) {
            /*
            // TODO: SORT THIS OUT
            if (rayDist > i_rayFalloffDistance) {
                o_output_reflection *= pow(i_rayFalloffDistance/rayDist, i_rayFalloff);
            }
            else {
                uniform float ss = log(1/i_maxIntensity);
                uniform float beta = -i_rayFalloff / ss;
                o_output_reflection *= (i_maxIntensity * exp(ss * pow(rayDist/i_rayFalloffDistance, beta)));
            }      
            */  
        }
    }
    else if (i_calculationMethod == 1 && isBakingRadiosity() < 1) { // Point Cloud
        if(getPointCloudFiles("Reflection", i_ptcFile, ptcFiles)){
            ptcColor = indirectdiffuse(P, normalize(R), 0, "pointbased", 1, "filenames", ptcFiles, "maxdist", i_ptcMaxDist, "samplebase", i_ptcSampleBase, "bias", i_ptcBias,
                "occlusion", ptcAlpha, "sortbleeding", i_ptcSortBleeding, "clamp", i_ptcClamp, "maxsolidangle", i_ptcMaxSolidAngle, "coneangle", max(0.01, i_ptcBlur*PI/2));
            ptcColor *= i_ptcIntensity;
            ptcAlpha *= i_ptcIntensity;
        }
        o_output_reflection = mix(color(0), ptcColor, ptcAlpha);
        o_output_reflection_env = mix(envColor, color(0), ptcAlpha);
    }
    else{
        o_output_reflection_env = envColor;
    }

    float occluded = 0;
    color occlusioncolor = 1;
    uniform float traceSamplesMult = 1;
    getReflOccAndSampMult(origin, Nf, R, i_occConeAngleMult, i_occSamplesMult, occluded, occlusioncolor, traceSamplesMult);
    occluded *= i_occIntensityMult;
    
    // comp kr and reflection occlusion
    o_output_reflection *= kr;
    o_output_reflection_env *= kr;
    
    o_output_reflection = mix(occlusioncolor, o_output_reflection, (1-occluded));
    o_output_reflection_env = mix(occlusioncolor, o_output_reflection_env, (1-occluded));

    o_output_reflection *= surfaceColor * globalIntensity;
    o_output_reflection_env *= surfaceColor * globalIntensity;
    
    /*
    // TODO: VERIFIY THIS
    if (i_maxIntensity >= 0){ 
        clampToMaxIntens(i_maxIntensity, i_maxIntensity*.1, o_output_reflection);
        clampToMaxIntens(i_maxIntensity, i_maxIntensity*.1, o_output_reflection_env);
    }
    */
      
    o_output_reflection_depth = rayDist;
    o_output_beauty = o_output_reflection + o_output_reflection_env;
    """


def initializePlugin(obj):
    dl_reflection.register(obj)

def uninitializePlugin(obj):
    dl_reflection.deregister(obj)
