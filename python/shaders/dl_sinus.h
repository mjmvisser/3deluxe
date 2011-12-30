#ifndef __dl_sinus_h
#define __dl_sinus_h

/*
begin inputs
	color defaultColor
	color colorGain
	color colorOffset
	float alphaGain
	float alphaOffset
	uniform float alphaIsLuminance
	uniform float invert
	init={ss,tt} float2 uvCoord
	uniform float symmetric
	uniform float normalized
	float power
	float2 uvFilterSize
end inputs

begin outputs
	color outColor
	float outAlpha
	color outTransparency
end outputs

*/

#include "utils.h"

void
maya_dl_sinus(
	// Inputs
	//
	color i_defaultColor;
	color i_colorGain;
	color i_colorOffset;
	float i_alphaGain;
	float i_alphaOffset;
	uniform float i_alphaIsLuminance;
	uniform float i_invert;
	float i_uvCoord[2];
	uniform float i_symmetric;
	uniform float i_normalized;
	float i_power;
	float i_uvFilterSize[2];
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	output color o_outTransparency;
	)
{

    varying float ss = i_uvCoord[0];
    varying float tt = 1 - i_uvCoord[1];
    
    if (ISUVDEFINED(ss, tt))
    {

    
    
    ss *=2*PI;
    tt *=2*PI;             
    if(i_symmetric)
    {
        o_outColor = sin(ss) * sin(tt);
        if (i_normalized)
        {
            o_outColor *=.5;
            o_outColor +=.5;
        }      
    }
    else
    {
        o_outColor = pow(abs(sin(ss)),i_power) *  pow(abs(sin(tt)),i_power);
    }
    o_outAlpha = luminance(o_outColor);  

        colorBalance(o_outColor, 
            o_outAlpha,
            i_alphaIsLuminance,
            i_alphaGain,
            i_alphaOffset,
            i_colorGain,
            i_colorOffset,
            i_invert);
    }
    else
    {
        o_outColor = i_defaultColor;
        o_outAlpha = luminance( o_outColor );
    }
    
    o_outTransparency = color(1 - o_outAlpha, 1 - o_outAlpha, 1 - o_outAlpha);   
}

#endif /* __dl_sinus_h */
