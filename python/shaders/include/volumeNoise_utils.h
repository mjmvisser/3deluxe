#ifndef __volumeNoise_utils_h
#define __volumeNoise_utils_h

/*
begin inputs
	float threshold
	float amplitude
	float ratio
	float frequencyRatio
	float depthMax
	float inflection
	float time
	float frequency
	point scale
	point origin
	float implode
	point implodeCenter
	float noiseType
	float density
	float spottyness
	float sizeRand
	float randomness
	float falloff
	float numWaves
	color defaultColor
	color colorGain
	color colorOffset
	float alphaGain
	float alphaOffset
	float alphaIsLuminance
	float invert
	float local
	float wrap
	float blend
	matrix placementMatrix
end inputs

begin outputs
	float outAlpha
	color outColor
end outputs


begin shader_extra_parameters Pref_param
	varying point Pref = 0;
end shader_extra_parameters
*/

#include "texture3d.h"
#include "utils.h"
#include "noise_utils.h"

// An ever-so-slightly modified version of maya_volumeNoise.
// It simply has varying i_frequency and i_origin parms instead
// of uniform to allow it to be used in the nsVaryFq function
// in dl_volumeNoise.

void
dl_maya_volumeNoise(
	/* "volumeNoise" related parameters */
	uniform float i_threshold, i_amplitude, i_ratio, i_frequencyRatio;
	uniform float i_depthMax;
	uniform float i_inflection;
	uniform float i_time;
    float i_frequency;
	uniform point i_scale;
    point i_origin;
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
	output color o_outColor; )
{
	extern point P;
	
	float outside;
	float edgeDist;

	varying point pp = transformP(i_blend, 
		i_local, 
		i_placementMatrix, 
		i_wrap, edgeDist, 
		outside );

	if(outside < 1)
	{
		/* Apply implosion. */
		if( i_implode != 0 )
		{
			vector dp = pp - i_implodeCenter;
			float l = length(dp);
			dp = dp / pow( l, i_implode );
			pp = dp + i_implodeCenter;
		}

		uniform float ripples[3] = {2, 2, 2};
		uniform float octaves[2] = {1, i_depthMax};

		point pn = vector(pp / i_scale) * i_frequency + i_origin;

		if( i_noiseType == 0 || i_noiseType == 3 || i_noiseType == 4 ) 
		{
			/* perlin, wispy and space time */

			if( i_noiseType == 3 )
			{
				/* wispy noise */
				pn += vector( noise( pn / 2 ) * 1.3 );
			}

			if( i_inflection > 0 )
			{
				o_outAlpha = i_amplitude * 
					fTurbulence(pn, i_time, 1, i_frequencyRatio, octaves, i_ratio, ripples);
			} else { 
				o_outAlpha = 
					fBm(pn, i_time, i_amplitude, octaves, 1, i_frequencyRatio, i_ratio);
			}
		}
		else if( i_noiseType == 1 )
		{
			/* "Billow" noise */
			float radius = sqrt( (0.5*0.5 + 0.5*0.5)*i_density );

			o_outAlpha = BillowNoise(
					pn, i_time, 3, radius, i_sizeRand, i_randomness, 
					i_falloff, i_spottyness, i_depthMax, 
					i_frequencyRatio, i_ratio, i_amplitude );
		}

		o_outAlpha += i_threshold;
		o_outAlpha = clamp(o_outAlpha,0,1);    
		o_outColor = o_outAlpha;

		colorBalance( o_outColor, 
			o_outAlpha, 
			i_alphaIsLuminance, 
			i_alphaGain, 
			i_alphaOffset, 
			i_colorGain, 
			i_colorOffset, 
			i_invert );
	}
	else
	{
		o_outColor = i_defaultColor;
		o_outAlpha = 0;
	}
}

#endif /* __volumeNoise_utils_h */

