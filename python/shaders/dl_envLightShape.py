import deluxe

class dl_envLightShape(deluxe.EnvLight):
    typeid = 0x00310002
    description = "Environment light for shiny reflections."
    includes = ["remap_utils.h", "physicalsky_utils.h", "env_utils.h"]
    
    #
#    deluxe.EnvLight.envMap.default = "default_env.tdl"

    # reflection occlusion
  
    environmentMap = deluxe.Group([deluxe.EnvLight.envMethod, deluxe.EnvLight.envMap, deluxe.EnvLight.envSpace, deluxe.EnvLight.physicalSky, deluxe.EnvLight.envColorCorrection], collapse=False, shortname='emg')
    
    occMethod = deluxe.Enum(default='Point Cloud',
                             choices=['None', 'Ray Tracing', 'Point Cloud', 'Use Ambient Occlusion'],
                             label='Occlusion Method',
                             help=""""Ray Tracing" uses the standard occlusion() call. 
                                     "Point Cloud" uses previously baked point clouds.
                                     "Use Ambient Occlusion" uses ambient occlusion from
                                     indirectLight, ALL REMAINING REFLECTION OCCLUSION
                                     PARMS ARE IGNORED!
                                     """)
                                     
    reflectionOcclusion = deluxe.Group([occMethod, deluxe.EnvLight.occPointCloud, deluxe.EnvLight.occRayTracing, deluxe.EnvLight.occAdvanced, deluxe.EnvLight.occRemapping],collapse=False,)


    traceSamplesMult = deluxe.Float(shortname='tsm',
                            softmin=0, softmax=2, default=1, storage='uniform',
                            label='Trace Samples Multiplier',
                            help="Multplier for raytraced reflection samples.")
    
    rayTracingOverrides = deluxe.Group([traceSamplesMult])
    
    # input messages
    __occSamplesMult = deluxe.Float(default=1, storage='uniform', message=True, messagetype='lightsource')
    __occConeAngleMult = deluxe.Float(default=1, storage='uniform', message=True, messagetype='lightsource')
    __physkyBlur = deluxe.Float(default=0, storage='uniform', message=True, messagetype='lightsource')
    __physkySamps = deluxe.Float(default=1, storage='uniform', message=True, messagetype='lightsource')
    __envDir = deluxe.Vector(default=12345, storage='varying', message=True, messagetype='lightsource')


    # output messages
    __map = deluxe.String(default='', storage='uniform', output=True, message=True, messagetype='lightsource')
    __coordsys = deluxe.String(default='', storage='uniform', output=True, message=True, messagetype='lightsource')
    __occlusion = deluxe.Float(default=0, storage='varying',  output=True, message=True, messagetype='lightsource')
    __occlusionColor = deluxe.Color(default=0, storage='varying',  output=True, message=True, messagetype='lightsource')
    __traceSamplesMult = deluxe.Float(default=1, storage='uniform',  output=True, message=True, messagetype='lightsource')
    __exposure = deluxe.Float(default=1, storage='uniform', output=True, message=True, messagetype='lightsource')
    __gamma = deluxe.Float(default=0.5, storage='uniform', output=True, message=True, messagetype='lightsource')
    __offset = deluxe.Float(default=0.5, storage='uniform', output=True, message=True, messagetype='lightsource')

    #
    __useAmbientOcclusion = deluxe.Boolean(default=False, output=True, message=True, messagetype='lightsource')

    # category
    __category = deluxe.String(default='environment', message=True, messagetype='lightsource')
    _3delight_light_category = deluxe.String(shortname='cat', default='environment', notemplate=True, norsl=True)
  
    rsl = \
    """
        extern string __map;
        extern string __coordsys;
        extern float __occlusion;
        extern color __occlusionColor;
        extern uniform float __traceSamplesMult;
        extern float __exposure;
        extern float __gamma;
        extern float __offset;
        extern float __occSamplesMult;
        extern float __occConeAngleMult;
        extern float __useAmbientOcclusion;
        extern float __physkyBlur;
        extern float __physkySamps;
        extern vector __envDir;

        point origin = Ps;
        normal dir = Ns;

        uniform float traceDisplacements = 0;
        attribute("trace:displacements", traceDisplacements);
        if (traceDisplacements == 0)
        {
            // get the undisplaced surface point and normal from the displacement shader
            displacement("__Porig", origin);
            displacement("__Norig", dir);
        }

        dir = normalize(dir);
        normal dirf = faceforward(dir, I);

        normal Nf = faceforward(normalize(Ns), I);
        vector In = normalize(I);
        
        // reflection vector
        float almostEq(vector a, b; float error) {
            float result = 0;
            if (abs(a[0] - b[0]) < error && abs(a[1] - b[1]) < error && abs(a[2] - b[2]) < error)
                result = 1;
            return result;
        }
        vector R = almostEq(__envDir, vector 12345, .001) == 1 ? reflect(In, dirf) : __envDir;
        
        // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
        illuminate(Ps + Nf)
        {
            float coneangle = radians(__occConeAngleMult * i_occConeAngle);
        
            float occluded_reflection = 0;

            // compute occlusion
            
            if (i_occMethod == 1)
                // Ray Tracing
            {
                float samples = __occSamplesMult * i_occSamples;
                
                if (i_envMethod == 1) {
                    // use i_envMap.for "distribution" (?)
                    occluded_reflection = occlusion(origin, R, samples,
                                                    "coneangle", coneangle,
                                                    "maxdist", i_occMaxDistance,
                                                    "adaptive", i_occAdaptiveSampling,
                                                    "bias", i_occRayBias,
                                                    "falloffmode", i_occFalloffMode,
                                                    "falloff", i_occFalloff,
                                                    "distribution", i_envMap);
                } else if (i_envMethod == 2) {
                    occluded_reflection = occlusion(origin, R, samples,
                                                    "coneangle", coneangle,
                                                    "maxdist", i_occMaxDistance,
                                                    "adaptive", i_occAdaptiveSampling,
                                                    "bias", i_occRayBias,
                                                    "falloffmode", i_occFalloffMode,
                                                    "falloff", i_occFalloff);
                }
            }
            else if (i_occMethod == 2)
            {
                string occPtcFiles[];
                if( getPointCloudFiles("ReflectionOcclusion", i_occPtcFile, occPtcFiles) > 0){
                    
                    uniform string occHitSides = "";
                    if (i_occHitSides == 0)
                        occHitSides = "front";
                    else if (i_occHitSides == 1)
                        occHitSides = "back";
                    else if (i_occHitSides == 2)
                        occHitSides = "both";
                
                    // Point Cloud
                    if (i_envMethod == 1) {
                        // use i_envMap.for "distribution" (?)
                        occluded_reflection = occlusion(Ps, R, 0,
                                                        "coneangle", coneangle,
                                                        "filenames", occPtcFiles,
                                                        "pointbased", 1,
                                                        "hitsides", occHitSides,
                                                        "samplebase", i_occSampleBase,
                                                        "bias", i_occRayBias,
                                                        "falloffmode", i_occFalloffMode,
                                                        "falloff", i_occFalloff,
                                                        "maxdist", i_occMaxDistance,
                                                        "maxsolidangle", i_occMaxSolidAngle,
                                                        "clamp", i_occClamp,
                                                        "distribution", i_envMap);
                    } else {
                        occluded_reflection = occlusion(Ps, R, 0,
                                                        "coneangle", coneangle,
                                                        "filenames", occPtcFiles,
                                                        "pointbased", 1,
                                                        "hitsides", occHitSides,
                                                        "samplebase", i_occSampleBase,
                                                        "bias", i_occRayBias,
                                                        "falloffmode", i_occFalloffMode,
                                                        "falloff", i_occFalloff,
                                                        "maxdist", i_occMaxDistance,
                                                        "maxsolidangle", i_occMaxSolidAngle,
                                                        "clamp", i_occClamp);
                    }
                }
            } 
            else if (i_occMethod == 3) // Tell the surface shader to use ambient occlusion for reflection occlusion.
            {
                __useAmbientOcclusion = 1;
            }

            // parameters are just returned via message passing
            // the actual environment map lookup happens in env_utils.h
            // ADDED IN dltools2.3: if i_envMethod == 2 (physical sky),
            // __map is set to "" so env_utils does nothing; instead,
            // the sky colour is multiplied into Cl.

            if (i_envMethod == 2) {
                float blurToUse = __physkyBlur < 0 ? i_physkyProceduralBlur : __physkyBlur;
                float sampsToUse = __physkySamps < 0 ? i_physkyProceduralSamples : __physkySamps;
                color skyClr = getPhysicalSky (
                    vtransform("world", R),
                    i_physkySunLightRotation,
                    sampsToUse,
                    blurToUse,
                    i_physkyHaze,
                    i_physkySaturation,
                    i_physkyYIsUp,
                    i_physkyHorizonHeight,
                    i_physkyHorizonBlur,
                    i_physkySunDiskIntensity,
                    i_physkySunDiskScale,
                    i_physkySunGlowIntensity,
                    i_physkySunMaxIntensity,
                    i_physkyGroundColour,
                    i_physkyRgbUnitConversion,
                    i_physkyMultiplier,
                    i_physkyRedBlueShift,
                    i_physkyNightColour,
                    i_physkyGroundTex,
                    i_physkyCloudTex,
                    i_physkyTextureBlur,
                    i_physkyJustSun,
                    i_physkyFakeSkyBlur,
                    i_physkyFakeSkyBlurUpBias
                    );
			    skyClr = remapHDRI(i_envExposure, i_envGamma, i_envOffset, skyClr);
                __map = "";
                Cl = i_intensity * i_lightColor * skyClr;;
            } else if (i_envMethod == 1){
                __map = i_envMap;
                Cl = i_intensity * i_lightColor;
            }
            __coordsys = i_envSpace;
            __occlusion = remapOcclusion(i_occIntensity, i_occBias, i_occGain, occluded_reflection);
            __occlusionColor = i_occColor;
            __traceSamplesMult = i_traceSamplesMult;
            __exposure = i_envExposure;
            __gamma = i_envGamma;
            __offset = i_envOffset;

        }
    """

    
def initializePlugin(obj):
    dl_envLightShape.register(obj)

def uninitializePlugin(obj):
    dl_envLightShape.deregister(obj)
