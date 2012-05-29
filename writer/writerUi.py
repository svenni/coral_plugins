
from PyQt4 import QtGui, QtCore
from coral.coralUi.pluginUi import PluginUi
from coral.coralUi.nodeInspector.nodeInspector import NodeInspectorWidget

class WriteNodeInspectorWidget(NodeInspectorWidget):
    def build(self):
        NodeInspectorWidget.build(self)

        button = QtGui.QPushButton("Write", self)
        self.layout().addWidget(button)
        #self.connect(button, QtCore.SIGNAL("clicked()"), self._buttonClicked)
        button.clicked.connect(self._buttonClicked)

    def _buttonClicked(self):
        node = self.coralNode()
        try:
            node.write()
        except RuntimeError, err:
            box = QtGui.QMessageBox()
            box.setText('Error: %s' % str(err))
            box.exec_();
        #print coral.coralUi.nodeEditor.nodeEditor.NodeEditor.selectedNodes()[0].findAttribute('in0').input().parent().play(0)#))

def loadPluginUi():
    pluginUi = PluginUi("WriteNodePluginUi")
    pluginUi.registerInspectorWidget("WriteNode", WriteNodeInspectorWidget)

    return pluginUi
