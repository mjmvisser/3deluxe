import delight

class dl_externFloat(delight.Extern):
    typeid = 0x00300030
    inputValue = delight.Float(default=1.0)
    outputValue = delight.Float(output=True)
    
def initializePlugin(obj):
    dl_externFloat.register(obj)

def uninitializePlugin(obj):
    dl_externFloat.deregister(obj)
