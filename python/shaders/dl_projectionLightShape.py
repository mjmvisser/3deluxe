import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math, sys

import deluxe

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

class dl_projectionLightShape(deluxe.Light):
    typeid = 0x00310005
    includes = ["shadow_utils.h", "utils.h"]

    color = deluxe.Color(shortname='clr', prepare=True, storage='varying', help="""
Colour to project.  Plug this into a maya File node's outColor to project a texture.
""")

    transparency = deluxe.Color(default=0, shortname='trn', storage='varying', help="""
Transparency (1-alpha) of projected colour.  Plug this into a maya File
node's outTransparency to use the texture's (inverted) alpha channel.
""")

    compositeMode = deluxe.Enum(shortname='cpmd', default='Over', choices=['Over', 'Add'], help="""
Compositing mode over previous projections.
projectionLights are evaluated in alphabetical order.
""")
    #repeatMode = deluxe.Enum(default='Blank', choices=['Blank', 'Repeat', 'Hold'], help="")

    projLightSubset = deluxe.String(default="", help="""
Only dl_projectionCollector nodes with matching projLightSubset
values will receive projections from this light.
""")

    # mapped shadows
    shadowBlur = deluxe.Float(label='Blur',
                               shortname='bl', default=0.01, min=0, softmax=0.2, storage='uniform',
                               help="""Amount to blur the shadow. A value of 1.0 would
                                       request that the entire texture be blurred in the result.""")
    shadowFilterType = deluxe.Enum(label='Filter Type',
                                    default='Gaussian',
                                    choices=['Box','Triangle','Gaussian']);
    shadowBias = deluxe.Float(label='Bias',
                               shortname='bi', default=0.225, min=0, softmax=5, storage='uniform',
                               help="Used to prevent self-shadowing. If set to 0, the global bias is used.")
    shadowSamples = deluxe.Integer(label='Samples',
                                    default=16, min=0, softmax=16)
    
    useSoftShadowDecay = deluxe.Boolean(default=False,
                                         help="Turns on soft shadows that decay with distance.")
    shadowMinimumRadius = deluxe.Float(label='Minimum Radius',
                                        shortname='mnr', default=0.001, min=0, softmax=0.2, storage='uniform')
    shadowMaximumRadius = deluxe.Float(label='Maximum Radius',
                                        shortname='mxr', default=0.1, min=0, softmax=0.2, storage='uniform')
    selfShadowReduce = deluxe.Float(default=2, min=0, softmax=5, storage='uniform')
    shadowDecay = deluxe.Float(label='Decay',
                                default=0, min=0, softmax=5, storage='uniform')
    shadowDecayCutOn = deluxe.Float(label='Decay Cut-On',
                                     shortname='sdcon', default=10, min=0, max=1000, storage='uniform')
    shadowDecayCutOff = deluxe.Float(label='Decay Cut-Off',
                                      shortname='sdcoff', default=10, min=0, max=1000, storage='uniform')
    
    softShadowDecay = deluxe.Group([useSoftShadowDecay,
                                     shadowMinimumRadius, shadowMaximumRadius,
                                     selfShadowReduce, shadowDecay,
                                     shadowDecayCutOn, shadowDecayCutOff])

    mappedShadows = deluxe.Group([shadowBlur, shadowFilterType, 
                                   shadowBias, shadowSamples,
                                   softShadowDecay])

    # output messages
    __compositeMode = deluxe.Float(default=0, storage='varying',  output=True, message=True, messagetype='lightsource')
    __alpha = deluxe.Float(default=1, storage='varying', output=True, message=True, messagetype='lightsource')
    __projLightSubset = deluxe.String(default="", output=True, message=True, messagetype='lightsource')


    # category
    __category = deluxe.String(default='texture', message=True, messagetype='lightsource')
    _3delight_light_category = deluxe.String(shortname='cat', default='texture', notemplate=True, norsl=True)

    rslprepare = \
    """
    extern float ss;
    extern float tt;
    extern point Ps;
    point Pl = transform("shader", Ps);
    ss = (Pl[0] + 1)/2;
    tt = (Pl[1] + 1)/2;
    """

    rsl = \
    """

        extern color Cl;
        extern vector L;
        extern point Ps;
        extern normal Ns;
        extern vector I;
        
        extern float __compositeMode;
        extern float __alpha;
        extern string __projLightSubset;

        point Pl = transform("shader", Ps);
        float ss = Pl[0];
        float tt = Pl[1];

        __compositeMode = i_compositeMode;
        float unshadowedAlpha = luminance(1-i_transparency);
        __projLightSubset = i_projLightSubset;

        illuminate(Ps)
        {
            extern uniform string shadowmapname;
            color unoccluded = color getShadowMapContribution(Ps,
                                                        shadowmapname,
                                                        i_shadowBlur,
                                                        i_shadowFilterType,
                                                        i_shadowBias,
                                                        i_shadowSamples,
                                                        i_useSoftShadowDecay,
                                                        i_shadowMinimumRadius,
                                                        i_shadowMaximumRadius,
                                                        i_selfShadowReduce,
                                                        i_shadowDecay,
                                                        i_shadowDecayCutOn,
                                                        i_shadowDecayCutOff);
            __alpha = unshadowedAlpha * luminance(unoccluded);
            Cl = i_color * unoccluded;
        }
    """

    def draw(self, view, path, style, status):
        thisNode = self.thisMObject()
     
        fnThisNode = OpenMaya.MFnDependencyNode(thisNode)
        
        view.beginGL()
        
        glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
        # Color of main light cone ui.
        def dormantColor(clrNum):
            if status == OpenMayaUI.M3dView.kDormant:
                view.setDrawColor(clrNum, OpenMayaUI.M3dView.kActiveColors)
            
        dormantColor(11)
        # Colours: 
        # 0 = black, 1 = mid grey, 2 = light grey, 3 = burgundy, 4 = dark blue,
        # 5 = mid blue, 6 = dark green, 7 = dark purple, 8 = pink, 9 = burgundy again,
        # 11 = burgundy again, 12 = red, 13 = green, 14 = blue, 15 = white, 16 = yellow

        
        glFT.glPushMatrix()
        #glFT.glScalef(iconSize, iconSize, iconSize)
        glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
        glFT.glVertex3f(-1, 1, 0)
        glFT.glVertex3f(1, 1, 0)
        glFT.glVertex3f(1, - 1, 0)
        glFT.glVertex3f(-1, - 1, 0)
        glFT.glEnd()
        glFT.glBegin(OpenMayaRender.MGL_LINES)
        glFT.glVertex3f(-1, 1, 0)
        glFT.glVertex3f(1, - 1, 0)
        glFT.glVertex3f(1, 1, 0)
        glFT.glVertex3f(-1, - 1, 0)
        glFT.glVertex3f(0, 0, 0)
        glFT.glVertex3f(0, 0, - 0.7)
        glFT.glVertex3f(0, 0, - 0.7)
        glFT.glVertex3f(0, 0.04, - 0.4)
        glFT.glVertex3f(0, 0, 0. - 0.7)
        glFT.glVertex3f(0, - 0.04, - 0.4)
        glFT.glVertex3f(0, 0.04, - 0.4)
        glFT.glVertex3f(0, - 0.04, - 0.4)
        glFT.glVertex3f(0, 0, - 0.7)
        glFT.glVertex3f(0.04, 0, - 0.4)
        glFT.glVertex3f(0, 0, 0. - 0.7)
        glFT.glVertex3f(-0.04, 0, - 0.4)
        glFT.glVertex3f(0.04, 0, - 0.4)
        glFT.glVertex3f(-0.04, 0, - 0.4)
        glFT.glEnd()
        glFT.glPopMatrix()
        
        glFT.glPopAttrib()
        
        view.endGL()

    
def initializePlugin(obj):
    dl_projectionLightShape.register(obj)

def uninitializePlugin(obj):
    dl_projectionLightShape.deregister(obj)
