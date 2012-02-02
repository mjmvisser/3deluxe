import os
from nose.tools import assert_equal, assert_not_equal, assert_raises, assert_true, assert_false

import maya.standalone
maya.standalone.initialize(name="python")

maya.cmds.loadPlugin("3delight_for_maya2011")

import maya.cmds as cmds
import maya.mel as mel

class TestLayer(object):
    def setup(self):
        dl_uberLightShape_plugin = os.path.join(os.path.dirname(__file__), "..", "python", "shaders", "dl_uberLightShape.py")
        result = cmds.loadPlugin(dl_uberLightShape_plugin)
        assert_not_equal(result, None)
        self.renderpass = mel.eval("DL_createBasicRenderPassNode")
        #cmds.setAttr("%s.renderMode" % self.renderpass, 3);        
    
    def teardown(self):
        cmds.file(newFile=True, force=True)
        cmds.unloadPlugin("dl_uberLightShape")

    def test_create_node_and_compile(self):
        sphere = cmds.sphere()
        node = cmds.shadingNode("dl_uberLightShape", asLight=True)
#        cmds.select(sphere, replace=True)
#        node_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=node);
#        cmds.defaultNavigation(connectToExisting=True, source=node, destination=node_sg)
#        mel.eval('connectNodeToNodeOverride("%s", "%s")' % (node, node_sg))
#        cmds.sets(edit=True, forceElement=node_sg)
        mel.eval("delightRender %s" % self.renderpass)
