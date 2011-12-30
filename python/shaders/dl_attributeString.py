from maya.OpenMaya import *

import delight

class dl_attributeString(delight.AttributeNode):
    typeid = 0x0c30c269
    description = "Generic string attribute."
    
    inputValue = delight.String()
    outputValue = delight.String(output=True)
    
def initializePlugin(obj):
    dl_attributeString.register(obj)

def uninitializePlugin(obj):
    dl_attributeString.deregister(obj)
