##
## Copyright (C) 2008 Lumiere Visual Effects. All rights reserved.
##
## $Id $
##

import maya.cmds

shaders = [
           # components
           'dl_ambient',
           'dl_diffuse',
           'dl_incandescence',
           'dl_reflection',
           'dl_refraction',
           'dl_specular',
           'dl_fur',

           # shaders
           'dl_layer',
           'dl_displacement',

           #textures
           'dl_curvature',
           'dl_cellNoise',
           'dl_textureMap',
           'dl_textureMapCoordsys',
           'dl_triplanar',
           'dl_axisProject',
           'dl_blendByAxis',
           'dl_blendByNormal',
           'dl_iridescence',
           'dl_switch',
           'dl_ocean',
           'dl_shadowBlocker',
           'dl_projectionCollector',
           'dl_volumeNoise',

            #lights
           'dl_uberLightShape',
           'dl_envLightShape',
           'dl_indirectLightShape',
           #'dl_pointCloudLightShape',
#           'dl_bakeLightShape',
           'dl_projectionLightShape',
           
           #utils
           'dl_attributeFloat',
           'dl_attributeColor',
           'dl_attributeString',
           'dl_externFloat',
           'dl_externColor',
           'dl_externString',
           ]

maya.cmds.loadPlugin('dl_mattePaint')
maya.cmds.loadPlugin('dl_delightSwatch')

for shader in shaders:
    if not maya.cmds.pluginInfo(shader, query=True, loaded=True):
        maya.cmds.loadPlugin('%s.py'%shader)

