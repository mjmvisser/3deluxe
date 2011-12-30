/**************************************************************************
 * fog.sl
 *
 * Description:
 *    This is a volume shader for fog.  Trapezoidal integration is
 *    used to find scattering and extinction.
 *
 * Parameters:
 *   opacity - overall fog density control as it affects its ability
 *          to block light from behind it.
 *   lightdensity - fog density control as it affects light scattering
 *          toward the viewer.
 *   integstart, integend - bounds along the viewing ray direction of the
 *          integration of atmospheric effects.
 *   stepsize - step size for integration
 *   smokefreq, smokeoctaves, smokevary - control the fBm of the noisy fog
 *          If either smokeoctaves or smokevary is 0, there is no noise
 *          to the fog.
 *   scatter - when non-1, can be used to give wavelength-dependent
 *          extinction coefficients.
 *
 * Author: Larry Gritz
 *
 * Reference:
 *   _Advanced RenderMan: Creating CGI for Motion Picture_, 
 *   by Anthony A. Apodaca and Larry Gritz, Morgan Kaufmann, 1999.
 *
 * $Revision: 1.1.1.1 $     $Date: 2000/08/28 01:30:35 $
 *
 **************************************************************************/


#include "filter_utils.h"

#ifndef snoise
/*
 * Signed noise -- the original Perlin kind with range (-1,1) We prefer
 * signed noise to regular noise mostly because its average is zero.
 * We define three simple macros:
 *   snoise(p) - Perlin noise on either a 1-D (float) or 3-D (point) domain.
 *   snoisexy(x,y) - Perlin noise on a 2-D domain.
 *   vsnoise(p) - vector-valued Perlin noise on either 1-D or 3-D domain.
 */
#define snoise(p) (2 * (float noise(p)) - 1)
#define snoisepw(p, w) (2 * (float noise(p, w)) - 1)
#define snoisexy(x,y) (2 * (float noise(x,y)) - 1)
#define vsnoise(p) (2 * (vector noise(p)) - 1)
#endif


/* If we know the filter size, we can crudely antialias snoise by fading
 * to its average value at approximately the Nyquist limit.
 */
#define filteredsnoise(p,width) (snoise(p) * (1-smoothstep (0.2,0.75,width)))
#define filteredsnoisepw(p, w, width) (snoisepw(p, w) * (1-smoothstep (0.2,0.75,width)))
#define filteredvsnoise(p,width) (vsnoise(p) * (1-smoothstep (0.2,0.75,width)))



/* fractional Brownian motion
 * Inputs: 
 *    p, filtwidth   position and approximate inter-pixel spacing
 *    octaves        max # of octaves to calculate
 *    lacunarity     frequency spacing between successive octaves
 *    gain           scaling factor between successive octaves
 */


float fBm4d (point p; float filtwidth;
    uniform float w, octaves, lacunarity, gain)
    {
        uniform float amp = 1;
        varying point pp = p;
        varying float sum = 0, fw = filtwidth;
        uniform float i;

        for (i = 0;  i < octaves;  i += 1) {
#pragma nolint
        sum += amp * filteredsnoisepw (pp, w, fw);
        amp *= gain;  pp *= lacunarity;  fw *= lacunarity;
    }
    return sum;
}



/* For point P (we are passed both the current and shader space
 * coordinates), gather illumination from the light sources and
 * compute the fog density at that point.  Only count lights tagged
 * with the "__foglight" parameter.  
 */
void
smokedensity (point Pcur, Pshad; 
	      uniform float frame;
          uniform float noisy, smokevary, smokefreq, smokeoctaves;
	      float stepsize;
	      output color Lscatter; output float fog)
{
    Lscatter = 0;//incandescence;
    illuminance (Pcur) {
        extern color Cl;
        float foglight = 1;
        lightsource("__foglight",foglight);
        if (foglight > 0)
            Lscatter += Cl;
    }
    if (smokeoctaves > 0 && smokevary > 0 && noisy > 0) {
        point Psmoke = Pshad * smokefreq;
#pragma nolint
        fog = snoisepw (Psmoke, frame);
        //Optimize: one octave only if not lit
        if (comp(Lscatter,0)+comp(Lscatter,1)+comp(Lscatter,2) > 0.01)
            fog += 0.5 * fBm4d (Psmoke*2, stepsize*2, frame, smokeoctaves-1, 2, 0.5);
        fog = smoothstep(-1,1,smokevary*fog);
        fog = mix(.5, fog, noisy);
    } else {
        fog = 0.5;
    }
}



/* Return a component-by-component exp() of a color */
color colorexp (color C)
{
    return color (exp(comp(C,0)), exp(comp(C,1)), exp(comp(C,2)));
}


volume
dl_fog (
    float opacity = 0;
    color diffuse = .25;
    color incandescence = 0;
    float integstart = 0;
    float integend = 100;
    float stepsize = 0.1;
    float maxsteps = 100000;
    float smokenoisy = 1;
    float smokeoctaves = 3;
    float smokefreq = 1;
    float smokevary = 1;
    vector animdir = 1;
    float animdirspeed = .015;
    float animambspeed = .025;
) {
    color scatter = 1;   /* FORMERLY A PARAMETER. for sky, try (1, 2.25, 21) */
    point Worigin = P - I;    /* Origin of volume ray */
    point origin = transform ("world", Worigin);
    float dtau, last_dtau;
    color li, last_li;

    /* Get current frame */
    uniform float frame = 322;
    option("user:delight_curr_frame", frame);


    /* Integrate forwards from the start point */
    float d = integstart + random()*stepsize;
    vector IN = normalize (vtransform ("world", I));
    vector WIN = vtransform ("world", "current", IN);

    /* Calculate a reasonable step size */
    float end = min (length (I), integend) - 0.0001;
    float ss = min (stepsize, end-d);
    /* Get the in-scattered light and the local fog density for the
    * beginning of the ray 
    */
    point Psmoke = origin + d * IN + normalize(animdir) * animdirspeed * frame;
    smokedensity (Worigin + d*WIN, Psmoke, frame*animambspeed,
        smokenoisy, smokevary, smokefreq, smokeoctaves, ss, last_li, last_dtau);

    color Cv = 0, Ov = 0;   /* color & opacity of volume that we accumulate */
    while (d <= end) {
        /* Take a step and get the local scattered light and fog density */
        ss = clamp (ss, 0.005, end-d);
        d += ss;
        point Psmoke = origin + d * IN + normalize(animdir) * animdirspeed * frame;
        smokedensity (Worigin + d*WIN, Psmoke, frame*animambspeed,
            smokenoisy, smokevary, smokefreq, smokeoctaves, ss, li, dtau);

        /* Find the blocking and light scattering contribution of 
        * the portion of the volume covered by this step.
        */
        float tau = opacity * ss/2 * (dtau + last_dtau);
        color lighttau = diffuse * ss/2 * (li*dtau + last_li*last_dtau);
        lighttau += incandescence * ss/2 * (dtau + last_dtau);

        /* Composite with exponential extinction of background light */
        Cv += (1-Ov) * lighttau;
        Ov += (1-Ov) * (1 - colorexp (-tau*scatter));
        last_dtau = dtau;
        last_li = li;
    }

    /* Ci & Oi are the color and opacity of the background element.
    * Now Cv is the light contributed by the volume itself, and Ov is the
    * opacity of the volume, i.e. (1-Ov)*Ci is the light from the background
    * which makes it through the volume.  So just composite!
    */
    Ci = Cv + (1-Ov)*Ci; 
    Oi = Ov + (1-Ov)*Oi;
}

