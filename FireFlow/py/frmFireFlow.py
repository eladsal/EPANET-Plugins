import sys
from PyQt4 import QtGui, QtCore
from frmFireFlowDesigner import Ui_frmFireFlow

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class frmFireFlow(QtGui.QMainWindow, Ui_frmFireFlow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdRun, QtCore.SIGNAL("clicked()"), self.cmdRun_Clicked)
        for i in range(10):
            self.lstJunctions.addItem(str(i + 1))


    def cmdRun_Clicked(self):
        fig1 = Figure()
        ax1f1 = fig1.add_subplot(1, 1, 1)
        x = []
        y = []
        for i in range(10):
            x.append(i)
            y.append(i * i)
        ax1f1.plot(x, y, marker='o')

        minDemand = (float(self.txtToDemand.toPlainText())-float(self.txtFromDemand.toPlainText()))/float(self.txtDeltaDemand.toPlainText())

        title=self.lstJunctions.selectedItems()
        fig1.suptitle(title[0].text())
        fig1.suptitle(self.txtToDemand.toPlainText())

        ax1f1.set(xlabel='x-label', ylabel='y-label')
        ax1f1.grid(True)
        self.canvas = FigureCanvas(fig1)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = frmFireFlow()
    myapp.show()
    sys.exit(app.exec_())