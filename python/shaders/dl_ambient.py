import deluxe

class dl_ambient(deluxe.ShadingComponent):
    typeid = 0x00300000
    description = "Ambient illumination component."
    includes = ["env_utils.h"]

    rsl = \
    """
    
    color col = 0;
    illuminance( "ambient", P ) {
        if( L == 0 ) {
            col += Cl;
        }
    }
    col *= globalIntensity * surfaceColor;
    o_output_ambient = col;
    o_output_beauty = col;
    """


def initializePlugin(obj):
    dl_ambient.register(obj)

def uninitializePlugin(obj):
    dl_ambient.deregister(obj)
