#ifndef __ray_utils_h
#define __ray_utils_h

float
getRaySamples(
		uniform float samples
		)
{
    uniform float factor;
    uniform float outsamples;
    if( option("user:tracebreadthfactor", factor) == 1 )
    {
    	outsamples = floor(samples * factor + .5);
    }
    else
    	outsamples = samples;

    if( option("user:tracedepthfactor", factor) == 1 && factor != 1 )
    {
    	uniform float depth;
    	rayinfo("depth", depth);
    	if( depth > 0 )
    	{
    		factor = pow(factor, depth);
    		outsamples = floor(factor * outsamples + .5);
    	}
    }
    return outsamples;
}

void
shapeSamples(
		string shape;
		uniform float samples;
		uniform float length;
		uniform float radiusheight;
		output uniform float nsamples;
		output uniform float msamples;
		)
{
    if (shape == "disk")
	{
		nsamples = floor(sqrt(samples));
		msamples = floor(samples/nsamples);
	}
	else if (shape == "line")
	{
		nsamples = samples;
		msamples = 1;
	}
	else if (shape == "cylinder")
	{
		/* Choose stratification: angle, z, or both.  (If the light source is
		 undergoing a non-uniform scaling, this choice might not be optimal.) */
		if (length < 0.2 * radiusheight)
		{
			/* cylinder is rather flat */
			nsamples = samples;
			msamples = 1;
		}
		else if (length> 5 * radiusheight)
		{
			/* cylinder is rather skinny */
			nsamples = 1;
			msamples = samples;
		}
		else
		{
			/* cylinder neither flat nor skinny */
			nsamples = floor(sqrt(samples));
			msamples = floor(samples/nsamples);
		}
	}
	else if (shape == "rectangle")
	{
		/* Choose best stratification: x, y, or both.  (If the light source is
		 undergoing a non-uniform scaling, this choice might not be optimal.) */
		if (length> 4 * radiusheight)
		{
			nsamples = samples;
			msamples = 1;
		}
		else
		if (radiusheight> 4 * length)
		{
			nsamples = 1;
			msamples = samples;
		}
		else
		{
			nsamples = floor(sqrt(samples));
			msamples = floor(samples/nsamples);
		}
	}
	else
	{
		/* sphere */
		nsamples = floor(sqrt(samples));
		msamples = floor(samples/nsamples);
	}
}

point
pointOnShape(
		string shape;
		uniform float length;
		uniform float radiusheight;
		uniform float n;
		uniform float nsamps;
		uniform float m;
		uniform float msamps;
		)
{
    point p;
    if (shape == "disk")
    {
        /* Compute uniformly distributed point (x,y) on unit disc */
        float angle = 2 * PI * (n + random()) / nsamps;
        float r = radiusheight * sqrt((m + random()) / msamps);
        /* Compute point p on rectangle */
        p = point "shader" (r * cos(angle), r * sin(angle), 0);
    }
    else if (shape == "line")
    {
        p = point "shader" (length * (n + random()) / nsamps, 0, 0);
    }
    else if (shape == "cylinder")
    {
        /* Compute stratified random angle in [0,2pi] */
        float angle = 2 * PI * (n + random()) / nsamps;
        /* Compute stratified random x on (0,length) */
        float x = length * (m + random()) / msamps;
        /* Compute point p on cylinder */
        p = point "shader" (x, radiusheight * cos(angle), radiusheight * sin(angle));
    }
    else if (shape == "rectangle")
    {
		float x, y;
		x = (n + random()) / nsamps;
        y = (m + random()) / msamps;
        /* Compute point p on rectangle */
        p = point "shader" ((x - 0.5) * length, (y - 0.5) * radiusheight, 0);
    }
    else
    {
    	/* sphere */
        /* Compute stratified random angle in [0,2pi] */
    	float angle = 2 * PI * (n + random()) / nsamps;
    	/* Compute stratified random z in [-1,1] */
        float z = 2 * ((m + random()) / msamps) - 1;
        /* Compute point p on sphere */
        float r = radiusheight * sqrt(1 - z*z);
        p = point "shader" (r * cos(angle), r * sin(angle), z);
    }
    return p;
}

/*
 * Build a set of four vectors around a center vector
 * This is necessary for making environment calls inside
 * of a gather loop. If we just used a single vector,
 * we would get derivative information based on neighboring
 * grids, which is not what we want. Instead, we want to
 * do a lookup on a patch of the environment that is inversely
 * related to the number of samples we are using.
 *
 * spread is the halfwidth of the patch we are using
 *
 * This is calculated as a separate function so that it can be
 * called outside of the gather loop (for the sake of optimization).
 */

float
calculateEnvSampleArea(
    float hemisphere;
    float numSamples;
    )
{
    return 0.5 * (hemisphere / numSamples);
}

void
buildEnvironmentVectors(
    float spread;
    vector dir;
    output vector v1;
    output vector v2;
    output vector v3;
    output vector v4;
    )
{
    vector udir, vdir, wdir;

    // construct basis vectors
    if (abs(xcomp(dir)) > 0 || abs(ycomp(dir)) > 0)
    {
		// dir ^ z (if valid)
		udir = normalize(vector (ycomp(dir), -xcomp(dir), 0));
    }
    else
    {
		// dir ^ x
		udir = normalize(vector (0, zcomp(dir), -ycomp(dir)));
    }

    // vdir is dir ^ u
    vdir = normalize(dir ^ udir);

    // calculate four directions
    vector uspread = spread*udir;
    vector vspread = spread*vdir;
    vector ndir = normalize(dir);

    v1 = ndir - uspread - vspread;
    v2 = ndir + uspread - vspread;
    v3 = ndir - uspread + vspread;
    v4 = ndir + uspread + vspread;
}



void getTraceOrGather(point pt; vector ray; string label; uniform float method; uniform float maxDistance; float samples; uniform float bias; float blur; string subset; output color outColor; output float outDistance; output color outTransmission;)
{
	uniform float xsamples = getRaySamples(samples);
	outTransmission = 1;
	if (method == 0) {
		outColor = trace( pt, ray, outDistance,
								"transmission", outTransmission,
								"subset", subset,
								"maxdist", maxDistance,
								"samplecone", blur*radians(5),
								"samples", xsamples,
								"bias", bias,
								"label", label);
	}
	else {
		// Gather
		color Cvol = -1;
		color Csurf = -1;
		gather("illuminance", pt, ray,
			   blur*radians(5), xsamples,
			   "distribution", "cosine",
			   "subset", subset,
			   "maxdist", maxDistance,
			   "bias", bias,
			   "label", label,
			   "surface:Ci", Csurf,
			   "volume:Ci", Cvol){
			outColor += luminance(Cvol) < 0 ? Csurf : Cvol;
			outTransmission = 0;
		}
		outColor /= xsamples;
	}
}

#endif /* __ray_utils_h */
