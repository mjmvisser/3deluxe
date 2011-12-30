#ifndef __dl_projectionCollector_h
#define __dl_projectionCollector_h

/*
begin inputs
	color baseColor
	float baseAlpha
	uniform string projLightSubset
end inputs

begin outputs
	color outColor
	float outAlpha
end outputs

*/

void
maya_dl_projectionCollector(
	// Inputs
	//
	color i_baseColor;
	float i_baseAlpha;
	uniform string i_projLightSubset;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	)
{
    

        color composite(
            float compMode;
            color bg, fg;
            float alpha;
            output float totalAlpha;
        ) {
            color outClr = 0;
            if (compMode == 0) {
                outClr = mix(bg, fg, alpha);
            } else {
                outClr = bg + fg;
            }
            totalAlpha = max(totalAlpha, alpha);
            return outClr;
        }


        extern point P;

        color totalColor = i_baseColor;
        float totalAlpha = i_baseAlpha;

        float ss = 0;
        float tt = 0;
        float compositeModeFromLight = 0;
        float alphaFromLight = 0;
        string textureFromLight = "";
        string projLightSubsetFromLight = "";

        illuminance("texture", P,
            "light:__ss", ss,
            "light:__tt", tt,
            "light:__compositeMode", compositeModeFromLight,
            "light:__texture", textureFromLight,
            "light:__alpha", alphaFromLight,
            "light:__projLightSubset", projLightSubsetFromLight
        ) {
            if (projLightSubsetFromLight == i_projLightSubset)
                totalColor = composite(compositeModeFromLight, totalColor, Cl, alphaFromLight, totalAlpha);
        }
        o_outColor = totalColor;
        o_outAlpha = totalAlpha;
}

#endif /* __dl_projectionCollector_h */
