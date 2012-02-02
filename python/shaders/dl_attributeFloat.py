import deluxe

class dl_attributeFloat(deluxe.AttributeNode):
    typeid = 0x39cb4863
    description = "Generic float attribute."
    
    inputValue = deluxe.Float(default=1.0)
    outputValue = deluxe.Float(output=True)
    
def initializePlugin(obj):
    dl_attributeFloat.register(obj)

def uninitializePlugin(obj):
    dl_attributeFloat.deregister(obj)
