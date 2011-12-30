import delight

class dl_pointCloudLightShape(delight.LightBase):
    typeid = 0x29f5d0a0
    description = "Point cloud control light."

    enable = delight.Boolean(default=True)
    enableAmbientOcclusion = delight.Boolean(default=True)
    enableColorBleeding = delight.Boolean(default=True, )
    enableReflection = delight.Boolean(default=True, shortname='erfl')
    enableReflectionOcclusion = delight.Boolean(default=True )
    enableRefraction = delight.Boolean(default=True, shortname='erfr', )
    enableSubsurface = delight.Boolean(default=True, shortname='ess')
    ptcFile = delight.File(label="Point Cloud File")

    #
    __enableAmbientOcclusion = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableColorBleeding = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableReflection = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableReflectionOcclusion = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableRefraction = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __enableSubsurface = delight.Boolean(default=False, output=True, message=True, messagetype='lightsource')
    __ptcFile = delight.String(output=True, message=True, messagetype='lightsource')

    # category
    __category = delight.String(default='pointcloud', message=True, messagetype='lightsource')
    _3delight_light_category = delight.String(shortname='cat', default='pointcloud', notemplate=True, norsl=True)

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
