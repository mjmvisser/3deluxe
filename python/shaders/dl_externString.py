import delight

class dl_externString(delight.Extern):
    typeid = 0x00300032
    inputValue = delight.String()
    outputValue = delight.String(output=True)
    
def initializePlugin(obj):
    dl_externString.register(obj)

def uninitializePlugin(obj):
    dl_externString.deregister(obj)
