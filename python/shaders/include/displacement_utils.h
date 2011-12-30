#ifndef __displacement_utils_h
#define __displacement_utils_h

float getLip(float lip, lipRimSharp, amount;)
{
	if (lip > 0) {
		float lipDisp = -amount;
		float noLipDisp = amount - 2*lip;
		float mixer = smoothstep(.5 * lipRimSharp,
			1 - .5 * lipRimSharp, amount/(lip * 2));
		return mix(lipDisp, noLipDisp, mixer);
	}
	return amount;
}

void
getDisplacement(
        float amount, doDisp, recalcNormal; 
        uniform float useShadingNormals;
        point Pold; normal Nold, deltaN;
        output point Pnew;
        output normal Nnew;
) {
    point PforN = Pold;

    PforN += Nold * amount;
    
    if (recalcNormal > 0)
    {
        //normal Nlayer = Nnew;
        if (useShadingNormals != 0)
            Nnew = normalize(normalize(calculatenormal(PforN)) + deltaN); 
        else
            Nnew = normalize(calculatenormal(PforN));
        
        Nnew = normalize(mix(Nold, Nnew, recalcNormal));
    }
    
    if (doDisp > 0)
        Pnew = PforN;
}

#endif /* __displacement_utils_h */
