import delight

class dl_blendByAxis(delight.Utility):
    typeid = 0x00300338
    description = "Blend by axis."

    coordsys = delight.CoordinateSystem(shortname='cs', default='world')
    axis = delight.Enum(default='Y', choices=['X', 'Y', 'Z'])

    globalWarpMode = delight.Enum(shortname='gm', default='Off', choices=['Off', 'Noise','Input'])
    globalWarpNoiseAmount = delight.Float(shortname='gwna', default=1)
    globalWarpNoiseFreq = delight.Float(shortname='gwnf', default=1)
    globalWarpNoiseOffset = delight.Vector(shortname='gwno', default=0)
    globalWarpInput = delight.Vector(shortname='gwi', default=0)
    globalWarp = delight.Group([globalWarpMode, globalWarpNoiseAmount, globalWarpNoiseFreq, globalWarpNoiseOffset, globalWarpInput])

    label = delight.String(shortname='lbl')
    colour = delight.Color(shortname='clr')
    value = delight.Float(default=0)
    blend = delight.Enum(default='smooth', choices=['smooth', 'linear', 'step'])

    warpToUse = delight.Enum(shortname='wtu', default='Global', choices=['Global','Local'])
    warpMode = delight.Enum(shortname='wm', default='Off', choices=['Off', 'Noise','Input'])
    warpNoiseAmount = delight.Float(shortname='wna', default=1)
    warpNoiseFreq = delight.Float(shortname='wnf', default=1)
    warpNoiseOffset = delight.Vector(shortname='wno', default=0)
    warpInput = delight.Vector(shortname='wi', default=0)

    entries = delight.Compound([label, colour, value, blend,
        warpToUse, warpMode, warpNoiseAmount, warpNoiseFreq, warpNoiseOffset, warpInput], array=True)

    outColor = delight.Color(output=True)

    element0outColor = delight.Color(output=True)
    element1outColor = delight.Color(output=True)
    element2outColor = delight.Color(output=True)
    element3outColor = delight.Color(output=True)
    element4outColor = delight.Color(output=True)
    element5outColor = delight.Color(output=True)
    element6outColor = delight.Color(output=True)
    element7outColor = delight.Color(output=True)

    element0outAlpha = delight.Float(output=True)
    element1outAlpha = delight.Float(output=True)
    element2outAlpha = delight.Float(output=True)
    element3outAlpha = delight.Float(output=True)
    element4outAlpha = delight.Float(output=True)
    element5outAlpha = delight.Float(output=True)
    element6outAlpha = delight.Float(output=True)
    element7outAlpha = delight.Float(output=True)

    # TODO: Uncomment and fix this so that when it's first 
    # instantiated, the node has 3 elements in the axes[] array, each
    # in world space, each with orientation = positive and negative, with
    # axisVector = (1,0,0), (0,1,0), and (0,0,1), respectively.
    #
    #def postConstructor(self):
    #    axesPlug = MPlug(self.thisMObject(), self.axes.obj)
    #    for i in range(0, 3):

    #        axes0Plug = axesPlug.elementByLogicalIndex(i)
    #        axesColorPlug = axes0Plug.child(self.axisColor.obj)
    #        axesColorPlug.setMObject(MFnStringData().create('whatever'))
    #    
    #    super(dl_blendByAxis, self).postConstructor()

    
    rsl = \
    """

#define assingElement(type, i, val) \
    if (i == 0) o_element0out##type = val; \
    else if (i == 1) o_element1out##type = val; \
    else if (i == 2) o_element2out##type = val; \
    else if (i == 3) o_element3out##type = val; \
    else if (i == 4) o_element4out##type = val; \
    else if (i == 5) o_element5out##type = val; \
    else if (i == 6) o_element6out##type = val; \
    else if (i == 7) o_element7out##type = val;

    float linInterp (float start, end, val) {
        return clamp((val-start)/(end-start), 0, 1);
    }

    float interp (float start, end, val, mode) {
        float result;
        if (mode < .5) {
            result = smoothstep(start, end, val);
        } else if (mode < 1.5) {
            result = linInterp(start, end, val);
        } else {
            result = filterstep(end, val);
        }
        return result;
    }


    float nElements = arraylength(i_colour);
    color result = 0;
    if (nElements > 0) {

        float nextI=0; float prevI=0;
        float nextVal=0; float prevVal=0;
        color nextClr=0; color prevClr=0;
        float nextBnd=0;

        float i;
        string coordsys = i_coordsys == "" ? "world" : i_coordsys;
        extern point P;
        point Pcs = transform(coordsys, P);
        float coord = Pcs[i_axis];
        point Pnoise = Pcs;
        Pnoise[i_axis] = 0;

        float warpedValues[nElements];



        for (i = 0; i < nElements; i += 1) {
            float warpMode = i_globalWarpMode;
            float warpNoiseAmount = i_globalWarpNoiseAmount;
            float warpNoiseFreq = i_globalWarpNoiseFreq;
            vector warpNoiseOffset = i_globalWarpNoiseOffset;
            vector warpInput = i_globalWarpInput;

            if (i_warpToUse[i] == 1) {
                warpMode = i_warpMode[i];
                warpNoiseAmount = i_warpNoiseAmount[i];
                warpNoiseFreq = i_warpNoiseFreq[i];
                warpNoiseOffset = i_warpNoiseOffset[i];
                warpInput = i_warpInput[i];
            }

            float warp = warpMode == 0 ? 0 : warpMode == 2 ? warpInput[i_axis] : 
                warpNoiseAmount * (1-2*(float noise((Pnoise + warpNoiseOffset)
                    * warpNoiseFreq)));

            warpedValues[i] = i_value[i] + warp;
        }

        float foundPrev = 0;
        float foundNext = 0;
        
        for (i = 0; i < nElements; i += 1) {
            if (warpedValues[i] > coord) {
                if (foundNext < .5 || warpedValues[i] < nextVal) {
                    foundNext = 1;
                    nextVal = warpedValues[i];
                    nextClr = i_colour[i];
                    nextBnd = i_blend[i];
                    nextI = i;
                }
            } else {
                if (foundPrev < .5 || warpedValues[i] > prevVal) {
                    foundPrev = 1;
                    prevVal = warpedValues[i];
                    prevClr = i_colour[i];
                    prevI = i;
                }
            }
        }

        if (foundPrev < .5) {
            result = nextClr;
            assingElement(Color, nextI, result);
            assingElement(Alpha, nextI, 1);
        } else if (foundNext < .5) {
            result = prevClr;
            assingElement(Color, prevI, result);
            assingElement(Alpha, prevI, 1);
        } else {
            float mixer = interp(prevVal, nextVal, coord, nextBnd);
            result = mix(prevClr, nextClr, mixer);
            assingElement(Color, nextI, nextClr * mixer);
            assingElement(Color, prevI, prevClr * (1-mixer));
            assingElement(Alpha, nextI, mixer);
            assingElement(Alpha, prevI, 1-mixer);
        }
    }

    o_outColor = result;
    """


    rslpost = ""


def initializePlugin(obj):
    dl_blendByAxis.register(obj)

def uninitializePlugin(obj):
    dl_blendByAxis.deregister(obj)
