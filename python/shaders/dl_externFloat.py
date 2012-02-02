import deluxe

class dl_externFloat(deluxe.Extern):
    typeid = 0x00300030
    inputValue = deluxe.Float(default=1.0)
    outputValue = deluxe.Float(output=True)
    
def initializePlugin(obj):
    dl_externFloat.register(obj)

def uninitializePlugin(obj):
    dl_externFloat.deregister(obj)
