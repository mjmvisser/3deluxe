import delight

class dl_attributeFloat(delight.AttributeNode):
    typeid = 0x39cb4863
    description = "Generic float attribute."
    
    inputValue = delight.Float(default=1.0)
    outputValue = delight.Float(output=True)
    
def initializePlugin(obj):
    dl_attributeFloat.register(obj)

def uninitializePlugin(obj):
    dl_attributeFloat.deregister(obj)
