import delight

class dl_shadowBlocker(delight.Utility):
    typeid = 0x00300201
    includes = ["shadow_utils.h"]
    
    color = delight.Color(default=0, storage='varying',help="Color to tint the fake shadow.", prepare=True)
    intensity = delight.Float(default=1, storage='uniform',help="Intensity of the fake shadow.", prepare=True)
    placementMatrix = delight.Matrix(notemplate=True,help="Placement Matrix of the fake shadow.")
      
    width = delight.Float(storage='uniform',default=1, help="Width of the blocker's superellipse.")
    height = delight.Float(storage='uniform',default=1, help="Height of the blocker's superellipse.")
    wedge = delight.Float(storage='uniform',shortname='wg', default=0.1, help="Defines horizontal edge fuzziness.")
    hedge = delight.Float(storage='uniform',shortname='hg', default=0.1, help="Defines vertical edge fuzziness.")
    roundness = delight.Float(default=1,storage='uniform', 
                              help="""controls how rounded the corners of the superellipse are.  
                                      If this value is 0, the cross-section will be a perfect rectangle.
                                      If the value is 1, the cross-section will be a perfect circle.""")

    cutOn = delight.Float(shortname='con',storage='uniform', default=0.01, help="Cut-on setting from light.",notemplate = True)
    parallelRays = delight.Boolean(default=False,storage='uniform', help="Parallel rays setting from light.",notemplate = True,connectable = True)

    outColor = delight.Color(output=True)
    outAlpha = delight.Float(output=True)
    
    rslprepare = \
    """
    extern point Ps;
    extern point P;
    extern float ss;
    extern float tt;

    point PsXf = transform("world", Ps);
    PsXf = transform(i_placementMatrix, PsXf);
    point PXf = transform("world", P);
    PXf = transform(i_placementMatrix, PXf);
    vector PtoPsXf = PsXf - PXf;
    // Intersect the ray from light to surface point with i_placementMatrix's xy plane (z=0).
    point Ptex = PXf - PtoPsXf * zcomp(PXf)/zcomp(PtoPsXf);
    ss =.5 + .5 * Ptex[0];
    tt =.5 + .5 * Ptex[1];
    """

    rsl = \
    """
    extern point Ps;

    point Pl = transform ("shader", Ps);

    point shadoworigin;
    if (i_parallelRays == 0) {
        shadoworigin = point "shader" (0,0,0);
    } else {
        shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
    }

    float unoccluded = pow(getBlockerContributionMx(Ps, shadoworigin, 
                                                    i_placementMatrix,
                                                    i_width, i_height,
                                                    i_wedge, i_hedge,
                                                    i_roundness), i_intensity);
     
   
    o_outColor = 1 - ((1 - unoccluded) *(1- i_color) *i_intensity);
    o_outAlpha = unoccluded;
    """

    
def initializePlugin(obj):
    dl_shadowBlocker.register(obj)

def uninitializePlugin(obj):
    dl_shadowBlocker.deregister(obj)
    
