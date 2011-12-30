import delight

class dl_indirectLightShape(delight.EnvLight):
    typeid = 0x00310003
    description = "Light that does ambient occlusion and indirect diffuse lighting."
    includes = ["remap_utils.h", "component_utils.h", "physicalsky_utils.h", "env_utils.h"]
    
    
#    delight.EnvLight.envMap.default = 'default_indirect.tdl'
    
    #
    envConvolveMode = delight.Enum(default='Use envBlur parm', label='Convolve Mode',
                                  choices=['Use envBlur parm', 'Auto (ignore envBlur parm)'],
                                  help="""Use envBlur parm = use environment() function with envBlur parm,
                                          Auto (ignore envBlur parm) = use indirectdiffuse() function which
                                          automitically blurs map.""")
    envBlur = delight.Float(min=0, softmax=1, default=0, storage='uniform', label='Blur', 
                                help= """Blur for envMap, only used when envConvolveMode = 'Use envBlur parm'.""")
    
    envIntensity = delight.Float(default=1, label='Intensity')
    envColor = delight.Color(default=1, label='Color')
    
    environmentMap = delight.Group([delight.EnvLight.envMethod, envIntensity, envColor, delight.EnvLight.envMap, delight.EnvLight.envSpace, envConvolveMode, envBlur, delight.EnvLight.physicalSky, delight.EnvLight.envColorCorrection], shortname='emg', collapse=False,)
    
    
    occMethod = delight.Enum(default='Point Cloud',
                             choices=['None', 'Ray Tracing', 'Point Cloud'],
                             label='Occlusion Method',
                             help=""""Ray Tracing" uses the standard occlusion() call. 
                                     "Point Cloud" uses previously baked point clouds.
                                     """)
    
    ambientOcclusion = delight.Group([occMethod, delight.EnvLight.occPointCloud, delight.EnvLight.occRayTracing, delight.EnvLight.occAdvanced, delight.EnvLight.occRemapping], collapse=False,)

    indirectMethod = delight.Enum(default='None',
                             choices=['None', 'Ray Tracing', 'Point Cloud'],
                             label='Color Bleeding Method',
                             shortname='indm',
                             help=""""Ray Tracing" uses the standard indirectdiffuse() call. 
                                     "Point Cloud" uses previously baked point clouds.
                                     """)
    
    indirectIntensity = delight.Float(default=1, label='Intensity')
                                     
    indirectMaxDistance = delight.Float(shortname='idmd',
                                        softmin=0, default=1e38, storage='uniform',
                                        label='Max Distance',
                                        help="(Ray Tracing, Point Cloud) Only consider intersections closer than this distance.")

    indirectSamples = delight.Integer(shortname='ids',
                                      min=0, max=256, default=64,
                                      label='Samples',
                                      help="""(Ray Tracing) The number of rays to trace.""")
    indirectAdaptiveSampling = delight.Boolean(shortname='idas',
                                               default=False,
                                               label='Adaptive Sampling',
                                               help="(Ray Tracing) Enables or disables adaptive sampling.")
    indirectRayBias = delight.Float(default=0.1,
                                    min=0, softmax=2,
                                    label='Ray Bias',
                                    help="""(Ray Tracing, Point Cloud) Specifies a bias for ray's starting point to avoid potentially erroneous 
                                            intersections with the emitting surface.""")
    indirectFalloffMode = delight.Enum(shortname="psifm", default='Linear',
                                       choices=['Exponential', 'Linear'],
                                       label='Falloff Mode',
                                       help="""(Ray Tracing, Point Cloud) Specifies the falloff curve to use.""")
    indirectFalloff = delight.Float(default=1, min=0, softmax=5,
                                    label='Falloff',
                                    help="""(Ray Tracing, Point Cloud) This shapes the falloff curve. In the exponential case the curve is exp( -falloff * hitdist ) 
                                            and in the linear case it is pow(1-hitdist/maxdist, falloff).""")
    indirectPtcFile = delight.File(default='',
                                label='Point Cloud File',
                                help="""(Point Cloud) The point cloud file in which baked points with radiosity are stored.""")
    occPtcFileIsDirectory = delight.Boolean(default=False)
    indirectMaxSolidAngle = delight.Float(softmin=0.01, softmax=0.5, default=0.1, storage='uniform',
                                          label='Max Solid Angle',
                                          help="""(Point Cloud) This is a quality vs speed control knob.""")
    indirectClamp = delight.Boolean(default=True,
                                    label='Clamp',
                                    help="""(Point Cloud) Setting this parameter to 1 will force 3DELIGHT to account for
                                            occlusion in dense environments. The results obtained with this
                                            parameter on should look similar to what a Ray Tracing rendering
                                            would give. Enabling this parameter will slow down the Point Cloud
                                            algorithm by a factor of 2.""")
    indirectSampleBase = delight.Float(default=1,
                                       label='Sample Base',
                                       help="""(Point Cloud) Scales the amount of jittering of the start position of rays. The default
                                               is to jitter over the area of one micropolygon.""")
    indirectHitSides = delight.Enum(default='Both',
                                    choices=['Front', 'Back', 'Both'],
                                    label='Hit Sides',
                                    help="""(Point Cloud) Specifies which side(s) of the point cloud's samples will produce occlusion.""")

    indirectPointCloud = delight.Group([indirectPtcFile, occPtcFileIsDirectory, indirectMaxSolidAngle, indirectClamp, indirectSampleBase, indirectHitSides], label="Point Cloud")
    
    indirectRayTracing = delight.Group([indirectSamples, indirectAdaptiveSampling, indirectRayBias], label="Ray Tracing",)

    indirectAdvanced = delight.Group([indirectMaxDistance, indirectFalloffMode, indirectFalloff],
                                label='Advanced')
    
    colorBleeding = delight.Group([indirectMethod, indirectIntensity, indirectPointCloud, indirectRayTracing, indirectAdvanced], collapse=False,)
    

    __computeOcclusion = delight.Float(default=1, message=True, messagetype='lightsource')
    __occluded = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    __occlusionColor = delight.Color(default=0, output=True, message=True, messagetype='lightsource')
    __indirect_color = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    __bentnormal = delight.Color(default=0, output=True, message=True, storage='varying', messagetype='lightsource')
    

    # category
    __category = delight.String(default='indirect', message=True, messagetype='lightsource')
    _3delight_light_category = delight.String(default='indirect', notemplate=True, norsl=True)
    
    
    rsl = \
    """
        extern color __occluded;
        extern color __occlusionColor;
        extern color __indirect_color;
        extern color __bentnormal;
        extern float __computeOcclusion;

        point origin = Ps;
        normal dir = Ns;
        vector dirW = transform("world", dir);

        uniform float traceDisplacements = 0;
        attribute("trace:displacements", traceDisplacements);
        if (traceDisplacements == 0)
        {
            // get the undisplaced surface point and normal from the displacement shader
            displacement("__Porig", origin);
            displacement("__Norig", dir);
        }

        dir = normalize(dir);
        normal dirf = ShadingNormal(dir);

        normal Nn = normalize(Ns);
        normal Nf = ShadingNormal(Nn);

        uniform string envspace = "world";
        if (i_envSpace != "")
            envspace = i_envSpace;

        // illuminate(from) implicitly sets L to Ps-from, so thus L=-Nf and the light is always visible
        illuminate(Ps + Nf)
        {
            // compute occlusion
            
            float occluded = 0;
            vector bentnormal = vector Nf;

            if (__computeOcclusion != 0)
            {
                if (i_occMethod == 1)
                    // Ray Tracing
                {
                    if (i_envMethod == 1) {
                        // use i_envMap.for "distribution" (?)
                        occluded = occlusion(origin, dirf, i_occSamples,
                                         "coneangle", radians(i_occConeAngle),
                                         "maxdist", i_occMaxDistance,
                                         "adaptive", i_occAdaptiveSampling,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "distribution", i_envMap,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    } else if (i_envMethod == 2) {
                        occluded = occlusion(origin, dirf, i_occSamples,
                                         "coneangle", radians(i_occConeAngle),
                                         "maxdist", i_occMaxDistance,
                                         "adaptive", i_occAdaptiveSampling,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    }
                }
                else if (i_occMethod == 2)
                {
                    uniform string occHitSides = "";
                    if (i_occHitSides == 0)
                        occHitSides = "front";
                    else if (i_occHitSides == 1)
                        occHitSides = "back";
                    else if (i_occHitSides == 2)
                        occHitSides = "both";
                
                    // Point Cloud
                    //if( textureinfo(i_occPtcFile, "exists", 0) )
                    string occPtcFile = i_occPtcFile;
                    if (i_occPtcFileIsDirectory) {
                        string objName = "";
                        attribute("user:delight_shortest_unique_name", objName);
                        occPtcFile = concat(occPtcFile, "/", objName, ".ptc");
                    }
                    
                    string occPtcFiles[];
                    if( getPointCloudFiles("AmbientOcclusion", occPtcFile, occPtcFiles) > 0)
                    {
                        occluded = occlusion(Ps, dirf, 0,
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
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                    }
                    /*
                    
                    // TODO MAKE THIS CLEANER
                    float selfOcclude = 1;
                    attribute("user:selfOcclude", selfOcclude);
                    if( selfOcclude == 1 && i_occPtcFileNoSelfOcclude != "")
                    {
                        float thisOcc = occlusion(Ps, dirf, 0,
                                         "filename", i_occPtcFileNoSelfOcclude,
                                         "pointbased", 1,
                                         "hitsides", occHitSides,
                                         "samplebase", i_occSampleBase,
                                         "bias", i_occRayBias,
                                         "falloffmode", i_occFalloffMode,
                                         "falloff", i_occFalloff,
                                         "maxdist", i_occMaxDistance,
                                         "maxsolidangle", i_occMaxSolidAngle,
                                         "clamp", i_occClamp,
                                         "environmentspace", envspace,
                                         "environmentdir", bentnormal);
                        // This is based on opacity compositing + is an inaccurate approximation of merging 2 pointclouds. 
                        occluded = 1 - (1-occluded) * (1-thisOcc); 
                    }
                    */
                    // markv: This statement doesn't compile
                    // from docs:  "environmentdir"      output varying vector      If specified, it is set to the
                    //             average un-occluded direction, which is the average of all sampled directions 
                    //             that do not hit any geometry. Note that this vector is defined in `current' space,
                    //             so it is necessary to transform it to `world' space if an environment() lookup is intended.  
                    //bentnormal = vtransform("world", "current", bentnormal);
                    //
                    // jeremye: When using pointclouds, environmentdir seems to be in world space, in spite
                    // of what the docs say.  I've sent a message to support@3delight.com to address this.
                    // In the meantime, the hack below effectively transforms bentnormal from world to
                    // current space without generating an error (warning really).
                    // UPDATE: This will be fixed soon, at which point REMOVE BELOW (and test).
                    //
                    // marcantoinep: not yet fixed , keeping code

                    vector tmp = vtransform("world", bentnormal);
                    tmp[0] = bentnormal[0]; tmp[1] = bentnormal[1]; tmp[2] = bentnormal[2];
                    bentnormal = vtransform("world", "current", tmp);
                }
            }
            bentnormal = vtransform(envspace, bentnormal);
            
            // compute indirect diffuse lighting

            color indirect_color = 0;
    
            if (i_envMethod == 1) {
                color envColor = 1;
                if( textureinfo(i_envMap, "exists", 0) ) {
                    vector envdir = normalize(bentnormal);
                    if (i_envConvolveMode == 0) 
                        envColor = environment(i_envMap, envdir, "blur", i_envBlur);
                    else
                        envColor = indirectdiffuse(i_envMap, envdir);
                }
                indirect_color += envColor * i_envColor * i_envIntensity;
            } else if (i_envMethod == 2) {
                // Lookup physical sky.
                indirect_color += getPhysicalSky (
                    dirW,
                    i_physkySunLightRotation,
                    i_physkyProceduralSamples,
                    i_physkyProceduralBlur,
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
                    i_physkyFakeSkyBlurUpBias);
                if (i_physkyBakeSkyMap == 1) {
                    float ss = 0, tt = 0;
                    normal Nw = normalize(ntransform("world", Ns));
                    stFromV(vector Nw, ss, tt);
                    bake(i_physkyBakeSkyMapFile, ss, tt, indirect_color);
                }
            }
        
            color indirectColor = 0;
            
            if (i_indirectMethod == 1)
            {
                // Ray Tracing
                if (i_envMethod == 1) {
                    // Missed rays lookup i_envMap.
                    indirectColor += indirectdiffuse(origin, dir, i_indirectSamples,
                                                 "maxdist", i_indirectMaxDistance,
                                                 "adaptive", i_indirectAdaptiveSampling,
                                                 "bias", i_indirectRayBias,
                                                 "falloffmode", i_indirectFalloffMode,
                                                 "falloff", i_indirectFalloff,
                                                 "environmentmap", i_envMap,
                                                 "environmentspace", envspace);
                } else if (i_envMethod == 2){
                    // Missed rays lookup physical sky.
                    indirectColor += indirectdiffuse(origin, dir, i_indirectSamples,
                                                 "maxdist", i_indirectMaxDistance,
                                                 "adaptive", i_indirectAdaptiveSampling,
                                                 "bias", i_indirectRayBias,
                                                 "falloffmode", i_indirectFalloffMode,
                                                 "falloff", i_indirectFalloff,
                                                 "environmentspace", envspace);
                    color skyClr = getPhysicalSky (
                        dirW,
                        i_physkySunLightRotation,
                        i_physkyProceduralSamples,
                        i_physkyProceduralBlur,
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
                        i_physkyFakeSkyBlurUpBias);
                    indirectColor += skyClr *(1-occluded);//mix(skyClr, indirectColor, occluded);
                }
            }
            else if (i_indirectMethod == 2)
            {
                uniform string indirectHitSides = "";
                if (i_indirectHitSides == 0)
                    indirectHitSides = "front";
                else if (i_indirectHitSides == 1)
                    indirectHitSides = "back";
                else if (i_indirectHitSides == 2)
                    indirectHitSides = "both";

                // Point Cloud
                string indirectPtcFiles[];
                if( getPointCloudFiles("ColorBleeding", i_indirectPtcFile, indirectPtcFiles) > 0){
                    indirectColor += indirectdiffuse(Ps, Nn, 0,
                                                     "filenames", indirectPtcFiles,
                                                     "pointbased", 1,
                                                     "hitsides", indirectHitSides,
                                                     "samplebase", i_indirectSampleBase,
                                                     "bias", i_indirectRayBias,
                                                     "falloffmode", i_indirectFalloffMode,
                                                     "falloff", i_indirectFalloff,
                                                     "maxdist", i_indirectMaxDistance,
                                                     "maxsolidangle", i_indirectMaxSolidAngle,
                                                     "clamp", i_indirectClamp);
                }
            }
            
            indirect_color += indirectColor * i_indirectIntensity;
            
            indirect_color = remapHDRI(i_envExposure, i_envGamma, i_envOffset, indirect_color);
            occluded = remapOcclusion(i_occIntensity, i_occBias, i_occGain, occluded);
            
            Cl = i_intensity * indirect_color * i_lightColor;
            
            // output occlusion to the surface
            __occluded = color occluded;
            __occlusionColor = i_occColor;
            __indirect_color = indirect_color;
            __bentnormal = color bentnormal;
        }

    """

    
def initializePlugin(obj):
    dl_indirectLightShape.register(obj)

def uninitializePlugin(obj):
    dl_indirectLightShape.deregister(obj)
