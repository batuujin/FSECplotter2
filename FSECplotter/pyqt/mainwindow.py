#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FSECplotter.pyqt.widgets.logfilelist import *
from FSECplotter.pyqt.widgets.plotwidget import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.centralWidget = QtWidgets.QWidget(self)
        self.splitter = QtWidgets.QSplitter(self)

        # set list view and plot widgets
        self.treeview = LogfileListWidget(self)
        self.plotarea = PlotArea(self.treeview.model, self)

        #self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        #self.horizontalLayout.addWidget(self.treeview)
        #self.horizontalLayout.addWidget(self.plotarea)

        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.plotarea)

        #self.setCentralWidget(self.centralWidget)
        self.setCentralWidget(self.splitter)

        self.resize(1200, 600)
        self.setWindowTitle("FSEC plotter 2")

        self.createActions()
        self.createMenus()
        self.createStatusBar()

    def createActions(self):
        # open
        self.openAction = QtWidgets.QAction("Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open the new log file.")
        self.openAction.triggered.connect(self.treeview.open_file)

        # save figure
        self.saveAsAction = QtWidgets.QAction("Save fig as ...", self)
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.setStatusTip("Save current figure as new name.")
        self.saveAsAction.triggered.connect(self.plotarea.save_figure)

        # quick save fig
        self.quickSaveAction = QtWidgets.QAction("Quick save", self)
        self.quickSaveAction.setShortcut("Ctrl+S")
        self.quickSaveAction.setStatusTip("One click save.")
        self.quickSaveAction.triggered.connect(self.plotarea.quick_save_figure)

        # app quit
        self.quitAction = QtWidgets.QAction("Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit app.")
        self.quitAction.triggered.connect(QtWidgets.QApplication.closeAllWindows)

        # tools
        # fsec-ts
        self.tsAction = QtWidgets.QAction("calc Tm", self)
        self.tsAction.setStatusTip("Calc Tm from FSEC-TS data.")
        self.tsAction.triggered.connect(self.fsec_ts)

    def createMenus(self):
        # file menu
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.quickSaveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        # tool menu
        self.toolMenu = self.menuBar().addMenu("Tool")
        self.toolMenu.addAction(self.tsAction)

    def createStatusBar(self):
        self.locationLabel = QtWidgets.QLabel(" W999 ")
        self.locationLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.locationLabel.setMinimumSize(self.locationLabel.sizeHint())

        self.fomulaLabel = QtWidgets.QLabel()
        self.fomulaLabel.setIndent(3)

        self.statusBar().addWidget(self.locationLabel)
        self.statusBar().addWidget(self.fomulaLabel)

        self.updateStatusBar()

    def updateStatusBar(self):
        self.locationLabel.setText("test")
        self.fomulaLabel.setText("testtest")

    def fsec_ts(self):
        pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
