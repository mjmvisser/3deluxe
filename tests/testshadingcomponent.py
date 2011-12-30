import os
from nose.tools import assert_equal, assert_not_equal, assert_raises, assert_true, assert_false

import maya.standalone
maya.standalone.initialize(name="python")

import maya.cmds as cmds

class TestShadingComponent(object):
    def setup(self):
        test_component_plugin = os.path.join(os.path.dirname(__file__), "nodes", "test_component.py")
        cmds.loadPlugin(test_component_plugin)
        
    def teardown(self):
        cmds.file(newFile=True, force=True)
        cmds.unloadPlugin("test_component")
        
    def test_loaded(self):
        assert_true(cmds.pluginInfo("test_component", query=True, loaded=True))
        
    def test_create(self):
        node = cmds.createNode("test_component")
        assert_true(node)
        
