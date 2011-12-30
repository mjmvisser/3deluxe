/****************************************************************************
* uberlight.sl - a light with many fun controls.
*
* Description:
*   Based on Ronen Barzel's paper "Lighting Controls for Computer
*   Cinematography" (in Journal of Graphics Tools, vol. 2, no. 1: 1-20).
*
* Rather than explicitly pass "from" and "to" points to indicate the
* position and direction of the light (as spotlight does), this light
* emits from the origin of the local light shader space, and points
* toward the +z axis (also in shader space).  Thus, to position and
* orient the light source, you must translate and rotate the
* coordinate system in effect when the light source is declared.
* Perhaps this is a new idea for some users, but it isn't really
* hard, and it vastly simplifies the math in the shader.
*
***************************************************************************
*
* This shader was written as part of the course notes for ACM
* SIGGRAPH '98, course 11, "Advanced RenderMan: Beyond the Companion"
* (co-chaired by Tony Apodaca and Larry Gritz).  Feel free to use and
* distribute the source code of this shader, but please leave the
* original attribution and all comments.
*
* This shader was tested using Pixar's PhotoRealistic RenderMan 3.7
* and the Blue Moon Rendering Tools (BMRT) release 2.3.6.  I have
* tried to avoid Shading Language constructs which wouldn't work on
* older versions of these renderers, but I do make liberal use of the
* "vector" type and I often declare variables where they are used,
* rather than only at the beginning of blocks.  If you are using a
* renderer which does not support these new language features, just
* substitute "point" for all occurrances of "vector", and move the
* variable declarations to the top of the shader.
*
* Author: coded by Larry Gritz, 1998
*         based on paper by Ronen Barzel, 1997
*
* Contacts:  {lg|ronen} AT pixar DOT com
*
*
* $Revision: 1.3 $    $Date: 2003/12/24 06:18:06 $
*
****************************************************************************/
#ifndef __uberlight_utils_h
#define __uberlight_utils_h


float
coneFalloff(varying point PL;                /* Test point on the x-y plane */
            uniform float cone, coneedge;    /* cone size */
         )
{
    float result;
    float x = xcomp(PL);
    float y = ycomp(PL);
    float q, r;

    float sqr(float x)
    {
        return x*x;
    }

    q = sqr(cone) / sqrt(sqr(cone*abs(x)) + sqr(cone*abs(y)));
    r = sqr(coneedge) / sqrt(sqr(coneedge*abs(x)) + sqr(coneedge*abs(y)));

    result = 1 - smoothstep(q, r, 1);

    return result;
}


// Set the type of illumination falloff with distance from the light
// source.
// off = no falloff.
// on = linear falloff.
// phys = inverse square falloff.
// user = arbitrary falloff shaping from user parameters.
//
float
getDistanceFalloff(point PL;                   // Surf point in light space.
                   float falloff;     // Distance falloff type = 0=none, 1=linear, 2=quadratic (physical)
                   float falloffdist; // distance at which light fades to 0
                   float maxintensity; // Intensity scale.
                  )
{
   float atten = 1;
   float PLlen = length(vector PL);




   /* Distance falloff */
   if (falloff != 0)
   {
       if (PLlen > falloffdist)
       {
           atten *= pow (falloffdist/PLlen, falloff);
       }
       else
       {
           float ss = log(1 / maxintensity);
           float beta = -falloff / ss;
           atten *= (maxintensity * exp (ss * pow(PLlen / falloffdist, beta)));
       }
   }


   return atten;
}


/* Volumetric light shaping
* Inputs:
*   - the point being shaded, in the local light space
*   - all information about the light shaping, including z smooth depth
*     clipping, superellipse x-y shaping
* Return value:
*   - attenuation factor based on shaping
*/
float
getLightConeVolume(varying point PL;                  // Surface point in light space.
                   uniform float lighttype;      // What kind of light. 0=spot, 1=point, 2=area
                   uniform point  from;        // Position of light.
                   uniform vector axis;           // Light axis.
                   uniform float  znear, zfar;    // z clipping.
                   uniform float  cutonwidth, cutoffwidth; // z clipping falloff.
                   uniform float  cutoncurve, cutoffcurve; // z power exp.
                   uniform float  coneangle, coneedge;      // Size of cone.
         )
{
    // Examine the z depth of PL to apply a (possibly smooth) cuton and cutoff.
    //
    float atten = 1;

    float Pz;

    if(lighttype == 0)
    {
        Pz = zcomp(PL);
    }
    else
    {
        // For non-spot lights use distance from the light.
        Pz = length(vector(PL));
    }

    atten *= pow(abs(smoothstep(znear-cutonwidth, znear, Pz)),
                 1/max(1.0e-6, cutoncurve));
    atten *= 1 - pow(abs(smoothstep(zfar, zfar+cutoffwidth, Pz)),
                     max(1.0e-6, cutoffcurve));

    // Clip to circle.
    //
    if(lighttype == 0)
    {
        // non-point lights
        atten *= coneFalloff(PL/Pz, coneangle, coneedge);
    }

    return atten;
}

float
getAngleFalloff(varying point PL;                           // Surface point in light space.
                uniform float  beamdistribution; // Cone rolloff.
                )
{
    float atten = 1;

    // Angle falloff.
    //
    if(beamdistribution > 0)
    {
        // non-point lights
        atten *= pow(zcomp(normalize(vector PL)), beamdistribution);
    }

    return atten;
}

float
getAngleFalloff(varying point PL;                           // Surface point in light space.
                uniform float beamdistribution; // Cone rolloff.
                uniform float conepluspenumbraangle;
                )
{
    float atten = 1;

    // Angle falloff.
    //
    if(beamdistribution > 0)
    {
        // non-point lights
        float cosine = zcomp(normalize(vector PL)); 
        float angToPL = acos(cosine);
        float angToPLnormalized = min(1,angToPL/conepluspenumbraangle);
        float base = cos(.5*PI*angToPLnormalized);
        atten *= pow(base, beamdistribution);
    }

    return atten;
}


/* Four barn door shapes to block illumination used in light shaders.
  PL is expected to be the surface point transformed to shader space
  in the light shader. The surface x,y position at 0,0 will then be
  in the center of the light Z axis. */

float
getBarnDoors(varying point PL;           // Surface point on the x-y plane.
             uniform float angleL, angleR;   // Left and right barn door angle.
             uniform float angleT, angleB;   // Top and bottom barn door angle.
             uniform float wedgeL, wedgeR;   // Left and right barn door falloff.
             uniform float hedgeT, hedgeB;   // Top and bottom barn door falloff.
             uniform float offsetL, offsetR; // Length of barn doors.
             uniform float offsetT, offsetB; // Length of barn doors.
             uniform float rollL, rollR;       // Z rotation of barn doors.
             uniform float rollT, rollB;       // Z rotation of barn doors.
            )
{
    void rotatedoor(float x;
                    float y;
                    float rad;
                    float ox;
                    float oy;
                    output float r)
    {
        //r = ((x) - (ox)) * cos(rad) - ((y) - (oy)) * sin(rad) + (ox) - (1-cos(rad));
        //r = ((x) ) * cos(rad) - ((y) ) * sin(rad)  - (1-cos(rad))*ox;
        float dist = sqrt(x*x+y*y);
        float ang = atan(x,y) - rad;
        r = sin(ang)*dist;
    }

    float result;

    if(angleL < 180 || angleR < 180 || angleT < 180 || angleB < 180)
    {
        float doors;

        float Pz = zcomp(PL);
        float x = xcomp(PL/Pz);
        float y = ycomp(PL/Pz);

        uniform float tanL = -abs(tan(radians(angleL)));
        uniform float tanR = abs(tan(radians(angleR)));
        uniform float tanT = abs(tan(radians(angleT)));
        uniform float tanB = -abs(tan(radians(angleB)));

        uniform float tanLedge = -abs(tan(radians(angleL+wedgeL)));
        uniform float tanRedge = abs(tan(radians(angleR+wedgeR)));
        uniform float tanTedge = abs(tan(radians(angleT+hedgeT)));
        uniform float tanBedge = -abs(tan(radians(angleB+hedgeB)));

        float xL = x;    // X positon for left door.
        float xR = x;    // X positon for right door.
        float yT = y;    // Y positon for top door.
        float yB = y;    // Y positon for bottom door.

        // Rotate the doors around the light Z axis.
        //
        if(rollL != 0.0)
            rotatedoor(x, y, -radians(rollL), -tanL, 0, xL);

        if(rollR != 0.0)
            rotatedoor(x, y, -radians(rollR), 0, 0, xR);

        if(rollT != 0.0)
            rotatedoor(y, x, radians(rollT), 0, 0, yT);

        if(rollB != 0.0)
            rotatedoor(y, x, radians(rollB), 0, 0, yB);

        // Slide the doors across the front of the light.
        //
        xL -= offsetL;
        xR -= offsetR;
        yT -= offsetT;
        yB -= offsetB;

        // Shape barn door cross-section.
        // negative then positve x.
        // positive then negative y.
        //
        result = smoothstep(tanLedge, tanL, xL) *
            (1-smoothstep(tanR, tanRedge, xR)) *
            (1-smoothstep(tanT, tanTedge, yT)) *
            smoothstep(tanBedge, tanB, yB);
    }
    else
    {
        result = 1.0;
   }

    return result;
}
#endif /* __uberlight_utils_h */
