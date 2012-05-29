import os
import time

from coral import Node, NumericAttribute, Imath, StringAttribute, GeoAttribute, EnumAttribute
from coral.plugin import Plugin


class WriteNode(Node):
    def __init__(self, name, parent):
        Node.__init__(self, name, parent)
        
        self._path = StringAttribute('filename', self)
        self._points = NumericAttribute('points', self)
        self._data = NumericAttribute('data', self)
        self._format = EnumAttribute('format', self)
        self._frame = NumericAttribute('frame', self)
        self._startFrame = NumericAttribute('startFrame', self)
        self._endFrame = NumericAttribute('endFrame', self)
        #self._geo = GeoAttribute('geo', self)
        
        self.addInputAttribute(self._path)
        self.addInputAttribute(self._points)
        self.addInputAttribute(self._data)
        self.addInputAttribute(self._format)
        self.addInputAttribute(self._frame)
        self.addInputAttribute(self._startFrame)
        self.addInputAttribute(self._endFrame)

        self._format.value().addEntry(0, 'pc2')
        self._format.value().addEntry(1, 'ascii')
        self._format.value().setCurrentIndex(0)
        
        self._setAttributeAllowedSpecializations(self._path, ['Path-write'])
        self._setAttributeAllowedSpecializations(self._points, ['Vec3Array'])
        self._setAttributeAllowedSpecializations(self._data, ['Float'])
        self._setAttributeAllowedSpecializations(self._frame, ['Float'])
        self._setAttributeAllowedSpecializations(self._startFrame, ['Float'])
        self._setAttributeAllowedSpecializations(self._endFrame, ['Float'])        
        
                
    def update(self, attribute):
        pass
        
    def write(self):
        # first we check if something is connected to the frame attr
        if self._frame.input() is None:
            raise RuntimeError('A time node isn\'t connected to \'frame\'')
        time_node = self._frame.input().parent()
        # and is it a time node?
        if time_node.className() != 'Time':
            raise RuntimeError('Input of \'frame\' is not a Time node.')
        time_attr = time_node.findAttribute('time')
        print dir(time_attr)
        
        # check the output path and range attrs
        output_path = self._path.value().stringValue()
        if output_path.strip() == '':
            raise RuntimeError('No output path specified.')
        
        start_frame = self._startFrame.value().floatValueAt(0)
        end_frame = self._endFrame.value().floatValueAt(0)
        
        if start_frame >= end_frame:
            raise RuntimeError('End is before start.')
        
        # create the folder for the output
        try:
            os.makedirs(os.path.dirname(output_path))
        except os.error:
            pass
        except Exception, err:
            raise RuntimeError('Unable to create folder %s: %s' % (os.path.dirname(output_path), str(err)))
            
        selected_format = self._format.value().entries()[self._format.value().currentIndex()]
        if selected_format == 'pc2':
            # write out pc2 data
            pass
        elif selected_format == 'ascii':
            f = open(output_path, 'wt')
            
            '''
            I decided to check what input to use from inside the loop because it makes things a bit clearer and a simple speed comparison show it isn't _that_
            much of a slowdown. With 100000 frames (the points array was 10 elements) I got these write times:
            points: 14.098s (loop inside input check) vs 14.34s (check inside loop)
            float: 4.036 (loop inside input check) vs 4.55 (check inside loop)
            
            '''
            for i in range(int(start_frame), int(end_frame+1)):
                time_attr.value().setFloatValueAt(0,i)
                time_attr.forceDirty()
                if self._points.input() is not None:
                    for p in self._points.value().vec3Values():
                        f.write('<%f %f %f>, ' % (p.x, p.y, p.z))
                    f.write('\n')

                elif self._data.input() is not None:
                    f.write('%s\n' % str(self._data.value().floatValueAt(0)))

                else:
                    f.close()
                    raise RuntimeError('No data to write!')
        
        
def loadPlugin():
    plugin = Plugin('WriteNodePlugin')        
    plugin.registerNode('WriteNode', WriteNode, tags=['sjtNodes'], description='Writes point data to various formats.')
    return plugin