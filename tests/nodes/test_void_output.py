import delight

class test_void_output(delight.Utility):
    typeid = 0x00300002
    description = "Test void outputs."

    param1 = delight.Color(shortname='p1', notemplate=True, output=True)
    param2 = delight.Float(shortname='p2', notemplate=True, output=True)
    voidOutput = delight.Compound([param1, param2], output=True)
    
    param3 = delight.Color(shortname='p3', output=True)

    rsl = \
    """
    """

def initializePlugin(obj):
    test_void_output.register(obj)

def uninitializePlugin(obj):
    test_void_output.deregister(obj)
    
