#ifndef __component_utils_h__
#define __component_utils_h__


/* 	Macro used in all shading component to loop through lighsets
	Very important and core to the dl_layer aov mechanism
	Index 0 is always reserved for lights with no lightset_* category,
	i.e. default lightset. Users of this are responsible to set their categories
	and outputs using defined variables (LIGHTSET_INDEX, LIGHTSET_CATEGORY, etc...)
*/
#define BEGIN_LIGHTSET_LOOP(OUTARRAY) \
	uniform float LIGHTSET_INDEX; \
	uniform float LIGHTSET_COUNT = arraylength(OUTARRAY); \
	string LIGHTSET_SKIPPED = ""; \
	for(LIGHTSET_INDEX = LIGHTSET_COUNT - 1; LIGHTSET_INDEX >= 0; LIGHTSET_INDEX -= 1) \
	{ \
		string LIGHTSET_ATTRIBUTE = format("lightset_%d", LIGHTSET_INDEX); \
		string LIGHTSET_NAME = ""; \
		string LIGHTSET_CATEGORY = ""; \
		if(LIGHTSET_INDEX != 0) \
		{ \
			LIGHTSET_NAME = LIGHTSET_ATTRIBUTE; \
			attribute(format("user:%s", LIGHTSET_ATTRIBUTE), LIGHTSET_NAME); \
			LIGHTSET_SKIPPED = format("%s&-%s", LIGHTSET_SKIPPED, LIGHTSET_NAME); \
			LIGHTSET_CATEGORY = format("&%s", LIGHTSET_NAME); \
		} \
		else \
		{ \
			LIGHTSET_NAME = LIGHTSET_SKIPPED; \
			LIGHTSET_CATEGORY = format("%s", LIGHTSET_NAME); \
		}

#define END_LIGHTSET_LOOP } /* This closes the brace above. */


/*
	isBakingRadiosity

	Returns true if point cloud lights in write mode found
*/
float isBakingRadiosity()
{
    shader lights[] = getlights("category", "bakelight");
    uniform float nblights = arraylength(lights), i;
    for(i = 0; i < nblights; i += 1)
    	if(lights[i]->isBaking() > 0)
    		return 1;
    return 0;
}


/*
	ShadingNormal

	A wrapper for faceforward which avoids faceforward for single-sided
	primitives or when using double-sided shading. This is to prevent artefacts
	around silhouette edges caused by the way "Sides 2" is usually shaded. Note
	that we don't explicitly check for double-sided shading as it also sets
	Sides to 1.
*/
normal ShadingNormal( normal i_N )
{
	extern vector I;
	normal Nf = i_N;

	uniform float sides = 2;
	attribute("Sides", sides);

	if( sides == 2 )
	{
        uniform float disableFaceforward = 0;
        attribute("user:disableFaceforward", disableFaceforward);
        extern point P;

    	// Disable faceforward if there are any bakelights in the scene.
        if (isBakingRadiosity() > 0)
        	disableFaceforward = 1;

		if (disableFaceforward == 0) {
            Nf = faceforward(Nf, I);
        } else {
            uniform float reverseN = 0;
            attribute("user:reverseN", reverseN);
            if (reverseN == 1) Nf = -Nf;
        }
	}
	else
	{
		/* This mess is to flip the normals of polygon meshes with reversed
		   orientation. We only want it when 'N' is attached to the primitive. */
		uniform float geometricnormal = 1;
		attribute( "geometry:geometricnormal", geometricnormal );

		if( geometricnormal == 0 )
		{
			uniform string orientation;
			attribute( "Ri:Orientation", orientation );
			if( orientation == "outside" )
				Nf = -Nf;
	   }
	}

	return Nf;
}




#endif
