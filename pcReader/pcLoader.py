import struct
import os

class pcLoader(object):
    id_fmt = '<12ci'
    header_fmt = 'iffi'
    
    def __init__(self, filename):
        self._filename = filename
        if not os.path.exists(self._filename):
            raise RuntimeError('Invalid filename')
        self._file = open(filename,'rb')
        buffer = self._file.read(struct.calcsize(self.id_fmt))
        #print 'buffer', buffer
        buffer = self._file.read(struct.calcsize(self.header_fmt))
        #print 'buffer2', struct.unpack(self.header_fmt, buffer)
        
        self._num_points, self._start_frame, self._sample_rate, self._num_samples = struct.unpack(self.header_fmt, buffer)
        self._header_size = struct.calcsize(self.id_fmt + self.header_fmt)
        
        #print self._num_points, self._start_frame, self._sample_rate, self._num_samples
        
    def get_frame(self, frame):
        frame = frame - self._start_frame
        if frame > self._num_samples - 1 or frame < 0:
            return []
        frame_size = self._num_points * struct.calcsize('fff')
        file_offset = frame * frame_size + self._header_size
        self._file.seek(file_offset)
        frame_points = []
        #print 'now at', self._file.tell()
        for i in range(self._num_points):
            point = self._file.read(struct.calcsize('fff'))
            frame_points.append(struct.unpack('fff',point))
        return frame_points
    def __del__(self):
        self._file.close()
        
if __name__ == '__main__':
    loader = pcLoader('/Users/sjt/Dev/pc2/cache.pc2')
    a = loader.get_frame(1)
    b = loader.get_frame(23)


    
'''
file = open('/Users/sjt/Dev/pc2/cache.pc2', 'rb')


buffer = file.read(struct.calcsize(id_fmt))
buffer = file.read(struct.calcsize(header_fmt))
numPoints, startFrame, sampleRate, numSamples = struct.unpack(header_fmt, buffer)
print numPoints, startFrame, sampleRate, numSamples
idx=0
geo=[]
while 1:
    frame = []
    for i in range(numPoints):
        point = file.read(struct.calcsize('fff'))
        frame.append(struct.unpack('fff', point))
    geo.append(frame)
    if point == '':
        print 'breaking'
    break
    #print 
    #print idx
    idx+=1
    
print 'first frame', geo[0]
'''