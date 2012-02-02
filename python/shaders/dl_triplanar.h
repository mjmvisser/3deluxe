#ifndef __dl_triplanar_h
#define __dl_triplanar_h

/*
begin inputs
	uniform string coordsys
	float scale
	float blendWidth
	uniform float warpMode
	float warpNoiseAmount
	float warpNoiseFreq
	vector warpNoiseOffset
	vector warpInput
	texture string Xtex
	float Xrot
	float XrepeatS
	uniform float XrepeatTSameAsS
	float XrepeatT
	texture string Ytex
	float Yrot
	float YrepeatS
	uniform float YrepeatTSameAsS
	float YrepeatT
	texture string Ztex
	float Zrot
	float ZrepeatS
	uniform float ZrepeatTSameAsS
	float ZrepeatT
end inputs

begin outputs
	color outColor
end outputs

begin shader_extra_parameters Pref_param
	varying point Pref = point (0, 0, 0);
end shader_extra_parameters

*/

void
maya_dl_triplanar(
	// Inputs
	//
	uniform string i_coordsys;
	float i_scale;
	float i_blendWidth;
	uniform float i_warpMode;
	float i_warpNoiseAmount;
	float i_warpNoiseFreq;
	vector i_warpNoiseOffset;
	vector i_warpInput;
	uniform string i_Xtex;
	float i_Xrot;
	float i_XrepeatS;
	uniform float i_XrepeatTSameAsS;
	float i_XrepeatT;
	uniform string i_Ytex;
	float i_Yrot;
	float i_YrepeatS;
	uniform float i_YrepeatTSameAsS;
	float i_YrepeatT;
	uniform string i_Ztex;
	float i_Zrot;
	float i_ZrepeatS;
	uniform float i_ZrepeatTSameAsS;
	float i_ZrepeatT;
	// Outputs
	//
	output color o_outColor;
	)
{


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
}

#endif /* __dl_triplanar_h */
