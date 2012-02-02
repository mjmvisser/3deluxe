import deluxe

class dl_blocker(deluxe.Utility):
    typeid = 0x00300201
    includes = ["shadow_utils.h"]
    
    color = deluxe.Color(default=1, storage="varying",help="Color to tint the fake shadow.", prepare=True)
    intensity = deluxe.Float(default=1, storage="varying",help="Intensity of the fake shadow.", prepare=True)
    coordsys = deluxe.CoordinateSystem(default="", shortname="cs", label="coordinateSystem")
      
    width = deluxe.Float(storage="uniform", default=1, help="Width of the blocker's superellipse.")
    height = deluxe.Float(storage="uniform", default=1, help="Height of the blocker's superellipse.")
    wedge = deluxe.Float(storage="uniform", shortname="wg", default=0.1, help="Defines horizontal edge fuzziness.")
    hedge = deluxe.Float(storage="uniform", shortname="hg", default=0.1, help="Defines vertical edge fuzziness.")
    roundness = deluxe.Float(default=1,storage="uniform", 
                              help="""Controls how rounded the corners of the superellipse are.  
                                      If this value is 0, the cross-section will be a perfect rectangle.
                                      If the value is 1, the cross-section will be a perfect circle.""")

    cutOn = deluxe.Float(shortname="con", storage="uniform", default=0.01, help="Cut-on setting from light.",
                          notemplate=True, connectable=True)
    lightType = deluxe.Enum(default='Spot', choices=['Spot', 'Point', 'Distant'], help="Light type setting from light.",
                             notemplate=True, connectable=True)

    blockerColor = deluxe.Color(output=True, notemplate=True, hidden=True)
    blockerValue = deluxe.Float(output=True, notemplate=True, hidden=True)
    
    blocker = deluxe.Compound([blockerColor, blockerValue], notemplate=True)
    
    rslprepare = \
    """
    extern point Ps;
    extern point P;
    extern vector L;
    extern float ss;
    extern float tt;

    if (i_coordsys != "")
    {
        point Pl = transform ("shader", Ps);
    
        point shadoworigin;
        if (i_lightType == 2) { // Parallel rays
            shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
        } else {
            shadoworigin = point "shader" (0,0,0);
        }

        vector sAx = normalize(vtransform(i_coordsys, "current", vector (1, 0, 0)));
        vector tAx = normalize(vtransform(i_coordsys, "current", vector (0, 1, 0)));
        point cOrg = transform(i_coordsys, "current", point (0, 0, 0));

        vector soToP = Ps - shadoworigin;
        vector Nplane = sAx^tAx;
        
        float t = ((-Nplane).(shadoworigin-cOrg)) / (Nplane.(Ps - shadoworigin));
        point Pint = shadoworigin + t*(shadoworigin-Ps);

        vector cOrgToPint = Pint - cOrg;
        point PintCs = transform(i_coordsys, Pint);
        float sBk = (1+PintCs[0])/2;
        float tBk = 1-(1+PintCs[1])/2;
        
        ss = sBk;
        tt = tBk;
    }
    """

    rsl = \
    """
    extern point Ps;

    point Pl = transform ("shader", Ps);

    point shadoworigin;
    if (i_lightType == 2) { // Parallel rays
        shadoworigin = point "shader" (xcomp(Pl), ycomp(Pl), i_cutOn);
    } else {
        shadoworigin = point "shader" (0,0,0);
    }

    float unoccluded = mix(1, getBlockerContribution(Ps, shadoworigin, 
                                                     i_coordsys,
                                                     i_width, i_height,
                                                     i_wedge, i_hedge,
                                                     i_roundness), i_intensity);
   
    // markv: not sure why i_intensity is multiplied here
    o_blockerColor = 1 - ((1 - unoccluded) *(1- i_color) *i_intensity);
    o_blockerValue = unoccluded;
    """
    
    
def initializePlugin(obj):
    dl_blocker.register(obj)

def uninitializePlugin(obj):
    dl_blocker.deregister(obj)
    
