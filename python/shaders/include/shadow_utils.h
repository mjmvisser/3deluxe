#ifndef __shadow_utils_h
#define __shadow_utils_h

// Bertrand Bry-Marfaing

void
generateHammersleyPointSet(float samples;
						   output uniform float sampleCoordX[];
						   output uniform float sampleCoordY[];
						   )
{
	// generate a series of random coordinates

	// note: init of variable size array (although uniform variable in this case) does not compile with prman.
	uniform float iter = 0;

	// find the num of decimals
	uniform float numOfDigits = ceil( log( samples, 2 ) );
	uniform float revBinValues[ numOfDigits ];

	for( iter = 0; iter < samples; iter += 1 )
	{
		// generate binary fractions and their reversed
		uniform float digit = 0;
		uniform float remainder = iter;
		for( digit = (numOfDigits - 1); digit >= 0; digit -= 1 )
		{
			uniform float power = pow( 2, digit );
			if ( remainder >= power  )
			{
				revBinValues[ digit ] = 1;
				remainder -= power;
			}
			else
				revBinValues[ digit ] = 0;
		}

		// convert back to floats
		uniform float x = 0;
		uniform float y = 0;
		uniform float index = 0;
		for( index = 1; index <=  numOfDigits; index += 1 )
		{
			x += ( pow( 2, -index ) * revBinValues[ numOfDigits-index ] );
			y += ( pow( 2, -index ) * revBinValues[ index-1 ] );
		}

		// scale x to compensate for the non-power-of-two sample numbers
		x *= pow( 2, numOfDigits ) / samples ;

		// store coordinates
		sampleCoordX[ iter ] = x;
		sampleCoordY[ iter ] = y;
	}
}

/*
	Function that interprets the previously generated x,y coordinates
	as angle and radius, and retruns the new coordinates.

	Output samples may be denser around 0,0 (for averaging occluder depth)
	or evenly spread (for shadowing sampling )
*/

void
hammersleyToRadial(float seed;
				   float shadowSampling;
				   output float sampleCoordX;
				   output float sampleCoordY;
				   )
{
	// if these samples are for light shadowing sampling
	if ( shadowSampling == 1 ){
		// samples should be evenly distributed
		sampleCoordY = sqrt( sampleCoordY );

		// vary the samples positions per shaded point
		sampleCoordX = mod( sampleCoordX + seed, 1 );
	}

	float angleOfSample = sampleCoordX * 2 * PI;
	sampleCoordX = cos( angleOfSample ) * sampleCoordY; // cos = adj / hypot
	sampleCoordY = sqrt( pow( sampleCoordY, 2 ) - pow( sampleCoordX, 2 ) ); // a2 + b2 = c2
	if( angleOfSample > PI )
		sampleCoordY *= -1;
}

/*
    Function that samples the shadow map,
    returns sampled depth and normalised raster distance of sample
*/

float
sampleShadowMap(uniform string shadowMap;
				float seed;
				float pShadS;
				float pShadT;
				float sampleX;
				float sampleY;
				float radius;
				float uniformSampling;
				output float distFromPs;
				)
{
	// sample coord
	float ss = sampleX;
	float tt = sampleY;
	hammersleyToRadial(seed, uniformSampling, ss, tt);
	ss *= radius;
	tt *= radius;
	ss += pShadS;
	tt += pShadT;

	// find distance from PS coord
	distFromPs = distance( point( pShadS, pShadT, 0), point( ss, tt, 0 ) );

	// sample map without filtering
	// this will generate warnings at compilation time with 3Delight
	return texture(shadowMap, ss, tt,
				   "width", 0.00001 ,
				   "samples", 1);
}

/*
    Function that returns shadow contribution.
*/

float
getShadowMapContribution(varying point PS;
                         uniform string shadowMap;
                         uniform float blur;
                         uniform float filterType;
                         uniform float bias;
                         uniform float samples;
                         uniform float useSoftShadowDecay;
                         uniform float minimumRadius;
                         uniform float maximumRadius;
                         uniform float selfShadowReduce;
                         uniform float shadowDecay;
                         uniform float shadowDecayCutOn;
                         uniform float shadowDecayCutOff)
{
    uniform string filterTypes[] = { "box", "triangle", "gaussian" };

    float unoccluded = 1;

    if (shadowMap != "")
    {
        if (useSoftShadowDecay != 0)
        {
            // Compute soft shadow
            uniform float sampleCoordX[samples];
            uniform float sampleCoordY[samples];
            
            // generate a set of random coordinates
            generateHammersleyPointSet(samples, sampleCoordX, sampleCoordY);
    
            // get the s and t coord of PS on shadowMap
            float pShadS, pShadT;
            uniform matrix shadProjSpace;
            textureinfo(shadowMap, "projectionmatrix", shadProjSpace);
            point shadProjP = transform(shadProjSpace, PS);
            pShadS = (1 + xcomp(shadProjP)) * 0.5;
            pShadT = (1 - ycomp(shadProjP)) * 0.5; 
            
            // get PS distance from shadow plane
            uniform matrix shadCamSpace;
            textureinfo( shadowMap, "viewingmatrix", shadCamSpace);
            point shadCamP = transform(shadCamSpace, PS);
            float PsDepth = zcomp(shadCamP);

            float seed = random();
            
            // get the average occluder depth in shadowMap around PS
            float avrgedDepth = 0;
            float totalWeight = 0;
            float i = 0;
            for (i = 0; i < samples; i += 1)
            {
                float sampleDepth, distFromPs;
                sampleDepth = sampleShadowMap(shadowMap,
                                              seed,
                                              pShadS, pShadT,
                                              sampleCoordX[i],
                                              sampleCoordY[i],
                                              maximumRadius, 0, distFromPs);
                 
                // weight according to raster distance from PS coord
                if ((sampleDepth+bias) < PsDepth)
                {
                    float sampleWeight = 1 - 0.9 * (distFromPs / maximumRadius);
                    totalWeight += sampleWeight;
                    avrgedDepth += (sampleDepth * sampleWeight); 
                }
            }
            if (totalWeight > 0)
                avrgedDepth /= totalWeight;
            
            float shadowValue = 0;
            if(avrgedDepth > 0) // there is an occluder
            {
                // compute the radius of the filter
                float filterRadius = minimumRadius + ( (maximumRadius-minimumRadius) * (1 - (avrgedDepth / PsDepth)) );
                        
                // sample the shadow map with varying filter width
                avrgedDepth = 0;
                totalWeight = 0;
                
                // get the shadow occlusion of PS
                for (i = 0; i < samples; i += 1)
                {
                    float sampleDepth, distFromPs;
                    sampleDepth = sampleShadowMap(shadowMap,
                                                  seed,
                                                  pShadS, pShadT,
                                                  sampleCoordX[i], sampleCoordY[i],
                                                  filterRadius, 1, distFromPs);
                            
                    // add bias cone
                    sampleDepth += bias + (distFromPs * selfShadowReduce); 
                            
                    if (sampleDepth < PsDepth)
                    { 
                        shadowValue += 1;
                        
                        // if shadow decay
                        if (shadowDecay > 0)
                        {
                            // store the occluder depth of the new sampling disc
                            float sampleWeight = 1 - 0.9 * (distFromPs / filterRadius);
                            totalWeight += sampleWeight;
                            avrgedDepth += (sampleDepth * sampleWeight); 
                        }
                    }
                }
                
                shadowValue /= samples;
                
                // decrease light attenuation as PS moves further from occluder
                if (shadowDecay > 0)
                {
                    if (totalWeight > 0) 
                        avrgedDepth /= totalWeight;
                    float distFromOccluder = PsDepth - avrgedDepth;
                    shadowValue *= 1 - (smoothstep(shadowDecayCutOn, shadowDecayCutOff, distFromOccluder) * shadowDecay);
                }
            }    
            
            unoccluded = 1 - shadowValue;
        }
        else
        {
            unoccluded = 1 - shadow(shadowMap, PS,
                                    "blur", blur,
                                    "bias", bias,
                                    "filter", filterTypes[filterType],
                                    "samples", samples);
        }
    }
    
    return unoccluded;
}

/*
    Function that returns shadow contribution using the transmission shadeop.
*/

color
getTracedShadowContribution(varying point PS;
                            point from;
                            uniform float sampleCone;
                            uniform float samples;
                            uniform string subset;
                            uniform float bias)
{
    color tran;
        if (subset == "") {
            tran = transmission(PS, from,
                        "samples", samples,
                        "samplecone", radians(sampleCone),
                        "bias", bias);
        } else {
            tran = transmission(PS, from,
                        "samples", samples,
                        "samplecone", radians(sampleCone),
                        "subset", subset,
                        "bias", bias);
        }
        return tran;
}

/* Superellipse soft clipping
* Input:
*   - point PL on the x-y plane
*   - the equations of two superellipses (with major/minor axes given by
*        a,b and A,B for the inner and outer ellipses, respectively)
* Return value:
*   - 0 if PL was inside the inner ellipse
*   - 1 if PL was outside the outer ellipse
*   - smoothly varying from 0 to 1 in between
*/
float
clipSuperellipse(varying point PL;          /* Test point on the x-y plane */
                 uniform float a, b;       /* Inner superellipse */
                 uniform float A, B;       /* Outer superellipse */
                 uniform float roundness;  /* Same roundness for both ellipses */
                )
{
    float result;
    float x = abs(xcomp(PL)), y = abs(ycomp(PL));
    if (roundness < 1.0e-6) {
        /* Simpler case of a square */
        result = 1 - (1-smoothstep(a,A,x)) * (1-smoothstep(b,B,y));
    } else {
        /* Harder, rounded corner case */
        float re = 2/roundness;   /* roundness exponent */
        float q = a * b * pow (pow(b*x, re) + pow(a*y, re), -1/re);
        float r = A * B * pow (pow(B*x, re) + pow(A*y, re), -1/re);
        result = smoothstep (q, r, 1);
    }
    return result;
}

/* Evaluate the occlusion between two points, P1 and P2, due to a fake
* blocker.  Return 0 if the light is totally blocked, 1 if it totally
* gets through.
*/
float
getBlockerContribution(varying point P1, P2;
                       uniform string blockercoords;
                       uniform float blockerwidth, blockerheight;
                       uniform float blockerwedge, blockerhedge;
                       uniform float blockerround;
                      )
{
    float unoccluded = 1;
    /* Get the surface and light positions in blocker coords */
    point Pb1 = transform (blockercoords, P1);
    point Pb2 = transform (blockercoords, P2);
    /* Blocker works only if it's straddled by ray endpoints. */
    if (zcomp(Pb2)*zcomp(Pb1) < 0) {
        vector Vlight = (Pb1 - Pb2);
        point Pplane = Pb1 - Vlight*(zcomp(Pb1)/zcomp(Vlight));
        unoccluded *= clipSuperellipse (Pplane, blockerwidth, blockerheight,
                blockerwidth+blockerwedge,
                blockerheight+blockerhedge,
                blockerround);
    }
    return unoccluded;
}

/* same as above but using a placement matrix instead of a C.S.
 */


float
getBlockerContributionMx(varying point P1, P2;
                        matrix placementMatrix;
                        uniform float blockerwidth, blockerheight;
                        uniform float blockerwedge, blockerhedge;
                        uniform float blockerround;
                      )
{
    float unoccluded = 1;
    /* Get the surface and light positions in blocker coords */
    varying point Pw1 = transform("world",P1);
    varying point Pw2 = transform("world",P2);

    varying point Pb1 = transform (placementMatrix, Pw1);
    varying point Pb2 = transform (placementMatrix, Pw2);

    /* Blocker works only if it's straddled by ray endpoints. */
    if (zcomp(Pb2)*zcomp(Pb1) < 0) {
        vector Vlight = (Pb1 - Pb2);
        point Pplane = Pb1 - Vlight*(zcomp(Pb1)/zcomp(Vlight));
        unoccluded *= clipSuperellipse (Pplane, blockerwidth, blockerheight,
                blockerwidth+blockerwedge,
                blockerheight+blockerhedge,
                blockerround);
    }
    return unoccluded;
}


/*  This is the entire "guts" of the dl_shadowCollector node.
It is wrapped into a function so that it can also be used by
the flat dl_shadowCollector.sl surface shader.
*/
/*
MOVED TO dl_shadowCollector.py
void dl_shadowCollector_getShadows (
	// Inputs
	//
	uniform float mute;
	uniform float contribution;
	float intensity;
	uniform float lightType;
	uniform float showInBty;
	color shadClr;
	float shadOpac;
	float hemispheres;
	float hemisphereFalloff;
	normal normalCamera;
	// Outputs
	//
	output color dlOutOpacity;
	output color dlOutIncandescence;
	output color dlOutShadow;
	output color dlOutOcclusion;

) {

    if (mute == 0) {
        extern point P;
        extern vector I;

        color indirectShad = 0;
        color directShad = 0;
        float hemisphereFalloff = 0;

        // handle subsurface scattering
        uniform string raytype = "unknown";
        rayinfo("type", raytype);
        if (raytype != "subsurface")
        {
            vector In = normalize(I);
            normal Nn = normalize(normalCamera);
            normal Nf = Nn;//ShadingNormal(Nn);
            vector V = -In;
        
            // shadowCollector is kinda diffuse
            uniform string category = "";
            if (lightType == 0)
                category = "diffuse&-indirect";
            else if (lightType == 1)
                category = "diffuse";
            else if (lightType == 2)
                category = "indirect";
            
            color occluded = 0;
            color shadowColor = 0;
            illuminance(category, P, Nf, hemispheres*PI/2,
                        "lightcache", "reuse",
                        "light:__occluded", occluded,
                        "light:__shadowColor", shadowColor)
            {
                string cat = "";
                lightsource("__category", cat);
                if (match("indirect", cat)) {
                    indirectShad = max(indirectShad, occluded) * intensity;
                } else {
                    float ang = acos(normalize(L).Nf);
                    ang = ang/PI;
                    float falloff = 1-smoothstep(hemispheres-hemisphereFalloff, hemispheres, 2*ang);
                    directShad = max(directShad, falloff*occluded) * intensity;
                    // This allows us to visualize the hemispheres of multiple lights.
                    hemisphereFalloff = mix(hemisphereFalloff, 1, falloff*.5);
                }
            }
        }
        
        // Add directShad and indirectShad because they are subtracted in dl_ultra.
        color bty;
        
        if (showInBty == 4 ) {
            // If showInBty == 4, rgb = 0, alpha = Direct + Indirect:  shadows are in alpha.
            bty = directShad + indirectShad + shadClr;
            dlOutOpacity = (directShad + indirectShad) * shadOpac;
        } else {
            bty = directShad + indirectShad +
            (showInBty == 0 ?
                (luminance(directShad), luminance(indirectShad), hemisphereFalloff):
            showInBty == 1 ? directShad + indirectShad :
            showInBty == 2 ? directShad : indirectShad
            ) * (shadOpac, shadOpac, 1);
            dlOutOpacity = 1;
        }

        bty *= contribution;

        dlOutIncandescence = bty;
        dlOutShadow = directShad * contribution;
        dlOutOcclusion = indirectShad * contribution;
    } else { // end of if (mute == 0)
        dlOutOpacity = 1;
    }
}
*/
#endif
