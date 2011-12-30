float luminance(color c) {
    return (c[0] + c[1] + c[2])/3;
}

float getSpecMultiplier (vector Ln; normal Nn; vector Vn; float roughness) {
    vector H = normalize(Ln+Vn);
    return pow(max(0.0, Nn.H), 1/roughness);
}


// From: /dfs1/net/home/jeremye/workspace/3delight/python/shaders/dl_uberLightShape.py
surface dl_hair (
    color basecolor=1;
    color tipcolor=1;
    color basecolorTint=1;
    color tipcolorTint=1;
    color spec1color=1;
    float specRoughness = .1;
    float spec1Intens=.02;
    float spec1shiftToRoot = 1;
    float spec2intens=1;
    float spec2shiftToTip = 1;
    float spec2thicknessShift = .3;
    float diffIntens=.5;
    float diffFalloff = .5;
    float debug = 0;
    )
{ 
    color baseclrToUse = (1, 0, 0);
    color tipclrToUse = (0, 1, 0);
    color spec1colorToUse = (0, 0, 1);
    if (debug < 1) {
        baseclrToUse = basecolor * basecolorTint;
        tipclrToUse = tipcolor * tipcolorTint;
        spec1colorToUse = spec1color;
    }

    float widCoord = u;
    vector In = normalize(I);
    vector widDir = normalize(dPdu);
    vector lenDir = normalize(dPdv);
    


    // Fake normal.
    float cosAng = 2*widCoord - 1;
    float sinAng = 1-cosAng*cosAng;
    vector toCam = vector "camera" (0, 0, -1);

    extern normal N;
    normal Nn = normalize(N);
    normal flatN = normal (cosAng * widDir + sinAng * Nn);
    float round = 1;
    Nn = normalize(mix(flatN, Nn, round));
    //Nn = faceforward(Nn, In);
    //Nn = normalize(widDir^lenDir);
    // the extent to which viewdir is perp to lenDir and widDir.
    vector V = -In;
    float perpToLen = lenDir.V;
    perpToLen = 1-perpToLen*perpToLen;
    float perpToWid = sinAng;

    color diffClr = mix(baseclrToUse, tipclrToUse, v);

    color c = 0;
    illuminance (P) 
    {
        extern point E;
        vector Ln = normalize(L);
        // First spec component from the surface.
        // The shaded point should be shifted along lengthDir toward root due to
        // serrated surface.  This moves spec toward root.

        point Pspec1 = P + spec1shiftToRoot * lenDir;
        vector Vspec1 = normalize(E - Pspec1);
        color spec1 = getSpecMultiplier (Ln, Nn, Vspec1, specRoughness );

        // Second spec component is reflected from the opposite, inner side of the hair.
        // The shaded point should be shifted along lengthDir toward tip due to
        // serrated surface.  This moves spec toward root.
        point Pspec2 = P - spec2shiftToTip * lenDir;

        // The shaded point should also be shifted along the surface toward the light because
        // that is where the ray would have entered the hair in order to come out at P.
        vector thicknessShift = -Ln+Nn*Ln.Nn;
        //Pspec2 = Pspec2 + thicknessShift * spec2thicknessShift;
        vector Vspec2 = normalize(E - Pspec2);
        color spec2 = specularbrdf (Ln, Nn, Vspec2, specRoughness );

        color diff = mix(1, max(0, Ln.Nn), diffFalloff);
        c += (spec1Intens * spec1colorToUse * spec1 + (spec2intens * spec2 + diffIntens * diff) * diffClr)*Cl;
        //c = Cl;
    }
    //c = Nn.V;

    //c[0] *= sinAng;
    Ci= c;
    //Ci[0] = (1, 0, 0).normalize(N);
    //Ci[1] = u;
    //Ci = diffClr;
    //Ci[2] = v;
    //Ci[0] = u;
    //Ci[1] = v;
    //Ci[2] = .5;
}


