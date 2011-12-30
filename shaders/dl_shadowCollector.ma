//Maya ASCII 2009 scene
//Name: dl_shadowCollector.ma
//Last modified: Wed, Jun 16, 2010 03:08:12 PM
//Codeset: UTF-8
requires maya "2009";
requires "dl_layer.py" "1.0";
requires "3delight_for_maya2009" "2";
requires "dl_externFloat.py" "1.0";
requires "dl_shadowCollector.py" "1.0";
requires "dl_externColor.py" "1.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya Complete 2009";
fileInfo "version" "2009 Service Pack 1a x64";
fileInfo "cutIdentifier" "200904080002-749524";
fileInfo "osv" "Linux 2.6.18-92.1.18.el5 #1 SMP Wed Nov 12 09:19:49 EST 2008 x86_64";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 27.236180263044297 19.745835165884138 29.619123523168106 ;
	setAttr ".r" -type "double3" -26.138352729602371 42.599999999999959 4.3208358477665914e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	addAttr -ci true -sn "usedBy3dfm" -ln "usedBy3dfm" -at "message";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pSphere1";
createNode mesh -n "pSphereShape1" -p "pSphere1";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode lightLinker -n "lightLinker1";
	setAttr -s 4 ".lnk";
	setAttr -s 4 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode dl_layer -n "dl_shadowCollector";
	setAttr ".lsc" 6;
	setAttr ".ord" -type "Int32Array" 0 ;
	setAttr ".l[0].lnm" -type "string" "layer0";
	setAttr ".l[0].ldor" -type "Int32Array" 0 ;
createNode shadingEngine -n "dl_layer1SG";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo1";
createNode dl_shadowCollector -n "dl_shadowCollectorComponent";
	setAttr ".lt" 0;
createNode polySphere -n "polySphere1";
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
	setAttr ".st" 6;
createNode delightRenderPass -n "delightRenderPass1";
	addAttr -ci true -sn "version" -ln "version" -at "float";
	addAttr -ci true -sn "connectToRenderGlobals" -ln "connectToRenderGlobals" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "shaderCollection" -ln "shaderCollection" -at "message";
	addAttr -ci true -sn "animation" -ln "animation" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "frameRange" -ln "frameRange" -at "float2" -nc 2;
	addAttr -ci true -sn "startFrame" -ln "startFrame" -dv 1 -at "float" -p "frameRange";
	addAttr -ci true -sn "endFrame" -ln "endFrame" -dv 1 -at "float" -p "frameRange";
	addAttr -ci true -sn "increment" -ln "increment" -dv 1 -at "float";
	addAttr -ci true -sn "cameraBlur" -ln "cameraBlur" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "transformationBlur" -ln "transformationBlur" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "deformationBlur" -ln "deformationBlur" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "cameraBlurSamples" -ln "cameraBlurSamples" -dv 2 -min 2 -max 
		20 -at "long";
	addAttr -ci true -sn "transformationSamples" -ln "transformationSamples" -dv 2 -min 
		2 -max 20 -at "long";
	addAttr -ci true -sn "deformationSamples" -ln "deformationSamples" -dv 2 -min 2 
		-max 20 -at "long";
	addAttr -ci true -sn "motionBlurPosition" -ln "motionBlurPosition" -dv 1 -min 0 
		-max 2 -en "end on frame:centred on frame:start on frame" -at "enum";
	addAttr -ci true -sn "shutterEfficiency" -ln "shutterEfficiency" -at "float2" -nc 
		2;
	addAttr -ci true -sn "shutterEfficiencyA" -ln "shutterEfficiencyA" -dv 1 -min 0 
		-max 1 -at "float" -p "shutterEfficiency";
	addAttr -ci true -sn "shutterEfficiencyB" -ln "shutterEfficiencyB" -dv 1 -min 0 
		-max 1 -at "float" -p "shutterEfficiency";
	addAttr -ci true -sn "shutterAngleScale" -ln "shutterAngleScale" -dv 1 -min 0.01 
		-at "float";
	addAttr -ci true -sn "camera" -ln "camera" -at "message";
	addAttr -ci true -sn "resolution" -ln "resolution" -at "long2" -nc 2;
	addAttr -ci true -sn "resolutionX" -ln "resolutionX" -dv 720 -at "long" -p "resolution";
	addAttr -ci true -sn "resolutionY" -ln "resolutionY" -dv 486 -at "long" -p "resolution";
	addAttr -ci true -sn "resolutionMultiplier" -ln "resolutionMultiplier" -min 0 -max 
		3 -en "Full:Half:Quarter:Eighth" -at "enum";
	addAttr -ci true -sn "pixelAspectRatio" -ln "pixelAspectRatio" -dv 1 -min 0.01 -at "float";
	addAttr -ci true -sn "ribFilename" -ln "ribFilename" -dt "string";
	addAttr -ci true -sn "binaryRib" -ln "binaryRib" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "compressedRib" -ln "compressedRib" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "backgroundRenderParams" -ln "backgroundRenderParams" -dt "string";
	addAttr -ci true -sn "renderLogFilename" -ln "renderLogFilename" -dt "string";
	addAttr -ci true -sn "generateRIBArchives" -ln "generateRIBArchives" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "ignoreArchivedObjects" -ln "ignoreArchivedObjects" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "archiveTransforms" -ln "archiveTransforms" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "archiveLighting" -ln "archiveLighting" -dv 2 -min 0 -max 2 
		-en "No Lighting:Light Linking:Light Sources & Light Linking" -at "enum";
	addAttr -ci true -sn "archiveGeometryAttributes" -ln "archiveGeometryAttributes" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "archiveGeometryShaders" -ln "archiveGeometryShaders" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "archiveWriteMode" -ln "archiveWriteMode" -dv 1 -min 0 -max 
		1 -en "Reuse existing archive:Overwrite existing archive" -at "enum";
	addAttr -ci true -sn "renderMode" -ln "renderMode" -min 0 -max 3 -en "Render:Save RIB:RIB Archive:Background Render" 
		-at "enum";
	addAttr -ci true -sn "pixelSamples" -ln "pixelSamples" -at "long2" -nc 2;
	addAttr -ci true -sn "pixelSamplesX" -ln "pixelSamplesX" -dv 3 -min 1 -at "long" 
		-p "pixelSamples";
	addAttr -ci true -sn "pixelSamplesY" -ln "pixelSamplesY" -dv 3 -min 1 -at "long" 
		-p "pixelSamples";
	addAttr -ci true -sn "shadingRate" -ln "shadingRate" -dv 1 -min 0.001 -at "float";
	addAttr -ci true -sn "pixelFilter" -ln "pixelFilter" -dv 5 -min 0 -max 8 -en "box:triangle:gaussian:catmull-rom:bessel:sinc:mitchell:zmin:zmax" 
		-at "enum";
	addAttr -ci true -sn "filterWidth" -ln "filterWidth" -at "float2" -nc 2;
	addAttr -ci true -sn "filterWidthX" -ln "filterWidthX" -dv 4 -min 0.001 -at "float" 
		-p "filterWidth";
	addAttr -ci true -sn "filterWidthY" -ln "filterWidthY" -dv 4 -min 0.001 -at "float" 
		-p "filterWidth";
	addAttr -ci true -sn "bucketSize" -ln "bucketSize" -at "long2" -nc 2;
	addAttr -ci true -sn "bucketSizeX" -ln "bucketSizeX" -dv 16 -min 2 -at "long" -p "bucketSize";
	addAttr -ci true -sn "bucketSizeY" -ln "bucketSizeY" -dv 16 -min 2 -at "long" -p "bucketSize";
	addAttr -ci true -sn "useCropWindow" -ln "useCropWindow" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "cropMin" -ln "cropMin" -at "float2" -nc 2;
	addAttr -ci true -sn "cropMinX" -ln "cropMinX" -min 0 -max 1 -at "float" -p "cropMin";
	addAttr -ci true -sn "cropMinY" -ln "cropMinY" -min 0 -max 1 -at "float" -p "cropMin";
	addAttr -ci true -sn "cropMax" -ln "cropMax" -at "float2" -nc 2;
	addAttr -ci true -sn "cropMaxX" -ln "cropMaxX" -dv 1 -min 0 -max 1 -at "float" -p "cropMax";
	addAttr -ci true -sn "cropMaxY" -ln "cropMaxY" -dv 1 -min 0 -max 1 -at "float" -p "cropMax";
	addAttr -ci true -sn "bucketOrder" -ln "bucketOrder" -min 0 -max 4 -en "horizontal:vertical:zigzag:spiral:circle" 
		-at "enum";
	addAttr -ci true -sn "preRenderMEL" -ln "preRenderMEL" -dt "string";
	addAttr -ci true -sn "postRenderMEL" -ln "postRenderMEL" -dt "string";
	addAttr -ci true -sn "preFrameMEL" -ln "preFrameMEL" -dt "string";
	addAttr -ci true -sn "postFrameMEL" -ln "postFrameMEL" -dt "string";
	addAttr -ci true -sn "postOptionMEL" -ln "postOptionMEL" -dt "string";
	addAttr -ci true -sn "preWorldMEL" -ln "preWorldMEL" -dt "string";
	addAttr -ci true -sn "postWorldMEL" -ln "postWorldMEL" -dt "string";
	addAttr -ci true -sn "layerToRender" -ln "layerToRender" -at "message";
	addAttr -ci true -sn "useNetCache" -ln "useNetCache" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "netCacheDir" -ln "netCacheDir" -dt "string";
	addAttr -ci true -sn "netCacheSize" -ln "netCacheSize" -dv 100 -min 100 -at "long";
	addAttr -ci true -sn "renderPhotonMaps" -ln "renderPhotonMaps" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "writePhotonMaps" -ln "writePhotonMaps" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "numberOfPhotons" -ln "numberOfPhotons" -min 0 -at "long";
	addAttr -ci true -sn "globalMap" -ln "globalMap" -dt "string";
	addAttr -ci true -sn "causticMap" -ln "causticMap" -dt "string";
	addAttr -ci true -sn "statisticsLevel" -ln "statisticsLevel" -min 0 -max 3 -at "long";
	addAttr -ci true -sn "statisticsFile" -ln "statisticsFile" -dt "string";
	addAttr -ci true -sn "outputRenderProgress" -ln "outputRenderProgress" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "shaderPath" -ln "shaderPath" -dt "string";
	addAttr -ci true -sn "proceduralPath" -ln "proceduralPath" -dt "string";
	addAttr -ci true -sn "texturePath" -ln "texturePath" -dt "string";
	addAttr -ci true -sn "archivePath" -ln "archivePath" -dt "string";
	addAttr -ci true -sn "gridSize" -ln "gridSize" -dv 256 -min 16 -at "long";
	addAttr -ci true -sn "textureMemory" -ln "textureMemory" -dv 32768 -min 128 -at "long";
	addAttr -ci true -sn "eyeSplits" -ln "eyeSplits" -dv 10 -min 0 -at "long";
	addAttr -ci true -sn "useImagerShaders" -ln "useImagerShaders" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "opacityThreshold" -ln "opacityThreshold" -at "float3" -nc 
		3;
	addAttr -ci true -sn "opacityThresholdR" -ln "opacityThresholdR" -dv 0.99608 -at "float" 
		-p "opacityThreshold";
	addAttr -ci true -sn "opacityThresholdG" -ln "opacityThresholdG" -dv 0.99608 -at "float" 
		-p "opacityThreshold";
	addAttr -ci true -sn "opacityThresholdB" -ln "opacityThresholdB" -dv 0.99608 -at "float" 
		-p "opacityThreshold";
	addAttr -ci true -sn "zThreshold" -ln "zThreshold" -at "float3" -nc 3;
	addAttr -ci true -sn "zThresholdR" -ln "zThresholdR" -dv 1 -at "float" -p "zThreshold";
	addAttr -ci true -sn "zThresholdG" -ln "zThresholdG" -dv 1 -at "float" -p "zThreshold";
	addAttr -ci true -sn "zThresholdB" -ln "zThresholdB" -dv 1 -at "float" -p "zThreshold";
	addAttr -ci true -sn "raytraceMaxDepth" -ln "raytraceMaxDepth" -dv 1 -min 0 -smx 
		16 -at "long";
	addAttr -ci true -sn "lightsToRender" -ln "lightsToRender" -at "message";
	addAttr -ci true -sn "objectsToRender" -ln "objectsToRender" -at "message";
	addAttr -ci true -sn "clippingPlanesToRender" -ln "clippingPlanesToRender" -at "message";
	addAttr -ci true -m -sn "displayRenderables" -ln "displayRenderables" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -m -sn "displayFilenames" -ln "displayFilenames" -dt "string";
	addAttr -ci true -m -sn "displayDrivers" -ln "displayDrivers" -dt "string";
	addAttr -ci true -m -sn "displayOutputVariables" -ln "displayOutputVariables" -dt "string";
	addAttr -ci true -m -sn "displayOverridePixelFilters" -ln "displayOverridePixelFilters" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -h true -m -sn "displayPixelFilters" -ln "displayPixelFilters" 
		-dv 5 -min 0 -max 8 -en "box:triangle:gaussian:catmull-rom:bessel:sinc:mitchell:zmin:zmax" 
		-at "enum";
	addAttr -ci true -m -sn "displayFilterWidthsX" -ln "displayFilterWidthsX" -dv 4 
		-min 0.001 -at "float";
	addAttr -ci true -m -sn "displayFilterWidthsY" -ln "displayFilterWidthsY" -dv 4 
		-min 0.001 -at "float";
	addAttr -ci true -m -sn "displayQuantizeZeros" -ln "displayQuantizeZeros" -at "long";
	addAttr -ci true -m -sn "displayQuantizeOnes" -ln "displayQuantizeOnes" -dv 255 
		-at "long";
	addAttr -ci true -m -sn "displayQuantizeMins" -ln "displayQuantizeMins" -at "long";
	addAttr -ci true -m -sn "displayQuantizeMaxs" -ln "displayQuantizeMaxs" -dv 255 
		-at "long";
	addAttr -ci true -m -sn "displayQuantizeDithers" -ln "displayQuantizeDithers" -dv 
		0.5 -at "float";
	addAttr -ci true -m -sn "displayGains" -ln "displayGains" -dv 1 -at "float";
	addAttr -ci true -m -sn "displayGammas" -ln "displayGammas" -dv 1 -at "float";
	addAttr -ci true -m -sn "displayMattes" -ln "displayMattes" -dv 1 -at "float";
	addAttr -ci true -m -sn "displayExclusives" -ln "displayExclusives" -at "float";
	addAttr -ci true -m -sn "displayAssociateAlphas" -ln "displayAssociateAlphas" -dv 
		1 -at "float";
	addAttr -ci true -m -sn "displayComputeAlphas" -ln "displayComputeAlphas" -at "float";
	addAttr -ci true -m -sn "displayEdgeEnables" -ln "displayEdgeEnables" -min 0 -max 
		1 -at "bool";
	addAttr -ci true -m -sn "displayEdgeVarNames" -ln "displayEdgeVarNames" -dt "string";
	addAttr -ci true -m -sn "displayEdgeThresholds" -ln "displayEdgeThresholds" -at "double";
	addAttr -ci true -uac -m -sn "displayEdgeColors" -ln "displayEdgeColors" -at "float3" 
		-nc 3;
	addAttr -ci true -sn "displayEdgeColorsR" -ln "displayEdgeColorsR" -at "float" -p "displayEdgeColors";
	addAttr -ci true -sn "displayEdgeColorsG" -ln "displayEdgeColorsG" -at "float" -p "displayEdgeColors";
	addAttr -ci true -sn "displayEdgeColorsB" -ln "displayEdgeColorsB" -at "float" -p "displayEdgeColors";
	addAttr -ci true -m -sn "displayEdgeFilterWidths" -ln "displayEdgeFilterWidths" 
		-at "double";
	addAttr -ci true -h true -m -sn "displayEdgeFilterWidthInterps" -ln "displayEdgeFilterWidthInterps" 
		-min 0 -max 1 -en "Pixels:% Of Frame Width" -at "enum";
	addAttr -ci true -m -sn "displayEdgeDepthEnables" -ln "displayEdgeDepthEnables" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -m -sn "displayEdgeDepthZMins" -ln "displayEdgeDepthZMins" -at "double";
	addAttr -ci true -m -sn "displayEdgeDepthZMaxs" -ln "displayEdgeDepthZMaxs" -at "double";
	addAttr -ci true -m -sn "displayEdgeDepthMinFilters" -ln "displayEdgeDepthMinFilters" 
		-at "double";
	addAttr -ci true -h true -m -sn "displayFrameCollapseStates" -ln "displayFrameCollapseStates" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -h true -m -sn "displayAdvancedFrameCollapseStates" -ln "displayAdvancedFrameCollapseStates" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -h true -m -sn "displayEdgeFrameCollapseStates" -ln "displayEdgeFrameCollapseStates" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "displaysAdvanceCollapseString" -ln "displaysAdvanceCollapseString" 
		-dt "string";
	addAttr -ci true -m -im false -sn "displaySubsetSets_0" -ln "displaySubsetSets_0" 
		-at "message";
	addAttr -ci true -sn "renderSecondaryDisplays" -ln "renderSecondaryDisplays" -dv 
		1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "renderShadowMaps" -ln "renderShadowMaps" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -m -sn "fragmentObjectSets" -ln "fragmentObjectSets" -at "message";
	addAttr -ci true -m -sn "fragmentFilenames" -ln "fragmentFilenames" -dt "string";
	addAttr -ci true -m -sn "fragmentUseStates" -ln "fragmentUseStates" -dv 1 -min 0 
		-max 1 -at "bool";
	addAttr -ci true -m -sn "fragmentWriteStates" -ln "fragmentWriteStates" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "fragmentBinaryRib" -ln "fragmentBinaryRib" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "fragmentCompressedRib" -ln "fragmentCompressedRib" -min 0 
		-max 1 -at "bool";
	addAttr -ci true -sn "fragmentWriteMode" -ln "fragmentWriteMode" -dv 1 -min 0 -max 
		1 -en "Reuse existing fragments:Overwrite existing fragments" -at "enum";
	addAttr -ci true -h true -m -sn "fragmentCollapseStates" -ln "fragmentCollapseStates" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "numberOfCPUs" -ln "numberOfCPUs" -at "long";
	addAttr -ci true -sn "useDisplacementShadersInShadows" -ln "useDisplacementShadersInShadows" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "useSurfaceShadersInShadows" -ln "useSurfaceShadersInShadows" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "useAtmosphereShadersInShadows" -ln "useAtmosphereShadersInShadows" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "useInteriorShadersInShadows" -ln "useInteriorShadersInShadows" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -sn "translateMayaShaders" -ln "translateMayaShaders" -dv 1 -min 
		0 -max 1 -at "bool";
	addAttr -ci true -sn "useMayaShaders" -ln "useMayaShaders" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "concatenateGeoTransforms" -ln "concatenateGeoTransforms" -dv 
		1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "concatenateLightTransforms" -ln "concatenateLightTransforms" 
		-dv 1 -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "standardAtmosphere" -ln "standardAtmosphere" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "volumeShadingRate" -ln "volumeShadingRate" -dv 1 -min 0.001 
		-at "float";
	addAttr -ci true -sn "hider" -ln "hider" -min 0 -max 2 -en "hidden:raytrace:photon" 
		-at "enum";
	addAttr -ci true -sn "translatedShadersAOVs" -ln "translatedShadersAOVs" -min 0 
		-max 2 -en "Default AOVs for Render Mode:Defined AOVs Only:All AOVs" -at "enum";
	addAttr -ci true -sn "depthFilter" -ln "depthFilter" -min 0 -max 3 -en "min:max:average:midpoint" 
		-at "enum";
	addAttr -ci true -sn "volumeInterpretation" -ln "volumeInterpretation" -min 0 -max 
		2 -en "Discrete:Continuous:Distance Inside" -at "enum";
	addAttr -ci true -h true -m -sn "displaySubsetTypes" -ln "displaySubsetTypes" -at "double";
	setAttr ".version" 2;
	setAttr ".ribFilename" -type "string" "3delight/<scene>/rib/<scene>_<pass>.<ext>";
	setAttr ".backgroundRenderParams" -type "string" "";
	setAttr ".renderLogFilename" -type "string" "3delight/<scene>/rib/<scene>_<pass>.<ext>.log";
	setAttr ".renderMode" 3;
	setAttr ".preRenderMEL" -type "string" "";
	setAttr ".postRenderMEL" -type "string" "";
	setAttr ".preFrameMEL" -type "string" "";
	setAttr ".postFrameMEL" -type "string" "";
	setAttr ".postOptionMEL" -type "string" "";
	setAttr ".preWorldMEL" -type "string" "";
	setAttr ".postWorldMEL" -type "string" "";
	setAttr ".netCacheDir" -type "string" "";
	setAttr ".globalMap" -type "string" "3delight/<scene>/photonmaps/global.pmap";
	setAttr ".causticMap" -type "string" "3delight/<scene>/photonmaps/caustic.pmap";
	setAttr ".statisticsFile" -type "string" "";
	setAttr ".shaderPath" -type "string" "@";
	setAttr ".proceduralPath" -type "string" "@";
	setAttr ".texturePath" -type "string" "@";
	setAttr ".archivePath" -type "string" "@";
	setAttr ".displayRenderables[0]" yes;
	setAttr ".displayFilenames[0]" -type "string" "3delight/<scene>/image/<scene>_<pass>.#.<ext>";
	setAttr ".displayDrivers[0]" -type "string" "mplay";
	setAttr ".displayOutputVariables[0]" -type "string" "rgba";
	setAttr ".displayQuantizeOnes[0]"  0;
	setAttr ".displayQuantizeMaxs[0]"  0;
	setAttr ".displayQuantizeDithers[0]"  0;
	setAttr ".displayEdgeVarNames[0]" -type "string" "Ci";
	setAttr ".displayEdgeThresholds[0]"  0.1;
	setAttr ".displayEdgeColors[0]" -type "float3"  1 1 1;
	setAttr ".displayEdgeFilterWidths[0]"  2;
	setAttr ".displayEdgeDepthZMaxs[0]"  1000;
	setAttr ".displayEdgeDepthMinFilters[0]"  1;
	setAttr ".displayAdvancedFrameCollapseStates[0]" yes;
	setAttr ".displayEdgeFrameCollapseStates[0]" yes;
createNode expression -n "delightRenderPass1_pixelRatioExpr";
	setAttr -k on ".nds";
	setAttr -s 3 ".in";
	setAttr -s 3 ".in";
	setAttr ".ixp" -type "string" ".O[0] = .I[0] / .I[1] * .I[2]";
	setAttr ".ani" 0;
createNode dl_externColor -n "dl_externColor1";
	setAttr ".iv" -type "float3" 0 0 0 ;
	setAttr ".pn" -type "string" "shadowColor";
createNode dl_externFloat -n "dl_externFloat1";
	setAttr ".pn" -type "string" "shadowOpacity";
createNode dl_externFloat -n "dl_externFloat2";
	setAttr ".iv" 0.89999997615814209;
	setAttr ".pn" -type "string" "hemispheres";
createNode dl_externFloat -n "dl_externFloat3";
	setAttr ".iv" 0.05000000074505806;
	setAttr ".pn" -type "string" "hemisphereFalloff";
createNode dl_externFloat -n "dl_externFloat4";
	setAttr ".pn" -type "string" "diffuseFalloff";
createNode shadingEngine -n "dl_layer2SG";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo2";
createNode dl_shadowCollector -n "dl_layer2_layer0_shadowcollector";
createNode dl_externFloat -n "dl_externFloat5";
	setAttr ".iv" 0;
	setAttr ".pn" -type "string" "beautyMode";
createNode dl_externFloat -n "dl_externFloat6";
	setAttr ".iv" 0;
	setAttr ".pn" -type "string" "lightType";
createNode dl_externFloat -n "dl_externFloat7";
	setAttr ".iv" 0;
	setAttr ".pn" -type "string" "useLightColor";
select -ne :time1;
	setAttr ".o" 1;
select -ne :renderPartition;
	setAttr -s 4 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 3 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 10 ".u";
select -ne :lightList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".fs" 1;
	setAttr ".ef" 10;
select -ne :defaultResolution;
	setAttr ".w" 1920;
	setAttr ".h" 1080;
	setAttr ".dar" 1.7777777910232544;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "polySphere1.out" "pSphereShape1.i";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[0].llnk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.lnk[0].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[1].llnk";
connectAttr ":initialParticleSE.msg" "lightLinker1.lnk[1].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[2].llnk";
connectAttr "dl_layer1SG.msg" "lightLinker1.lnk[2].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[3].llnk";
connectAttr "dl_layer2SG.msg" "lightLinker1.lnk[3].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[0].sllk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.slnk[0].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[1].sllk";
connectAttr ":initialParticleSE.msg" "lightLinker1.slnk[1].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[2].sllk";
connectAttr "dl_layer1SG.msg" "lightLinker1.slnk[2].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[3].sllk";
connectAttr "dl_layer2SG.msg" "lightLinker1.slnk[3].solk";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "dl_shadowCollectorComponent.ocmp" "dl_shadowCollector.l[0].lcmp[0]"
		;
connectAttr "dl_shadowCollector.oc" "dl_layer1SG.ss";
connectAttr "pSphereShape1.iog" "dl_layer1SG.dsm" -na;
connectAttr "dl_layer1SG.msg" "materialInfo1.sg";
connectAttr "dl_shadowCollector.msg" "materialInfo1.m";
connectAttr "dl_shadowCollector.msg" "materialInfo1.t" -na;
connectAttr "dl_externColor1.ov" "dl_shadowCollectorComponent.shc";
connectAttr "dl_externFloat1.ov" "dl_shadowCollectorComponent.sho";
connectAttr "dl_externFloat2.ov" "dl_shadowCollectorComponent.h";
connectAttr "dl_externFloat3.ov" "dl_shadowCollectorComponent.hf";
connectAttr "dl_externFloat4.ov" "dl_shadowCollectorComponent.dfo";
connectAttr "dl_externFloat5.ov" "dl_shadowCollectorComponent.bm";
connectAttr "dl_externFloat7.ov" "dl_shadowCollectorComponent.ulc";
connectAttr ":defaultResolution.w" "delightRenderPass1.resolutionX";
connectAttr ":defaultResolution.h" "delightRenderPass1.resolutionY";
connectAttr "delightRenderPass1_pixelRatioExpr.out[0]" "delightRenderPass1.pixelAspectRatio"
		;
connectAttr ":perspShape.usedBy3dfm" "delightRenderPass1.camera";
connectAttr ":defaultResolution.h" "delightRenderPass1_pixelRatioExpr.in[0]";
connectAttr ":defaultResolution.w" "delightRenderPass1_pixelRatioExpr.in[1]";
connectAttr ":defaultResolution.dar" "delightRenderPass1_pixelRatioExpr.in[2]";
connectAttr "dl_layer2SG.msg" "materialInfo2.sg";
connectAttr "dl_layer1SG.pa" ":renderPartition.st" -na;
connectAttr "dl_layer2SG.pa" ":renderPartition.st" -na;
connectAttr "dl_shadowCollector.msg" ":defaultShaderList1.s" -na;
connectAttr "dl_shadowCollectorComponent.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "dl_externColor1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat4.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_layer2_layer0_shadowcollector.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "dl_externFloat5.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat6.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "dl_externFloat7.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "lightLinker1.msg" ":lightList1.ln" -na;
// End of dl_shadowCollector.ma
