#ifndef __filter_utils_h
#define __filter_utils_h

/* adapted from filterwidth.h by Larry Gritz */


/* Define metrics for estimating filter widths, if none has already
 * been defined.  This is crucial for antialiasing.
 */
#ifndef MINFILTWIDTH
#  define MINFILTWIDTH 1.0e-6
#endif


/* The filterwidth macro takes a float and returns the approximate
 * amount that the float changes from pixel to adjacent pixel.
 */
#ifndef filterwidth
#define filterwidth(x)  max(abs(Du(x)*du) + abs(Dv(x)*dv), 1e-6)
#endif


/* The filterwidthp macro is similar to filterwidth, but is for
 * point data.
 */
#define filterwidthp(p) max (sqrt(area(p)), MINFILTWIDTH)


/* Given a function g, its known average g_avg, its high frequency
 * feature size, and a filter width, fade to the average as we approach
 * the Nyquist limit.
 */
#define fadeout(g,g_avg,featuresize,fwidth) \
        mix (g, g_avg, smoothstep(.2,.6,fwidth/featuresize))

/* filterWidth2 - a filtersize estimator based on the vectors dpu, dpv . */
#define looseFilterWidth2(dpu,dpv) \
    max( length(dpu+dpv), MINFILTWIDTH )

#define tightFilterWidth2(dpu,dpv) \
    max( length(dpu^dpv), MINFILTWIDTH )

#ifdef SHADER_TYPE_displacement
#define filterWidth2(a, b) looseFilterWidth2(a,b)
#else
#define filterWidth2(a, b) tightFilterWidth2(a,b)
#endif

#define filteredFNoise2(p, dpu, dpv) \
    (fadeout(float noise(p), .5, 1, filterWidth2(dpu, dpv)))

#define filteredCNoise2(p, dpu, dpv) \
    (fadeout(color noise(p), color(.5), 1, filterWidth2(dpu, dpv)))

#define filteredVNoise2(p, dpu, dpv) \
    (vector vsnoise(p)*(1-smoothstep (0.2,0.75, filterWidth2(dpu, dpv))))

#endif /* __filter_utils_h */
