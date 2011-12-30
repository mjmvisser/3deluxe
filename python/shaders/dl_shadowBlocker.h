#ifndef __dl_shadowBlocker_h
#define __dl_shadowBlocker_h

/*
begin inputs
	prepare color color
	prepare float intensity
	matrix placementMatrix
	uniform float width
	uniform float height
	uniform float wedge
	uniform float hedge
	uniform float roundness
	uniform float cutOn
	uniform float parallelRays
end inputs

begin outputs
	color outColor
	float outAlpha
end outputs

*/

#include "shadow_utils.h"

void
prepare_maya_dl_shadowBlocker(
	// Inputs
	//
	varying color i_color;
	uniform float i_intensity;
	matrix i_placementMatrix;
	uniform float i_width;
	uniform float i_height;
	uniform float i_wedge;
	uniform float i_hedge;
	uniform float i_roundness;
	uniform float i_cutOn;
	uniform float i_parallelRays;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{

    extern point Ps;
    extern point P;
    extern float ss;
    extern float tt;

    point PsXf = transform("world", Ps);
    PsXf = transform(i_placementMatrix, PsXf);
    point PXf = transform("world", P);
    PXf = transform(i_placementMatrix, PXf);
    vector PtoPsXf = PsXf - PXf;
    // Intersect the ray from light to surface point with i_placementMatrix's xy plane (z=0).
    point Ptex = PXf - PtoPsXf * zcomp(PXf)/zcomp(PtoPsXf);
    ss =.5 + .5 * Ptex[0];
    tt =.5 + .5 * Ptex[1];
}

void
end_maya_dl_shadowBlocker(
	// Inputs
	//
	varying color i_color;
	uniform float i_intensity;
	matrix i_placementMatrix;
	uniform float i_width;
	uniform float i_height;
	uniform float i_wedge;
	uniform float i_hedge;
	uniform float i_roundness;
	uniform float i_cutOn;
	uniform float i_parallelRays;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{

    extern point Ps;

    point Pl = transform ("shader", Ps);

    point shadoworigin;
    if (i_parallelRays == 0) {
        shadoworigin = point "shader" (0,0,0);
    } else {
        shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
    }

    float unoccluded = pow(getBlockerContributionMx(Ps, shadoworigin, 
                                                    i_placementMatrix,
                                                    i_width, i_height,
                                                    i_wedge, i_hedge,
                                                    i_roundness), i_intensity);
     
   
    o_outColor = 1 - ((1 - unoccluded) *(1- i_color) *i_intensity);
    o_outAlpha = unoccluded;
}

#endif /* __dl_shadowBlocker_h */
