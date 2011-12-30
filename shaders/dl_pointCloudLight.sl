class
dl_pointCloudLight(

       	string pointCloudFile = "/tmp/default.ptc";
	       	
       	uniform float enableAmbientOcclusion = 1.0;
       	uniform float enableReflectionOcclusion = 1.0;
		uniform float enableReflection = 1.0;
		uniform float enableRefraction = 1.0;
		uniform float enableSubsurface = 1.0;
		uniform float enableColorBleeding = 1.0;
		
       	uniform float bakeMode = 0.0;
       	uniform float bakeRadiusScale = 1.0;
       	uniform float bakeRadiosity = 0.0;
       	uniform float bakeRaytracing = 0.0;
       	uniform float bakeMultiPassIndex = -1.0;
		string bakeCoordSys = "world";
		
        string __category = "bakelight";
){
	
	public string getFile()
	{
		return pointCloudFile;
	}
	
	
	public float isReadable()
	{
		if (bakeMode < 1)
			return 1;
		else if (bakeMode < 2)
			return 0;

		uniform float doBake = 0;
		attribute("user:ptcbake", doBake);							
		if(doBake == 0)
			return 1;
			
		uniform float bakeIndex = -1;
		attribute("user:ptcbakeindex", bakeIndex);
		if(bakeIndex >= bakeMultiPassIndex)
			return 1;

		return 0;
	}
	
	
	public float isBaking()
	{
		if(bakeMode > 1){
			float doBake = 0;
			attribute("user:ptcbake", doBake);
			if(doBake == 1){
				float bakeIndex = -1;
				attribute("user:ptcbakeindex", bakeIndex);
				if(bakeIndex != bakeMultiPassIndex)
					doBake = 0;
			}
			
			return doBake;
		}

		return bakeMode;
	}
	
	public void light(output vector L; output color Cl;)
    {
    	L = 0;
    	Cl = 0;
    	
		extern point Ps;
	    extern normal Ns;
	    extern vector I;
	    
    	normal Nn = normalize(Ns);
    	
    	float doBake = isBaking();
    	if(doBake){
        	float ray_depth = 0;
        	rayinfo( "depth", ray_depth );
        	if(ray_depth == 0 || bakeRaytracing == 1){
        	
        		string fileName = getFile();
        		uniform float selfOcclude = 1;
                attribute("user:selfOcclude", selfOcclude);
                if (selfOcclude == 0)
                	fileName = lm_replace(fileName, ".ptc", ".noself.ptc");
                	
                if (bakeRadiosity != 0){
                    color radiosity = 1;
                    surface("Ci", radiosity);
                    bake3d(fileName, "", Ps, Nn,
                           "coordsystem", bakeCoordSys,
                           "radiusscale", bakeRadiusScale,
                           "_radiosity", radiosity,
                           "interpolate", 1 );
                }
                else {
                    bake3d(fileName, "", Ps, Nn,
                           "coordsystem", bakeCoordSys,
                           "radiusscale", bakeRadiusScale,
                           "interpolate", 1 );
                }
	        }
    	}
    }
}
