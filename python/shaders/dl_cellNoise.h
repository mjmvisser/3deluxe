#ifndef __dl_cellNoise_h
#define __dl_cellNoise_h

/*
begin inputs
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
	float jitter
	uniform float clamp
	float c1
	float c2
	uniform color avgcolor
	uniform float colorvariation
	uniform float frequency
	uniform float noisetype
	matrix placementMatrix
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

void
maya_dl_cellNoise(
	// Inputs
	//
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
	float i_jitter;
	uniform float i_clamp;
	float i_c1;
	float i_c2;
	uniform color i_avgcolor;
	uniform float i_colorvariation;
	uniform float i_frequency;
	uniform float i_noisetype;
	matrix i_placementMatrix;
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
          
            extern float du, dv;
   	       	pp *= i_frequency;

            if (i_noisetype == 2) {

                color varyColor(color avgcolor; float variance; float seed;)
                {
                    color hsl = ctransform("hsl", avgcolor);
                    float h, s, l;
                    h = comp(hsl, 0); s = comp(hsl, 1); l = comp(hsl, 2);
                    h += variance * (cellnoise(seed+3)-0.5);
                    s += variance * (cellnoise(seed-14)-0.5);
                    l += variance * (cellnoise(seed+37)-0.5);
                    hsl = color(mod(h,1), clamp(s, 0, 1), clamp(l, 0, 1));
                    return ctransform("hsl", "rgb", hsl);
                }

#ifndef MINFILTWIDTH
#  define MINFILTWIDTH 1.0e-6
#endif
#define fadeout(g,g_avg,featuresize,fwidth)         mix (g, g_avg, smoothstep(.2,.6,fwidth/featuresize))
#define tightFilterWidth(dpu,dpv)     max( length(dpu^dpv), MINFILTWIDTH )
#define filterWidth(a, b) tightFilterWidth(a,b)

                extern vector dPdu;
                extern vector dPdv;

                vector dppu = i_frequency * du*dPdu;
                vector dppv = i_frequency * dv*dPdv;
                color c, c1,c2,c3,c4;
                float f1, f2, f3, f4;
                point p2, p3, p4;

// This is to avoid warnings for getting cellnoise in "current" space.
#define addVtoPsameSpace(pOut, pIn, vIn)     pOut = pIn;     pOut[0] = pIn[0] + vIn[0];     pOut[1] = pIn[1] + vIn[1];     pOut[2] = pIn[2] + vIn[2];
                
                vector dppuv = dppu + dppv;
                addVtoPsameSpace(p2, pp, dppu)
                addVtoPsameSpace(p3, pp, dppv)
                addVtoPsameSpace(p4, pp, dppuv)

                f1 = float cellnoise(pp);
                f2 = float cellnoise(p2);
                f3 = float cellnoise(p3);
                f4 = float cellnoise(p4);
                c1 = varyColor(i_avgcolor, i_colorvariation, 100*f1);
                c2 = varyColor(i_avgcolor, i_colorvariation, 100*f2);
                c3 = varyColor(i_avgcolor, i_colorvariation, 100*f3);
                c4 = varyColor(i_avgcolor, i_colorvariation, 100*f4);
                c =  .25 * (c1 + c2 + c3 + c4);
                o_outColor = fadeout(c, i_avgcolor, 1, filterWidth(dppu, dppv));
                o_outAlpha = luminance( o_outColor );
            } else {
   	       	    
                float f1,f2;
                varying color g;   	
                point thiscell = point (floor(xcomp(pp))+0.5,
                                        floor(ycomp(pp))+0.5,
                            floor(zcomp(pp))+0.5);
                f1 = f2 = 1000;
                uniform float i, j, k;
                for (i = -1;  i <= 1;  i += 1) {
                    for (j = -1;  j <= 1;  j += 1) {
                        for (k = -1;  k <= 1;  k += 1) {
                    point testcell = thiscell + vector(i,j,k);
                            point pos = testcell + i_jitter * 
                        (vector cellnoise (testcell) - 0.5);
                    vector offset = pos - pp;
                            float dist;
                    if (i_noisetype == 0)  	
                        dist = offset.offset;
                    else
                    {
                        dist =  abs(xcomp(offset)) +
                                abs(ycomp(offset)) +
                            abs(zcomp(offset));
                    }
                            if (dist < f1) {
                                f2 = f1;
                                f1 = dist;
                            } else if (dist < f2) {
                                f2 = dist;
                    }
                        }
                }
                }
                if (i_noisetype == 0)  	
                        {
                    f1 = sqrt(f1);
                    f2 = sqrt(f2);
                }
                g = f1 * i_c1 + f2 * i_c2;
                if (i_clamp != 0)
                {
                    g = clamp(g, 0, 1);
                }
                o_outColor = g;
                o_outAlpha = luminance( o_outColor );
            }

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

#endif /* __dl_cellNoise_h */
