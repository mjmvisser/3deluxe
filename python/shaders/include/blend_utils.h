#ifndef __blend_utils_h
#define __blend_utils_h


color applyAlphaToTransparency(	color trans;
								float alpha)
{
	uniform color white = color(1,1,1);

	return  white - ((white-trans)*alpha);
}
void
blend(uniform float mode;
      color fgc;
      color fga;
      color bgc;
      color bga;
      output color resultc;
      output color resulta;
    )
{
	uniform color white = color(1,1,1);
	if(mode == 0) /* over */
	{
		color tmp = white - fga;
		resultc = fgc + tmp * bgc;
		resulta = fga + tmp * bga;
	}
	else if(mode == 1) /* under */
	{
		color tmp = (white - bga);
		resultc = bgc + tmp * fgc;
		resulta = bga + tmp * fga;
	}
	else if(mode == 2) /* in */
	{
		resultc = bga * fgc;
		resulta = fga * bga;
	}
	else if(mode == 3) /* out */
	{
		color tmp = (white - bga);
		resultc = tmp * fgc;
		resulta = tmp * bga;
	}
	else if(mode == 4) /* atop */
	{
		color tmp = (white - fga);
		resultc = bga * fgc + tmp * bgc;
		resulta = bga * fga + tmp * bga;
	}
	else if(mode == 5) /* xor */
	{
		color tmp1 = (white - bga);
		color tmp2 = (white - fga);
		resultc = tmp1 * fgc + tmp2 * bgc;
		resulta = tmp1 * fga + tmp2 * bga;
	}
	else if(mode == 6) /* cover */
	{
		color tmp = 1 - fga;
		resultc = fgc + ((comp(bga,0) <= comp(tmp, 0)) ? bgc : tmp * (bgc / bga));
		resulta = fga + ((comp(bga,0) <= comp(tmp, 0)) ? bga : tmp);
	}
	else if(mode == 7) /* add */
	{
		resultc = fgc + bgc;
		resulta = fga + bga;
	}
	else if(mode == 8) /* subtract */
	{
		resultc = fgc - bgc;
		resulta = fga - bga;
	}
	else if(mode == 9) /* multiply */
	{
		resultc = fgc * bgc;
		resulta = fga * bga;
	}
	else if(mode == 10) /* difference */
	{
		color tmp = fgc - bgc;
		color tmp2 = white - fga;
		setcomp(tmp, 0, abs(comp(tmp,0)));
		setcomp(tmp, 1, abs(comp(tmp,1)));
		setcomp(tmp, 2, abs(comp(tmp,2)));
		resultc = tmp + bgc * tmp2;
		resulta = fga + bga * tmp2;
	}
	else if(mode == 11) /* lighten */
	{
		color tmp = white - fga;
		resultc = max(fgc, bgc) + bgc * tmp;
		resulta = fga + bga * tmp;
	}
	else if(mode == 12) /* darken */
	{
		color tmp = white - fga;
		resultc = min(fgc, bgc) + bgc * tmp;
		resulta = fga + bga * tmp;
	}
	else if(mode == 13) /* saturate */
	{
		resultc = bgc * (1 + fgc);
		resulta = bga;
	}
	else if(mode == 14) /* desaturate */
	{
		resultc = bgc * (1 - fgc);
		resulta = bga;
	}
	else if(mode == 15) /* illuminate */
	{
		resultc = bgc;
		resulta = bga * (1 - fga);
	}
	else /* none */
	{
		resultc = fgc;
		resulta = fga;
	}
}

void
blendWithTransparency(
		uniform float mode;
		color fgc;
		color fgt;
		color bgc;
		color bgt;
		output color resultc;
		output color resultt;
		)
{
	uniform color white = color(1,1,1);
	color fga = white - fgt;
	color bga = white - bgt;
	color resulta;
	blend(mode,fgc,fga,bgc,bga,resultc,resulta);

	resultc = bgc;
	resultt = white - resulta;
}

/*
color blendPremultColor(uniform float mode;
						color fgc;
						color fga;
						color bgc;
						color bga;)
{
	color resultColor, resultOpacity;
	blend(mode, fgc*fga, fga, bgc, bga, resultColor, resultOpacity);
	return resultColor;
}

color blendPremultFloat(uniform float mode;
						float fgf;
						color fga;
						float bgf;
						color bga;)
{
	color resultColor, resultOpacity;
	blend(mode, color(fgc*fga), fga, color(bgc), bga, resultColor, resultOpacity);
	return resultColor;
}

*/
#endif /* __blend_utils_h */
