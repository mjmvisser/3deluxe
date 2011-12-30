class CounterMeta(type):
    '''
    A simple meta class which adds a ``_counter`` attribute to the instances of
    the classes it is used on. This counter is simply incremented for each new
    instance.
    Shamelessly copied from the Elixir project.
    '''
    counter = 0

    def __call__(self, *args, **kwargs):
        instance = type.__call__(self, *args, **kwargs)
        instance._counter = CounterMeta.counter
        CounterMeta.counter += 1
        return instance


class Item(object):
    __metaclass__ = CounterMeta
    __defaultArgs = {'longname': None, 'shortname': None, 'output': False, 
                     'array': False, 'hidden': False, 'notemplate': False, 'parent': None }

    def setDefaults(self, defaultArgs):
        # set defaults
        for k,v in defaultArgs.items():
            if not self.__dict__.has_key(k):
                self.__dict__[k] = v

    def __init__(self, *args, **kwargs):
        self.setDefaults(Item.__defaultArgs)
        #super(Item, self).__init__(*args, **kwargs)

        for k,v in kwargs.items():
            # use setattr instead of assigning to dict so properties are invoked
            setattr(self, k, v)

    def getTemplate(self):
        return None

    def getHelpers(self):
        return None

class Separator(Item):
    def createAttributes(self):
        self.obj = None

    def addAttributes(self):
        pass

    def validate(self):
        pass
        
    def getTemplate(self):
        if not self.hidden and not self.notemplate:
            return r"""
                    editorTemplate -addSeparator;"""
        else:
            return ''

    def getHelpers(self):
        return None
