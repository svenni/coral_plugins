from coral import Node, NumericAttribute, Imath, StringAttribute
from coral.plugin import Plugin
import pcLoader

class pcReader(Node):
    def __init__(self, name, parent):
        Node.__init__(self, name, parent)
        
        self.path = StringAttribute('filename', self)
        self.input = NumericAttribute('frame', self)
        self.output = NumericAttribute('points',self)
        
        self.addInputAttribute(self.input)
        self.addInputAttribute(self.path)
        self.addOutputAttribute(self.output)
        
        self._setAttributeAffect(self.input, self.output)
        self._setAttributeAffect(self.path, self.output)
        
        
        self._setAttributeAllowedSpecializations(self.input, ['Float'])
        self._setAttributeAllowedSpecializations(self.output, ['Vec3Array'])
        
        #self._pcLoader = pcLoader.pcLoader('/Users/sjt/Dev/pc2/cache.pc2')
        
        
    def update(self, attribute):
        path = self.path.value().stringValue()        
        self._pcLoader = pcLoader.pcLoader(path)
        
        value1 = self.input.value().floatValueAt(0)
        points = self._pcLoader.get_frame(value1)

        
        imath_points = []
        for point in points:
            imath_points.append(Imath.Vec3f(point[0],point[1],point[2]))
        
        self.output.outValue().setVec3Values(imath_points)
        
        
def loadPlugin():
    plugin = Plugin('pcReaderPlugin')
    plugin.registerNode('pcReader', pcReader, tags=['sjtNodes'], description='Reads data from a pc2 file.')
    return plugin

        