from maya.OpenMaya import *

import delight

class dl_componentBuilder(delight.ShadingComponent):
    typeid = 0x1a98068f
    description = "Utility node to create component data"
    
    lightSetIndex = delight.Integer(affect=False)
    
    rsl = ""
    for channel in delight.ComponentData.channels:
        exec '%s = delight.%s(shortname="i%s", default=0, affect=False)'%(channel.longname, channel.apitype, channel.shortname)
        rsl += '\to_output_%s%s = i_%s * globalIntensity * i_color;\n'%(channel.longname, ['', '[i_lightSetIndex]'][channel.array], channel.longname)
        
        
def initializePlugin(obj):
    dl_componentBuilder.register(obj)

def uninitializePlugin(obj):
    dl_componentBuilder.deregister(obj)
