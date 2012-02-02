import os
from nose.tools import assert_equal, assert_not_equal, assert_raises, assert_true, assert_false

import maya.standalone
maya.standalone.initialize(name="python")

maya.cmds.loadPlugin("3delight_for_maya2011")

import maya.cmds as cmds
import maya.mel as mel

class TestLayer(object):
    def setup(self):
        test_void_input_plugin = os.path.join(os.path.dirname(__file__), "nodes", "test_void_input.py")
        test_void_output_plugin = os.path.join(os.path.dirname(__file__), "nodes", "test_void_output.py")
        cmds.loadPlugin(test_void_input_plugin)
        cmds.loadPlugin(test_void_output_plugin)
        self.renderpass = mel.eval("DL_createBasicRenderPassNode")
        #cmds.setAttr("%s.renderMode" % self.renderpass, 3);
        os.environ["_3DFM_SL_INCLUDE_PATH"] += ":" + os.path.join(os.path.dirname(__file__), "nodes")
    
    def teardown(self):
        cmds.file(newFile=True, force=True)
        cmds.unloadPlugin("test_void_input")
        cmds.unloadPlugin("test_void_output")

    def test_create_node_and_compile(self):
        mel.eval("source createRenderNode")
        test_void_input = cmds.shadingNode("test_void_input", asShader=True)
        test_void_output = cmds.shadingNode("test_void_output", asUtility=True)

        sphere = cmds.sphere()
        cmds.select(sphere, replace=True)
        node_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="test_void_inputSG1");
        cmds.defaultNavigation(connectToExisting=True, source=test_void_input, destination=node_sg)
        mel.eval('connectNodeToNodeOverride("%s", "%s")' % (test_void_input, node_sg))
        cmds.sets(edit=True, forceElement=node_sg)

        cmds.connectAttr(test_void_output + ".voidOutput", test_void_input + ".voidInput[0]", force=True)
        cmds.connectAttr(test_void_output + ".param3", test_void_input + ".param3", force=True)

        
        mel.eval("delightRender %s" % self.renderpass)

