#include "mattePaintNode.h"
#include <maya/MGlobal.h>
#include <maya/MFnPlugin.h>

using namespace delight;

MStatus initializePlugin(MObject obj)
{
    MFnPlugin plugin(obj, "3Delight", "1.0", "Any");

	const MString UserClass("shader/surface:swatch/3delight_surface");

	MStatus status = plugin.registerNode("dl_mattePaint",
							 mattePaintNode::m_id,
							 mattePaintNode::creator,
							 mattePaintNode::initialize,
							 MPxNode::kDependNode,
							 &UserClass);
	if(!status)
		return status;

	MGlobal::executeCommand("source dl_mattePaint;");

	MGlobal::executeCommand("if(`window -ex createRenderNodeWindow`)"
								"refreshCreateRenderNodeWindow \"shader/surface\";\n");

    return MS::kSuccess;
}

MStatus uninitializePlugin(MObject obj)
{
    MFnPlugin plugin(obj);

    MStatus status = plugin.deregisterNode(mattePaintNode::m_id);
    if(!status)
    	return status;

	MGlobal::executeCommand("if(`window -ex createRenderNodeWindow`)"
								"refreshCreateRenderNodeWindow \"shader/surface\";\n");

    return MS::kSuccess;
}
