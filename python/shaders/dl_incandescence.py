import deluxe

class dl_incandescence(deluxe.ShadingComponent):
    typeid = 0x0030000a
    description = "Simple incandescence to simulate internal illumination."
    
    bakeIncomingColor = deluxe.Enum(
                            help="""
                                To bake a color or float to a 2d texture using uv
                                coordinates, plug the output from a hypershade node
                                into the Color parameter, set this to 'As color' or
                                'As float' and specify a path in the Bake File parameter.
                                To ensure that the baked color does not contribute to the
                                beauty pass, set Intensity and/or Contribution to 0.
                                """, default='Off',
                            choices=['Off', 'As color', 'As float (luminance)']
                            )
    bakeFile = deluxe.String (help="""
                                File to bake 2d texture to.  The .bake suffix is
                                recommended, then do tdlmake filename.bake filename.tdl.
                            """, default="bakedColor.bake")
    method = deluxe.Enum(default='Uniform',
                          choices=['Uniform', 'Facing', 'Edge', 'Light'],
                          storage='uniform',
                          help="Method of incandescence approximation")
    shape = deluxe.Float(default=1, storage='uniform',
                          help='Shape of falloff (for "Edge" and "Facing" methods). Values above 1 falloff sooner. Values below 1 fall off later.')

    rsl = \
    """
    
    extern float s;
    extern float t;
        
    // bake incoming color.
    if (i_bakeIncomingColor > 0) {
        if (i_bakeIncomingColor == 1) {
            bake(i_bakeFile, s, t, i_color);
        } else {
            float lum = luminance(i_color);
            bake(i_bakeFile, s, t, lum);
        }
    }
        
    color col = surfaceColor * globalIntensity;

    if( i_method != 3 ) {
    	if( i_method != 0 ) {
    	    float facing = max(Nf.V, 0);
    	    if( i_method == 2 ) {
        		facing = sqrt(1 - facing*facing);
    	    }
    	    col *= pow(facing, i_shape);
    	}
    }
    else {
    	float lum = 0;
    	uniform vector vec = (.3,.59,.11);
    	illuminance("-environment&-indirect&-bakelight", P, Nf, PI/2,
            	    "lightcache", "reuse") {
    	    lum += vec.vector(Cl);
    	}
    	col *= lum;
    }
    
    o_output_incandescence = col;
    o_output_beauty = col;
    """


def initializePlugin(obj):
    dl_incandescence.register(obj)

def uninitializePlugin(obj):
    dl_incandescence.deregister(obj)
