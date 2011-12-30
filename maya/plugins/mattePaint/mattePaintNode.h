#ifndef _MATTEPAINTNODE_H
#define _MATTEPAINTNODE_H

#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MObject.h>
#include <maya/MImage.h>

#include <Magick++.h>

#include <map>

class MPlug;
class MDataBlock;

namespace delight
{
class Texture
{
public:

	Texture():
		m_loaded(false),
		m_resolution(32){
	};

	~Texture(){};

	bool load(const MString& name, int resolution){

		if(m_loaded && name == m_name && resolution == m_resolution)
			return true;

		try{
			m_image.read(name.asChar());
			m_loaded = true;
			m_name = name;
			m_resolution = resolution;
		}
		catch(Magick::Exception e ){
			return false;
		}

		return true;
	}

	bool m_loaded;
	MString m_name;
	int m_resolution;
	Magick::Image m_image;
};

class mattePaintNode : public MPxNode
{
public:

    mattePaintNode();
    ~mattePaintNode();

    static void*  	creator();
    static MStatus  initialize();

    MStatus 		compute(const MPlug& plug, MDataBlock& data);
/*
    bool 			getInternalValueInContext(	const MPlug& plug,
												MDataHandle& dataHandle,
												MDGContext& ctx);
*/
    static MTypeId	m_id;

private:

    std::map<int, Texture> m_textures;

    //
    static MObject  m_defaultColor;
    static MObject  m_defaultTransparency;

    // Per layers
    static MObject  m_layers;
    static MObject  m_layerName;
    static MObject  m_textureFile;
    static MObject  m_enableState;
    static MObject  m_cameraMessage;
    static MObject  m_cameraMatrix;
    static MObject  m_cameraFocalLength;
    static MObject  m_cameraFilmAperture;

    // passed by Maya
    static MObject  m_refPointCamera;
    static MObject  m_pointCamera;
    static MObject  m_pointWorld;
    static MObject  m_matrixEyeToNormPersp;
    static MObject  m_matrixEyeToWorld;
    static MObject  m_matrixNormPerspToEye;
    static MObject  m_matrixWorldToEye;




    //
    static MObject  m_resolution;

    // Ouptuts
    static MObject  m_outColor;
    static MObject  m_outTransparency;

};

}
#endif // _MATTEPAINTNODE_H
