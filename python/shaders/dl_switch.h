#ifndef __dl_switch_h
#define __dl_switch_h

/*
begin inputs
	uniform float selectInput
	uniform float primvarOverride
	uniform float colorSet1nChoices
	uniform string ribAttrOverride
	float inputFloat0
	float inputFloat1
	float inputFloat2
	float inputFloat3
	float inputFloat4
	float inputFloat5
	float inputFloat6
	float inputFloat7
	float inputFloat8
	float inputFloat9
	color inputColor0
	color inputColor1
	color inputColor2
	color inputColor3
	color inputColor4
	color inputColor5
	color inputColor6
	color inputColor7
	color inputColor8
	color inputColor9
end inputs

begin outputs
	color outColor
	float outAlpha
end outputs

begin shader_extra_parameters dl_switch_selectInput_override_0
	float dl_switch_selectInput_override_0 = -1.0;
	float dl_switch_selectInput_override_1 = -1.0;
	float dl_switch_selectInput_override_2 = -1.0;
	float dl_switch_selectInput_override_3 = -1.0;
	float dl_switch_selectInput_override_4 = -1.0;
	float dl_switch_selectInput_override_5 = -1.0;
	float dl_switch_selectInput_override_6 = -1.0;
	float dl_switch_selectInput_override_7 = -1.0;
	float dl_switch_selectInput_override_8 = -1.0;
	float dl_switch_selectInput_override_9 = -1.0;
	varying color colorSet1 = color (-1, -1, -1);
end shader_extra_parameters

*/

void
maya_dl_switch(
	// Inputs
	//
	uniform float i_selectInput;
	uniform float i_primvarOverride;
	uniform float i_colorSet1nChoices;
	uniform string i_ribAttrOverride;
	float i_inputFloat0;
	float i_inputFloat1;
	float i_inputFloat2;
	float i_inputFloat3;
	float i_inputFloat4;
	float i_inputFloat5;
	float i_inputFloat6;
	float i_inputFloat7;
	float i_inputFloat8;
	float i_inputFloat9;
	color i_inputColor0;
	color i_inputColor1;
	color i_inputColor2;
	color i_inputColor3;
	color i_inputColor4;
	color i_inputColor5;
	color i_inputColor6;
	color i_inputColor7;
	color i_inputColor8;
	color i_inputColor9;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{
    

        // By default, use i_selectInput for the selected input.
        float selectInput = i_selectInput;

        // Rib attribute override.
        if (i_ribAttrOverride != "") attribute(i_ribAttrOverride, selectInput);

        // Primvar override.

        extern float dl_switch_selectInput_override_0;
        extern float dl_switch_selectInput_override_1;
        extern float dl_switch_selectInput_override_2;
        extern float dl_switch_selectInput_override_3;
        extern float dl_switch_selectInput_override_4;
        extern float dl_switch_selectInput_override_5;
        extern float dl_switch_selectInput_override_6;
        extern float dl_switch_selectInput_override_7;
        extern float dl_switch_selectInput_override_8;
        extern float dl_switch_selectInput_override_9;
        extern color colorSet1;

        if (i_primvarOverride == 0) {
            if (dl_switch_selectInput_override_0 >= 0) selectInput = dl_switch_selectInput_override_0;
        } else if (i_primvarOverride == 1) {
            if (dl_switch_selectInput_override_1 >= 0) selectInput = dl_switch_selectInput_override_1;
        } else if (i_primvarOverride == 2) {
            if (dl_switch_selectInput_override_2 >= 0) selectInput = dl_switch_selectInput_override_2;
        } else if (i_primvarOverride == 3) {
            if (dl_switch_selectInput_override_3 >= 0) selectInput = dl_switch_selectInput_override_3;
        } else if (i_primvarOverride == 4) {
            if (dl_switch_selectInput_override_4 >= 0) selectInput = dl_switch_selectInput_override_4;
        } else if (i_primvarOverride == 5) {
            if (dl_switch_selectInput_override_5 >= 0) selectInput = dl_switch_selectInput_override_5;
        } else if (i_primvarOverride == 6) {
            if (dl_switch_selectInput_override_6 >= 0) selectInput = dl_switch_selectInput_override_6;
        } else if (i_primvarOverride == 7) {
            if (dl_switch_selectInput_override_7 >= 0) selectInput = dl_switch_selectInput_override_7;
        } else if (i_primvarOverride == 8) {
            if (dl_switch_selectInput_override_8 >= 0) selectInput = dl_switch_selectInput_override_8;
        } else if (i_primvarOverride == 9) {
            if (dl_switch_selectInput_override_9 >= 0) selectInput = dl_switch_selectInput_override_9;
        } else if (i_primvarOverride == 10) {
            if (colorSet1[0] >= 0) {
                float rnd = cellnoise(.84 + colorSet1[0] * 140.45 * i_colorSet1nChoices);
                selectInput = floor(rnd*i_colorSet1nChoices);
            }
        }

        // Assign outputs.
        o_outAlpha =
            selectInput == 0 ? i_inputFloat0 :
            selectInput == 1 ? i_inputFloat1 :
            selectInput == 2 ? i_inputFloat2 :
            selectInput == 3 ? i_inputFloat3 :
            selectInput == 4 ? i_inputFloat4 :
            selectInput == 5 ? i_inputFloat5 :
            selectInput == 6 ? i_inputFloat6 :
            selectInput == 7 ? i_inputFloat7 :
            selectInput == 8 ? i_inputFloat8 : i_inputFloat9;

        o_outColor =
            selectInput == 0 ? i_inputColor0 :
            selectInput == 1 ? i_inputColor1 :
            selectInput == 2 ? i_inputColor2 :
            selectInput == 3 ? i_inputColor3 :
            selectInput == 4 ? i_inputColor4 :
            selectInput == 5 ? i_inputColor5 :
            selectInput == 6 ? i_inputColor6 :
            selectInput == 7 ? i_inputColor7 :
            selectInput == 8 ? i_inputColor8 : i_inputColor9;
}

#endif /* __dl_switch_h */
