import maya.cmds as cmds

# adapted from pymel

class AETemplate(object):
    def __init__(self, nodeName):
        self._nodeName = nodeName

    def addControl(self, control, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False):
        args = [control]
        kwargs = {'preventOverride': preventOverride}
        if dynamic:
            kwargs['addDynamicControl'] = True
        else:
            kwargs['addControl'] = True
        if changeCommand:
            args.append(changeCommand)
        if label:
            kwargs['label'] = label
        if annotation:
            kwargs['annotation'] = annotation
        cmds.editorTemplate(*args, **kwargs)

    def callCustom(self, newFunc, replaceFunc, *attrs):
        cmds.editorTemplate(newFunc, replaceFunc, callCustom=True, *attrs)

    def suppress(self, control):
        cmds.editorTemplate(suppress=control)

    def dimControl(self, nodeName, control, state):
        cmds.editorTemplate(dimControl=(nodeName, control, state))

    def beginLayout(self, name, collapse=True):
        cmds.editorTemplate(beginLayout=name, collapse=collapse)

    def endLayout(self):
        cmds.editorTemplate(endLayout=True)

    def beginScrollLayout(self):
        cmds.editorTemplate(beginScrollLayout=True)

    def endScrollLayout(self):
        cmds.editorTemplate(endScrollLayout=True)

    def beginNoOptimize(self):
        cmds.editorTemplate(beginNoOptimize=True)

    def endNoOptimize(self):
        cmds.editorTemplate(endNoOptimize=True)

    def interruptOptimize(self):
        cmds.editorTemplate(interruptOptimize=True)

    def addSeparator(self):
        cmds.editorTemplate(addSeparator=True)

    def addComponents(self):
        cmds.editorTemplate(addComponents=True)

    def addExtraControls(self, label=None):
        kwargs = {}
        if label:
            kwargs['extraControlsLabel'] = label
        cmds.editorTemplate(addExtraControls=True, **kwargs)
    