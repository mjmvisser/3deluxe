#ifndef __dl_blendByNormal_h
#define __dl_blendByNormal_h

/*
begin inputs
	uniform string globalCoordsys
	float blendWidth
	uniform float globalWarpMode
	float globalWarpNoiseAmount
	float globalWarpNoiseFreq
	vector globalWarpNoiseOffset
	vector globalWarpInput
	uniform string[] axes[].label
	color[] axes[].colour
	uniform float[] axes[].coordsysToUse
	uniform string[] axes[].coordsysForThisAxis
	vector[] axes[].direction
	uniform float[] axes[].orientation
	float[] axes[].hemispheres
	float[] axes[].weight
	uniform float[] axes[].warpToUse
	uniform float[] axes[].warpMode
	float[] axes[].warpNoiseAmount
	float[] axes[].warpNoiseFreq
	vector[] axes[].warpNoiseOffset
	vector[] axes[].warpInput
end inputs

begin outputs
	color outColor
	color element0outColor
	color element1outColor
	color element2outColor
	color element3outColor
	color element4outColor
	color element5outColor
	color element6outColor
	color element7outColor
	float element0outAlpha
	float element1outAlpha
	float element2outAlpha
	float element3outAlpha
	float element4outAlpha
	float element5outAlpha
	float element6outAlpha
	float element7outAlpha
end outputs

*/

void
maya_dl_blendByNormal(
	// Inputs
	//
	uniform string i_globalCoordsys;
	float i_blendWidth;
	uniform float i_globalWarpMode;
	float i_globalWarpNoiseAmount;
	float i_globalWarpNoiseFreq;
	vector i_globalWarpNoiseOffset;
	vector i_globalWarpInput;
	uniform string i_label[];
	color i_colour[];
	uniform float i_coordsysToUse[];
	uniform string i_coordsysForThisAxis[];
	vector i_direction[];
	uniform float i_orientation[];
	float i_hemispheres[];
	float i_weight[];
	uniform float i_warpToUse[];
	uniform float i_warpMode[];
	float i_warpNoiseAmount[];
	float i_warpNoiseFreq[];
	vector i_warpNoiseOffset[];
	vector i_warpInput[];
	// Outputs
	//
	output color o_outColor;
	output color o_element0outColor;
	output color o_element1outColor;
	output color o_element2outColor;
	output color o_element3outColor;
	output color o_element4outColor;
	output color o_element5outColor;
	output color o_element6outColor;
	output color o_element7outColor;
	output float o_element0outAlpha;
	output float o_element1outAlpha;
	output float o_element2outAlpha;
	output float o_element3outAlpha;
	output float o_element4outAlpha;
	output float o_element5outAlpha;
	output float o_element6outAlpha;
	output float o_element7outAlpha;
	)
{


#define assingElement(type, i, val)     if (i == 0) o_element0out##type = val;     else if (i == 1) o_element1out##type = val;     else if (i == 2) o_element2out##type = val;     else if (i == 3) o_element3out##type = val;     else if (i == 4) o_element4out##type = val;     else if (i == 5) o_element5out##type = val;     else if (i == 6) o_element6out##type = val;     else if (i == 7) o_element7out##type = val;

    void warpV(
        float warpMode;
        float warpNoiseAmount;
        float warpNoiseFreq;
        vector warpNoiseOffset;
        vector warpInput;
        point Pp;
        output vector v)
    {
        if (warpMode == 1) {
            v += (1-2*(vector noise((Pp + warpNoiseOffset)*warpNoiseFreq)))*warpNoiseAmount;
        } else if (warpMode == 2) {
            v += warpInput;
        }
        v = normalize(v);
    }

    float weights[30];

    float nAxes = arraylength(i_colour);

    extern normal N;

    uniform float i;
    float wtTotal = 0;
    
    for (i = 0; i < nAxes; i += 1) {
        string coordsys = i_coordsysToUse[i] == 0 ? i_globalCoordsys : i_coordsysForThisAxis[i];
        coordsys = coordsys == "" ? "world" : coordsys;
        normal Nn = normalize(ntransform(coordsys, N));
        extern point P;
        point Pp = transform(coordsys, P);
        vector dir = i_direction[i];

        float warpMode = i_globalWarpMode;
        float warpNoiseAmount = i_globalWarpNoiseAmount;
        float warpNoiseFreq = i_globalWarpNoiseFreq;
        vector warpNoiseOffset = i_globalWarpNoiseOffset;
        vector warpInput = i_globalWarpInput;
        if (i_warpToUse[i] == 1) {
            warpMode = i_warpMode[i];
            warpNoiseAmount = i_warpNoiseAmount[i];
            warpNoiseOffset = i_warpNoiseOffset[i];
            warpNoiseFreq = i_warpNoiseFreq[i];
            warpInput = i_warpInput[i];
        }
        warpV(warpMode, warpNoiseAmount, warpNoiseFreq, warpNoiseOffset,
            warpInput, Pp, dir);

        float dot = Nn.normalize(dir);
        float posWt = smoothstep(1-i_hemispheres[i], 1, dot);
        float negWt = smoothstep(1-i_hemispheres[i], 1, -dot);
        float weight = i_orientation[i] == 0 ? posWt :
                i_orientation[i] == 1 ? posWt + negWt : negWt;
        weights[i] = i_weight[i]*pow(weight, 1/max(.01, i_blendWidth));
        wtTotal += weights[i];
    }

    color clrTotal = 0;
    if (wtTotal > 0) {
        for (i = 0; i < nAxes; i += 1) {
            clrTotal += i_colour[i] * weights[i]/wtTotal;
            assingElement(Color, i, i_colour[i]*weights[i]/wtTotal);
            assingElement(Alpha, i, weights[i]/wtTotal);
        }
    }

    o_outColor = clrTotal;

}

#endif /* __dl_blendByNormal_h */
