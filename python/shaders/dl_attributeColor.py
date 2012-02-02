import deluxe

class dl_attributeColor(deluxe.AttributeNode):
    typeid = 0x18831ced
    description = "Generic color attribute"
    
    inputValue = deluxe.Color(default=1.0)
    outputValue = deluxe.Color(output=True)
    
def initializePlugin(obj):
    dl_attributeColor.register(obj)

def uninitializePlugin(obj):
    dl_attributeColor.deregister(obj)
