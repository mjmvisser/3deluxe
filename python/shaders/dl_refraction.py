import delight

class dl_refraction(delight.ReflectionRefractionComponent):
    typeid = 0x00300006
    description = "Calculates refraction."

 
    rsl = \
    """

    // Refract vector
	float eta = (V.dir >= 0) ? (1/i_indexOfRefraction) : i_indexOfRefraction;
	vector R = refract(In, dir, eta);

    // Get map 
    if (i_mapContribution > 0) {
        getEnvironmentReflection(origin, Nf, R, i_mapBlur, i_mapBlurS, i_mapBlurT, envFilter, i_physicalSkySamples, envColor);
        envColor *= i_mapContribution;
    }
    
    // Ray Tracing
	if (i_calculationMethod == 0) {
	    color rayTransmission = 1;
	    getTraceOrGather(P, R, "refraction", i_rayMethod, i_rayMaxDistance, i_raySamples, i_rayBias, i_rayBlur, i_raySubset, o_output_refraction, rayDist, rayTransmission);
	    if(rayTransmission == 1)
	        o_output_refraction = envColor;
    }
	else if (i_calculationMethod == 1 && isBakingRadiosity() < 1) { // Point Cloud
	    if(getPointCloudFiles("Refraction", i_ptcFile, ptcFiles)){
            ptcColor = indirectdiffuse(P, normalize(R), 0, "pointbased", 1, "filenames", ptcFiles,  "maxdist", i_ptcMaxDist, "samplebase", i_ptcSampleBase, "bias", i_ptcBias,
                "occlusion", ptcAlpha, "sortbleeding", i_ptcSortBleeding, "clamp", i_ptcClamp, "maxsolidangle", i_ptcMaxSolidAngle, "coneangle", max(0.01, i_ptcBlur*PI/2));
            ptcColor *= i_ptcIntensity;
            ptcAlpha *= i_ptcIntensity;
	    }
        
        // Mix object on top of env
        o_output_refraction = mix(envColor, ptcColor, ptcAlpha);
	}
    else{
        o_output_refraction = envColor;
    }
    
    // TODO: SORT THIS OUT
    // handle falloff
    /* THIS IS FROM dl_reflection, BUT I DON'T UNDERSTAND IT. (falloffDistance parm required).
    if (i_falloff != 0) {
        if (rayDist < 1e30) {
            if (rayDist > i_falloffDistance) {
                o_output_refraction *= pow(i_falloffDistance/rayDist, i_falloff);
            }
            else {
                uniform float ss = log(1/i_maxIntensity);
                uniform float beta = -i_falloff / ss;
                o_output_refraction *= (i_maxIntensity * exp(ss * pow(rayDist/i_falloffDistance, beta)));
            }
        }
    }

    if (i_falloff != 0)
        o_output_refraction = mix(i_falloffColor, o_output_refraction, pow(max(0, 1-(rayDist/i_rayMaxDistance)), i_falloff));
    
    if (i_maxIntensity >= 0) 
        clampToMaxIntens(i_maxIntensity, i_maxIntensity*.1, o_output_refraction);
    */

	o_output_refraction *= surfaceColor * globalIntensity;
    o_output_beauty = o_output_refraction;
    """


def initializePlugin(obj):
    dl_refraction.register(obj)

def uninitializePlugin(obj):
    dl_refraction.deregister(obj)
