#ifndef __dl_iridescence_h
#define __dl_iridescence_h

/*
begin inputs
	color facingColour
	uniform float hueShift
	uniform float noise
	uniform float noiseFrequency
	uniform float noiseOctaves
	uniform float noiseWarp
	uniform float noiseSpeed
	uniform float ior
end inputs

begin outputs
	color outColor
	float outAlpha
end outputs

*/

#include "noise_utils.h"
#include "env_utils.h"
#include "component_utils.h"

void
maya_dl_iridescence(
	// Inputs
	//
	color i_facingColour;
	uniform float i_hueShift;
	uniform float i_noise;
	uniform float i_noiseFrequency;
	uniform float i_noiseOctaves;
	uniform float i_noiseWarp;
	uniform float i_noiseSpeed;
	uniform float i_ior;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{
    
    extern float time;
    extern point P;
    extern vector I;
    extern normal N;
    normal Nn = normalize(N);
    normal Nf = ShadingNormal(Nn);
    vector In = normalize(I);
    vector R, T;
    float Kr, Kt;
    fresnel (In, Nn, 1/i_ior,  Kr, Kt, R, T);
    float facing = Nn.In;

    point Pw = transform("world", P);

    

    // Hardcode some good noise parameters.
    uniform float initialAmplitude = 1;
    uniform float lacunarity = 1;
    uniform float frequencyRatio = 2;
    uniform float ratio = .5;
    uniform float ripples[3] = {1, 1, 1};  // not exactly sure what this is for....

    uniform float oct[2] = {i_noiseOctaves, i_noiseOctaves};

    vector Vns = vfBm((Pw + vector(0, time*i_noiseSpeed, 0))*i_noiseFrequency, oct, lacunarity, ratio, ripples);

    point Pnoise = Pw*i_noiseFrequency + i_noiseWarp * Vns * i_noise;

    //float ns =  fBm( point Vns, time*i_noiseSpeed,
    float ns =  fBm( Pnoise, time*i_noiseSpeed,
        initialAmplitude, oct, lacunarity, frequencyRatio, ratio);

    facing += i_noise * ns;
    color cHsv = ctransform("rgb", "hsv", i_facingColour);
    cHsv[0] = mod(cHsv[0] + (1-facing)*i_hueShift, 1);

    o_outColor = ctransform("hsv", "rgb", cHsv);
    o_outAlpha =  Kr;
}

#endif /* __dl_iridescence_h */
