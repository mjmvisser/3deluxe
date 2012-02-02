import deluxe

class dl_cellNoise(deluxe.Texture3D):
    typeid = 0x0030013b
    description = "\"Worley noise\" from \"A Cellular Texture Basis Function\", SIGGRAPH '96"
    
    frequency = deluxe.Float(default=4, softmin=.1, softmax=10, storage='uniform', help="Controls the size of the cells. Higher frequencies make smaller cells.")
    noisetype = deluxe.Enum(default='Voronoi Euclidian',choices=['Voronoi Euclidian','Voronoi Manhattan','Simple Cellnoise'] ,storage='uniform', help="The means to measure distances to neighboring cells. Manhattan distance gives more rectangular shapes and Euclidian distance gives more spherical shapes.")
    jitter = deluxe.Float(default=0.75, softmin=0, softmax=1, help="Controls the distortion of the cells.")
    clamp = deluxe.Boolean(default=True, storage='uniform', help="Causes resulting distances to be clamped to the range 0->1")
    c1 = deluxe.Float(default=0.8, softmin=-2, softmax=2, help="Multiplier for the distances to the first feature.")
    c2 = deluxe.Float(default=-0.2, softmin=-2, softmax=2, help="Multiplier for the distance to the second feature.")
    voronoi = deluxe.Group([jitter, clamp, c1, c2], collapse=False)
    avgcolor = deluxe.Color(shortname='ac', default=1, storage='uniform', help="")
    colorvariation = deluxe.Float(shortname='cv', default=.5, storage='uniform', help="")
    simple = deluxe.Group([avgcolor, colorvariation], collapse=False)
    
    rslpost = ""
    rsl = \
    """          
            extern float du, dv;
   	       	pp *= i_frequency;

            if (i_noisetype == 2) {

                color varyColor(color avgcolor; float variance; float seed;)
                {
                    color hsl = ctransform("hsl", avgcolor);
                    float h, s, l;
                    h = comp(hsl, 0); s = comp(hsl, 1); l = comp(hsl, 2);
                    h += variance * (cellnoise(seed+3)-0.5);
                    s += variance * (cellnoise(seed-14)-0.5);
                    l += variance * (cellnoise(seed+37)-0.5);
                    hsl = color(mod(h,1), clamp(s, 0, 1), clamp(l, 0, 1));
                    return ctransform("hsl", "rgb", hsl);
                }

#ifndef MINFILTWIDTH
#  define MINFILTWIDTH 1.0e-6
#endif
#define fadeout(g,g_avg,featuresize,fwidth)         mix (g, g_avg, smoothstep(.2,.6,fwidth/featuresize))
#define tightFilterWidth(dpu,dpv)     max( length(dpu^dpv), MINFILTWIDTH )
#define filterWidth(a, b) tightFilterWidth(a,b)

                extern vector dPdu;
                extern vector dPdv;

                vector dppu = i_frequency * du*dPdu;
                vector dppv = i_frequency * dv*dPdv;
                color c, c1,c2,c3,c4;
                float f1, f2, f3, f4;
                point p2, p3, p4;

// This is to avoid warnings for getting cellnoise in "current" space.
#define addVtoPsameSpace(pOut, pIn, vIn) \
    pOut = pIn; \
    pOut[0] = pIn[0] + vIn[0]; \
    pOut[1] = pIn[1] + vIn[1]; \
    pOut[2] = pIn[2] + vIn[2];
                
                vector dppuv = dppu + dppv;
                addVtoPsameSpace(p2, pp, dppu)
                addVtoPsameSpace(p3, pp, dppv)
                addVtoPsameSpace(p4, pp, dppuv)

                f1 = float cellnoise(pp);
                f2 = float cellnoise(p2);
                f3 = float cellnoise(p3);
                f4 = float cellnoise(p4);
                c1 = varyColor(i_avgcolor, i_colorvariation, 100*f1);
                c2 = varyColor(i_avgcolor, i_colorvariation, 100*f2);
                c3 = varyColor(i_avgcolor, i_colorvariation, 100*f3);
                c4 = varyColor(i_avgcolor, i_colorvariation, 100*f4);
                c =  .25 * (c1 + c2 + c3 + c4);
                o_outColor = fadeout(c, i_avgcolor, 1, filterWidth(dppu, dppv));
                o_outAlpha = luminance( o_outColor );
            } else {
   	       	    
                float f1,f2;
                varying color g;   	
                point thiscell = point (floor(xcomp(pp))+0.5,
                                        floor(ycomp(pp))+0.5,
                            floor(zcomp(pp))+0.5);
                f1 = f2 = 1000;
                uniform float i, j, k;
                for (i = -1;  i <= 1;  i += 1) {
                    for (j = -1;  j <= 1;  j += 1) {
                        for (k = -1;  k <= 1;  k += 1) {
                    point testcell = thiscell + vector(i,j,k);
                            point pos = testcell + i_jitter * 
                        (vector cellnoise (testcell) - 0.5);
                    vector offset = pos - pp;
                            float dist;
                    if (i_noisetype == 0)  	
                        dist = offset.offset;
                    else
                    {
                        dist =  abs(xcomp(offset)) +
                                abs(ycomp(offset)) +
                            abs(zcomp(offset));
                    }
                            if (dist < f1) {
                                f2 = f1;
                                f1 = dist;
                            } else if (dist < f2) {
                                f2 = dist;
                    }
                        }
                }
                }
                if (i_noisetype == 0)  	
                        {
                    f1 = sqrt(f1);
                    f2 = sqrt(f2);
                }
                g = f1 * i_c1 + f2 * i_c2;
                if (i_clamp != 0)
                {
                    g = clamp(g, 0, 1);
                }
                o_outColor = g;
                o_outAlpha = luminance( o_outColor );
            }
    """


def initializePlugin(obj):
    dl_cellNoise.register(obj)

def uninitializePlugin(obj):
    dl_cellNoise.deregister(obj)
