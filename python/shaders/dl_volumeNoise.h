#ifndef __dl_volumeNoise_h
#define __dl_volumeNoise_h

/*
begin inputs
	uniform float frequencyIncrement
	uniform float threshold
	uniform float amplitude
	uniform float ratio
	uniform float frequencyRatio
	uniform float depthMax
	uniform float inflection
	uniform float time
	float frequency
	uniform point scale
	uniform point origin
	float implode
	point implodeCenter
	uniform float noiseType
	float density
	float spottyness
	float sizeRand
	float randomness
	uniform float falloff
	float numWaves
	matrix placementMatrix
	color defaultColor
	color colorGain
	color colorOffset
	float alphaGain
	float alphaOffset
	uniform float alphaIsLuminance
	uniform float blend
	uniform float local
	uniform float wrap
	uniform float invert
end inputs

begin outputs
	color outColor
	float outAlpha
	color outTransparency
end outputs

begin shader_extra_parameters Pref
	varying point Pref = point (0, 0, 0);
end shader_extra_parameters

*/

#include "texture3d.h"
#include "utils.h"
#include "volumeNoise_utils.h"

void
maya_dl_volumeNoise(
	// Inputs
	//
	uniform float i_frequencyIncrement;
	uniform float i_threshold;
	uniform float i_amplitude;
	uniform float i_ratio;
	uniform float i_frequencyRatio;
	uniform float i_depthMax;
	uniform float i_inflection;
	uniform float i_time;
	float i_frequency;
	uniform point i_scale;
	uniform point i_origin;
	float i_implode;
	point i_implodeCenter;
	uniform float i_noiseType;
	float i_density;
	float i_spottyness;
	float i_sizeRand;
	float i_randomness;
	uniform float i_falloff;
	float i_numWaves;
	matrix i_placementMatrix;
	color i_defaultColor;
	color i_colorGain;
	color i_colorOffset;
	float i_alphaGain;
	float i_alphaOffset;
	uniform float i_alphaIsLuminance;
	uniform float i_blend;
	uniform float i_local;
	uniform float i_wrap;
	uniform float i_invert;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	output color o_outTransparency;
	)
{

    float edgeDist;
    float outside;  
    varying point pp = transformP(i_blend, 
        i_local, 
        i_placementMatrix, 
        i_wrap, edgeDist, 
        outside);
    if(outside < 1)
    {   


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

    colorBalance(o_outColor, 
            o_outAlpha, 
            i_alphaIsLuminance, 
            i_alphaGain, 
            i_alphaOffset, 
            i_colorGain, 
            i_colorOffset, 
            i_invert);

        if(i_blend > 0 && edgeDist >= 0)
        {
            o_outColor = blendDefaultColor(i_blend, i_defaultColor, edgeDist, o_outColor);
        }
    }
    else
    {
        o_outColor = i_defaultColor;
        o_outAlpha = 0;
    } 
    o_outTransparency = color(1 - o_outAlpha, 1 - o_outAlpha, 1 - o_outAlpha);  
}

#endif /* __dl_volumeNoise_h */
