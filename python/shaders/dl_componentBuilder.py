from maya.OpenMaya import *

import deluxe

class dl_componentBuilder(deluxe.ShadingComponent):
    typeid = 0x1a98068f
    description = "Utility node to create component data"
    
    lightSetIndex = deluxe.Integer(affect=False)
    
    rsl = ""
    for channel in deluxe.ComponentData.channels:
        exec '%s = deluxe.%s(shortname="i%s", default=0, affect=False)'%(channel.longname, channel.apitype, channel.shortname)
        rsl += '\to_output_%s%s = i_%s * globalIntensity * i_color;\n'%(channel.longname, ['', '[i_lightSetIndex]'][channel.array], channel.longname)
        
        
def initializePlugin(obj):
    dl_componentBuilder.register(obj)

def uninitializePlugin(obj):
    dl_componentBuilder.deregister(obj)
