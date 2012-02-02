#ifndef __dl_blocker_h
#define __dl_blocker_h

/*
begin inputs
	prepare color color
	prepare float intensity
	uniform string coordsys
	uniform float width
	uniform float height
	uniform float wedge
	uniform float hedge
	uniform float roundness
	uniform float cutOn
	uniform float lightType
end inputs

begin outputs
	color blocker.blockerColor
	float blocker.blockerValue
end outputs

*/

#include "shadow_utils.h"

void
prepare_maya_dl_blocker(
	// Inputs
	//
	varying color i_color;
	varying float i_intensity;
	uniform string i_coordsys;
	uniform float i_width;
	uniform float i_height;
	uniform float i_wedge;
	uniform float i_hedge;
	uniform float i_roundness;
	uniform float i_cutOn;
	uniform float i_lightType;
	// Outputs
	//
	output color o_blockerColor;
	output float o_blockerValue;
	)
{

    extern point Ps;
    extern point P;
    extern vector L;
    extern float ss;
    extern float tt;

    if (i_coordsys != "")
    {
        point Pl = transform ("shader", Ps);
    
        point shadoworigin;
        if (i_lightType == 2) { // Parallel rays
            shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
        } else {
            shadoworigin = point "shader" (0,0,0);
        }

        vector sAx = normalize(vtransform(i_coordsys, "current", vector (1, 0, 0)));
        vector tAx = normalize(vtransform(i_coordsys, "current", vector (0, 1, 0)));
        point cOrg = transform(i_coordsys, "current", point (0, 0, 0));

        vector soToP = Ps - shadoworigin;
        vector Nplane = sAx^tAx;
        
        float t = ((-Nplane).(shadoworigin-cOrg)) / (Nplane.(Ps - shadoworigin));
        point Pint = shadoworigin + t*(shadoworigin-Ps);

        vector cOrgToPint = Pint - cOrg;
        point PintCs = transform(i_coordsys, Pint);
        float sBk = (1+PintCs[0])/2;
        float tBk = 1-(1+PintCs[1])/2;
        
        ss = sBk;
        tt = tBk;
    }
}

void
end_maya_dl_blocker(
	// Inputs
	//
	varying color i_color;
	varying float i_intensity;
	uniform string i_coordsys;
	uniform float i_width;
	uniform float i_height;
	uniform float i_wedge;
	uniform float i_hedge;
	uniform float i_roundness;
	uniform float i_cutOn;
	uniform float i_lightType;
	// Outputs
	//
	output color o_blockerColor;
	output float o_blockerValue;
	)
{

    extern point Ps;

    point Pl = transform ("shader", Ps);

    point shadoworigin;
    if (i_lightType == 2) { // Parallel rays
        shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
    } else {
        shadoworigin = point "shader" (0,0,0);
    }

    float unoccluded = mix(1, getBlockerContribution(Ps, shadoworigin, 
                                                     i_coordsys,
                                                     i_width, i_height,
                                                     i_wedge, i_hedge,
                                                     i_roundness), i_intensity);
   
    // markv: not sure why i_intensity is multiplied here
    o_blockerColor = 1 - ((1 - unoccluded) *(1- i_color) *i_intensity);
    o_blockerValue = unoccluded;
}

#endif /* __dl_blocker_h */
