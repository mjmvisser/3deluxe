#ifndef __dl_screen_h
#define __dl_screen_h

/*
begin inputs
	float density
	float frequency
	float2 uvFilterSize
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

*/

#include "utils.h"

void
maya_dl_screen(
	// Inputs
	//
	float i_density;
	float i_frequency;
	float i_uvFilterSize[2];
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


#define boxstep(a,b,x) (clamp(((x)-(a))/((b)-(a)),0,1))
#define MINFILTERWIDTH 1.0e-7

  extern varying float du, dv; 
  normal Nf;    /* Forward facing Normal vector */
  vector IN;    /* normalized incident vector */
  float d;      /* Density at the sample point */
  float sss, ttt; /* s,t, parameters in phase */
  float swidth, twidth, GWF, w, h;

  /* Determine how wide in s-t space one pixel projects to */
  swidth = max (abs(Du(ss)*du) + abs(Dv(ss)*dv), MINFILTERWIDTH) * i_frequency;
  twidth = max (abs(Du(tt)*du) + abs(Dv(tt)*dv), MINFILTERWIDTH) * i_frequency;

  /* Figure out where in the pattern we are */
  sss = mod (i_frequency * ss, 1);
  ttt = mod (i_frequency * tt, 1);

  /* Figure out where the strips are. Do some simple antialiasing. */
  GWF = i_density*0.5;
  if (swidth >= 1)
      w = 1 - 2*GWF;
  else w = clamp (boxstep(GWF-swidth,GWF,sss), max(1-GWF/swidth,0), 1)
	 - clamp (boxstep(1-GWF-swidth,1-GWF,sss), 0, 2*GWF/swidth);
  if (twidth >= 1)
      h = 1 - 2*GWF;
  else h = clamp (boxstep(GWF-twidth,GWF,ttt), max(1-GWF/twidth,0),1)
	 - clamp (boxstep(1-GWF-twidth,1-GWF,ttt), 0, 2*GWF/twidth); 
  d = 1 - w*h;
  o_outColor = d;  
  o_outAlpha = d;  

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

#endif /* __dl_screen_h */
