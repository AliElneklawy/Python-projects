from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from tkinter import filedialog as fd
from tkinter.filedialog import  Tk
import os

class Ui_MainWindow(object):

    def __init__(self) -> None:
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        self.file_path = None
        self.folderfield = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 312)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.folderfield = QtWidgets.QLineEdit(self.centralwidget)
        self.folderfield.setGeometry(QtCore.QRect(220, 70, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.folderfield.setFont(font)
        self.folderfield.setObjectName("folderfield")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(84, 70, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.bbrowse = QtWidgets.QPushButton(self.centralwidget)
        self.bbrowse.setGeometry(QtCore.QRect(550, 70, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(12)
        self.bbrowse.setFont(font)
        self.bbrowse.setObjectName("bbrowse")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 150, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.extensionfiled = QtWidgets.QLineEdit(self.centralwidget)
        self.extensionfiled.setGeometry(QtCore.QRect(220, 140, 113, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.extensionfiled.setFont(font)
        self.extensionfiled.setObjectName("extensionfiled")
        self.bdelete = QtWidgets.QPushButton(self.centralwidget)
        self.bdelete.setStyleSheet("QPushButton::hover{"
            "background-color: red;"
            "}")
        self.bdelete.setGeometry(QtCore.QRect(322, 210, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.bdelete.setFont(font)
        self.bdelete.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.bdelete.setObjectName("bdelete")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.bbrowse.clicked.connect(lambda: self.bbrowse_clicked())
        self.bdelete.clicked.connect(lambda: self.bdelete_clicked())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Choose folder"))
        self.bbrowse.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", "Extension"))
        self.bdelete.setText(_translate("MainWindow", "Delete"))

    def bbrowse_clicked(self):
        self.file_path = fd.askdirectory(title = "Choose folder")
        self.folderfield.insert(self.file_path)

    def bdelete_clicked(self):
        msg = QMessageBox()
        if self.extensionfiled.text() == "":
            msg.setText("Please enter file extension")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid")
            msg.exec_()
        try:
            files_in_directory = os.listdir(self.folderfield.text())
            filtered_files = [file for file in files_in_directory if file.endswith(f".{self.extensionfiled.text()}")]
            for file in filtered_files:
                path_to_file = os.path.join(self.folderfield.text(), file)
                os.remove(path_to_file)
        except (FileNotFoundError, OSError):
            msg.setText("Folder doesn't exist")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
