#ifndef _remap_utils_h
#define _remap_utils_h

#define LN05 (-0.693147181)

// Perlin's bias and gain
float
floatBias(float bias; float t; )
{
    if (bias == 0.5)
        return t;
    else
	   return pow(t, log(bias)/LN05);
}

color
colorBias(float bias; color c; )
{
    if (bias == 0.5)
    {
        return c;
    }
    else
    {
	    float k = log(bias)/LN05;
    	return color(pow(comp(c, 0), k), pow(comp(c, 1), k), pow(comp(c, 2), k));
	}
}

float
floatGain( float gain; float t; )
{
    if (gain == 0.5)
    {
        return t;
    }
    else
    {
    	if (t < 0.5)
    		return 0.5*floatBias(1-gain, 2*t);
    	else
    		return 1-0.5*floatBias(1-gain, 2-2*t);
    }
}

color
colorGain( float gain; color c; )
{
    if (gain == 0.5)
    {
        return c;
    }
    else
    {
    	return color(floatGain(gain, comp(c, 0)),
    				 floatGain(gain, comp(c, 1)),
    				 floatGain(gain, comp(c, 2)));
    }
}

// Christopher Schlick's approximation to bias and gain
// Note: this blows up badly if inputs are outside of [0,1]
float
floatFastBias(float bias;float t; )
{
    if (bias == 0.5)
        return t;
    else
        return t / ((1/max(bias,1e-4) - 2) * (1 - t) + 1);
}

color
colorFastBias( float bias; color c; )
{
    if (bias == 0.5)
    {
        return c;
    }
    else
    {
        color cb, w = color(1,1,1);
        return c / ((w/max(bias,1e-4) - 2) * (w - c) + w);
    }
}

float
floatFastGain( float gg; float t; )
{
    if (gg == 0.5)
    {
        return t;
    }
    else
    {
        float tg, gain;
        gain = clamp(gg, .0001, .9999);
        if( t < .5 )
        {
        	tg = t / ((1/gain - 2) * (1 - 2*t) + 1);
        }
        else
        {
        	tg = ((1/gain - 2) * (1 - 2*t) - t) /
    			((1/gain - 2) * (1 - 2*t) - 1);
        }
        return tg;
    }
}

color
colorFastGain( float gain; color c; )
{
    if (gain == 0.5)
    {
        return c;
    }
    else
    {
        color cb;
        setcomp(cb, 0, floatFastGain( gain, comp(c,0) ) );
        setcomp(cb, 1, floatFastGain( gain, comp(c,1) ) );
        setcomp(cb, 2, floatFastGain( gain, comp(c,2) ) );
        return cb;
    }
}

float
remapFloat(float intensity; float bias; float gain; float t; )
{
   return intensity * floatGain(gain, floatBias(bias, t));
}

color
remapColor(float intensity; float bias; float gain; color c; )
{
	return intensity * colorGain(gain, colorBias(bias, c));
}

float
remapOcclusion(float intensity; float bias; float gain; float occ; )
{
	// occ is occlusion -- 0 = unoccluded, 1 = completely occluded
	float unocc = 1-occ;
	unocc = floatBias(bias, unocc);
	unocc = floatGain(gain, unocc);
	return min((1-unocc) * intensity, 1);
}

color
remapHDRI(float exposure; float gamma; float offset; color c; )
{
	color
	powc(color x; float y;)
	{
		return color(pow(comp(x, 0), y), pow(comp(x, 1), y), pow(comp(x, 2), y));
	}

    return powc(c*pow(2, exposure), gamma)+offset;
}

#endif
