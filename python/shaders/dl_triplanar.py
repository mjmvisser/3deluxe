import deluxe

class dl_triplanar(deluxe.Utility):
    typeid = 0x00300335
    description = "Triplanar texture projector."
    
    
    coordsys = deluxe.CoordinateSystem(shortname="cs", default="world", help="""
        Enter a standard shading space (eg 'world', 'object') or a coordinate system shape.
        """)
    scale = deluxe.Float(shortname="sc", default=1, help="Global scale for x, y, and z projections.")
    blendWidth = deluxe.Float(shortname="bl", default=.5,
        help="How much to blend between x, y, and z projections (0 makes hard line between them).")

    warpMode = deluxe.Enum(shortname='wm', default='Off', choices=['Off', 'Noise','Input'])
    warpNoiseAmount = deluxe.Float(shortname='wna', default=1)
    warpNoiseFreq = deluxe.Float(shortname='wnf', default=1)
    warpNoiseOffset = deluxe.Vector(shortname='wno', default=0)
    warpInput = deluxe.Vector(shortname='wi', default=0)
    warp = deluxe.Group([warpMode, warpNoiseAmount, warpNoiseFreq, warpNoiseOffset, warpInput])

    Xtex = deluxe.Image(shortname="xtx", default="", help="Texture for projection on x-axis.")
    Xrot = deluxe.Float(shortname="xro", default=0, softmin=-180, softmax=180,
        help="Rotation about x-axis of x-axis projection.")
    XrepeatS = deluxe.Float(shortname="xrs", default=1, help="Repetitions of s-coordinate.", softmin = -2, softmax = 2)
    XrepeatTSameAsS = deluxe.Boolean(shortname="xrst", default=True, 
        help="Also use XrepeatS value for repetitions of t-coordinate (ignore XrepeatT parameter).")
    XrepeatT = deluxe.Float(shortname="xrt", default=1, help="Repetitions of t-coordinate (ignored if XrepeatTSameAsS is on).", softmin = -2, softmax = 2) 

    Xprojection = deluxe.Group([Xtex, Xrot, XrepeatS, XrepeatTSameAsS, XrepeatT], collapse=False)

    Ytex = deluxe.Image(shortname="ytx", default="",
        help="Texture for projection on y-axis.  If blank or invalid, Xtex is used.")
    Yrot = deluxe.Float(shortname="yro", default=0, softmin=-180, softmax=180,
        help="Rotation about y-axis of y-axis projection.")
    YrepeatS = deluxe.Float(shortname="yrs", default=1, help="Repetitions of s-coordinate.", softmin = -2, softmax = 2)
    YrepeatTSameAsS = deluxe.Boolean(shortname="yrst", default=True,
        help="Also use YrepeatS value for repetitions of t-coordinate (ignore YrepeatT parameter).")
    YrepeatT = deluxe.Float(shortname="yrt", default=1, help="Repetitions of t-coordinate (ignored if YrepeatTSameAsS is on).", softmin = -2, softmax = 2)

    Yprojection = deluxe.Group([Ytex, Yrot, YrepeatS, YrepeatTSameAsS, YrepeatT], collapse=False)

    Ztex = deluxe.Image(shortname="ztx", default="",
        help="Texture for projection on z-axis.  If blank or invalid, Xtex is used.")
    Zrot = deluxe.Float(shortname="zro", default=0, softmin=-180, softmax=180,
        help="Rotation about z-axis of z-axis projection.")
    ZrepeatS = deluxe.Float(shortname="zrs", default=1, help="Repetitions of s-coordinate.", softmin = -2, softmax = 2)
    ZrepeatTSameAsS = deluxe.Boolean(shortname="zrst", default=True,
        help="Also use ZrepeatS value for repetitions of t-coordinate (ignore ZrepeatT parameter).")
    ZrepeatT = deluxe.Float(shortname="zrt", default=1, help="Repetitions of t-coordinate (ignored if ZrepeatTSameAsS is on).", softmin = -2, softmax = 2)

    Zprojection = deluxe.Group([Ztex, Zrot, ZrepeatS, ZrepeatTSameAsS, ZrepeatT], collapse=False)

    Pref = deluxe.Point(message=True, messagetype='Pref_param', storage='varying')
    
    outColor = deluxe.Color(output=True)
    
    
    rslpost = ""
    rsl = \
    """

    void warpN(
        float warpMode;
        float warpNoiseAmount;
        float warpNoiseFreq;
        vector warpNoiseOffset;
        vector warpInput;
        point Pp;
        output vector n)
    {
        if (warpMode == 1) {
            n += (1-2*(vector noise((Pp + warpNoiseOffset)*warpNoiseFreq)))*warpNoiseAmount;
        } else if (warpMode == 2) {
            n += warpInput;
        }
        n = normalize(n);
    }

    float fit (float v, omn, omx, nmn, nmx) {
        return nmn + (v-omn)/(omx-omn) * (nmx - nmn);
    }

    void rotST(float rot; output float ss, tt) {
        float ssRemap = fit(ss, 0, 1, -1, 1);
        float ttRemap = fit(tt, 0, 1, -1, 1);
        float dist = sqrt(ssRemap*ssRemap + ttRemap*ttRemap);
        float ang = atan(ssRemap, ttRemap);
        ang += radians(rot);
        ss = fit(dist*sin(ang), -1, 1, 0, 1);
        tt = fit(dist*cos(ang), -1, 1, 0, 1);
    }

    void getTextureAndWeight (
        float ss, tt; string tx;
        normal Nw; vector axis;
        float repeatS, repeatTSameAsS, repeatT, blend, rot;
        output color txClr; output float weight
    ) {

        weight = abs(Nw.axis);
        if (blend != 0) weight = pow(weight, 1/blend);

        if (tx == "" || textureinfo(tx, "exists", 0) == 0) {
            txClr = 0;
        } else {
            float ssFinal = Nw.axis > 0 ? ss : 1-ss;
            float ttFinal = tt;
            rotST(rot, ssFinal, ttFinal);
            ssFinal *= repeatS;
            ttFinal *= repeatTSameAsS == 1 ? repeatS : repeatT;
            txClr = texture(tx, ssFinal, ttFinal);
        }
    }

    extern varying point P;
    extern varying point Pref;
    extern vector I;
    extern normal N;

    point pp = P;
    if(Pref != point(0))
        pp = Pref;
        
    point Pcs = transform(i_coordsys, pp);
    point Ptex = Pcs / i_scale;
    normal Nn = normalize(N);
    normal Ncs = normalize(ntransform(i_coordsys, Nn));
    
    warpN(i_warpMode, i_warpNoiseAmount, i_warpNoiseFreq,
        i_warpNoiseOffset, i_warpInput, Pcs, Ncs);

    color XtxClr, YtxClr, ZtxClr;
    float Xw, Yw, Zw;

    string YtexFinal = (i_Ytex == "" || textureinfo(i_Ytex, "exists", 0) == 0) ? i_Xtex : i_Ytex;
    string ZtexFinal = (i_Ztex == "" || textureinfo(i_Ztex, "exists", 0) == 0) ? i_Xtex : i_Ztex;

    getTextureAndWeight (-Ptex[2], -Ptex[1], i_Xtex, Ncs, (1, 0, 0), 
        i_XrepeatS, i_XrepeatTSameAsS, i_XrepeatT, i_blendWidth, i_Xrot, XtxClr, Xw);
    getTextureAndWeight (-Ptex[0], -Ptex[2], YtexFinal, Ncs, (0, 1, 0), 
        i_YrepeatS, i_YrepeatTSameAsS, i_YrepeatT, i_blendWidth, i_Yrot, YtxClr, Yw);
    getTextureAndWeight (-Ptex[1], -Ptex[0], ZtexFinal, Ncs, (0, 0, 1), 
        i_ZrepeatS, i_ZrepeatTSameAsS, i_ZrepeatT, i_blendWidth, i_Zrot, ZtxClr, Zw);

    if (i_blendWidth == 0) {
        if (Xw > Yw && Xw > Zw)
            Yw = Zw = 0;
        else if (Yw > Xw && Yw > Zw)
            Xw = Zw = 0;
        else
            Xw = Yw = 0;
    }
    o_outColor = (XtxClr * Xw + YtxClr * Yw + ZtxClr * Zw)/(Xw + Yw + Zw);
    """


def initializePlugin(obj):
    dl_triplanar.register(obj)

def uninitializePlugin(obj):
    dl_triplanar.deregister(obj)
