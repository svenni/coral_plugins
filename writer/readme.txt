Can write out data as pc2 or just text dump of values.
NOTE: I learned how to write pc 2 caches in python from Matt Ebb's script for blender:http://mattebb.com/projects/bpython/pointcache/export_pc2.py and I thnak him for that.

To use it you have to either plug point data into the points attr or some float value into 'data' (this is super-useful ;) ). Connect a Time node to the 'frame' plug and set some reasonable values for 'startFrame' and 'endFrame'. Oh, don't forget to specify a path. Then just hit 'write' and the node will go from 'startFrame' to 'endFrame' and update the value in the Time node and write out the resulting 'points' (or floats) to disk.

