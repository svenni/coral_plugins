
from PyQt4 import QtGui, QtCore
from coral.coralUi.pluginUi import PluginUi
from coral.coralUi.nodeInspector.nodeInspector import NodeInspectorWidget

class PC2ImporterInspectorWidget(NodeInspectorWidget):
    def build(self):

        NodeInspectorWidget.build(self)
        button = QtGui.QPushButton("Say Hi!", self)
        
        self.layout().addWidget(button)
        print self.layout().count()
        print self.layout().itemAt(0).widget().getText()
        self.connect(button, QtCore.SIGNAL("clicked()"), self._buttonClicked)

    def _buttonClicked(self):
        print "EITTHVAD!"

def loadPluginUi():
    pluginUi = PluginUi("PC2ImporterPluginUi")
    pluginUi.registerInspectorWidget("PC2Importer", PC2ImporterInspectorWidget)

    return pluginUi
