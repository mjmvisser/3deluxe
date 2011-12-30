from delight import ShadingComponent, Boolean

class test_component(ShadingComponent):
    typeid = 0x00300000
    description = "Test component."
    bool_param = Boolean()

    rsl = \
    """
    """

def initializePlugin(obj):
    test_component.register(obj)

def uninitializePlugin(obj):
    test_component.deregister(obj)
