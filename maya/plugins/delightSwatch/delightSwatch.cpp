#include <maya/MGlobal.h>
#include <maya/MFileObject.h>
#include <maya/MImage.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MSwatchRenderRegister.h>
#include <maya/MSwatchRenderBase.h>

#include <string>
#include <map>

using namespace std;

// To store buffers
map<string, MImage> NodeTypeImages;

class DelightSwatch : public MSwatchRenderBase
{
public:

	DelightSwatch(MObject obj, MObject renderObj, int res);
	bool doIteration();
};

DelightSwatch::DelightSwatch(MObject obj, MObject renderObj, int res) : MSwatchRenderBase(obj, renderObj, res)
{
}

bool DelightSwatch::doIteration()
{
	MObject nodeObj = node();
	MFnDependencyNode nodeFn(nodeObj);

	MString nodeType = nodeFn.typeName();
	string nodeTypeKey = nodeType.asChar();

	if(NodeTypeImages.find(nodeTypeKey) == NodeTypeImages.end()){

		MFileObject iconFile;
		iconFile.setResolveMethod(MFileObject::kExact);
		iconFile.setRawName("render_" + nodeType + ".xpm");
		iconFile.setRawPath("$XBMLANGPATH");

		// We need to strip the stupid '/%B'
#if defined(LINUX)
		MString cleanPath;
		for(int i = 0; i < iconFile.pathCount(); i++){
			MString path = iconFile.ithPath(i);
			cleanPath += ":" + path.substring(0, path.length() - 5);
		}
		iconFile.setRawPath(cleanPath);
#endif

		MString imgPath = iconFile.resolvedFullName();
		if(!iconFile.exists()){
			iconFile.setRawName("render_particleSamplerInfo.xpm");
			imgPath = iconFile.resolvedFullName();
		}

		NodeTypeImages[nodeTypeKey] = MImage();

		NodeTypeImages[nodeTypeKey].readFromFile(iconFile.resolvedFullName());

		NodeTypeImages[nodeTypeKey].verticalFlip();
	}

	unsigned w, h;
	NodeTypeImages[nodeTypeKey].getSize(w, h);

	MImage& imgRef = image();
	imgRef.setPixels(NodeTypeImages[nodeTypeKey].pixels(), w, h);


	return true;
}

MSwatchRenderBase* DelightSwatchCreator(MObject dependNode, MObject renderNode, int imageResolution)
{
	DelightSwatch * delightSwatchPtr = new DelightSwatch(dependNode, renderNode, imageResolution);

	return delightSwatchPtr;
}

MStatus initializePlugin( MObject obj )
{
	CHECK_MSTATUS_AND_RETURN_IT(MSwatchRenderRegister::registerSwatchRender("3delight", &DelightSwatchCreator));

	return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj )
{
	CHECK_MSTATUS_AND_RETURN_IT(MSwatchRenderRegister::unregisterSwatchRender("3delight"));

	return MS::kSuccess;
}
