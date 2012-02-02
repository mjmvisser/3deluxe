import deluxe

class dl_bakeLightShape(deluxe.Light):
    typeid = 0x00310004
    description = "Light that bakes geometry to point clouds."
    includes = ['utils.h']
    
    #
#    deluxe.Light.intensity.hidden = True
#    deluxe.Light.lightColor.hidden = True
    
    
    ptcFile = deluxe.File(default='default.ptc', label='Point Cloud File',
                             help="""The point cloud file in which to bake geometry.""")
    
    ptcFileNoSelfOcclude = deluxe.File(default='default.ptc', label='Point Cloud (No Self) File', hidden=True,
                             help="""The point cloud file in which to bake objects
                                        THAT DON'T OCCLUDE THEMSELVES OR EACH OTHER
                                    ( Attribute "user" "float selfOcclude" [ 0 ] ), eg groundplane.""")
    coordSys = deluxe.CoordinateSystem(default='world',
                                        label='Coordinate System', 
                                        help="""The coordinate system in which points will be stored in the ptc file. Default is "world".""")

    radiusScale = deluxe.Float(shortname='rsc', default = 1, softmax = 3,
         help="Scale radius of baked points.")
    
    bakeRadiosity = deluxe.Boolean(default=False,
                                   help="""Bake radiosity at each point. Turn this on if you are doing
                                           point-based indirect lighting (color bleeding).""")

    bakeRadiosityVariable = deluxe.String(default="Ci",
                                   help="""If bakeRadiosity is on, this is the variable that is baked from surface shaders.
                                            To avoid baking camera-dependent channels such as specular and reflection,
                                            you can bake just diffuse illumination by entering 'aov_diffuse'.
                                            The aov_diffuse AOV must be enabled for this to work.""")

    bakeRaytracing = deluxe.Boolean(shortname='brt', default=False,
                                   help="""Bake raytrace points (bug-prone).""")

    opacityThreshold = deluxe.Float(shortname='oth', default=-1, help="Points with opacity lower than this value will not be baked.")

    useBoundingBoxes = deluxe.Boolean(shortname='usebbx', default=False, help="Use bounding boxes")

    boundBox1enable = deluxe.Boolean(shortname='bbxe1', default=False, help="Use bounding box 1")
    boundBox1min = deluxe.Point(shortname='bbxmn1', help="xyz minimum for bounding box 1.")
    boundBox1max = deluxe.Point(shortname='bbxmx1', help="xyz maximum for bounding box 1.")
    boundBox1buffer = deluxe.Float(shortname='bbxbf1', softmax = 10,
        help="How much extra space to add to each side of bounding box 1.")
    
    boundBox2enable = deluxe.Boolean(shortname='bbxe2', default=False, help="Use bounding box 2")
    boundBox2min = deluxe.Point(shortname='bbxmn2', help="xyz minimum for bounding box 2.")
    boundBox2max = deluxe.Point(shortname='bbxmx2', help="xyz maximum for bounding box 2.")
    boundBox2buffer = deluxe.Float(shortname='bbxbf2', softmax = 10,
        help="How much extra space to add to each side of bounding box 2.")
    
    boundBox3enable = deluxe.Boolean(shortname='bbxe3', default=False, help="Use bounding box 3")
    boundBox3min = deluxe.Point(shortname='bbxmn3', help="xyz minimum for bounding box 3.")
    boundBox3max = deluxe.Point(shortname='bbxmx3', help="xyz maximum for bounding box 3.")
    boundBox3buffer = deluxe.Float(shortname='bbxbf3', softmax = 10,
        help="How much extra space to add to each side of bounding box 3.")
    
    boundBox4enable = deluxe.Boolean(shortname='bbxe4', default=False, help="Use bounding box 4")
    boundBox4min = deluxe.Point(shortname='bbxmn4', help="xyz minimum for bounding box 4.")
    boundBox4max = deluxe.Point(shortname='bbxmx4', help="xyz maximum for bounding box 4.")
    boundBox4buffer = deluxe.Float(shortname='bbxbf4', softmax = 10,
        help="How much extra space to add to each side of bounding box 4.")
    
    boundBox5enable = deluxe.Boolean(shortname='bbxe5', default=False, help="Use bounding box 5")
    boundBox5min = deluxe.Point(shortname='bbxmn5', help="xyz minimum for bounding box 5.")
    boundBox5max = deluxe.Point(shortname='bbxmx5', help="xyz maximum for bounding box 5.")
    boundBox5buffer = deluxe.Float(shortname='bbxbf5', softmax = 10,
        help="How much extra space to add to each side of bounding box 5.")

    boundingBoxes = deluxe.Group([
        useBoundingBoxes,
        boundBox1enable, boundBox1min, boundBox1max, boundBox1buffer,
        boundBox2enable, boundBox2min, boundBox2max, boundBox2buffer,
        boundBox3enable, boundBox3min, boundBox3max, boundBox3buffer,
        boundBox4enable, boundBox4min, boundBox4max, boundBox4buffer,
        boundBox5enable, boundBox5min, boundBox5max, boundBox5buffer])
    

    do_bake = deluxe.Boolean(default=True, message=True, messagetype='lightsource')
    
    # category
    __category = deluxe.String(default='bakelight', message=True, messagetype='lightsource')
    _3delight_light_category = deluxe.String(default='bakelight', notemplate=True, norsl=True)


    
    
    rsl = \
    """
        extern float do_bake;
        point Pw = transform("world", Ps);
       
#define INBOUND(n) (i_boundBox##n##enable > 0 && \
       Pw[0] < i_boundBox##n##max[0] + i_boundBox##n##buffer && Pw[0] > i_boundBox##n##min[0] - i_boundBox##n##buffer && \
       Pw[1] < i_boundBox##n##max[1] + i_boundBox##n##buffer && Pw[1] > i_boundBox##n##min[1] - i_boundBox##n##buffer && \
       Pw[2] < i_boundBox##n##max[2] + i_boundBox##n##buffer && Pw[2] > i_boundBox##n##min[2] - i_boundBox##n##buffer)
        float ray_depth = 0;
        rayinfo( "depth", ray_depth );
        if (do_bake == 1 && (ray_depth == 0 || i_bakeRaytracing == 1)) 
        {
            normal Nn = normalize(Ns);
            normal Nf = faceforward(Nn, I);
            

            // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
            illuminate(Ps + Nf)
            {
                color surfOpacity =1;
                surface("Oi", surfOpacity);
                if (luminance(surfOpacity) > i_opacityThreshold &&
                        i_useBoundingBoxes == 0 || INBOUND(1) || INBOUND(2) || INBOUND(3) || INBOUND(4) || INBOUND(5))
                {
                    uniform string ptcCoordSys = "world";
                    if (i_coordSys != "")
                        ptcCoordSys = i_coordSys;
                    
                    uniform float selfOcclude = 1;
                    attribute("user:selfOcclude", selfOcclude);
                    uniform string ptcFile = selfOcclude == 1 ? i_ptcFile : i_ptcFileNoSelfOcclude;

                    if (i_bakeRadiosity != 0)
                    {
                        color radiosity = 1;
                        surface(i_bakeRadiosityVariable, radiosity);
                        bake3d(ptcFile, "", Ps, Nn,
                               "coordsystem", ptcCoordSys,
                               "radiusscale", i_radiusScale,
                               "_radiosity", radiosity,
                               "interpolate", 1 );
                    }
                    else
                    {
                        bake3d(ptcFile, "", Ps, Nn,
                               "coordsystem", ptcCoordSys,
                               "radiusscale", i_radiusScale,
                               "interpolate", 1 );
                    }
                }
            
                Cl = 0;
            }
        }
    """

    
def initializePlugin(obj):
    dl_bakeLightShape.register(obj)

def uninitializePlugin(obj):
    dl_bakeLightShape.deregister(obj)
