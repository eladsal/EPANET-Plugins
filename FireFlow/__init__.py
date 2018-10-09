# Name: FireFlow
# Author: Elad Salomons
# Email: selad@optiwater.com
# License: MIT

# This plugin works with EPANET MTP4r2:
# https://github.com/USEPA/SWMM-EPANET_User_Interface/releases/tag/MTP4r2

import sys
import time

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import dates
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from Externals.epanet.outputapi.ENOutputWrapper import OutputObject, ENR_node_type, ENR_link_type

plugin_name = 'FireFlow'
plugin_create_menu = True
__all__ = {"Analyze":3, "What is a plugin 1?":1, "What is a plugin 2?":11, "About":2}

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def run(session=None, choice=None):
    ltopTitle = 'FireFlow by Elad Salomons'
    title_text = session.project.title.title

    if choice is None:
        choice = 99

    ############## START FORM UI ##################
    class Ui_frmFireFlow(object):
        def setupUi(self, frmFireFlow):
            frmFireFlow.setObjectName(_fromUtf8("frmFireFlow"))
            frmFireFlow.resize(1047, 712)
            self.centralWidget = QtGui.QWidget(frmFireFlow)
            self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
            self.cmdRun = QtGui.QPushButton(self.centralWidget)
            self.cmdRun.setGeometry(QtCore.QRect(250, 570, 151, 111))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.cmdRun.setFont(font)
            self.cmdRun.setObjectName(_fromUtf8("cmdRun"))
            self.lstJunctions = QtGui.QListWidget(self.centralWidget)
            self.lstJunctions.setGeometry(QtCore.QRect(20, 50, 141, 331))
            self.lstJunctions.setObjectName(_fromUtf8("lstJunctions"))
            self.mplwindow = QtGui.QWidget(self.centralWidget)
            self.mplwindow.setGeometry(QtCore.QRect(170, 20, 851, 501))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
            self.mplwindow.setSizePolicy(sizePolicy)
            self.mplwindow.setAutoFillBackground(False)
            self.mplwindow.setObjectName(_fromUtf8("mplwindow"))
            self.mplvl = QtGui.QVBoxLayout(self.mplwindow)
            self.mplvl.setMargin(11)
            self.mplvl.setSpacing(6)
            self.mplvl.setObjectName(_fromUtf8("mplvl"))
            self.line = QtGui.QFrame(self.centralWidget)
            self.line.setGeometry(QtCore.QRect(170, 520, 851, 20))
            self.line.setFrameShape(QtGui.QFrame.HLine)
            self.line.setFrameShadow(QtGui.QFrame.Sunken)
            self.line.setObjectName(_fromUtf8("line"))
            self.txtFromDemand = QtGui.QPlainTextEdit(self.centralWidget)
            self.txtFromDemand.setGeometry(QtCore.QRect(170, 570, 61, 31))
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("Arial"))
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.txtFromDemand.setFont(font)
            self.txtFromDemand.setMouseTracking(False)
            self.txtFromDemand.setObjectName(_fromUtf8("txtFromDemand"))
            self.txtToDemand = QtGui.QPlainTextEdit(self.centralWidget)
            self.txtToDemand.setGeometry(QtCore.QRect(170, 650, 61, 31))
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("Arial"))
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.txtToDemand.setFont(font)
            self.txtToDemand.setMouseTracking(False)
            self.txtToDemand.setObjectName(_fromUtf8("txtToDemand"))
            self.txtDeltaDemand = QtGui.QPlainTextEdit(self.centralWidget)
            self.txtDeltaDemand.setGeometry(QtCore.QRect(170, 610, 61, 31))
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("Arial"))
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.txtDeltaDemand.setFont(font)
            self.txtDeltaDemand.setMouseTracking(False)
            self.txtDeltaDemand.setMidLineWidth(0)
            self.txtDeltaDemand.setObjectName(_fromUtf8("txtDeltaDemand"))
            self.label = QtGui.QLabel(self.centralWidget)
            self.label.setGeometry(QtCore.QRect(20, 20, 141, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setUnderline(True)
            font.setWeight(75)
            self.label.setFont(font)
            self.label.setObjectName(_fromUtf8("label"))
            self.label_2 = QtGui.QLabel(self.centralWidget)
            self.label_2.setGeometry(QtCore.QRect(20, 570, 161, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setUnderline(False)
            font.setWeight(50)
            self.label_2.setFont(font)
            self.label_2.setObjectName(_fromUtf8("label_2"))
            self.label_3 = QtGui.QLabel(self.centralWidget)
            self.label_3.setGeometry(QtCore.QRect(20, 610, 161, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setUnderline(False)
            font.setWeight(50)
            self.label_3.setFont(font)
            self.label_3.setObjectName(_fromUtf8("label_3"))
            self.label_4 = QtGui.QLabel(self.centralWidget)
            self.label_4.setGeometry(QtCore.QRect(20, 650, 161, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setUnderline(False)
            font.setWeight(50)
            self.label_4.setFont(font)
            self.label_4.setObjectName(_fromUtf8("label_4"))
            frmFireFlow.setCentralWidget(self.centralWidget)
            self.statusBar = QtGui.QStatusBar(frmFireFlow)
            self.statusBar.setObjectName(_fromUtf8("statusBar"))
            frmFireFlow.setStatusBar(self.statusBar)

            self.retranslateUi(frmFireFlow)
            QtCore.QMetaObject.connectSlotsByName(frmFireFlow)

        def retranslateUi(self, frmFireFlow):
            frmFireFlow.setWindowTitle(_translate("frmFireFlow", "FireFlow plugin for EPANET", None))
            self.cmdRun.setText(_translate("frmFireFlow", "Run ", None))
            self.txtFromDemand.setPlainText(_translate("frmFireFlow", "0", None))
            self.txtToDemand.setPlainText(_translate("frmFireFlow", "1200", None))
            self.txtDeltaDemand.setPlainText(_translate("frmFireFlow", "60", None))
            self.label.setText(_translate("frmFireFlow", "Junctions:", None))
            self.label_2.setText(_translate("frmFireFlow", "Minimum demand:", None))
            self.label_3.setText(_translate("frmFireFlow", "Demand step:", None))
            self.label_4.setText(_translate("frmFireFlow", "Maximum demand:", None))

    ############## END FORM UI ##################
    
    ############## START FORM ##################

    class frmFireFlow(QtGui.QMainWindow, Ui_frmFireFlow):

        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self)
            self.setupUi(self)
            QtCore.QObject.connect(self.cmdRun, QtCore.SIGNAL("clicked()"), self.cmdRun_Clicked)
            junctions_list = session.project.junctions.value[:]
            for j in junctions_list:
                self.lstJunctions.addItem(j.name)

        def cmdRun_Clicked(self):
            listitem = self.lstJunctions.selectedItems()
            junc = listitem[0].text()

            title = 'Minimum pressure vs. demand at junction ' + junc
            (d, p) = run_fire_flow(junc, float(self.txtFromDemand.toPlainText()), float(self.txtDeltaDemand.toPlainText()), float(self.txtToDemand.toPlainText()))
            fig1 = Figure()
            ax1f1 = fig1.add_subplot(1, 1, 1)
            ax1f1.plot(d, p, label='', linestyle='--', marker='o', color='b')
            fig1.suptitle(title, fontsize=14)
            ax1f1.grid(True)

            attribute = ENR_node_type.get_attribute_by_name('Pressure')
            atrn = attribute.name
            atru = attribute.units(session.output.unit_system)
            ylabel = atrn + ' (' + atru + ')'
            attribute = ENR_node_type.get_attribute_by_name('Demand')
            atrn = attribute.name
            atru = attribute.units(session.output.unit_system)
            xlabel = atrn + ' (' + atru + ')'

            ax1f1.set(xlabel=xlabel, ylabel=ylabel)

            self.canvas = FigureCanvas(fig1)
            self.mplvl.addWidget(self.canvas)
            self.canvas.draw()
            self.toolbar = NavigationToolbar(self.canvas, self.mplwindow, coordinates=True)
            self.mplvl.addWidget(self.toolbar)

    ############## END FORM ##################

    def run_fire_flow(junc, min_demand, delta_demand, max_demand):
        d = []
        p = []
        junctions_list = session.project.junctions.value[:]
        for j in junctions_list:
            if j.name == junc:
                orig_demand = j.base_demand_flow
                n = int((max_demand-min_demand)/delta_demand)
                for i in range(0, n):
                    dem = min_demand + i * delta_demand
                    d.append(dem)

                    j.base_demand_flow = dem
                    i = session.run_simulation()

                    nod = session.output.nodes[junc]
                    pres = nod.get_series(session.output, ENR_node_type.AttributePressure)
                    #txt = 'Minimum ' + atrn + ': ' + str(min(pres)) + ' ' + atru
                    p.append(min(pres))
                j.base_demand_flow = orig_demand

        return d, p

        plt.grid(True)

    # main menus
    if choice == 3:

        myapp = frmFireFlow(session)
        myapp.show()

        self.kuku=2 #adding some error so that the form would not close!!!

        pass
    if choice == 2:
        explain_text = 'This is a demo EPANET plugin\n\n' + title_text
        QMessageBox.information(None, ltopTitle, explain_text, QMessageBox.Ok)
        pass
    elif choice == 1:
        txt = '<font size = 10 color = blue >What is a Plugin?</font><br><br>'
        txt = txt + '<font size = 6 color = black >The core of EPANET should be designed to be lean and lightweight, to maximize flexibility and minimize code bloat.<br><br> <font color=blue>Plugins</font> then offer custom functions and features so that each user can tailor EPANET to their specific needs.</font><br><br>'
        txt = txt + 'Adopted from: <a href=https://codex.wordpress.org/Plugins>https://codex.wordpress.org/Plugins</a>'
        QMessageBox.information(None, ltopTitle, txt, QMessageBox.Ok)
        pass
    elif choice == 11:
        txt = '<font size = 10 color = blue >What is a Plugin?</font><br><br>'
        txt = txt +'<font size = 6 color = black >A <font color=blue>Plugin</font> is a piece of software containing a group of functions that can be added to EPANET. They can extend functionality or add new features.<br><br> EPANET <font color=blue>Plugins</font> are written in the Python programming language and integrate seamlessly with EPANET. They make it easy for users to add features to EPANET without knowing a single line of code</font><br><br>'
        txt = txt + 'Adopted from: <a href=http://www.wpbeginner.com/glossary/plugin>http://www.wpbeginner.com/glossary/plugin</a>'
        QMessageBox.information(None, ltopTitle, txt, QMessageBox.Ok)
        pass
    elif choice == 99:
        pass
    else:
        pass


