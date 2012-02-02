#ifndef __dl_brick_h
#define __dl_brick_h

/*
begin inputs
	color brickColor
	color mortarColor
	float jagged
	float brickVary
	float brickWidth
	float brickHeight
	float mortarThickness
	float rowVary
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
maya_dl_brick(
	// Inputs
	//
	color i_brickColor;
	color i_mortarColor;
	float i_jagged;
	float i_brickVary;
	float i_brickWidth;
	float i_brickHeight;
	float i_mortarThickness;
	float i_rowVary;
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

#define BMWIDTH (i_brickWidth+i_mortarThickness)
#define BMHEIGHT (i_brickHeight+i_mortarThickness)
#define MWF (i_mortarThickness*0.5/BMWIDTH)
#define MHF (i_mortarThickness*0.5/BMHEIGHT)
#define snoise(x) (2 * noise((x)) - 1)
#define boxstep(a,b,x) (clamp(((x)-(a))/((b)-(a)),0,1))
#define MINFILTERWIDTH 1.0e-7
  color bcolor;
  point PP2, Nf;
  float sbrick, tbrick, w, h;
  float scoord, tcoord, sss, ttt;
  float swidth, twidth;
  float Nfactor;
  
  extern varying float du,dv;    

  /* Determine how wide in ss-tt space one pixel projects to */
  swidth = max (abs(Du(ss)*du) + abs(Dv(ss)*dv), MINFILTERWIDTH);
  twidth = max (abs(Du(tt)*du) + abs(Dv(tt)*dv), MINFILTERWIDTH);

  

  /* Make the shapes of the bricks vary just a bit */
  PP2 = point noise (ss/BMWIDTH, tt/BMHEIGHT);
  scoord = ss + i_jagged * xcomp (PP2);
  tcoord = tt + i_jagged * ycomp (PP2);

  sss = scoord / BMWIDTH;   /* Determine which brick the point is in */
  ttt = tcoord / BMHEIGHT;  /*                   "                   */
  swidth /= BMWIDTH;
  twidth /= BMHEIGHT;

  /* shift alternate rows */
  if (mod (ttt*0.5, 1) > 0.5)
      sss += 0.5;

  tbrick = floor (ttt);   /* which brick row? */
  /* Shift the columns randomly by row */
  sss += i_rowVary * (noise (tbrick+0.5) - 0.5);

  sbrick = floor (sss);   /* which brick column? */
  sss -= sbrick;          /* Now sss and ttt are coords within the brick */
  ttt -= tbrick;

  /* Choose a color for the surface */
  if (swidth >= 1)
      w = 1 - 2*MWF;
  else w = clamp (boxstep(MWF-swidth,MWF,sss), max(1-MWF/swidth,0), 1)
     - clamp (boxstep(1-MWF-swidth,1-MWF,sss), 0, 2*MWF/swidth);

  if (twidth >= 1)
      h = 1 - 2*MHF;
  else h = clamp (boxstep(MHF-twidth,MHF,ttt), max(1-MHF/twidth,0),1)
     - clamp (boxstep(1-MHF-twidth,1-MHF,ttt), 0, 2*MHF/twidth);

  /* Choose a brick color that varies from brick to brick */
  bcolor = i_brickColor * (1 + (i_brickVary * snoise (tbrick+(100*sbrick)+0.5)));

  o_outColor = mix(i_mortarColor, bcolor, w*h);
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

#endif /* __dl_brick_h */
