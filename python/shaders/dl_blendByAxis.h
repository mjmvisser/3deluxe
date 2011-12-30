#ifndef __dl_blendByAxis_h
#define __dl_blendByAxis_h

/*
begin inputs
	uniform float globalWarpMode
	float globalWarpNoiseAmount
	float globalWarpNoiseFreq
	vector globalWarpNoiseOffset
	vector globalWarpInput
	uniform string coordsys
	uniform float axis
	uniform string[] entries[].label
	color[] entries[].colour
	float[] entries[].value
	uniform float[] entries[].blend
	uniform float[] entries[].warpToUse
	uniform float[] entries[].warpMode
	float[] entries[].warpNoiseAmount
	float[] entries[].warpNoiseFreq
	vector[] entries[].warpNoiseOffset
	vector[] entries[].warpInput
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
maya_dl_blendByAxis(
	// Inputs
	//
	uniform float i_globalWarpMode;
	float i_globalWarpNoiseAmount;
	float i_globalWarpNoiseFreq;
	vector i_globalWarpNoiseOffset;
	vector i_globalWarpInput;
	uniform string i_coordsys;
	uniform float i_axis;
	uniform string i_label[];
	color i_colour[];
	float i_value[];
	uniform float i_blend[];
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

    float linInterp (float start, end, val) {
        return clamp((val-start)/(end-start), 0, 1);
    }

    float interp (float start, end, val, mode) {
        float result;
        if (mode < .5) {
            result = smoothstep(start, end, val);
        } else if (mode < 1.5) {
            result = linInterp(start, end, val);
        } else {
            result = filterstep(end, val);
        }
        return result;
    }


    float nElements = arraylength(i_colour);
    color result = 0;
    if (nElements > 0) {

        float nextI=0; float prevI=0;
        float nextVal=0; float prevVal=0;
        color nextClr=0; color prevClr=0;
        float nextBnd=0;

        float i;
        string coordsys = i_coordsys == "" ? "world" : i_coordsys;
        extern point P;
        point Pcs = transform(coordsys, P);
        float coord = Pcs[i_axis];
        point Pnoise = Pcs;
        Pnoise[i_axis] = 0;

        float warpedValues[nElements];



        for (i = 0; i < nElements; i += 1) {
            float warpMode = i_globalWarpMode;
            float warpNoiseAmount = i_globalWarpNoiseAmount;
            float warpNoiseFreq = i_globalWarpNoiseFreq;
            vector warpNoiseOffset = i_globalWarpNoiseOffset;
            vector warpInput = i_globalWarpInput;

            if (i_warpToUse[i] == 1) {
                warpMode = i_warpMode[i];
                warpNoiseAmount = i_warpNoiseAmount[i];
                warpNoiseFreq = i_warpNoiseFreq[i];
                warpNoiseOffset = i_warpNoiseOffset[i];
                warpInput = i_warpInput[i];
            }

            float warp = warpMode == 0 ? 0 : warpMode == 2 ? warpInput[i_axis] : 
                warpNoiseAmount * (1-2*(float noise((Pnoise + warpNoiseOffset)
                    * warpNoiseFreq)));

            warpedValues[i] = i_value[i] + warp;
        }

        float foundPrev = 0;
        float foundNext = 0;
        
        for (i = 0; i < nElements; i += 1) {
            if (warpedValues[i] > coord) {
                if (foundNext < .5 || warpedValues[i] < nextVal) {
                    foundNext = 1;
                    nextVal = warpedValues[i];
                    nextClr = i_colour[i];
                    nextBnd = i_blend[i];
                    nextI = i;
                }
            } else {
                if (foundPrev < .5 || warpedValues[i] > prevVal) {
                    foundPrev = 1;
                    prevVal = warpedValues[i];
                    prevClr = i_colour[i];
                    prevI = i;
                }
            }
        }

        if (foundPrev < .5) {
            result = nextClr;
            assingElement(Color, nextI, result);
            assingElement(Alpha, nextI, 1);
        } else if (foundNext < .5) {
            result = prevClr;
            assingElement(Color, prevI, result);
            assingElement(Alpha, prevI, 1);
        } else {
            float mixer = interp(prevVal, nextVal, coord, nextBnd);
            result = mix(prevClr, nextClr, mixer);
            assingElement(Color, nextI, nextClr * mixer);
            assingElement(Color, prevI, prevClr * (1-mixer));
            assingElement(Alpha, nextI, mixer);
            assingElement(Alpha, prevI, 1-mixer);
        }
    }

    o_outColor = result;
}

#endif /* __dl_blendByAxis_h */
