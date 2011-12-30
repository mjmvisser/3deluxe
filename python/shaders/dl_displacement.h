#ifndef __dl_displacement_h
#define __dl_displacement_h

/*
begin inputs
	uniform float globalScale
	uniform float globalOffset
	uniform float useShadingNormals
	uniform float useNormalMap
	varying color normalMap
	uniform float[] inputs[].enable
	float[] inputs[].alpha
	float[] inputs[].scale
	float[] inputs[].offset
	float[] inputs[].bumpOrDisplace
	float[] inputs[].recalculateNormal
	float[] inputs[].amount
	float[] inputs[].lip
	float[] inputs[].lipRimSharp
	uniform float selectedInput
end inputs

begin outputs
	color outColor
	float outAlpha
end outputs

begin shader_extra_parameters displacement
	output varying point __Porig = point (0, 0, 0);
	output varying normal __Norig = normal (0, 0, 0);
end shader_extra_parameters

*/

#include "displacement_utils.h"

void
maya_dl_displacement(
	// Inputs
	//
	uniform float i_globalScale;
	uniform float i_globalOffset;
	uniform float i_useShadingNormals;
	uniform float i_useNormalMap;
	varying color i_normalMap;
	uniform float i_enable[];
	float i_alpha[];
	float i_scale[];
	float i_offset[];
	float i_bumpOrDisplace[];
	float i_recalculateNormal[];
	float i_amount[];
	float i_lip[];
	float i_lipRimSharp[];
	uniform float i_selectedInput;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{

    extern point P;
    extern normal N;
    extern normal Ng;
    extern point __Porig;
    extern normal __Norig;

    // save P and N for use when raytracing without displacements
    __Porig = P;
    __Norig = N;

    normal Nn = normalize(N);
    normal deltaN = Nn - normalize(Ng);
    
    point Pnew = P + Nn * i_globalOffset;
    normal Nnew = Nn;
    
    uniform float num_inputs = arraylength(i_enable);

    
    float i;
    for (i = 0; i < num_inputs; i += 1)
    {
        if (i_enable[i] != 0)
        {
            float amount = i_amount[i];
            float lip = i_lip[i];

            if (lip > 0) {
                float lipDisp = -amount;
                float noLipDisp = amount - 2*lip;
                float mixer = smoothstep(.5 * i_lipRimSharp[i],
                    1 - .5 * i_lipRimSharp[i], amount/(lip * 2));
                amount = mix(lipDisp, noLipDisp, mixer);
                //amount = amount > lip ? amount - 2*lip : - amount;
            }

            amount = (amount * i_scale[i] * i_globalScale + i_offset[i]) * i_alpha[i];

            point Pold = Pnew;
            normal Nold = Nnew;
            getDisplacement(
                    amount,
                    i_bumpOrDisplace[i],
                    i_recalculateNormal[i],
                    i_useShadingNormals,
                    Pold,
                    Nold,
                    deltaN,
                    Pnew,
                    Nnew);
        }
    }
    
    if (i_useNormalMap == 1) {
        normal NmapWorld = normal i_normalMap;
        normal Nmap = ntransform("world", "current", NmapWorld);
        Nnew = Nmap + (Nnew-__Norig);
    }

    N = Nnew;
    P = Pnew;
}

#endif /* __dl_displacement_h */
