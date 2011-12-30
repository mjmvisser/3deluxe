import delight

class dl_curvature(delight.Utility):
    typeid = 0x0030000c
    description = "Simple incandescence to simulate internal illumination. "

    CurvatureType = delight.Enum(default='mean', description="""
        I'm honestly not sure how these calculations are done,
        but 'mean' seems work best.""",
        choices=['gaussian', 'mean', 'ku', 'kv', 'min', 'max'])

    remapInMin = delight.Float(default=-1, shortname='inmin',
        description='(unclamped) minimum input value to remap curvature')
    remapInMax = delight.Float(default=1, shortname='inmax',
        description='(unclamped) maximum input value to remap curvature')
    remapOutMin = delight.Float(default=0, shortname='outmin',
        description='(unclamped) minimum output value to remap curvature')
    remapOutMax = delight.Float(default=1, shortname='outmax',
        description='(unclamped) maximum output value to remap curvature')

    outColor = delight.Color(output=True)
    outAlpha = delight.Float(output=True)

    
    rsl = \
    """
/* 
 * Copyright (c) 1998 Thomas E. Burge.  All rights reserved.  
 * 
 * FILE:  showk.sl
 *
 * DESCRIPTION:  
 *   Calculates different types of curvature.  Right now this only works
 *   on PRMan, but I'll publish it here in case someone finds it of
 *   interest.  It needs more testing, but the numbers do seem to match
 *   Alias's numbers.
 *
 * TO-DO:
 *   The way a curvature value is matched to a color needs to be improved
 *   and I need to double check the expressions with the terms Puu.NN, 
 *   Puv.NN and Pvv.NN.
 *
 *   Do note that the second derivatives seem to cause some renderers 
 *   problems as the values do not appear too valid at times.
 */


/*#define DEBUG*/

/* Note that the value 1/Calck(dPdu, Du(dPdu)) is the radius
 *    of curvature in the u direction of a surface.  So
 *    a cylinder (with an unscaled cirular cross section) 
 *    would have a radius at P equal to the radius of 
 *    curvature at P.
 * Q1 is a first derivative and Q2 is the matching second 
 *    derivative Q1'.
 */
float Calck( vector Q1; vector Q2 )
{
   return length((Q1^Q2)/pow(length(Q1),3));
}


/* Solves the quadratic equation and finds two roots. */
void CalcQuadEquation( float a; float b; float c; 
                       output float r1; output float r2 )
{
   float q;

   q = b*b - 4*a*c;
   if ( q < 0 ) 
   {
      r1 = 0;
      r2 = 0;
   }
   else
   {
      q = -0.5*( b + sign(b) * sqrt(q));
      r1 = q / a;
      r2 = c / q;
   }
}


/* Solves a quadratic equation for principle curvatures k1 and k2. */
#define CALC_K1K2() \
       CalcQuadEquation( ((dPdu.dPdu)*(dPdv.dPdv) - pow(dPdu.dPdv, 2)), \
			 -((dPdu.dPdu)*(Pvv.NN)+(dPdv.dPdv)*(Puu.NN)    \
			   - 2*(dPdu.dPdv)*(Puv.NN)),                   \
			 ((Puu.NN)*(Pvv.NN) - pow(Puv.NN, 2)),          \
			 k1,k2)


/* The way the color ramp is handled is not very good.  You need to
 *    find the min and max values of the type of curvature you are
 *    viewing, otherwise one color gets used for the entire surface.
 */

    extern normal N;
    extern point P;
    extern vector I;
    extern vector dPdu;
    extern vector dPdv;
    extern float u;
    extern float v;


    normal  NN;
    vector  V;
    vector  Puu, Puv, Pvv;
    float   k, k1, k2;
    float   G, M;

    NN = normalize(N);
    V = -normalize(I);

    if ( i_CurvatureType == 0) 
    {
       Puu = Du(dPdu);
       Puv = Du(dPdv);
       Pvv = Dv(dPdv);
       k = ((Puu.NN)*(Pvv.NN) - pow(Puv.NN, 2)) 
	  / ((dPdu.dPdu)*(dPdv.dPdv) - pow(dPdu.dPdv, 2));

#ifdef DEBUG
       /* The Gaussian curvature is the product of the principle 
	*    curvatures at point P.  Note that the Gaussian curvature
	*    can be calculated as above or from the principle 
	*    curvatures referred to below as k1 and k2.  The values
	*    can be calculated by solving a quadratic equation or
	*    a simpler equation when dPdu.dPdv==Puv.NN==0.
	*/
       CALC_K1K2();

       if ( abs(dPdu.dPdv)<0.000001 && abs(Puv.NN)<0.000001 )
	  printf(
	      "dPdu.dPdv:%g Puv.NN:%g k:%g=k1*k2=%g (k1=%g=%g)(k2=%g=%g)\n", 
	      dPdu.dPdv, Puv.NN, k, k1*k2, 
	      k1,(Puu.NN)/(dPdu.dPdu), 
	      k2,(Pvv.NN)/(dPdv.dPdv) );
       else
	  printf(" dPdu.dPdv:%g Puv.NN:%g k:%g = k1*k2 = %g\n", 
		 dPdu.dPdv, Puv.NN, k, k1*k2 );
#endif       
    }
    else if ( i_CurvatureType == 1) 
    {
       Puu = Du(dPdu);
       Puv = Du(dPdv);
       Pvv = Dv(dPdv);
       k = ((dPdu.dPdu)*(Pvv.NN)+(dPdv.dPdv)*(Puu.NN) 
	    - 2*(dPdu.dPdv)*(Puv.NN))
	  / (2*((dPdu.dPdu)*(dPdv.dPdv) - pow(dPdu.dPdv, 2)));
#ifdef DEBUG
       /* The Mean curvature is the average of the principle 
	*    curvatures at point P.  Note that the Mean curvature
	*    can be calculated as above or from the principle 
	*    curvatures referred to below as k1 and k2.  The values
	*    can be calculated by solving a quadratic equation or
	*    a simpler equation when dPdu.dPdv==Puv.NN==0.
	*/
       CALC_K1K2();

       if ( abs(dPdu.dPdv)<0.000001 && abs(Puv.NN)<0.000001 )
	  printf(
             "dPdu.dPdv:%g Puv.NN:%g k:%g=(k1+k2)/2:%g (k1=%g=%g)(k2=%g=%g)\n",
	     dPdu.dPdv, Puv.NN, k, (k1+k2)/2, 
	     k1,(Puu.NN)/(dPdu.dPdu), 
	     k2,(Pvv.NN)/(dPdv.dPdv) );
       else
	  printf(" dPdu.dPdv:%g Puv.NN:%g k:%g = (k1+k2)/2 = %g\n", 
		 dPdu.dPdv, Puv.NN, k, (k1+k2)/2 );
#endif
    }
    else if ( i_CurvatureType == 2) 
    {
       k = Calck(dPdu, Du(dPdu));
    }
    else if ( i_CurvatureType == 3) 
    {
       k = Calck(dPdv, Du(dPdv));
    }
    else if ( i_CurvatureType == 4) 
    {
       Puu = Du(dPdu);
       Puv = Du(dPdv);
       Pvv = Dv(dPdv);
       CALC_K1K2();

       k = min(k1,k2);
#ifdef DEBUG
       printf( "min k:%g k1:%g k2:%g\n", k, k1, k2 );
#endif
    }
    else if ( i_CurvatureType == 5) 
    {
       Puu = Du(dPdu);
       Puv = Du(dPdv);
       Pvv = Dv(dPdv);
       CALC_K1K2();

       k = max(k1,k2);
#ifdef DEBUG
       printf( "max k:%g\n", k );
#endif
    }
    else /* information printed out */
    {
       /* Print surface information for testing by adding the following
	* line to a RIB file such as the one attached below:
	*
	*      Surface "showk" "CurvatureType" "" 
	*
	* Using the above Surface statement in the RIB file below (bumpy.rib),
	* the following file creates file listing Gaussian, Mean and 
	* principle curvatures:
	*
	*      prman bumpy.rib > junk.txt
	*
	*/
       Puu = Du(dPdu);
       Puv = Du(dPdv);
       Pvv = Dv(dPdv);
       G = ((Puu.NN)*(Pvv.NN) - pow(Puv.NN, 2)) 
	  / ((dPdu.dPdu)*(dPdv.dPdv) - pow(dPdu.dPdv, 2));
       M = ((dPdu.dPdu)*(Pvv.NN)+(dPdv.dPdv)*(Puu.NN) 
	    - 2*(dPdu.dPdv)*(Puv.NN))
	  / (2*((dPdu.dPdu)*(dPdv.dPdv) - pow(dPdu.dPdv, 2)));
       CALC_K1K2();

       printf("u,v(%g,%g)G:%g M:%g k1:%g k2:%g\n", u,v, G, M, k1, k2);

    }

    float fit (float v, omn, omx, nmn, nmx) {
        return nmn + (v-omn)/(omx-omn) * (nmx - nmn);
    }

    o_outColor = o_outAlpha = fit(k, i_remapInMin, i_remapInMax, i_remapOutMin, i_remapOutMax);
    //i_mult*k + i_add;
    """


def initializePlugin(obj):
    dl_curvature.register(obj)

def uninitializePlugin(obj):
    dl_curvature.deregister(obj)
