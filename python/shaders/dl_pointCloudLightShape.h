#ifndef __dl_pointCloudLightShape_h
#define __dl_pointCloudLightShape_h

/*
begin inputs
	uniform float enable
	uniform float enableAmbientOcclusion
	uniform float enableColorBleeding
	uniform float enableReflection
	uniform float enableReflectionOcclusion
	uniform float enableRefraction
	uniform float enableSubsurface
	uniform string ptcFile
end inputs

begin shader_extra_parameters lightsource
	output uniform float __enableAmbientOcclusion = 0.0;
	output uniform float __enableColorBleeding = 0.0;
	output uniform float __enableReflection = 0.0;
	output uniform float __enableReflectionOcclusion = 0.0;
	output uniform float __enableRefraction = 0.0;
	output uniform float __enableSubsurface = 0.0;
	output uniform string __ptcFile = "";
	uniform string __category = "pointcloud";
	uniform string shadowmapname = "";
	output float __nondiffuse = 1.0;
	output varying float __nonspecular = 1.0;
end shader_extra_parameters

*/

void
maya_dl_pointCloudLightShape(
	// Inputs
	//
	uniform float i_enable;
	uniform float i_enableAmbientOcclusion;
	uniform float i_enableColorBleeding;
	uniform float i_enableReflection;
	uniform float i_enableReflectionOcclusion;
	uniform float i_enableRefraction;
	uniform float i_enableSubsurface;
	uniform string i_ptcFile;
	)
{

    extern float __enableAmbientOcclusion;
    extern float __enableColorBleeding;
    extern float __enableReflection;
    extern float __enableReflectionOcclusion;
    extern float __enableRefraction;
    extern float __enableSubsurface;
    extern string __ptcFile;
    
    if(i_enable > 0){
        __enableAmbientOcclusion =  i_enableAmbientOcclusion;
        __enableColorBleeding = i_enableColorBleeding;
        __enableReflection = i_enableReflection;
        __enableReflectionOcclusion = i_enableReflectionOcclusion;
        __enableRefraction = i_enableRefraction;
        __enableSubsurface = i_enableSubsurface;
    }
    else{
        __enableAmbientOcclusion =  0;
        __enableColorBleeding = 0;
        __enableReflection = 0;
        __enableReflectionOcclusion = 0;
        __enableRefraction = 0;
        __enableSubsurface = 0;
    }
    __ptcFile = i_ptcFile;
}

#endif /* __dl_pointCloudLightShape_h */
