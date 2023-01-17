# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_tab_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1039, 800)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_file_root = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_file_root.setReadOnly(True)
        self.lineEdit_file_root.setObjectName("lineEdit_file_root")
        self.horizontalLayout_2.addWidget(self.lineEdit_file_root)
        self.pushButton_set_file_root = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_set_file_root.setObjectName("pushButton_set_file_root")
        self.horizontalLayout_2.addWidget(self.pushButton_set_file_root)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_files = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget_files.setObjectName("tabWidget_files")
        self.tab_local = QtWidgets.QWidget()
        self.tab_local.setObjectName("tab_local")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_local)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_local)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 463, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeView_local_files = QtWidgets.QTreeView(self.scrollAreaWidgetContents)
        self.treeView_local_files.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_local_files.setObjectName("treeView_local_files")
        self.verticalLayout_3.addWidget(self.treeView_local_files)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.tabWidget_files.addTab(self.tab_local, "")
        self.tab_server = QtWidgets.QWidget()
        self.tab_server.setObjectName("tab_server")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_server)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab_server)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 463, 600))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.treeWidget_server_files = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents_2)
        self.treeWidget_server_files.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_server_files.setObjectName("treeWidget_server_files")
        self.treeWidget_server_files.headerItem().setText(0, "1")
        self.verticalLayout_5.addWidget(self.treeWidget_server_files)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.scrollArea_2)
        self.tabWidget_files.addTab(self.tab_server, "")
        self.tab_different = QtWidgets.QWidget()
        self.tab_different.setObjectName("tab_different")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_different)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.tab_different)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 463, 600))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.treeWidget_different = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents_3)
        self.treeWidget_different.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_different.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_different.setObjectName("treeWidget_different")
        self.treeWidget_different.headerItem().setText(0, "1")
        self.verticalLayout_7.addWidget(self.treeWidget_different)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_6.addWidget(self.scrollArea_3)
        self.tabWidget_files.addTab(self.tab_different, "")
        self.horizontalLayout.addWidget(self.tabWidget_files)
        self.tabWidget_files_2 = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget_files_2.setObjectName("tabWidget_files_2")
        self.tab_commit = QtWidgets.QWidget()
        self.tab_commit.setObjectName("tab_commit")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_commit)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_commit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.textEdit_commit_desc = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_commit_desc.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textEdit_commit_desc.setObjectName("textEdit_commit_desc")
        self.verticalLayout_8.addWidget(self.textEdit_commit_desc)
        self.pushButton_commit = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_commit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_commit.setObjectName("pushButton_commit")
        self.verticalLayout_8.addWidget(self.pushButton_commit)
        self.verticalLayout_10.addWidget(self.groupBox_2)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.tab_commit)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 463, 433))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.treeWidget_commit = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents_4)
        self.treeWidget_commit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_commit.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_commit.setObjectName("treeWidget_commit")
        self.treeWidget_commit.headerItem().setText(0, "1")
        self.verticalLayout_9.addWidget(self.treeWidget_commit)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout_10.addWidget(self.scrollArea_4)
        self.tabWidget_files_2.addTab(self.tab_commit, "")
        self.tab_ignore_list = QtWidgets.QWidget()
        self.tab_ignore_list.setObjectName("tab_ignore_list")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_ignore_list)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.tab_ignore_list)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 463, 600))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.treeWidget_ignore = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents_5)
        self.treeWidget_ignore.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_ignore.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_ignore.setObjectName("treeWidget_ignore")
        self.treeWidget_ignore.headerItem().setText(0, "1")
        self.verticalLayout_12.addWidget(self.treeWidget_ignore)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_11.addWidget(self.scrollArea_5)
        self.tabWidget_files_2.addTab(self.tab_ignore_list, "")
        self.horizontalLayout.addWidget(self.tabWidget_files_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_log = QtWidgets.QLabel(self.centralwidget)
        self.label_log.setText("")
        self.label_log.setObjectName("label_log")
        self.horizontalLayout_3.addWidget(self.label_log)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(500, 20))
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolTip("")
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPull_From_Server = QtWidgets.QAction(MainWindow)
        self.actionPull_From_Server.setObjectName("actionPull_From_Server")
        self.actionPlease_Wait = QtWidgets.QAction(MainWindow)
        self.actionPlease_Wait.setObjectName("actionPlease_Wait")
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPull_From_Server)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlease_Wait)

        self.retranslateUi(MainWindow)
        self.tabWidget_files.setCurrentIndex(2)
        self.tabWidget_files_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit_file_root, self.pushButton_set_file_root)
        MainWindow.setTabOrder(self.pushButton_set_file_root, self.scrollArea)
        MainWindow.setTabOrder(self.scrollArea, self.treeView_local_files)
        MainWindow.setTabOrder(self.treeView_local_files, self.tabWidget_files)
        MainWindow.setTabOrder(self.tabWidget_files, self.tabWidget_files_2)
        MainWindow.setTabOrder(self.tabWidget_files_2, self.scrollArea_2)
        MainWindow.setTabOrder(self.scrollArea_2, self.treeWidget_server_files)
        MainWindow.setTabOrder(self.treeWidget_server_files, self.scrollArea_3)
        MainWindow.setTabOrder(self.scrollArea_3, self.treeWidget_different)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trainers\' Legend Barbecue"))
        self.label.setText(_translate("MainWindow", "File Root"))
        self.pushButton_set_file_root.setText(_translate("MainWindow", "set"))
        self.tabWidget_files.setTabText(self.tabWidget_files.indexOf(self.tab_local), _translate("MainWindow", "Local Files"))
        self.tabWidget_files.setTabText(self.tabWidget_files.indexOf(self.tab_server), _translate("MainWindow", "Server Files"))
        self.tabWidget_files.setTabText(self.tabWidget_files.indexOf(self.tab_different), _translate("MainWindow", "Different Files"))
        self.textEdit_commit_desc.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_commit_desc.setPlaceholderText(_translate("MainWindow", "Input your description..."))
        self.pushButton_commit.setText(_translate("MainWindow", "Commit"))
        self.tabWidget_files_2.setTabText(self.tabWidget_files_2.indexOf(self.tab_commit), _translate("MainWindow", "Commit Changes"))
        self.tabWidget_files_2.setTabText(self.tabWidget_files_2.indexOf(self.tab_ignore_list), _translate("MainWindow", "Ignore List"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionPull_From_Server.setText(_translate("MainWindow", "Pull From Server"))
        self.actionPlease_Wait.setText(_translate("MainWindow", "Synchronizing data, please wait"))
        self.actionPlease_Wait.setToolTip(_translate("MainWindow", "Synchronizing data, please wait"))
from . import msrc_rc