#include "PC2Importer.h"
#include "../coral-repo/coral/coral/src/NumericAttribute.h"
#include "../coral-repo/coral/coral/src/StringAttribute.h"
#include "../coral-repo/coral/coral/src/NetworkManager.h"
#include <coral/pythonWrapperUtils.h>

#include <fstream>
#include <boost/python.hpp>


#ifdef __APPLE__
#include <OpenGL/gl.h>
#else
#if defined(WIN64) || defined(_WIN64) || defined(WIN32) || defined(_WIN32)
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <GL/gl.h>
#endif
#endif


using namespace coral;

PC2Importer::PC2Importer(const std::string &name, Node *parent) : Node(name, parent){
	_filename = new StringAttribute("filename", this);
	_frame = new NumericAttribute("frame", this);
	_points = new NumericAttribute("points", this);
	
	addInputAttribute(_filename);
	addInputAttribute(_frame);
	addOutputAttribute(_points);
	
	setAttributeAffect(_filename, _points);
	setAttributeAffect(_frame, _points);
	
	std::vector<std::string> specs;
	specs.push_back("Float");
	setAttributeAllowedSpecializations(_frame, specs);
	specs.clear();
	specs.push_back("Vec3Array");
	setAttributeAllowedSpecializations(_points, specs);
}

PC2Importer::~PC2Importer(){
}

void PC2Importer::updateSlice(Attribute *attribute, unsigned int slice){
	std::string filename = _filename->value()->stringValue();
	filename = NetworkManager::resolveFilename(filename);
	
	std::ifstream file(filename.c_str(), std::ios::in | std::ios::ate);
	if(!file || !file.tellg()){
			std::vector<Imath::V3f> tmp;
			_points->outValue()->setVec3Values(tmp);
			return;
	}
	pc2Header *header = new pc2Header();
	
	file.seekg(0, std::ios::beg);
	file.read((char*)&(header->signature), 12);

	file.read((char*)&(header->fileVersion), sizeof(int));
	//header->fileVersion = ntohi(header->fileVersion);

	file.read((char*)&(header->numPoints), sizeof(int));
	//header->numPoints = ntohi(header->numPoints);
		
	file.read((char*)&(header->startFrame), sizeof(float));
	//header->startFrame = ntohf(header->startFrame);
	file.read((char*)&(header->sampleRate), sizeof(float));
	//header->sampleRate = ntohf(header->sampleRate);
	file.read((char*)&(header->numSamples), sizeof(int));
	//header->numSamples = ntohi(header->numSamples);
	
	int headerSize = file.tellg();
	//std::cout << "with tellg: " << headerSize << " with calc: " << sizeof(int)*3 + sizeof(float)*2 + sizeof(char) * 12 << std::endl;
	
	float currentFrame = _frame->value()->floatValueAt(0) - header->startFrame;
	//currentFrame = 1;
	std::cout << "_frame: " << _frame->value()->floatValueAt(0) << std::endl;
	std::cout << "currentFrame " << currentFrame << std::endl;
	float frame_size = header->numPoints * sizeof(float) * 3;
	std::cout << "frame_size " << frame_size << std::endl;
	
	float file_offset = currentFrame * frame_size + (float)headerSize; 
	std::cout << "before seek" << file.tellg() << std::endl;
	file.seekg((int)file_offset, std::ios::beg);
	std::cout << "after seek" << file.tellg() << std::endl;	
	std::vector<Imath::V3f> points;
	
	float *a_point = new float[3];
	std::cout << "HEADER DUMP:" << header->signature << "," << header->fileVersion << "," << header->numPoints << "," << header->startFrame << "," << header->sampleRate << "," << header->numSamples << std::endl;
	for(int i=0; i<header->numPoints; i++)
	{
		for(int j=0; j<3; j++){
			file.read((char *)&a_point[j], sizeof(float));
		}
		//std::cout << "complete point:" << Imath::V3f(a_point[0],a_point[1],a_point[2]) << std::endl;
		points.push_back(Imath::V3f(a_point[0],a_point[1],a_point[2]));
	}
	
	
	
	
	file.close();
	
	
	
	_points->outValue()->setVec3Values(points);
	
}

BOOST_PYTHON_MODULE(PC2Importer){
	pythonWrapperUtils::pythonWrapper<PC2Importer, Node>("PC2Importer");
}

int ntohi( const int inInt )
{
   int retVal;
   char *floatToConvert = ( char* ) & inInt;
   char *returnFloat = ( char* ) & retVal;

   // swap the bytes into a temporary buffer
   returnFloat[0] = floatToConvert[3];
   returnFloat[1] = floatToConvert[2];
   returnFloat[2] = floatToConvert[1];
   returnFloat[3] = floatToConvert[0];

   return retVal;
}

float ntohf( const float inFloat )
{
   float retVal;
   char *floatToConvert = ( char* ) & inFloat;
   char *returnFloat = ( char* ) & retVal;

   // swap the bytes into a temporary buffer
   returnFloat[0] = floatToConvert[3];
   returnFloat[1] = floatToConvert[2];
   returnFloat[2] = floatToConvert[1];
   returnFloat[3] = floatToConvert[0];

   return retVal;
}

