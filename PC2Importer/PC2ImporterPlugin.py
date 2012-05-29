from coral.plugin import Plugin
from PC2Importer import PC2Importer

def loadPlugin():
    plugin = Plugin("PC2ImporterPlugin")
    
    plugin.registerNode("PC2Importer", PC2Importer, tags = ["sjtNodes"], description = "An example node to jitter points.")
    
    return plugin
