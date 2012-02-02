import delight

class test_void_input(delight.ShadingNode):
    typeid = 0x00300001
    description = "Test void inputs."
    classification = "shader/surface"
    
    param1 = delight.Color(shortname='p1', notemplate=True)
    param2 = delight.Float(shortname='p2', notemplate=True)
    voidInput = delight.Compound([param1, param2], prepare=True, array=True)

    param3 = delight.Color(shortname='p3')
    
    outColor = delight.Color(shortname='oc', output=True)

    rsl = \
    """
    """

def initializePlugin(obj):
    test_void_input.register(obj)

def uninitializePlugin(obj):
    test_void_input.deregister(obj)
    
