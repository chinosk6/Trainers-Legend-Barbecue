from . import main_ui, main_tab_ui, file_preview_ui

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class MainUI(main_ui.Ui_MainWindow, QWidget):
    def __init__(self):
        super(MainUI, self).__init__()

    def setupUi(self, MainWindow):
        super(MainUI, self).setupUi(MainWindow)
        # MainWindow.setFixedSize(MainWindow.rect().width(), MainWindow.rect().height())

    def show_messagebox(self, title, text, bts=QtWidgets.QMessageBox.Yes):
        QtWidgets.QMessageBox.information(self, title, text, bts)


class MainTabUI(main_tab_ui.Ui_MainWindow, QWidget):
    def __init__(self):
        super(MainTabUI, self).__init__()

    def setupUi(self, MainWindow):
        super(MainTabUI, self).setupUi(MainWindow)
        # MainWindow.setFixedSize(MainWindow.rect().width(), MainWindow.rect().height())

    def show_messagebox(self, title, text, bts=QtWidgets.QMessageBox.Yes):
        QtWidgets.QMessageBox.information(self, title, text, bts)


class FilePreviewUI(file_preview_ui.Ui_MainWindow, QWidget):
    def __init__(self):
        super(FilePreviewUI, self).__init__()

    def setupUi(self, MainWindow):
        super(FilePreviewUI, self).setupUi(MainWindow)
        # MainWindow.setFixedSize(MainWindow.rect().width(), MainWindow.rect().height())

    def show_messagebox(self, title, text, bts=QtWidgets.QMessageBox.Yes):
        QtWidgets.QMessageBox.information(self, title, text, bts)
