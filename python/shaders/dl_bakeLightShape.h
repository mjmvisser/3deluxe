#ifndef __dl_bakeLightShape_h
#define __dl_bakeLightShape_h

/*
begin inputs
	uniform string ptcFile
	uniform string ptcFileNoSelfOcclude
	uniform string coordSys
	float radiusScale
	uniform float bakeRadiosity
	uniform string bakeRadiosityVariable
	uniform float bakeRaytracing
	float opacityThreshold
	uniform float intensity
	uniform color lightColor
	uniform float useBoundingBoxes
	uniform float boundBox1enable
	point boundBox1min
	point boundBox1max
	float boundBox1buffer
	uniform float boundBox2enable
	point boundBox2min
	point boundBox2max
	float boundBox2buffer
	uniform float boundBox3enable
	point boundBox3min
	point boundBox3max
	float boundBox3buffer
	uniform float boundBox4enable
	point boundBox4min
	point boundBox4max
	float boundBox4buffer
	uniform float boundBox5enable
	point boundBox5min
	point boundBox5max
	float boundBox5buffer
end inputs

begin shader_extra_parameters lightsource
	uniform float do_bake = 1.0;
	uniform string __category = "bakelight";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

#include "utils.h"

void
maya_dl_bakeLightShape(
	// Inputs
	//
	uniform string i_ptcFile;
	uniform string i_ptcFileNoSelfOcclude;
	uniform string i_coordSys;
	float i_radiusScale;
	uniform float i_bakeRadiosity;
	uniform string i_bakeRadiosityVariable;
	uniform float i_bakeRaytracing;
	float i_opacityThreshold;
	uniform float i_intensity;
	uniform color i_lightColor;
	uniform float i_useBoundingBoxes;
	uniform float i_boundBox1enable;
	point i_boundBox1min;
	point i_boundBox1max;
	float i_boundBox1buffer;
	uniform float i_boundBox2enable;
	point i_boundBox2min;
	point i_boundBox2max;
	float i_boundBox2buffer;
	uniform float i_boundBox3enable;
	point i_boundBox3min;
	point i_boundBox3max;
	float i_boundBox3buffer;
	uniform float i_boundBox4enable;
	point i_boundBox4min;
	point i_boundBox4max;
	float i_boundBox4buffer;
	uniform float i_boundBox5enable;
	point i_boundBox5min;
	point i_boundBox5max;
	float i_boundBox5buffer;
	)
{

    extern color Cl;
    extern vector L;
    extern point Ps;
    extern point P;
    extern normal N;
    extern normal Ns;
    extern vector I;
    extern float __nonspecular;
    extern float __nondiffuse;
        

        extern float do_bake;
        point Pw = transform("world", Ps);
       
#define INBOUND(n) (i_boundBox##n##enable > 0 &&        Pw[0] < i_boundBox##n##max[0] + i_boundBox##n##buffer && Pw[0] > i_boundBox##n##min[0] - i_boundBox##n##buffer &&        Pw[1] < i_boundBox##n##max[1] + i_boundBox##n##buffer && Pw[1] > i_boundBox##n##min[1] - i_boundBox##n##buffer &&        Pw[2] < i_boundBox##n##max[2] + i_boundBox##n##buffer && Pw[2] > i_boundBox##n##min[2] - i_boundBox##n##buffer)
        float ray_depth = 0;
        rayinfo( "depth", ray_depth );
        if (do_bake == 1 && (ray_depth == 0 || i_bakeRaytracing == 1)) 
        {
            normal Nn = normalize(Ns);
            normal Nf = faceforward(Nn, I);
            

            // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
            illuminate(Ps + Nf)
            {
                color surfOpacity =1;
                surface("Oi", surfOpacity);
                if (luminance(surfOpacity) > i_opacityThreshold &&
                        i_useBoundingBoxes == 0 || INBOUND(1) || INBOUND(2) || INBOUND(3) || INBOUND(4) || INBOUND(5))
                {
                    uniform string ptcCoordSys = "world";
                    if (i_coordSys != "")
                        ptcCoordSys = i_coordSys;
                    
                    uniform float selfOcclude = 1;
                    attribute("user:selfOcclude", selfOcclude);
                    uniform string ptcFile = selfOcclude == 1 ? i_ptcFile : i_ptcFileNoSelfOcclude;

                    if (i_bakeRadiosity != 0)
                    {
                        color radiosity = 1;
                        surface(i_bakeRadiosityVariable, radiosity);
                        bake3d(ptcFile, "", Ps, Nn,
                               "coordsystem", ptcCoordSys,
                               "radiusscale", i_radiusScale,
                               "_radiosity", radiosity,
                               "interpolate", 1 );
                    }
                    else
                    {
                        bake3d(ptcFile, "", Ps, Nn,
                               "coordsystem", ptcCoordSys,
                               "radiusscale", i_radiusScale,
                               "interpolate", 1 );
                    }
                }
            
                Cl = 0;
            }
        }
}

#endif /* __dl_bakeLightShape_h */
