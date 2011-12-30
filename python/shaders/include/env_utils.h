#ifndef _env_utils_h
#define _env_utils_h

#include <remap_utils.h>

void
getEnvironmentReflection (point P;
						 normal N;
						 vector R;
						 float blur;
						 float sblur;
						 float tblur;
						 uniform string filter;
                         float physicalSkySamps;
                         float occConeAngle;
                         float occSamples;
						 output color col;
						)
{
	uniform string map = "";
	uniform string coordsys = "";
    float occluded = 0;
    uniform color occlusionColor = 0;
	uniform float exposure = 0;
	uniform float gamma = 1;
	uniform float offset = 0;
	illuminance ("environment", P, N, PI/2,
                 "send:light:__occConeAngleMult", occConeAngle,
                 "send:light:__occSamplesMult", occSamples,
                 "send:light:__physkyBlur", blur,
                 "send:light:__physkySamps", physicalSkySamps,
				 "send:light:__envDir", R,
				 "light:__map", map,
				 "light:__coordsys", coordsys,
				 "light:__occlusion", occluded,
				 "light:__occlusionColor", occlusionColor,
				 "light:__exposure", exposure,
				 "light:__gamma", gamma,
				 "light:__offset", offset,
				 "lightcache", "reuse")
	{
		color envcolor = 1;
		if (map != "")
		{
			vector dir;
			if (coordsys != "")
				dir = normalize(vtransform(coordsys, R));
			else
				dir = normalize(vtransform("world", R));

			if(sblur > 0 && tblur > 0)
				envcolor = environment(map, dir,
									   "sblur", max(0, sblur),
									   "tblur", max(0, tblur),
									   "filter", filter);
			else
				envcolor = environment(map, dir,
									   "blur", max(0, blur),
									   "filter", filter);

			envcolor = remapHDRI(exposure, gamma, offset, envcolor);
		}

        // col += mix(occlusionColor, Cl * envcolor, (1-occluded));
        // Don't do the above mixing yet, refl occl will be applied with getReflectionOcclusion.
		col += Cl * envcolor;
	}
}

void
getEnvironmentReflection (point P;
						 normal N;
						 vector R;
						 float blur;
						 float blurs;
						 float blurt;
						 uniform string filter;
                         float physicalSkySamps;
						 output color col;
						)
{
    getEnvironmentReflection (P,
                             N,
                             R,
                             blur,
                             blurs,
                             blurt,
                             filter,
                             physicalSkySamps,
                             1,
                             1,
                             col);
}


string
getEnvironmentMap(point P;
                  normal N;
                  )
{
    uniform string map = "";
    illuminance ("environment", P, N, PI/2,
                 "light:__map", map,
                 "lightcache", "reuse")
    {
        // do nothing
    }
    
    return map;
}

void
getReflOccAndSampMult(point P;
                       normal N;
                       vector R;
                       float occConeAngle;
                       float occSamples;
                       output float occluded; 
                       output color occlusionColor;
                       output uniform float traceSamplesMult; 
                       )
{
    occluded = 0;
    occlusionColor = 0;
    float useAmbientOcclusion = 0;

    // We must use temporary variables as arguments to illuminance()
    // and assign the passed messages inside the illuminance block
    // to avoid getting junk values from non-"environment" lights.
    illuminance ("environment", P, N, PI/2,
                 "send:light:__occConeAngleMult", occConeAngle,
                 "send:light:__occSamplesMult", occSamples,
                 "lightcache", "reuse")
    {
    	 float occludedFromLt = 0;
    	 color occlusionColorFromLt = 0;
    	 uniform float traceSamplesMultFromLt = 0;

    	 lightsource("__occlusion", occludedFromLt);
		 lightsource("__occlusionColor", occlusionColorFromLt);
		 lightsource("__traceSamplesMult", traceSamplesMultFromLt);

		 occluded += occludedFromLt;
		 occlusionColor += occlusionColorFromLt;
		 traceSamplesMult += traceSamplesMultFromLt;

		 lightsource("__useAmbientOcclusion", useAmbientOcclusion);
    }

    if (useAmbientOcclusion > 0) {
        illuminance("indirect", P, N, PI/2,
                    "lightcache", "reuse")
        {
            // Each surface should not be illuminated by more than one
            // indirect light, so no need to sum these.
            color occludedClr = 0;
            lightsource("__occluded", occludedClr);
            occluded = luminance(occludedClr);
        }
    }
}

float getPointCloudFiles(string type; string first; output string ptcFiles[])
{
	if(first != "")
		push(ptcFiles, first);

	shader lights[] = getlights("category", "bakelight");
	uniform float nblights = arraylength(lights), i;
	for(i = 0; i < nblights; i += 1){
		uniform float read = lights[i]->isReadable();
		if(lights[i]->isBaking() == 0 && lights[i]->isReadable() == 1){
			uniform float enabled = 0;
			getvar(lights[i], format("enable%s", type), enabled);
			if(enabled){
				string ptcFile = lights[i]->getFile();
				if(ptcFile != "")
					push(ptcFiles, ptcFile);
			}
		}
	}

	return arraylength(ptcFiles);
}

// A hacky way of softly clamping to - but never reaching - a limit.
float asymptote(float limit, buffer, v) {
    float result = v;
    float mxMinusO = limit-buffer;
    if (v > mxMinusO) {
        float arbitrarySlopeCorrector = .8;
        result = mxMinusO + buffer*atan((v-(mxMinusO))/
            (arbitrarySlopeCorrector*buffer))/(PI/2);
    }
    return result;
}

void clampToMaxIntens(float maxIntensity, buffer; output color col) {
    color c = ctransform("rgb", "hsv", col);
    c[2] = asymptote(maxIntensity, buffer, c[2]);
    col = ctransform("hsv", "rgb", c);
}


#endif
