from maya.OpenMaya import *
from maya.OpenMayaMPx import *

from .items import Item

class Container(Item):
    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)

        children = []
        for arg in args:
            children += arg

        self.children = children

        for child in children:
            child.parent = self

    def validate(self):
        if not isinstance(self.children, (tuple, list)):
            raise TypeError('Children must be a list or tuple')
        
    def createAttributes(self):
        for child in self.children:
            child.createAttributes()

    def addAttributes(self):
        for child in self.children:
            child.addAttributes()

    def getTemplate(self):
        if not self.hidden and not self.notemplate:
            # default behavior is to return the children
            return '\n'.join([child.getTemplate() for child in self.children if child.getTemplate() != None])
        else:
            return ''

    def getHelpers(self):
        return '\n'.join([child.getHelpers() for child in self.children if child.getHelpers() != None])

    def filterAttributes(self, func=lambda p: True):
        from .attributes import Attribute
        params = []
        for child in self.children:
            if isinstance(child, Attribute) and func(child):
                params.append(child)
            if isinstance(child, Container):
                params += child.filterAttributes(func)
        return params

    def getInputData(self, dataHandle):
        data = {}
        for child in self.children:
            data.update(child.getInputData(dataHandle))
        return data

    def getOutputData(self, dataHandle):
        data = {}
        for child in self.children:
            data.update(child.getOutputData(dataHandle))
        return data

    def setOutputData(self, dataHandle, data):
        for child in self.children:
            child.setOutputData(dataHandle, data)
        

class Master(Container):
    def __init__(self, *args, **kwargs):
        super(Master, self).__init__(*args, **kwargs)

        if self.hidden and not self.notemplate:
            raise TypeError('The master template layout cannot be hidden')

    def getTemplate(self):
        return \
        """
            AEswatchDisplay $node;
            editorTemplate -beginScrollLayout;
            %s
            AEdependNodeTemplate $node;
            editorTemplate -addExtraControls;
            editorTemplate -endScrollLayout;
        """ % super(Master, self).getTemplate()

class Group(Container):
    __defaultArgs = {'order':None,
                     'collapse': True,
                     'label': None}

    def __init__(self, *args, **kwargs):
        self.setDefaults(Group.__defaultArgs)
        super(Group, self).__init__(*args, **kwargs)

    def getTemplate(self):
        if not self.hidden and not self.notemplate:
            if self.label == None:
                name = '(interToUI(\"%s\"))' % self.longname
            else:
                name = '("%s")' % self.label
            return \
            """
                editorTemplate -beginLayout %s  -collapse %d;
                %s
                editorTemplate -endLayout;
            """ % (name, self.collapse, super(Group, self).getTemplate())
        else:
            return ''
