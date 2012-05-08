from coral.plugin import Plugin
from PC2Importer import PC2Importer

print 'here!'
def loadPlugin():
    print 'loading!'
    plugin = Plugin("PC2ImporterPlugin")
    
    plugin.registerNode("PC2Importer", PC2Importer, tags = ["examples"], description = "An example node to jitter points.")
    
    return plugin
