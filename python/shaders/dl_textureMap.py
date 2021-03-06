import deluxe

class dl_textureMap(deluxe.Texture2D):
    typeid = 0x00370001
    description = "Wrapper around 3Delight \"texture\" function"
    
    textureName = deluxe.Image(storage='uniform',
                                help="""Texture file in tdl format. Use 'N' or 'NNNN' for the
                                        frame number if using indexed sprites.""")
    indexedSprites = deluxe.Boolean(help="Treat the filename as a sequence indexed with spritePP.")
    blur = deluxe.Float(default=0, min=0, softmax=0.2, storage='uniform',
                         help="""Specifies an additional length to be added to texture
                                 lookup region in both s and t, expressed in units of texture
                                 coordinates (range = [0..1]). A value of 1.0 would request that
                                 the entire texture be blurred in the result.""")    
    filterType = deluxe.Enum(default='Gaussian',
                              choices=['Box', 'Triangle', 'Gaussian'],
                              storage='uniform',
                              help="Specifies the reconstruction filter to use when accessing the texture map.");   
    samples = deluxe.Integer(default=4, storage='uniform',
                              help="(Box filter only) Number of samples.")
    gamma = deluxe.Float3(default=1, min=0.0001, max=3,
                           help="Gamma correction to apply to the texture.")
   
    gammaCorrection = deluxe.Group([gamma])
    
    spriteNumPP = deluxe.Integer(default=0, storage='uniform', message=True)

    coordsys = deluxe.CoordinateSystem(help="""
        Coordinate system (or camera) in which to look up texture.
        Use a delightCoordinateSystem shape name (eg. delightCoordinateSystemShape1)
        or mayaCamera:cameraName (eg. "mayaCamera:persp", NOT "mayaCamera:perspShape").
        """)

    alphaInsideUVMult = deluxe.Float(shortname="aism", default=1, help="""
        Multiply the alpha by this value where the surface is inside the UV coordinates
        (ie. u and v are > 0 and < 1).
        """)

    alphaInsideUVOffset = deluxe.Float(shortname="aiso", default=0, help="""
        Add this value to the alpha where the surface is inside the UV coordinates
        (ie. u and v are > 0 and < 1).
        """)

    specifyAlphaOutsideUV = deluxe.Boolean(default=False, help="""
            If on, alpha will be set to alphaOutsideUV value where the surface is
            outside the UV coordinates (ie. u or v is > 1 or < 0).""")


    alphaOutsideUV = deluxe.Float(shortname="aos", default=0,
        help="""If specifyAlphaOutsideUV is on, this is the alpha where the
            surface is outside the UV coordinates (ie. u or v is > 1 or < 0).""")

    alphaCorrection = deluxe.Group([alphaInsideUVMult, alphaInsideUVOffset, specifyAlphaOutsideUV, alphaOutsideUV])

    warpMode = deluxe.Enum(shortname='wm', default='Off', choices=['Off', 'Noise','Input'])
    warpNoiseAmount = deluxe.Float2(shortname='wna', default=1)
    warpNoiseFreq = deluxe.Float2(shortname='wnf', default=1)
    warpNoiseOffset = deluxe.Float2(shortname='wno', default=0)
    warpInput = deluxe.Float2(shortname='wi', default=0)
    warp = deluxe.Group([ warpMode, warpNoiseAmount, warpNoiseFreq, warpNoiseOffset, warpInput]) 

    rsl = """    
        void warpST(
            float warpMode;
            float warpNoiseAmount[2];
            float warpNoiseFreq[2];
            float warpNoiseOffset[2];
            float warpInput[2];
            output float ss, tt)
        {
            if (warpMode == 1) {
                float ss0 = ss;
                float tt0 = tt;
                ss += (1-2*noise((tt0 + warpNoiseOffset[0])*warpNoiseFreq[0]))*warpNoiseAmount[0];
                tt += (1-2*noise((ss0 + warpNoiseOffset[1])*warpNoiseFreq[1]))*warpNoiseAmount[1];
            } else if (warpMode == 2) {
                ss += warpInput[0];
                tt += warpInput[1];
            }
        }

        uniform float num_channels;
        textureinfo(i_textureName, "channels", num_channels);
     
        uniform string filterName= "gaussian";
        
        if (i_filterType == 0)
        {
            filterName = "box";
        }
        else if (i_filterType == 1)
        {
            filterName = "triangle";
        }

        // Coordinate system.
        if (i_coordsys != "") {
            extern point P;
            point Pw = transform("world", P);

            point Ptex = transform(i_coordsys, P);
            Ptex = transform("world", Ptex);

            Ptex = transform("current", "world", P);
            Ptex = transform(i_coordsys, "current", Ptex);

            uniform float frameFormat[3];
            option( "Format", frameFormat );
            float frameAR = frameFormat[0] / frameFormat[1];

            ss = Ptex[0]/2 + .5;
            tt = Ptex[1]*frameAR/2 + .5;
            tt = 1-tt;
        }
   
        uniform string tex = i_textureName;
        if (i_indexedSprites != 0)
        {
            uniform string template = i_textureName;
            template = dl_replace(template, ".NNNN.", ".%04d.");
            template = dl_replace(template, ".N.", ".%d.");

            extern uniform float spriteNumPP;
            tex = format(template, spriteNumPP);
        }

        warpST( i_warpMode, i_warpNoiseAmount, i_warpNoiseFreq, i_warpNoiseOffset,
            i_warpInput, ss, tt);
         
        if (num_channels == 1)
        {
            o_outColor = float texture(tex, ss, tt, 
                                       "blur", i_blur,
                                       "samples", i_samples,
                                       "filter", filterName,
                                       "fill", 1);
        } 
        else 
        {
            o_outColor = texture(tex, ss, tt, 
                                 "blur", i_blur, 
                                 "samples", i_samples,
                                 "filter", filterName,
                                 "fill", 1);
        }
    
        // apply gamma correction
        o_outColor = color(pow(comp(o_outColor, 0), 1.0 / i_gamma[0]),
                           pow(comp(o_outColor, 1), 1.0 / i_gamma[1]),
                           pow(comp(o_outColor, 2), 1.0 / i_gamma[2]));

    
        if (i_specifyAlphaOutsideUV == 1 && (ss > 1 || ss < 0 || tt > 1 || tt < 0))
        {
            o_outAlpha = i_alphaOutsideUV;
        } else {
            if (num_channels > 3)
            {
                o_outAlpha = texture(tex[3], ss, tt, 
                                     "blur", i_blur,
                                     "samples", i_samples,
                                     "filter", filterName,
                                     "fill", 1);
            } 
            else 
            {
                o_outAlpha = luminance(o_outColor);
            }
            o_outAlpha = o_outAlpha * i_alphaInsideUVMult + i_alphaInsideUVOffset;
        }
    """
    
       
def initializePlugin(obj):
    dl_textureMap.register(obj)

def uninitializePlugin(obj):
    dl_textureMap.deregister(obj)
