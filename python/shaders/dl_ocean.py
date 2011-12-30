import delight

class dl_ocean(delight.ShadingNode):
    typeid = 0x3acd90d0
    description = "Houdini's ocean "
    
    #
    globalScale = delight.Float(default=1, min=0.000001, help='THE global scale')
    gridResolution = delight.Integer(default=8, help='This is the resolution of the grid that the ocean will be simulated on. You can think of it in the same way as you would a texture image that you would tile the ocean surface with. The resolution of the image would be 2 to the power of res so e.g. res=10 would make a 1024x1024 image. Be warned, going to res=11 means you are going to use quite a bit of memory since the code uses more arrays of this size to store intermediate computations.')
    oceanSize = delight.Float(default=100, help='The grid mentiond above is computed for and applied to the input geometry in tiles of this size.')
    windSpeed = delight.Float(default=30, help='Affects the shape of the waves')
    waveHeigth = delight.Float(default=3, help='This is used to set the so called "A" fiddle factor in the Tessendorf paper. The waves are scaled so that they will be roughly less than this height (strictly so for the t=0 timestep).')
    shortestWave = delight.Float(default=0.02, help='Waves below this lenght will be filterd out.'    )
    windDirection = delight.Float(default=0, help='Affects the direction the waves travel in.')
    dampReflections = delight.Float(default=0.5, help='In a "fully developed" ocean you will have waves travelling in both the forward and backwards directions. This parameter damps out the negative direcion waves')
    windAlign = delight.Float(default=2, help='Controls how closely the waves travel in the direction of the wind.')
    oceanDepth = delight.Float(default=200, help='Affects the spectrum of waves generated. Visually in doesnt seem to have that great an influence')
    chopAmount = delight.Float(default=1, help='The amount of chop displacenemnt that is applied to the input points.')
    doNormal = delight.Boolean(default=False)
    doEigen = delight.Boolean(default=False)
    time = delight.Float(default=0, help='The time that the surface will be evaluated at. You will usually just plug the expression timr in here.')
    seed = delight.Integer(shortname='sd', default=0, help='Seeds the random number generator.')
    
    Pref = delight.Point(message=True, messagetype='Pref_param', storage='varying')
    
    outColor = delight.Color(default=0, output=True)
    outAlpha = delight.Float(default=0, output=True)
    outNormal = delight.Color(default=0, output=True)
    outJMinus = delight.Float(default=0, output=True)
    outJPlus = delight.Float(default=0, output=True)
    outEMinus = delight.Color(default=0, output=True)
    outEPlus = delight.Color(default=0, output=True)
    
                              
    rsl = """
extern varying point P;
extern varying point Pref;

point PP = P;
if(Pref != point(0))
    PP = Pref;

PP = transform("object", PP);

float ss = PP[0] * 1.0/i_globalScale;
float tt = PP[2] * 1.0/i_globalScale;;

float doChop = 1;
if(i_chopAmount == 0)
    doChop = 0;
    
vector disp = 1, eminus=1, eplus = 1;
normal nml = 1;
float jminus=1, jplus = 1;
ocean_eval( ss, tt, i_time, i_waveHeigth,
            doChop, i_chopAmount, disp,
            i_doNormal, nml,
            i_doEigen, jminus, jplus, eminus, eplus,
            i_gridResolution, i_oceanSize, i_windSpeed, i_shortestWave,
            i_windDirection, i_dampReflections, i_windAlign, i_oceanDepth, i_seed);
          
disp = transform("current", disp);
disp *= i_globalScale;
o_outColor = color(disp);
o_outAlpha = length(disp);

nml = ntransform("current", nml);    
o_outNormal = color(nml);
o_outJMinus = jminus;
o_outJPlus = jplus;
o_outEMinus = color(eminus);
o_outEPlus = color(eplus);
"""

        
def initializePlugin(obj):
    dl_ocean.register(obj)

def uninitializePlugin(obj):
    dl_ocean.deregister(obj)