import delight

class dl_externColor(delight.Extern):
    typeid = 0x00300031
    inputValue = delight.Color()
    outputValue = delight.Color(output=True)
    
def initializePlugin(obj):
    dl_externColor.register(obj)

def uninitializePlugin(obj):
    dl_externColor.deregister(obj)
