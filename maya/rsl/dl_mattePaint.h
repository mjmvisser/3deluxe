#ifndef __dl_mattePaint_h
#define __dl_mattePaint_h

/*
begin inputs
	color defaultColor
	color defaultTransparency
	string[] layers[].layerName
	string[] layers[].textureFile
	float[] layers[].enableState
	sourcename string[] layers[].cameraMessage
	matrix[] layers[].cameraMatrix
end inputs

begin outputs
	color outColor
	color outTransparency
end outputs

begin shader_extra_parameters Pref_param
	varying point Pref = point (0, 0, 0);
end shader_extra_parameters

*/

#include "utils.h"
#include "blend_utils.h"

void
maya_dl_mattePaint(
	// Inputs
	//
	color defaultColor;
	color defaultTransparency;

	// for each layer
	string layerName[];
	string textureFile[];
	float enableState[];
	string cameraMessage[];
	matrix cameraMatrix[];

	// Outputs
	//
	output color outColor;
	output color outTransparency;
){

	extern point P;
	extern point Pref;

	color outAlpha = color(1) - defaultTransparency;
	outColor = defaultColor;

	// CAVEAT: Assuming arrays are matching size!!!
	uniform float nbLayers = arraylength(layerName);
	uniform float i = 0;

	for(i = 0; 	i < nbLayers; i += 1) {
		//
		string cameraSpace = concat("mayaCamera:", cameraMessage[i]);

		//
		point Ptex = P;
		if( Pref != point(0) )
			Ptex = Pref;

		//
		Ptex = transform("current", "world", Ptex);
		Ptex = transform(cameraSpace, "current", Ptex);

		// Don't project object back of cam
		if( zcomp(Ptex) > 1 )
			continue;

		// For some reason calls to "texture" shadop fails if done with array[index]
		string texFile = textureFile[i];

		// Image aspect ratio (if no success do nothing)
		uniform float imageRes[2];
		if( textureinfo( texFile, "resolution", imageRes ) == 0)
			continue;

		uniform float imageAR = imageRes[0] / imageRes[1];

		// Proj coords
		float ss = Ptex[0] / 2.0 + 0.5;
		float tt = 1.0 - (Ptex[1] * imageAR / 2.0 + 0.5);

		if(ss < 0 || ss > 1 || tt < 0 || tt > 1)
			continue;

		// Get color and alpha from tex file
		float layerAlpha = float texture(texFile[3], ss, tt);
		color layerColor = texture(texFile, ss, tt);

		// Layer enabled? then comp over
		if( enableState[i] != 0 )
			blend(0, layerColor, layerAlpha, outColor, outAlpha, outColor, outAlpha);

		// aov
		string outputNameColor = layerName[i];
		if(outputNameColor != ""){
			string outputNameAlpha = concat(layerName[i], "_alpha");
			outputchannel(outputNameColor, layerColor);
			outputchannel(outputNameAlpha, layerAlpha);
		}
	}

	outTransparency = color(1) - outAlpha;
}

#endif /* __dl_mattePaint_h */

