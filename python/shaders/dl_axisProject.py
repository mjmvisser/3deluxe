import delight

class dl_axisProject(delight.Utility):
    typeid = 0x00300336
    description = "Axis projection."
    
    scale = delight.Vector(default=1)
    coordsys = delight.String(default="world")

    xst = delight.UV(output=True)
    yst = delight.UV(output=True)
    zst = delight.UV(output=True)
    
    
    rsl = \
    """
    extern point P;
    string coordsys = i_coordsys == "" ? "world" : i_coordsys;
    point Pw = transform(coordsys, P)/i_scale;

    o_xst[0] = (Pw[1] + 1)/2;
    o_xst[1] = (Pw[2] + 1)/2;
    o_yst[0] = (Pw[0] + 1)/2;
    o_yst[1] = (Pw[2] + 1)/2;
    o_zst[0] = (Pw[0] + 1)/2;
    o_zst[1] = (Pw[1] + 1)/2;
    

    """


    rslpost = ""


def initializePlugin(obj):
    dl_axisProject.register(obj)

def uninitializePlugin(obj):
    dl_axisProject.deregister(obj)
