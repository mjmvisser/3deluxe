/*
	Copyright (c) TAARNA Studios International.
*/

/*
	Following parameters are not supported:

	use_background
	background
	visibility_distance
	diffuse_horizontal_illuminance
*/

// Enable/disable extended mode.

#include "physicalsky_utils.h"

#define bool float
#define true 1
#define false 0

// Compute the square of a given value.
float sq(float x)
{
  return x * x;
}

//
// Main line of the physical sky shader.
//

imager dl_physicalsky(
    float physkyFakeSkyBlur = 0;
    float physkyFakeSkyBlurUpBias = 0;
    color tint = 1;
    float physkyJustSun = 0;
    string physkyCloudTex = "";
    string physkyGroundTex = "";
    float physkyTextureBlur = .1;
	float physkyMultiplier = 1.0;
	float physkyRgbUnitConversion[3] = 0;
	float physkyHaze = 0;
	float physkyRedBlueShift = 0.0;
	float physkySaturation = 1.0;
	float physkyHorizonHeight = 0;
	float physkyHorizonBlur = 0.1;
	color physkyGroundColour = 0.2;
	color physkyNightColour = 0;

    // Sun
	vector physkySunLightRotation = vector(-60,0,0);
	float physkySunDiskIntensity = 1.0;
	float physkySunDiskScale = 4.0;
	float physkySunGlowIntensity = 1.0;
	float physkySunMaxIntensity = 500000.0;

	//
	bool physkyYIsUp = true;
	
	string physkyCoordsys = "world";

	)
{

	vector reflection_dir = CameraRay( physkyCoordsys );
    vector ssunrot = vtransform("shader", physkySunLightRotation);
    color result= getPhysicalSky (
            reflection_dir,
	        ssunrot,
            1,  //Samples.
            0,  //Blur.
            physkyHaze,
            physkySaturation,
            physkyYIsUp,
            physkyHorizonHeight,
            physkyHorizonBlur,
            physkySunDiskIntensity,
            physkySunDiskScale,
            physkySunGlowIntensity,
            physkySunMaxIntensity,
            physkyGroundColour,
            physkyRgbUnitConversion,
            physkyMultiplier,
            physkyRedBlueShift,
            physkyNightColour,
            physkyGroundTex,
            physkyCloudTex,
            physkyTextureBlur,
            physkyJustSun,
            physkyFakeSkyBlur,
            physkyFakeSkyBlurUpBias
            );
    result *= tint;

	Ci += ( 1-alpha ) * result;
}
