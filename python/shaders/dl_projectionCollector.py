import delight

class dl_projectionCollector(delight.Utility):
    typeid = 0x00370003
    classification = 'utility/color'
    description = "Wrapper around 3Delight \"texture\" function"

    baseColor = delight.Color(default=0, help="Color before projected textures are applied.")
    baseAlpha = delight.Float(default=0, help="Alpha before projected textures are applied.")
    projLightSubset = delight.String(default="", help="""
Receive projections only from projectionLights with matching projLightSubset values.
They are evaluated in alphabetical order.
    """)

    outColor = delight.Color(shortname="oc", output=True)
    outAlpha = delight.Float(shortname="al", output=True)

              
    rsl = """    

        color composite(
            float compMode;
            color bg, fg;
            float alpha;
            output float totalAlpha;
        ) {
            color outClr = 0;
            if (compMode == 0) {
                outClr = mix(bg, fg, alpha);
            } else {
                outClr = bg + fg;
            }
            totalAlpha = max(totalAlpha, alpha);
            return outClr;
        }


        extern point P;

        color totalColor = i_baseColor;
        float totalAlpha = i_baseAlpha;

        float ss = 0;
        float tt = 0;
        float compositeModeFromLight = 0;
        float alphaFromLight = 0;
        string textureFromLight = "";
        string projLightSubsetFromLight = "";

        illuminance("texture", P,
            "light:__ss", ss,
            "light:__tt", tt,
            "light:__compositeMode", compositeModeFromLight,
            "light:__texture", textureFromLight,
            "light:__alpha", alphaFromLight,
            "light:__projLightSubset", projLightSubsetFromLight
        ) {
            if (projLightSubsetFromLight == i_projLightSubset)
                totalColor = composite(compositeModeFromLight, totalColor, Cl, alphaFromLight, totalAlpha);
        }
        o_outColor = totalColor;
        o_outAlpha = totalAlpha;
    """

    # It would be nice to have an appropriate UI, eg. a square with a perpendicular arrow pointing
    #  from a corner.  I tried to start this based on dl_uberLightShape but got no visible results.
    # def draw(self, view, path, style, status):
    #     view.beginGL()
    #     glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
    #     glFT.glPushMatrix()
    #     glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
    #     divs = 10
    #     for i in range(0, divs, 1):
    #         glFT.glVertex3f(0, i, 0.0)
    #     glFT.glEnd()
    #     glFT.glPopMatrix()
    #     glFT.glPopAttrib()
    #     view.endGL()
    
       
def initializePlugin(obj):
    dl_projectionCollector.register(obj)

def uninitializePlugin(obj):
    dl_projectionCollector.deregister(obj)
