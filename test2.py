from PyQt5 import QtCore, QtWidgets

STYLESHEET = '''QTreeWidget {border:None} 
    QTreeWidget::Item{
        border-bottom:2px solid black;
        color: rgba(255,255,255,255);
    }
    QTreeView{
        alternate-background-color: rgba(170,170,170,255);
        background: rgba(211,211,211,255);
    }'''


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        s = super(StyledItemDelegate, self).sizeHint(option, index)
        if index.parent().isValid():
            s.setHeight(40)
        else:
            s.setHeight(80)
        return s


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.treeWidget = QtWidgets.QTreeWidget()
        delegate = StyledItemDelegate(self.treeWidget)
        self.treeWidget.setItemDelegate(delegate)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setStyleSheet(STYLESHEET)
        self.treeWidget.setProperty("houdiniStyle", True)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.treeWidget)
        for i in range(5):
            it = QtWidgets.QTreeWidgetItem(["parent {}".format(i)])
            self.treeWidget.addTopLevelItem(it)
            for j in range(5):
                child = QtWidgets.QTreeWidgetItem(["children {}{}".format(i, j)])
                it.addChild(child)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())