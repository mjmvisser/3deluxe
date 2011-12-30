import delight

class dl_attributeColor(delight.AttributeNode):
    typeid = 0x18831ced
    description = "Generic color attribute"
    
    inputValue = delight.Color(default=1.0)
    outputValue = delight.Color(output=True)
    
def initializePlugin(obj):
    dl_attributeColor.register(obj)

def uninitializePlugin(obj):
    dl_attributeColor.deregister(obj)
