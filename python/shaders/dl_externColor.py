import deluxe

class dl_externColor(deluxe.Extern):
    typeid = 0x00300031
    inputValue = deluxe.Color()
    outputValue = deluxe.Color(output=True)
    
def initializePlugin(obj):
    dl_externColor.register(obj)

def uninitializePlugin(obj):
    dl_externColor.deregister(obj)
