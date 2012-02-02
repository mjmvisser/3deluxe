import deluxe

class dl_pointCloudLightShape(deluxe.LightBase):
    typeid = 0x29f5d0a0
    description = "Point cloud control light."

    enable = deluxe.Boolean(default=True)
    enableAmbientOcclusion = deluxe.Boolean(default=True)
    enableColorBleeding = deluxe.Boolean(default=True, )
    enableReflection = deluxe.Boolean(default=True, shortname='erfl')
    enableReflectionOcclusion = deluxe.Boolean(default=True )
    enableRefraction = deluxe.Boolean(default=True, shortname='erfr', )
    enableSubsurface = deluxe.Boolean(default=True, shortname='ess')
    ptcFile = deluxe.File(label="Point Cloud File")

    #
    __enableAmbientOcclusion = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableColorBleeding = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableReflection = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableReflectionOcclusion = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableRefraction = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableSubsurface = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __ptcFile = deluxe.String(output=True, message=True, messagetype='lightsource')

    # category
    __category = deluxe.String(default='pointcloud', message=True, messagetype='lightsource')
    _3delight_light_category = deluxe.String(shortname='cat', default='pointcloud', notemplate=True, norsl=True)

    rsl = \
    """
    extern float __enableAmbientOcclusion;
    extern float __enableColorBleeding;
    extern float __enableReflection;
    extern float __enableReflectionOcclusion;
    extern float __enableRefraction;
    extern float __enableSubsurface;
    extern string __ptcFile;
    
    if(i_enable > 0){
        __enableAmbientOcclusion =  i_enableAmbientOcclusion;
        __enableColorBleeding = i_enableColorBleeding;
        __enableReflection = i_enableReflection;
        __enableReflectionOcclusion = i_enableReflectionOcclusion;
        __enableRefraction = i_enableRefraction;
        __enableSubsurface = i_enableSubsurface;
    }
    else{
        __enableAmbientOcclusion =  0;
        __enableColorBleeding = 0;
        __enableReflection = 0;
        __enableReflectionOcclusion = 0;
        __enableRefraction = 0;
        __enableSubsurface = 0;
    }
    __ptcFile = i_ptcFile;
    """


def initializePlugin(obj):
    dl_pointCloudLightShape.register(obj)

def uninitializePlugin(obj):
    dl_pointCloudLightShape.deregister(obj)
