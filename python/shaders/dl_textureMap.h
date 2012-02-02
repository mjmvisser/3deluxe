#ifndef __dl_textureMap_h
#define __dl_textureMap_h

/*
begin inputs
	texture string textureName
	uniform float indexedSprites
	uniform float blur
	uniform float filterType
	uniform float samples
	uniform string coordsys
	float2 uvFilterSize
	float3 gamma
	float alphaInsideUVMult
	float alphaInsideUVOffset
	uniform float specifyAlphaOutsideUV
	float alphaOutsideUV
	uniform float warpMode
	float2 warpNoiseAmount
	float2 warpNoiseFreq
	float2 warpNoiseOffset
	float2 warpInput
	color defaultColor
	color colorGain
	color colorOffset
	float alphaGain
	float alphaOffset
	uniform float alphaIsLuminance
	uniform float invert
	init={ss,tt} float2 uvCoord
end inputs

begin outputs
	color outColor
	float outAlpha
	color outTransparency
end outputs

begin shader_extra_parameters spriteNumPP
	uniform float spriteNumPP = 0.0;
end shader_extra_parameters

*/

#include "utils.h"

void
maya_dl_textureMap(
	// Inputs
	//
	uniform string i_textureName;
	uniform float i_indexedSprites;
	uniform float i_blur;
	uniform float i_filterType;
	uniform float i_samples;
	uniform string i_coordsys;
	float i_uvFilterSize[2];
	float i_gamma[3];
	float i_alphaInsideUVMult;
	float i_alphaInsideUVOffset;
	uniform float i_specifyAlphaOutsideUV;
	float i_alphaOutsideUV;
	uniform float i_warpMode;
	float i_warpNoiseAmount[2];
	float i_warpNoiseFreq[2];
	float i_warpNoiseOffset[2];
	float i_warpInput[2];
	color i_defaultColor;
	color i_colorGain;
	color i_colorOffset;
	float i_alphaGain;
	float i_alphaOffset;
	uniform float i_alphaIsLuminance;
	uniform float i_invert;
	float i_uvCoord[2];
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
    
        void warpST(
            float warpMode;
            float warpNoiseAmount[2];
            float warpNoiseFreq[2];
            float warpNoiseOffset[2];
            float warpInput[2];
            output float ss, tt)
        {
            if (warpMode == 1) {
                float ss0 = ss;
                float tt0 = tt;
                ss += (1-2*noise((tt0 + warpNoiseOffset[0])*warpNoiseFreq[0]))*warpNoiseAmount[0];
                tt += (1-2*noise((ss0 + warpNoiseOffset[1])*warpNoiseFreq[1]))*warpNoiseAmount[1];
            } else if (warpMode == 2) {
                ss += warpInput[0];
                tt += warpInput[1];
            }
        }

        uniform float num_channels;
        textureinfo(i_textureName, "channels", num_channels);
     
        uniform string filterName= "gaussian";
        
        if (i_filterType == 0)
        {
            filterName = "box";
        }
        else if (i_filterType == 1)
        {
            filterName = "triangle";
        }

        // Coordinate system.
        if (i_coordsys != "") {
            extern point P;
            point Pw = transform("world", P);

            point Ptex = transform(i_coordsys, P);
            Ptex = transform("world", Ptex);

            Ptex = transform("current", "world", P);
            Ptex = transform(i_coordsys, "current", Ptex);

            uniform float frameFormat[3];
            option( "Format", frameFormat );
            float frameAR = frameFormat[0] / frameFormat[1];

            ss = Ptex[0]/2 + .5;
            tt = Ptex[1]*frameAR/2 + .5;
            tt = 1-tt;
        }
   
        uniform string tex = i_textureName;
        if (i_indexedSprites != 0)
        {
            uniform string template = i_textureName;
            template = dl_replace(template, ".NNNN.", ".%04d.");
            template = dl_replace(template, ".N.", ".%d.");

            extern uniform float spriteNumPP;
            tex = format(template, spriteNumPP);
        }

        warpST( i_warpMode, i_warpNoiseAmount, i_warpNoiseFreq, i_warpNoiseOffset,
            i_warpInput, ss, tt);
         
        if (num_channels == 1)
        {
            o_outColor = float texture(tex, ss, tt, 
                                       "blur", i_blur,
                                       "samples", i_samples,
                                       "filter", filterName,
                                       "fill", 1);
        } 
        else 
        {
            o_outColor = texture(tex, ss, tt, 
                                 "blur", i_blur, 
                                 "samples", i_samples,
                                 "filter", filterName,
                                 "fill", 1);
        }
    
        // apply gamma correction
        o_outColor = color(pow(comp(o_outColor, 0), 1.0 / i_gamma[0]),
                           pow(comp(o_outColor, 1), 1.0 / i_gamma[1]),
                           pow(comp(o_outColor, 2), 1.0 / i_gamma[2]));

    
        if (i_specifyAlphaOutsideUV == 1 && (ss > 1 || ss < 0 || tt > 1 || tt < 0))
        {
            o_outAlpha = i_alphaOutsideUV;
        } else {
            if (num_channels > 3)
            {
                o_outAlpha = texture(tex[3], ss, tt, 
                                     "blur", i_blur,
                                     "samples", i_samples,
                                     "filter", filterName,
                                     "fill", 1);
            } 
            else 
            {
                o_outAlpha = luminance(o_outColor);
            }
            o_outAlpha = o_outAlpha * i_alphaInsideUVMult + i_alphaInsideUVOffset;
        }

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

#endif /* __dl_textureMap_h */
