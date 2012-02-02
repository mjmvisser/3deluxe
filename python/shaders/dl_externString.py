import deluxe

class dl_externString(deluxe.Extern):
    typeid = 0x00300032
    inputValue = deluxe.String()
    outputValue = deluxe.String(output=True)
    
def initializePlugin(obj):
    dl_externString.register(obj)

def uninitializePlugin(obj):
    dl_externString.deregister(obj)
