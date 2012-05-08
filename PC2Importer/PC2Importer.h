#ifndef PC2IMPOERTERNODE_H
#define PC2IMPOERTERNODE_H

#include "../coral-repo/coral/coral/src/Node.h"

namespace coral{
	class StringAttribute;
	class NumericAttribute;
	
struct pc2Header{
	char signature[12];
	int fileVersion;
	int numPoints;
	float startFrame;
	float sampleRate;
	int numSamples;
};

class PC2Importer : public Node{
public:
	PC2Importer(const std::string &name, Node *parent);
	~PC2Importer();
	
	void updateSlice(Attribute *attribute, unsigned int slice);
	
	StringAttribute *fileName(){
		return _filename;
	}
	
	NumericAttribute *frame(){
		return _frame;
	}
	
	NumericAttribute *points(){
		return _points;
	}
private:
	StringAttribute *_filename;
	NumericAttribute *_frame;
	NumericAttribute *_points;
	
};
}

int ntohi( const int  );
float ntohf( const float  );


#endif