#ifndef __dl_hextile_h
#define __dl_hextile_h

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
	color tileColor
	color mortarColor
	float tileRadius
	float mortarWidth
	float tileVary
	float tileScuffing
	float stains
	float stainFrequency
	float tileScuffFrequency
	color tileScuffColor
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
maya_dl_hextile(
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
	color i_tileColor;
	color i_mortarColor;
	float i_tileRadius;
	float i_mortarWidth;
	float i_tileVary;
	float i_tileScuffing;
	float i_stains;
	float i_stainFrequency;
	float i_tileScuffFrequency;
	color i_tileScuffColor;
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

#define snoise(x) (2*noise(x)-1)
#define snoise2(x,y) (2*noise((x),(y))-1)
  
  
  extern varying float du, dv; 
  point Nf;
  color Ct, Ctile;
  float tilewidth;
  float sss, ttt;
  float ttile, stile;
  float x, y;
  float mortar;
  float swidth, twidth, sfuzz, tfuzz, fuzzmax;
  float mw2;
  float tileindex;
  float stain, scuff;
  float ks;

  /* Determine how wide in ss-tt space one pixel projects to */
  swidth = abs(Du(ss)*du) + abs(Dv(ss)*dv);
  twidth = abs(Du(tt)*du) + abs(Dv(tt)*dv);
  sfuzz = 0.5 * swidth;
  tfuzz = 0.5 * twidth;
  fuzzmax = max (sfuzz, tfuzz);

  tilewidth = i_tileRadius * 1.7320508;  /* sqrt(3) */
  ttt = mod (tt, 1.5*i_tileRadius);
  ttile = floor (tt/(1.5*i_tileRadius));
  if (mod (ttile/2, 1) == 0.5)
       sss = ss + tilewidth/2;
  else sss = ss;
  stile = floor (sss / tilewidth);
  sss = mod (sss, tilewidth);
  mortar = 0;
  mw2 = i_mortarWidth/2;
  if (ttt < i_tileRadius) {
      mortar =  1 - (smoothstep(mw2,mw2+sfuzz,sss) *
             (1 - smoothstep(tilewidth-mw2-sfuzz,tilewidth-mw2,sss)));
    }
  else {
      x = tilewidth/2 - abs (sss - tilewidth/2);
      y = 1.7320508 * (ttt - i_tileRadius);
      if (y > x) {
      if (mod (ttile/2, 1) == 0.5)
          stile -= 1;
      ttile += 1;
      if (sss > tilewidth/2)
          stile += 1;
    }
      mortar = (smoothstep (x-1.73*mw2-tfuzz, x-1.73*mw2, y) *
        (1 - smoothstep (x+1.73*mw2, x+1.73*mw2+tfuzz, y)));
    }

  tileindex = stile+41*ttile;
  Ctile = i_tileColor * (1 + i_tileVary * snoise(tileindex+0.5));

  stain = i_stains * smoothstep (.5,1, noise(ss*i_stainFrequency,tt*i_stainFrequency));

  scuff = i_tileScuffing * smoothstep (.6,1, noise(tt*i_tileScuffFrequency-90.26,
                         ss*i_tileScuffFrequency+123.82));

  
  o_outColor = (1-stain) * mix (mix (Ctile, i_tileScuffColor, scuff), i_mortarColor, mortar);
  o_outAlpha = luminance( o_outColor );
    
    

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

#endif /* __dl_hextile_h */
