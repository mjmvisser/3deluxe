#include "mattePaintNode.h"

#include <maya/MImage.h>
#include <maya/MPlug.h>
#include <maya/MColor.h>
#include <maya/MMatrix.h>
#include <maya/MAngle.h>
#include <maya/MGlobal.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MFloatVector.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>

using namespace Magick;

using namespace delight;

MTypeId mattePaintNode::m_id(0x0c2d1d0e);

MObject mattePaintNode::m_defaultColor;
MObject mattePaintNode::m_defaultTransparency;
MObject mattePaintNode::m_layers;
MObject mattePaintNode::m_layerName;
MObject mattePaintNode::m_textureFile;
MObject mattePaintNode::m_enableState;
MObject mattePaintNode::m_cameraFocalLength;
MObject mattePaintNode::m_cameraFilmAperture;
MObject mattePaintNode::m_cameraMessage;
MObject mattePaintNode::m_cameraMatrix;
MObject mattePaintNode::m_refPointCamera;
MObject mattePaintNode::m_pointCamera;
MObject mattePaintNode::m_pointWorld;
MObject mattePaintNode::m_matrixEyeToNormPersp;
MObject mattePaintNode::m_matrixEyeToWorld;
MObject mattePaintNode::m_matrixNormPerspToEye;
MObject mattePaintNode::m_matrixWorldToEye;
MObject mattePaintNode::m_resolution;
MObject mattePaintNode::m_outColor;
MObject mattePaintNode::m_outTransparency;

mattePaintNode::mattePaintNode()
{
}

mattePaintNode::~mattePaintNode()
{
}

void* mattePaintNode::creator()
{
    return new mattePaintNode();
}

MStatus mattePaintNode::initialize()
{
    MStatus status;
    MFnTypedAttribute typAttr;
    MFnCompoundAttribute compAttr;
    MFnNumericAttribute numAttr;
    MFnMatrixAttribute mtxAttr;
    MFnMessageAttribute msgAttr;

    m_defaultColor = numAttr.createColor("defaultColor",  "dc");
    CHECK_MSTATUS(addAttribute(m_defaultColor));

    m_defaultTransparency = numAttr.createColor("defaultTransparency",  "dt");
    CHECK_MSTATUS(addAttribute(m_defaultTransparency));

    // Layers
    m_layerName = typAttr.create("layerName", "ln", MFnData::kString);
    m_textureFile = typAttr.create("textureFile", "tf", MFnData::kString);
    m_enableState = numAttr.create("enableState", "es", MFnNumericData::kBoolean);
    numAttr.setDefault(true);
    m_cameraMessage = msgAttr.create("cameraMessage", "cmg");
    m_cameraMatrix = mtxAttr.create("cameraMatrix", "cmx", MFnMatrixAttribute::kFloat);
    m_cameraFocalLength = numAttr.create("cameraFocalLength", "cfl", MFnNumericData::kFloat);
    m_cameraFilmAperture = numAttr.create("cameraFilmAperture", "cfa", MFnNumericData::kFloat);

    m_layers = compAttr.create("layers", "ls");
    compAttr.setArray(true);
    compAttr.addChild(m_layerName);
    compAttr.addChild(m_textureFile);
    compAttr.addChild(m_enableState);
    compAttr.addChild(m_cameraMessage);
    compAttr.addChild(m_cameraMatrix);
    compAttr.addChild(m_cameraFocalLength);
    compAttr.addChild(m_cameraFilmAperture);
    CHECK_MSTATUS(addAttribute(m_layers));

    // Maya render stuff

    m_refPointCamera = numAttr.createPoint("refPointCamera", "rpc");
    numAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(m_refPointCamera));


    m_pointCamera = numAttr.createPoint("pointCamera", "p");
    numAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(m_pointCamera));

    m_pointWorld = numAttr.createPoint("pointWorld", "pw");
    numAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(m_pointWorld));

    m_matrixEyeToNormPersp = mtxAttr.create("matrixEyeToNormPersp", "etp", MFnMatrixAttribute::kFloat);
    CHECK_MSTATUS(addAttribute(m_matrixEyeToNormPersp));

    m_matrixEyeToWorld = mtxAttr.create("matrixEyeToWorld", "etw", MFnMatrixAttribute::kFloat);
    CHECK_MSTATUS(addAttribute(m_matrixEyeToWorld));

    m_matrixNormPerspToEye = mtxAttr.create("matrixNormPerspToEye", "pte", MFnMatrixAttribute::kFloat);
    CHECK_MSTATUS(addAttribute(m_matrixNormPerspToEye));

    m_matrixWorldToEye = mtxAttr.create("matrixWorldToEye", "wte", MFnMatrixAttribute::kFloat);
    CHECK_MSTATUS(addAttribute(m_matrixWorldToEye));

    m_resolution = numAttr.create("resolution", "resolution", MFnNumericData::kLong);
    numAttr.setDefault(32);
    CHECK_MSTATUS(addAttribute(m_resolution));

    m_outColor = numAttr.createColor("outColor",  "oc");
    numAttr.setWritable(false);
    numAttr.setStorable(false);
    CHECK_MSTATUS(addAttribute(m_outColor));

    m_outTransparency = numAttr.createColor("outTransparency",  "ot");
    numAttr.setWritable(false);
    numAttr.setStorable(false);
    CHECK_MSTATUS(addAttribute(m_outTransparency));

    CHECK_MSTATUS(attributeAffects(m_defaultColor, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_layers, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_refPointCamera, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_pointCamera, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_pointWorld, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_matrixEyeToNormPersp, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_matrixEyeToWorld, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_matrixNormPerspToEye, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_matrixWorldToEye, m_outColor));
    CHECK_MSTATUS(attributeAffects(m_resolution, m_outColor));

    CHECK_MSTATUS(attributeAffects(m_defaultTransparency, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_layers, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_refPointCamera, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_pointCamera, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_pointWorld, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_matrixEyeToNormPersp, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_matrixEyeToWorld, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_matrixNormPerspToEye, m_outTransparency));
    CHECK_MSTATUS(attributeAffects(m_matrixWorldToEye, m_outTransparency));

    CHECK_MSTATUS(attributeAffects(m_resolution, m_outTransparency));

    return MS::kSuccess;
}

MStatus mattePaintNode::compute(const MPlug& plug, MDataBlock& data)
{
    if(plug != m_outColor && plug != m_outTransparency)
        return MS::kUnknownParameter;

    int resolution = data.inputValue(m_resolution).asLong();


    MFloatVector defaultTransparency = data.inputValue(m_defaultTransparency).asFloatVector();
    MFloatVector outColor = data.inputValue(m_defaultColor).asFloatVector();
    MFloatVector white(1, 1, 1);
    MFloatVector outAlpha = white - defaultTransparency;

    MFloatVector cP = data.inputValue(m_refPointCamera).asFloatVector();
    //MFloatVector cP = data.inputValue(m_pointCamera).asFloatVector();
    MFloatVector wP = data.inputValue(m_pointWorld).asFloatVector();

    MArrayDataHandle layersHdl = data.inputArrayValue(m_layers);

    MFloatMatrix etpMtx = data.inputValue(m_matrixEyeToNormPersp).asFloatMatrix();
    MFloatMatrix etwMtx = data.inputValue(m_matrixEyeToWorld).asFloatMatrix();
    MFloatMatrix pteMtx = data.inputValue(m_matrixNormPerspToEye).asFloatMatrix();
    MFloatMatrix wteMtx = data.inputValue(m_matrixWorldToEye).asFloatMatrix();
/*

    for(int i = 0; i < layersHdl.elementCount(); i++, layersHdl.next()){

    	MDataHandle layerHdl = layersHdl.inputValue();

    	// Enabled?
    	if(!layerHdl.child(m_enableState).asBool())
    		continue;

    	// Has file?
    	MString textureFile = layerHdl.child(m_textureFile).asString();
    	if(textureFile == "")
    	    continue;

    	//
    	int index = layersHdl.elementIndex();

    	//
       	if(!m_textures[index].load(textureFile, resolution))
       		continue;

       	int width = m_textures[index].m_image.columns();
       	int height = m_textures[index].m_image.rows();
       	if(!width || !height)
       		continue;

       	float focal = layerHdl.child(m_cameraFocalLength).asFloat();
		float aperture = layerHdl.child(m_cameraFilmAperture).asFloat();
		float fov = (0.5 * aperture) / (focal * 0.03937);

		fov = 2.0 * atan(fov);
		float fovd = 57.29578 * fov;

		cout << fov << " " << fovd << endl;
		//double fov = MAngle(double(fovd), MAngle::kDegrees).asRadians();

       	//
		MFloatMatrix camMtx = layerHdl.child(m_cameraMatrix).asFloatMatrix();

		//Ptex = transform("current", "world", Ptex);
//		Ptex = transform(cameraSpace, "current", Ptex);

		// TODO: get this right
		MFloatVector Ptex = wP * camMtx;


		//
		float imageAR = float(width) / float(height);

		// Proj coords
//		float ss = (Ptex.x / 2.0 + 0.5);
//		float tt = (1.0 - (Ptex.y * imageAR / 2.0 + 0.5));
		float ss = Ptex.x * (Ptex.z * fov) ;
		float tt = (Ptex.y * imageAR ) * (Ptex.z * fov);

//		if(ss < 0 || ss > 1 || tt < 0 || tt > 1)
//			continue;

		int x = float(width) * ss;
		int y = float(height) * tt;

		//
		ColorRGB c(m_textures[index].m_image.pixelColor(x, y));

		outColor.x = c.red();
		outColor.y = c.green();
		outColor.z = c.blue();
    }
    */

    data.outputValue(m_outColor).set(outColor);
    data.outputValue(m_outTransparency).set(white-outAlpha);

    data.setClean(plug);

    return MS::kSuccess;
}

