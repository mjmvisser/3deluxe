#ifndef __physicalsky_utils_h
#define __physicalsky_utils_h

#ifndef MINFILTWIDTH
#  define MINFILTWIDTH 1.0e-6
#endif

#define filterwidth(x)  max (abs(Du(x)*du) + abs(Dv(x)*dv), MINFILTWIDTH)



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

#define bool float
#define true 1
#define false 0

// Compute the CIE luminance (Rec. 709) of a given color.
float luminance(color c)
{
	return c[0] * 0.212671 + c[1] * 0.715160 + c[2] * 0.072169;
}

// Clamp a given scalar to the [0, 1] range.
float saturate(float x)
{
	return clamp(x, 0.0, 1.0);
}

/*
	Compute the luminance at zenith, in Kcd/m^2.

	PARAMETERS
	turbidity : atmosphere turbidity, 1.0 = pure air, 64.0 = thin fog
	theta_sun : sun zenith angle in radians, 0.0 = zenith
*/
float compute_zenith_luminance(
	float		   turbidity;
	float		   theta_sun)
{
	// The 1000.0 factor is a conversion from kcd/m^2 to cd/m^2.
	float xi = (4.0 / 9.0 - turbidity / 120.0) * (PI - 2.0 * theta_sun);
	return 1000.0 * (4.0453 * turbidity - 4.9710) *
		tan(xi) - 0.2155 * turbidity + 2.4192;
}

/*
	Compute the chromacity at zenith.

	PARAMETERS
	turbidity : atmosphere turbidity, 1.0 = pure air, 64.0 = thin fog
	theta_sun : sun zenith angle in radians, 0.0 = zenith

	OUTPUT
	xy		: chromacity at zenith
*/
void compute_zenith_chromacity(
	float		   turbidity;
	float		   theta_sun;
	output float	xy[2])
{
	// Compute turbidity^2, theta_sun^2 and theta_sun^3.
	float turbidity2 = turbidity*turbidity;
	float theta_sun2 = theta_sun*theta_sun;
	float theta_sun3 = theta_sun * theta_sun2;

	// Compute chromacity x.
	float a =  0.00166 * turbidity2 - 0.02903 * turbidity + 0.11693;
	float b = -0.00375 * turbidity2 + 0.06377 * turbidity - 0.21196;
	float c =  0.00209 * turbidity2 - 0.03202 * turbidity + 0.06052;
	float d =						 0.00394 * turbidity + 0.25886;
	xy[0] = a * theta_sun3 + b * theta_sun2 + c * theta_sun + d;

	// Compute chromacity y.
	float e =  0.00275 * turbidity2 - 0.04214 * turbidity + 0.15346;
	float f = -0.00610 * turbidity2 + 0.08970 * turbidity - 0.26756;
	float g =  0.00317 * turbidity2 - 0.04153 * turbidity + 0.06670;
	float h =						 0.00516 * turbidity + 0.26688;
	xy[1] = e * theta_sun3 + f * theta_sun2 + g * theta_sun + h;
}

/*
	Compute the coefficients of the luminance distribution function.

	PARAMETERS
	turbidity : atmosphere turbidity, 1.0 = pure air, 64.0 = thin fog

	OUTPUT
	coeffs	: distribution coefficients (A,B,C,D and E)
*/
void compute_luminance_distrib_coeffs(
	float		   turbidity;
	output float	coeffs[5])
{
	coeffs[0] =  0.1787 * turbidity - 1.4630;
	coeffs[1] = -0.3554 * turbidity + 0.4275;
	coeffs[2] = -0.0227 * turbidity + 5.3251;
	coeffs[3] =  0.1206 * turbidity - 2.5771;
	coeffs[4] = -0.0670 * turbidity + 0.3703;
}

/*
	Compute the coefficients of the x chromacity distribution function.

	PARAMETERS
	turbidity : atmosphere turbidity, 1.0 = pure air, 64.0 = thin fog

	OUTPUT
	coeffs	: distribution coefficients (A,B,C,D and E)
*/
void compute_chromacity_x_distrib_coeffs(
	float		   turbidity;
	float		   cos_theta_sun;
	output float	coeffs[5])
{
	coeffs[0] = -0.0193 * turbidity - (0.29 - sqrt(cos_theta_sun) * 0.09);
	coeffs[1] = -0.0665 * turbidity + 0.0008;
	coeffs[2] = -0.0004 * turbidity + 0.2125;
	coeffs[3] = -0.0641 * turbidity - 0.8989;
	coeffs[4] = -0.0033 * turbidity + 0.0452;
}

/*
	Compute the coefficients of the y chromacity distribution function.

	PARAMETERS
	turbidity : atmosphere turbidity, 1.0 = pure air, 64.0 = thin fog

	OUTPUT
	coeffs	: distribution coefficients (A,B,C,D and E)
*/
void compute_chromacity_y_distrib_coeffs(
	float		   turbidity;
	output		  float coeffs[5])
{
	coeffs[0] = -0.0167 * turbidity - 0.2608;
	coeffs[1] = -0.0950 * turbidity + 0.0092;
	coeffs[2] = -0.0079 * turbidity + 0.2102;
	coeffs[3] = -0.0441 * turbidity - 1.6537;
	coeffs[4] = -0.0109 * turbidity + 0.0529;
}

/*
	Perez formula describing the sky luminance distribution.

	PARAMETERS
	theta	 : viewer zenith angle in radians, 0.0 = zenith
	gamma	 : sun-viewer relative azimuth angle in radians
	coefs	 : distribution coefficients (A, B, C, D, E)
*/
float perez_formula(
	float		   cos_theta;
	float		   gamma;
	float		   cos_gamma;
	float		   coeffs[5])
{
	float u = 1.0 + coeffs[0] * exp(coeffs[1] / cos_theta);
	float v = 1.0 + coeffs[2] * exp(coeffs[3] * gamma)
				  + coeffs[4] * cos_gamma * cos_gamma;
	return u * v;
}

/*
	Compute one of the three quantity defining the sky aspect:
	the sky luminance Y, and the sky chromacities x and y.

	PARAMETERS:
	theta	 : viewer zenith angle in radians, 0.0 = zenith
	gamma	 : sun-viewer relative azimuth angle in radians
	theta_sun : sun zenith angle in radians, 0.0 = zenith
	zenith_val: value of the quantity at zenith
	coefs	 : distribution coefficients (A, B, C, D, E)
*/
float compute_sky_quantity(
	float		   cos_theta;
	float		   gamma;
	float		   cos_gamma;
	float		   theta_sun;
	float		   cos_theta_sun;
	float		   zenith_val;
	float		   coeffs[5])
{
	return
		zenith_val
	  * perez_formula(cos_theta, gamma, cos_gamma, coeffs)
	  / perez_formula(1.0, theta_sun, cos_theta_sun, coeffs);
}

float compute_saturation(float saturation, turbidity)
{
	if (saturation > 1.0)
		return saturation;
	else
	{
		float saturation3 = pow(saturation, 3.0);
		float k = pow(saturate((turbidity - 2.0) / 15.0), 3.0);
		return mix(saturation, saturation3, k);
	}
}

vector transform_direction(
	vector		  direction;
	bool			y_is_up;
	float		   horizon_height)
{
	vector dir = direction;

	// Make sure Y is always the 'up' direction.
	if (y_is_up == false)
	{
		float y = dir[1];
		dir[1] = dir[2];
		dir[2] = y;
	}

	if (horizon_height != 0.0)
	{
		dir[1] -= horizon_height * 0.1;
		dir = normalize(dir);
	}

	return dir;
}

vector fixup_direction(vector direction)
{
	vector dir = direction;

	// Make sure the direction points above the horizon.
	if (dir[1] < 0.001)
	{
		dir[1] = 0.001;
		dir = normalize(dir);
	}

	return dir;
}

color compute_sky_color(
	vector  sun_direction;
	float   theta_sun;
	float   cos_theta_sun;
	float   zenith_luminance;
	float   lumimance_coeffs[5];
	float   zenith_chromacity[2];
	float   chromacity_x_coeffs[5];
	float   chromacity_y_coeffs[5];
	vector  direction)
{
    color result = 0;
	// Compute the zenith angle of this direction.
	float cos_theta = direction[1];

	// Compute the relative azimuth angle of this direction.
	float cos_gamma = direction . sun_direction;
	cos_gamma = max(cos_gamma, 0.0);
	if (cos_gamma > 1.0)
		cos_gamma = 2.0 - cos_gamma;
	float gamma = acos(cos_gamma);

	// Compute sky luminance along this direction.
	float luminance =
		compute_sky_quantity(
			cos_theta,
			gamma,
			cos_gamma,
			theta_sun,
			cos_theta_sun,
			zenith_luminance,
			lumimance_coeffs);

	// Compute sky chromacities along this direction.
	float chromacity_x =
		compute_sky_quantity(
			cos_theta,
			gamma,
			cos_gamma,
			theta_sun,
			cos_theta_sun,
			zenith_chromacity[0],
			chromacity_x_coeffs);
	float chromacity_y =
		compute_sky_quantity(
			cos_theta,
			gamma,
			cos_gamma,
			theta_sun,
			cos_theta_sun,
			zenith_chromacity[1],
			chromacity_y_coeffs);

	// Convert Yxy to CIE XYZ.
	float cie_x = chromacity_x / chromacity_y * luminance;
	float cie_y = luminance;
	float cie_z = (1.0 - chromacity_x - chromacity_y) / chromacity_y * luminance;

	// Convert CIE XYZ to sRGB (D65 white point).
	result =
		color(
			 3.240479 * cie_x - 1.537150 * cie_y - 0.498530 * cie_z,
			-0.969256 * cie_x + 1.875991 * cie_y + 0.041556 * cie_z,
			 0.055648 * cie_x - 0.204043 * cie_y + 1.057311 * cie_z);

	return result * PI;
}

color compute_sky_color_fakeBlur(
	vector  sun_direction;
	float   theta_sun;
	float   cos_theta_sun;
	float   zenith_luminance;
	float   lumimance_coeffs[5];
	float   zenith_chromacity[2];
	float   chromacity_x_coeffs[5];
	float   chromacity_y_coeffs[5];
	vector  direction;
    uniform float fakeSkyBlur;
    float fakeSkyBlurUpBias;
    
    )
{
    color result;
    /* NOTE: If this optimization is uncommented, horrible random artifacts occur.
    if (fakeSkyBlur <= 0) {
	    result = compute_sky_color(
                    sun_direction,
                    theta_sun,
                    cos_theta_sun,
                    zenith_luminance,
                    lumimance_coeffs,
                    zenith_chromacity,
                    chromacity_x_coeffs,
                    chromacity_y_coeffs,
                    direction);
    } else {*/
        void bendUp(float bias; output vector v) {
            v = normalize( mix(v, vector (0, 1, 0), bias));
        }

        vector dirBlurTowardsUp = normalize(mix(direction, vector (0, 1, 0), fakeSkyBlur));
        bendUp(fakeSkyBlurUpBias, dirBlurTowardsUp);
        dirBlurTowardsUp = fixup_direction(dirBlurTowardsUp);
        //dirBlurTowardsUp = normalize( mix(dirBlurTowardsUp, vector (0, 1, 0), fakeSkyBlurUpBias));
	    color resultUp = compute_sky_color(
                    sun_direction,
                    theta_sun,
                    cos_theta_sun,
                    zenith_luminance,
                    lumimance_coeffs,
                    zenith_chromacity,
                    chromacity_x_coeffs,
                    chromacity_y_coeffs,
                    dirBlurTowardsUp);

        vector dirBlurTowardsHoriz = normalize(mix(direction, direction * (1, 0, 1), fakeSkyBlur));
        bendUp(fakeSkyBlurUpBias, dirBlurTowardsHoriz);
        dirBlurTowardsHoriz = fixup_direction(dirBlurTowardsHoriz);
	    color resultHoriz = compute_sky_color(
                    sun_direction,
                    theta_sun,
                    cos_theta_sun,
                    zenith_luminance,
                    lumimance_coeffs,
                    zenith_chromacity,
                    chromacity_x_coeffs,
                    chromacity_y_coeffs,
                    dirBlurTowardsUp);

        // A hacky way of bending dir away from up -- for unknown reasons, directly mixing it
        // with -Y axis (mix(direction, vector (0, -1, 0), fakeSkyBlur)) caused artifacts.
        vector dirBlurTowardsDown = normalize(mix(direction, vector (0, 1, 0), -fakeSkyBlur));
        bendUp(fakeSkyBlurUpBias, dirBlurTowardsDown);
        dirBlurTowardsDown = fixup_direction(dirBlurTowardsDown);
	    color resultDown = compute_sky_color(
                    sun_direction,
                    theta_sun,
                    cos_theta_sun,
                    zenith_luminance,
                    lumimance_coeffs,
                    zenith_chromacity,
                    chromacity_x_coeffs,
                    chromacity_y_coeffs,
                    dirBlurTowardsDown);

        result = (resultUp + resultHoriz + resultDown)/3;
    //}
    return result;
}

color compute_sun_color(
	float   turbidity;
	float   theta_sun;	
	float   cos_theta_sun)
{
	if (cos_theta_sun <= 0.0)
		return 0.0;

	color lambda_o = color(12.0, 8.5, 0.9);
	color lambda = color(0.610, 0.550, 0.470);
	color sun_intensity =
		color(
			  1.0 * 127500 / 0.9878,
			0.992 * 127500 / 0.9878,
			0.911 * 127500 / 0.9878);

	// Relative Optical Mass equivalent.
	float m = 1.0 / (cos_theta_sun + 0.15 * pow(93.885 - theta_sun * 180 / PI, -1.253));

	// Amount of aerosols present.
	float beta = 0.04608366 * turbidity - 0.04586026;

	float Alpha = 1.3;	  // ratio of small to large particle sizes (0 to 4, usually 1.3)
	float Ozone = 0.0035;   // amount of ozone in meters (NTP)
	float W = 2.0;		  // precipitable water vapor in centimeters (standard = 2)

	// Aerosal (water + dust) attenuation.
	color tau_a;
	tau_a[0] = exp(-m * beta * pow(lambda[0], -Alpha));
	tau_a[1] = exp(-m * beta * pow(lambda[1], -Alpha));
	tau_a[2] = exp(-m * beta * pow(lambda[2], -Alpha));

	// Attenuation due to ozone absorption.
	color tau_o;
	tau_o[0] = exp(-m * lambda_o[0] * Ozone);
	tau_o[1] = exp(-m * lambda_o[1] * Ozone);
	tau_o[2] = exp(-m * lambda_o[2] * Ozone);

	// Rayleigh Scattering.
	color tau_r;
	tau_r[0] = exp(-m * 0.008735 * pow(lambda[0], -4.08));
	tau_r[1] = exp(-m * 0.008735 * pow(lambda[1], -4.08));
	tau_r[2] = exp(-m * 0.008735 * pow(lambda[2], -4.08));

	return tau_r * tau_a * tau_o * sun_intensity;
}

color compute_sun_disk(
	vector  direction;
	vector  sun_direction;
	float   turbidity;
	color   sun_color;
	float   sun_disk_intensity;
	float   sun_disk_scale;
	float   sun_glow_intensity)
{
	float cos_gamma = direction . sun_direction;
	float gamma = acos(cos_gamma);

	float sun_angular_radius = 0.00465 * sun_disk_scale * 10.0;

	color ret = 0;
	if (gamma < sun_angular_radius )
	{
	  float k = (1.0 - gamma / sun_angular_radius) * 10.0;

	  ret = sun_color * (
		  pow(k / 10.0, 3.0) * 2.0 * sun_glow_intensity +
		  smoothstep(8.5, 9.5 + turbidity / 50.0, k) * 100.0 * sun_disk_intensity);
	}

	return ret;
}

color compute_ground_lighting(
	vector  sun_direction;
	float   theta_sun;
	float   cos_theta_sun;
	float   zenith_luminance;
	float   lumimance_coeffs[5];
	float   zenith_chromacity[2];
	float   chromacity_x_coeffs[5];
	float   chromacity_y_coeffs[5];
    uniform float fakeSkyBlur;
    float fakeSkyBlurUpBias
    )
{
	uniform float Samples = 1.0;

	vector direction = 0.0;
	color result = 0.0;

#if 0
	gather (
		"samplepattern",
		0.0,
		vector(0.0, 1.0, 0.0),
		PI / 2.0,
		Samples,
		"distribution", "cosine",
		"ray:direction", direction)
	{
	}
	else
#else
	// Meanwhile, look up only one direction.
	direction = vector(0.0, 1.0, 0.0);
#endif
	{
		result +=
			compute_sky_color_fakeBlur(
				sun_direction,
				theta_sun,
				cos_theta_sun,
				zenith_luminance,
				lumimance_coeffs,
				zenith_chromacity,
				chromacity_x_coeffs,
				chromacity_y_coeffs,
				direction,
                fakeSkyBlur,
                fakeSkyBlurUpBias
                );
	}

	return result / Samples;
}

vector CameraRay( string i_skyspace )
{
	extern float u, v;

	/* Find out the coordinates, in camera space, of the current pixel. To
	   do so, we first tranform from NDC (wich is defined in the [0..1] x
	   [0..1] square) to screen space. This gives us the 'x' & 'y'
	   coordinates in camera space. The 'z' coordinate is actually the
	   distance of the screen space to the camera center and we need the
	   FOV to find out this value (D = 1/tan(fov * 0.5)). With the camera
	   space coordinate of the pixel in hand, we can easily compute a world
	   space vector that can then be used in the environment() function.
	   Please refer to The RenderMan Companion p.168 for a visualization of
	   this operation.

       NOTE: (u, v) coordinates in an imager shader are defined in the
       [0..1]x[0..1] square, which is our starting NDC coordinate system. */

	point screen_space = transform( "NDC", "screen", point(u, v, 0) );

	/* Compute distance from camera EYE to screen as explained above.
	   We need the field of view of the render for that. */
	uniform float fov = 70;
	option( "FieldOfView", fov );
	float D = 1.0 / tan( radians(fov) * 0.5 );

	/* Make our world vector using the (x, y) coordinates on the screen
	   plane and 'D'. */

	vector world_vector = vtransform( i_skyspace,
			vector(xcomp(screen_space), ycomp(screen_space), D) );

	return world_vector;
}


float texExists(string tx) {
    return tx != "" && textureinfo(tx, "exists", 0) == 1 ? 1 : 0;
}

float texHasAlpha(string tx) {
    float nchannels = 0;
    textureinfo(tx, "channels", nchannels);
    return nchannels > 3 ? 1 : 0;
}

void domeTex (string gndTex, skyTex; vector V; float ortho, pwr, blur;
        output color clr;
        output float alph;) {
    extern float du;
    extern float dv;
    float k = 1-pow(abs(V[1]), pwr)*(1-ortho);
    float ss = .5 + .5 * V[0] * k;
    float tt = .5 + .5 * V[2] * k;

    color skyClr = 0, gndClr = 0;
    float skyAlph = 0, gndAlph = 0;

    if (texExists(skyTex)) {
        //printf ("\n skyTex EXISTS %s", skyTex);
        skyClr = texture(skyTex, ss, tt, "blur", blur);
        skyAlph = texHasAlpha(skyTex) ? texture(skyTex[3], ss, tt, "blur", blur) : 1;
    } else {
        //printf ("\n skyTex EXISTS NNNNNOOOT!!! %s", skyTex);
    }

    if (texExists(gndTex)) {
        gndClr = texture(gndTex, ss, tt, "blur", blur);
        gndAlph = texHasAlpha(gndTex) ? texture(gndTex[3], ss, tt, "blur", blur) : 1;
        //printf ("\n gndTex = %s,texHasAlpha(gndTex) = %f", gndTex, texHasAlpha(gndTex));
    }

    //float mixer = fliterwidth(V[1]) > filterstep(0, V[1]);
    float mixer = filterstep(0, V[1]); 
    float blurScaled = blur*8;
    if (filterwidth(V[1]) < 2 * blurScaled)
        mixer = smoothstep(-blurScaled, blurScaled, V[1]);
    clr = mix(gndClr, skyClr, mixer);

    alph = mix(gndAlph, skyAlph, mixer);
}

void stFromV(vector V; output float ss, tt) {
    ss = .5 + .5 * V[1];
    tt = .5 + atan(V[0], V[2])/(2*PI);
}



color getPhysicalSkySample (
    vector reflection_dir;
    float i_haze;
    float i_saturation;
    float i_y_is_up;
    float i_horizon_height;
    float i_horizon_blur;
    //float i_sky_luminance_mode;
    vector sunDir;
    float i_sun_disk_intensity;
    float i_sun_disk_scale;
    float i_sun_glow_intensity;
    float i_sun_maxintensity;
    color i_ground_color;
	float i_rgb_unit_conversion[3];
	float i_multiplier;
	float i_redblueshift;
	color i_night_color;
    float justSun;
    uniform float fakeSkyBlur;
    float fakeSkyBlurUpBias;

) {
    color result;
    // Compute turbidity value from haze parameter.
    float turbidity = 2.0 + i_haze;
    if (turbidity < 2.0)
        turbidity = 2.0;

    // Compute saturation value.
    float saturation = compute_saturation(i_saturation, turbidity);

    // Compute the sun direction.
    vector sun_direction =
        transform_direction(
            normalize(vector sunDir),
                i_y_is_up,
                i_horizon_height);


        float below_horiz_factor = sun_direction[1] < 0.0 ? 1.0 + sun_direction[1] : 1.0;

        // Make sure the sun is above the horizon.
        sun_direction = fixup_direction(sun_direction);

        // Compute the zenith angle of the sun, in radians.
        float cos_theta_sun = sun_direction[1];
        float theta_sun = acos(cos_theta_sun);

        // Compute the reflection direction.
        // todo: remove normalize() if reflection_dir is always unit length.
        vector direction =
            transform_direction(
                normalize(reflection_dir),
                i_y_is_up,
            i_horizon_height);

    // Compute the zenith angle of this direction.
    float cos_theta = direction[1];

    // Make sure the direction points above the horizon.
    direction = fixup_direction(direction);

    // Compute the luminance parameters.
    float zenith_luminance;
    float lumimance_coeffs[5];
#ifdef EXTENDED
    if (i_sky_luminance_mode == 0)
#endif
    {
        // Compute luminance at zenith.
        zenith_luminance = compute_zenith_luminance(turbidity, theta_sun);

        // Compute the coefficients of the luminance distribution function.
        compute_luminance_distrib_coeffs(
            turbidity,
            lumimance_coeffs);
    }
#ifdef EXTENDED
    else if (i_sky_luminance_mode == 1)
    {
        // todo: support the i_diffuse_horizontal_illuminance parameter.
        zenith_luminance = i_zenith_luminance;

        // Use the provided luminance distribution function coefficients.
        lumimance_coeffs[0] = i_a;
        lumimance_coeffs[1] = i_b;
        lumimance_coeffs[2] = i_c;
        lumimance_coeffs[3] = i_d;
        lumimance_coeffs[4] = i_e;
    }
    else  // i_sky_luminance_mode == 2
    {
        // todo: implement CIE Clearsky model.
    }
#endif

    // Compute the chromacity at zenith.
    float zenith_chromacity[2];
    compute_zenith_chromacity(turbidity, theta_sun, zenith_chromacity);

    // Compute the coefficients of the chromacity distribution functions.
    float chromacity_x_coeffs[5];
    float chromacity_y_coeffs[5];
    compute_chromacity_x_distrib_coeffs(
        turbidity,
        cos_theta_sun,
        chromacity_x_coeffs);
    compute_chromacity_y_distrib_coeffs(
        turbidity,
        chromacity_y_coeffs);

    if (justSun == 0) {
        // Compute the sky color.
        result =
            compute_sky_color_fakeBlur(
                sun_direction,
                theta_sun,
                cos_theta_sun,
                zenith_luminance,
                lumimance_coeffs,
                zenith_chromacity,
                chromacity_x_coeffs,
                chromacity_y_coeffs,
                direction,
                fakeSkyBlur,
                fakeSkyBlurUpBias);
        result *= below_horiz_factor;
    }

    // Compute the sun color.
    color sun_color =
        compute_sun_color(
            turbidity, theta_sun, cos_theta_sun);

    // Add the sun disk.
    if (i_sun_disk_intensity > 0.0 && i_sun_disk_scale > 0.0)
    {
        color sun =
            compute_sun_disk(
                direction,
                sun_direction,
                turbidity,
                sun_color,
                i_sun_disk_intensity,
                i_sun_disk_scale,
                i_sun_glow_intensity);
        float sunLum = luminance(sun);
        if (sunLum > .9 * i_sun_maxintensity) {
            sun /= sunLum;
            sun *= i_sun_maxintensity * (.9 + .1 *
                smoothstep(i_sun_maxintensity*.9, i_sun_maxintensity, sunLum));
            //sun = (100, 0, 0);
        }
        //printf("\n sunLum = %f", sunLum);
        result += sun;
    }

    // Add the ground plane.
    float sky_amount = 1.0;
    if (justSun == 0 && cos_theta <= 0.0)
    {
        // Compute the lighting on the ground plane.
        color lighting =
            compute_ground_lighting(
                sun_direction,
                theta_sun,
                cos_theta_sun,
                zenith_luminance,
                lumimance_coeffs,
                zenith_chromacity,
                chromacity_x_coeffs,
                chromacity_y_coeffs,
                fakeSkyBlur,
                fakeSkyBlurUpBias
                );

        // Compute the color of the illuminated ground plane.
        color ground = i_ground_color * (lighting + sun_color * cos_theta_sun);

        // Smoothly blend between the ground plane and sky.
        if (i_horizon_blur > 0.0)
        {
            float ground_amount = -cos_theta;
            ground_amount /= i_horizon_blur * 0.1;
            ground_amount = min(ground_amount, 1.0);
            ground_amount = smoothstep(0.0, 1.0, ground_amount);
            result = mix(result, ground, ground_amount);
            sky_amount = 1.0 - ground_amount;
        }
        else
        {
            result = ground;
            sky_amount = 0.0;
        }
    }

    // Rescale the final color.
    color unit_conversion = color(
        i_rgb_unit_conversion[0], i_rgb_unit_conversion[1], i_rgb_unit_conversion[2] );

    if (unit_conversion == 0.0 )
        result *= 1.0 / 80000.0;
    else
        result *= unit_conversion;

    // Apply global multiplier.
    result *= i_multiplier;

    // Apply saturation correction.
    if (saturation <= 0.0)
        result = luminance(result);
    else
    {
        result = mix(luminance(result), max(result, 0.0), saturation);
        result = max(result, 0.0);
    }

    // Apply red/blue shift.
    result[0] *= 1.0 + i_redblueshift;
    result[2] *= 1.0 - i_redblueshift;

    // Apply base light level.
    if (sky_amount > 0.0)
        result = max(result, i_night_color * sky_amount);
    return result;
}

color getPhysicalSky (
    vector dirW;
    vector i_physkySunLightRotation;
    float i_physkyProceduralSamples;
    float i_physkyProceduralBlur;
    float i_haze;
    float i_saturation;
    float i_y_is_up;
    float i_horizon_height;
    float i_horizon_blur;
    //float i_sky_luminance_mode;
    float i_sun_disk_intensity;
    float i_sun_disk_scale;
    float i_sun_glow_intensity;
    float i_sun_maxintensity;
    color i_ground_color;
	float i_rgb_unit_conversion[3];
	float i_multiplier;
	float i_redblueshift;
	color i_night_color;
    string i_physkyGroundTex;
    string i_physkyCloudTex;
    float i_physkyTextureBlur;
    float justSun;
    uniform float fakeSkyBlur;
    float fakeSkyBlurUpBias;

) {
    vector sunDir, dirWtoUse;
    float justSunDb = justSun;
    if (justSunDb == 0) {
        dirWtoUse = dirW;
        point Prot = point (0, 0, 1);
        Prot = rotate(Prot, radians(i_physkySunLightRotation[0]), point 0, point (1, 0, 0));
        Prot = rotate(Prot, radians(i_physkySunLightRotation[1]), point 0, point (0, 1, 0));
        Prot = rotate(Prot, radians(i_physkySunLightRotation[2]), point 0, point (0, 0, 1));
        sunDir = vector Prot;
    } else {
        point Prot = point 0 + dirW;
        Prot = rotate(Prot, radians(-i_physkySunLightRotation[2]), point 0, point (0, 0, 1));
        Prot = rotate(Prot, radians(-i_physkySunLightRotation[1]), point 0, point (0, 1, 0));
        Prot = rotate(Prot, radians(-i_physkySunLightRotation[0]), point 0, point (1, 0, 0));
        Prot = rotate(Prot, radians( -90), point 0, point (1, 0, 0));
        dirWtoUse = vector Prot;
        sunDir = (0, 1, 0);
    }



    point Psamp = point 0 + dirWtoUse;
    color indirect_color = 0;
    float i;
    for (i = 0; i < i_physkyProceduralSamples; i += 1) { 
        vector vRand = vector 1 - 2*(vector random());
        vector perp = vRand^dirWtoUse;
        float ang = random() * i_physkyProceduralBlur * PI/2;
        point PsampRot = rotate(Psamp, ang, point 0, point 0 + perp);
        vector sampDir = PsampRot - (point 0);
        sampDir = normalize(sampDir);
        indirect_color += getPhysicalSkySample (
            sampDir,
            i_haze,
            i_saturation,
            i_y_is_up,
            i_horizon_height,
            i_horizon_blur,
            sunDir,
            i_sun_disk_intensity,
            i_sun_disk_scale,
            i_sun_glow_intensity,
            i_sun_maxintensity,
            i_ground_color,
            i_rgb_unit_conversion,
            i_multiplier,
            i_redblueshift,
            i_night_color,
            justSun,
            fakeSkyBlur,
            fakeSkyBlurUpBias);
    }
    indirect_color /= max(1, i_physkyProceduralSamples);

    color texClr;
    float texAlph, ortho = .5, pwr = .5;
    domeTex(i_physkyGroundTex, i_physkyCloudTex, dirW, ortho, pwr, i_physkyTextureBlur,
       texClr, texAlph);
    float blendByLum = .5;
    indirect_color = mix(indirect_color, texClr, texAlph * mix(1, luminance(texClr), blendByLum));
    return indirect_color;
}
#endif

color getPhysicalSky (
    vector dirW;
    vector i_physkySunLightRotation;
    float i_physkyProceduralSamples;
    float i_physkyProceduralBlur;
    float i_haze;
    float i_saturation;
    float i_y_is_up;
    float i_horizon_height;
    float i_horizon_blur;
    //float i_sky_luminance_mode;
    float i_sun_disk_intensity;
    float i_sun_disk_scale;
    float i_sun_glow_intensity;
    float i_sun_maxintensity;
    color i_ground_color;
	float i_rgb_unit_conversion[3];
	float i_multiplier;
	float i_redblueshift;
	color i_night_color;
    string i_physkyGroundTex;
    string i_physkyCloudTex;
    float i_physkyTextureBlur;
) {
    return getPhysicalSky (
        dirW,
        i_physkySunLightRotation,
        i_physkyProceduralSamples,
        i_physkyProceduralBlur,
        i_haze,
        i_saturation,
        i_y_is_up,
        i_horizon_height,
        i_horizon_blur,
        i_sun_disk_intensity,
        i_sun_disk_scale,
        i_sun_glow_intensity,
        i_sun_maxintensity,
        i_ground_color,
        i_rgb_unit_conversion[3],
        i_multiplier,
        i_redblueshift,
        i_night_color,
        i_physkyGroundTex,
        i_physkyCloudTex,
        i_physkyTextureBlur,
        0,
        0);
}
