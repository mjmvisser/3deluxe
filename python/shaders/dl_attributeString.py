from maya.OpenMaya import *

import deluxe

class dl_attributeString(deluxe.AttributeNode):
    typeid = 0x0c30c269
    description = "Generic string attribute."
    
    inputValue = deluxe.String()
    outputValue = deluxe.String(output=True)
    
def initializePlugin(obj):
    dl_attributeString.register(obj)

def uninitializePlugin(obj):
    dl_attributeString.deregister(obj)
