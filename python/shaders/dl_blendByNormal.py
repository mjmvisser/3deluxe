import delight

class dl_blendByNormal(delight.Utility):
    typeid = 0x00300337
    description = "Blend by normal."

    globalCoordsys = delight.CoordinateSystem(shortname='gcs', label='Global Coordsys', default='world',
        description="Coordsys to use if an axis' Coordsys To Use is set to Global Coordsys (default).")
    globalWarpMode = delight.Enum(shortname='gm', default='Off', choices=['Off', 'Noise','Input'])
    globalWarpNoiseAmount = delight.Float(shortname='gwna', default=1)
    globalWarpNoiseFreq = delight.Float(shortname='gwnf', default=1)
    globalWarpNoiseOffset = delight.Vector(shortname='gwno', default=0)
    globalWarpInput = delight.Vector(shortname='gwi', default=0)
    globalWarp = delight.Group([globalWarpMode, globalWarpNoiseAmount, globalWarpNoiseFreq, globalWarpNoiseOffset, globalWarpInput])
    blendWidth = delight.Float(default=1)

    label = delight.String(shortname='lbl', description="""
        label of this axis. """)
    colour = delight.Color(shortname='clr', description="""
        See help for "direction" parm. """)
    coordsysToUse = delight.Enum(shortname='cstu', default='Global Coordsys',
        choices=['Global Coordsys', 'Coordsys For This Axis'], description="""
        Which coordinate system to use, Global Coordsys parm or Coordsys For This Axis
        """)
    coordsysForThisAxis = delight.String(shortname='cs',
        default='world', description=""" Coordinate system of the "direction" parm.  """)
    direction = delight.Vector(shortname='dir', default=(0,1,0), description="""
        Where the normal is closest to this direction (or its reverse,
        see help for "orientation" parm), the corresponding "colour"
        parameter will have the greatest influence.
    """)
    orientation = delight.Enum(default='positive and negative',
        choices=['positive', 'positive and negative', 'negative'],
        description = """
        Choose whether this axis affects the surface where N is
        aligned with the axis direction ("positive"), opposite
        to it ("negative"), or both ("positive and negative").
        """)
    hemispheres = delight.Float(default=1, min=0, max=2,
        description="How many hemispheres this axis affects, 1=half the sphere, 2=the whole sphere")
    weight = delight.Float(shortname='wt', default=1,
        description="The relative influence of this axis.")

    warpToUse = delight.Enum(shortname='wtu', default='Global', choices=['Global','Local'])
    warpMode = delight.Enum(shortname='wm', default='Off', choices=['Off', 'Noise','Input'])
    warpNoiseAmount = delight.Float(shortname='wna', default=1)
    warpNoiseFreq = delight.Float(shortname='wnf', default=1)
    warpNoiseOffset = delight.Vector(shortname='wno', default=0)
    warpInput = delight.Vector(shortname='wi', default=0)

    axes = delight.Compound([label, colour, coordsysToUse, coordsysForThisAxis, direction,
        orientation, hemispheres, weight, warpToUse, warpMode, warpNoiseAmount,
        warpNoiseFreq, warpNoiseOffset, warpInput], shortname='xs', array=True)



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
    #    super(dl_blendByNormal, self).postConstructor()

    
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

    void warpV(
        float warpMode;
        float warpNoiseAmount;
        float warpNoiseFreq;
        vector warpNoiseOffset;
        vector warpInput;
        point Pp;
        output vector v)
    {
        if (warpMode == 1) {
            v += (1-2*(vector noise((Pp + warpNoiseOffset)*warpNoiseFreq)))*warpNoiseAmount;
        } else if (warpMode == 2) {
            v += warpInput;
        }
        v = normalize(v);
    }

    float weights[30];

    float nAxes = arraylength(i_colour);

    extern normal N;

    uniform float i;
    float wtTotal = 0;
    
    for (i = 0; i < nAxes; i += 1) {
        string coordsys = i_coordsysToUse[i] == 0 ? i_globalCoordsys : i_coordsysForThisAxis[i];
        coordsys = coordsys == "" ? "world" : coordsys;
        normal Nn = normalize(ntransform(coordsys, N));
        extern point P;
        point Pp = transform(coordsys, P);
        vector dir = i_direction[i];

        float warpMode = i_globalWarpMode;
        float warpNoiseAmount = i_globalWarpNoiseAmount;
        float warpNoiseFreq = i_globalWarpNoiseFreq;
        vector warpNoiseOffset = i_globalWarpNoiseOffset;
        vector warpInput = i_globalWarpInput;
        if (i_warpToUse[i] == 1) {
            warpMode = i_warpMode[i];
            warpNoiseAmount = i_warpNoiseAmount[i];
            warpNoiseOffset = i_warpNoiseOffset[i];
            warpNoiseFreq = i_warpNoiseFreq[i];
            warpInput = i_warpInput[i];
        }
        warpV(warpMode, warpNoiseAmount, warpNoiseFreq, warpNoiseOffset,
            warpInput, Pp, dir);

        float dot = Nn.normalize(dir);
        float posWt = smoothstep(1-i_hemispheres[i], 1, dot);
        float negWt = smoothstep(1-i_hemispheres[i], 1, -dot);
        float weight = i_orientation[i] == 0 ? posWt :
                i_orientation[i] == 1 ? posWt + negWt : negWt;
        weights[i] = i_weight[i]*pow(weight, 1/max(.01, i_blendWidth));
        wtTotal += weights[i];
    }

    color clrTotal = 0;
    if (wtTotal > 0) {
        for (i = 0; i < nAxes; i += 1) {
            clrTotal += i_colour[i] * weights[i]/wtTotal;
            assingElement(Color, i, i_colour[i]*weights[i]/wtTotal);
            assingElement(Alpha, i, weights[i]/wtTotal);
        }
    }

    o_outColor = clrTotal;

    """


    rslpost = ""


def initializePlugin(obj):
    dl_blendByNormal.register(obj)

def uninitializePlugin(obj):
    dl_blendByNormal.deregister(obj)
