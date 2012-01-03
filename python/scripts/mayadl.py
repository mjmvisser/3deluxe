#!/usr/bin/env mayapy

import sys, imp, inspect, os
from optparse import OptionParser

import maya.standalone
import maya.cmds as cmds

# Very important to make sure that the delight module is relative
sys.path.insert(0, '../')
import delight

usage = 'usage: %prog [options] shader'

parser = OptionParser(usage=usage)

parser.add_option('-o', '--output', type='string', dest='output',
                  help='file to write or "-" for stdout', default='-')
parser.add_option('-t', '--template', action='store_true', dest='template',
                  help='write the template generated by the node')
parser.add_option('-r', '--rsl', action='store_true', dest='rsl',
                  help='write the rsl generated by the node')
parser.add_option('-s', '--simulate', action='store_true', dest='simulate',
                  help='simulate loading the plugin in maya')

options, args = parser.parse_args()

try:
    filename = args[0]
    fin = open(filename, 'r')
except Exception, e:
    #print 'Error: ' + str(e)
    parser.print_help()
    sys.exit(1)

if options.output == '-':
    fout = sys.stdout
else:
    fout = open(options.output, 'w')


module = imp.load_module('shader', fin, filename, ('', 'r', imp.PY_SOURCE))
fin.close()
classes = filter(lambda o: isinstance(o[1], type) and issubclass(o[1], delight.Shader),
                 inspect.getmembers(module))

for name, cls in classes:
    if options.template:
        cls.setupAttributes()
        fout.write(cls.getTemplate())
    
    if options.rsl:
        cls.setupAttributes()
        fout.write(cls.getRSL())
        
    if options.simulate:            
        dirname, filename = os.path.split(filename)
        nodename=os.path.splitext(filename)[0]
        os.environ['MAYA_PLUG_IN_PATH'] = '%s:%s'%(dirname, os.environ['MAYA_PLUG_IN_PATH'])
        
        maya.standalone.initialize()
        
        if not cmds.pluginInfo(filename, query=True, loaded=True):        
            cmds.loadPlugin(filename)
            
        node = cmds.createNode(nodename)                
        cmds.delete(node)
        cmds.file(new=True, force=True)
        cmds.unloadPlugin(nodename)
