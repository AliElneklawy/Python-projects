from os.path import dirname
import time
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from tkinter import filedialog as fd
from tkinter.filedialog import Tk
import pyttsx3
import PyPDF2

class Ui_Dialog(object):
    def __init__(self) -> None:
        self.cur_path = dirname(__file__)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(840, 640)
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.imge = QtWidgets.QLabel(self.centralwidget)
        self.imge.setGeometry(QtCore.QRect(0, 0, 840, 640))
        self.imge.setPixmap(QtGui.QPixmap(f"{self.cur_path}\\1.jpg"))
        self.imge.setScaledContents(True)
        self.imge.setObjectName("imge")

        self.liIn = QtWidgets.QLabel(self.centralwidget)
        self.liIn.setGeometry(QtCore.QRect(30, 570, 31, 31))
        self.liIn.setPixmap(QtGui.QPixmap(f"{self.cur_path}\\linkedin-3-32.png"))
        self.liIn.setScaledContents(True)
        self.liIn.setObjectName("liIn")

        self.github = QtWidgets.QLabel(self.centralwidget)
        self.github.setGeometry(QtCore.QRect(80, 570, 31, 31))
        self.github.setPixmap(QtGui.QPixmap(f"{self.cur_path}\\github-8-32.png"))
        self.github.setScaledContents(True)
        self.github.setObjectName("github")

        Dialog.setSizeGripEnabled(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 90, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(560, 90, 93, 28))
        self.pushButton.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:white;\n"
"}\n"
"QPushButton:hover{\n"
"border: 1px solid \n"
"}\n"
"QPushButton:pressed{\n"
"border: 2px solid\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(300, 270, 91, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(260, 210, 281, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(190, 270, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(190, 330, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(190, 390, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.error1label = QtWidgets.QLabel(Dialog)
        self.error1label.setGeometry(QtCore.QRect(310, 370, 55, 16))
        self.error1label.setText("")
        self.error1label.setObjectName("error1label")
        self.error2label = QtWidgets.QLabel(Dialog)
        self.error2label.setGeometry(QtCore.QRect(310, 430, 55, 16))
        self.error2label.setText("")
        self.error2label.setObjectName("error2label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 140, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 510, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:white;\n"
"}\n"
"QPushButton:hover{\n"
"border: 1px solid \n"
"}\n"
"QPushButton:pressed{\n"
"border: 2px solid\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 150, 93, 28))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:white;\n"
"}\n"
"QPushButton:hover{\n"
"border: 1px solid \n"
"}\n"
"QPushButton:pressed{\n"
"border: 2px solid\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 330, 101, 31))
        self.lineEdit_5.setStyleSheet("QLineEdit{\n"
"border: 2px solid rgb(39, 39, 48);\n"
"border-radius: 30px;\n"
"color:black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"background-color: white;\n"
"}\n"
"QLineEdit:hover{\n"
"border: 3px solid rgb(48, 50, 62)\n"
"}\n"
"QLineEdit:focus{\n"
"border: 2px solid rgb(85, 170, 255);\n"
"}")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(250, 90, 281, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(250, 150, 281, 31))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(300, 390, 101, 31))
        self.lineEdit_8.setStyleSheet("QLineEdit{\n"
"border: 2px solid rgb(39, 39, 48);\n"
"border-radius: 30px;\n"
"color:black;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"background-color: white;\n"
"}\n"
"QLineEdit:hover{\n"
"border: 3px solid rgb(48, 50, 62)\n"
"}\n"
"QLineEdit:focus{\n"
"border: 2px solid rgb(85, 170, 255);\n"
"}")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setEnabled(False)
        self.groupBox.setGeometry(QtCore.QRect(490, 260, 301, 161))
        self.groupBox.setStyleSheet("QGroupBox#groupBox{\n"
"background-image: url(:/1/1.jpg);}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(50, 40, 241, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(90, 70, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.pagenumber = QtWidgets.QLabel(self.groupBox)
        self.pagenumber.setGeometry(QtCore.QRect(215, 70, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pagenumber.setFont(font)
        self.pagenumber.setStyleSheet("color: rgb(255, 255, 255);")
        self.pagenumber.setText("")
        self.pagenumber.setObjectName("pagenumber")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 570, 31, 31))
        self.pushButton_5.setStyleSheet("background-repeat: none;\n"
"background-image: url(:/linked in/linkedin-3-32.png);")
        self.pushButton_5.setText("")
        self.pushButton_5.setAutoRepeat(False)
        self.pushButton_5.setAutoExclusive(False)
        self.pushButton_5.setAutoRepeatDelay(300)
        self.pushButton_5.setAutoRepeatInterval(100)
        self.pushButton_5.setAutoDefault(True)
        self.pushButton_5.setDefault(False)
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(80, 570, 31, 31))
        self.pushButton_6.setStyleSheet("background-repeat: none;\n"
"background-image: url(:/github/github-8-32.png);")
        self.pushButton_6.setText("")
        self.pushButton_6.setAutoRepeat(False)
        self.pushButton_6.setAutoExclusive(False)
        self.pushButton_6.setAutoRepeatDelay(300)
        self.pushButton_6.setAutoRepeatInterval(100)
        self.pushButton_6.setAutoDefault(True)
        self.pushButton_6.setDefault(False)
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(lambda: self.browse1_clicked())
        self.pushButton_2.clicked.connect(lambda: self.browse2_clicked())
        self.pushButton_3.clicked.connect(lambda: self.initilize_thread())
        self.pushButton_6.clicked.connect(lambda: self.git_clicked())
        self.pushButton_5.clicked.connect(lambda: self.liIn_clicked())

    def git_clicked(self):
        webbrowser.open('https://github.com/AliElneklawy/')

    def liIn_clicked(self):
        webbrowser.open('https://eg.linkedin.com/in/ali-elneklawy-b690961a8?trk=public_profile_browsemap_profile-result-card_result-card_full-click')

    def browse1_clicked(self):
        self.file_path = fd.askopenfilename(title = 'Select a file', filetypes = [("pdf files", "*.pdf")])
        self.lineEdit_6.insert(self.file_path)

    def browse2_clicked(self):
        self.save_path = fd.askdirectory(title = 'Save')
        self.lineEdit_7.insert(self.save_path)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Choose PDF"))
        self.pushButton.setText(_translate("Dialog", "Browse"))
        self.comboBox.setItemText(0, _translate("Dialog", "Male voice"))
        self.comboBox.setItemText(1, _translate("Dialog", "Female voice"))
        self.label_3.setText(_translate("Dialog", "Voice"))
        self.label_4.setText(_translate("Dialog", "Start page"))
        self.label_5.setText(_translate("Dialog", "End page"))
        self.label_2.setText(_translate("Dialog", "Save"))
        self.pushButton_3.setText(_translate("Dialog", "Convert"))
        self.pushButton_2.setText(_translate("Dialog", "Browse"))
        self.progressBar.setFormat(_translate("Dialog", "%p%"))
        self.label_6.setText(_translate("Dialog", "Processing page"))

    def listen(self, message, i):
        self.progressBar.setValue(message)
        self.pagenumber.setText(str(i))
        if not self.thread.isRunning():
            self.progressBar.setValue(0)


    def initilize_thread(self):
        self.book = open(self.file_path, "rb")
        self.pdfreader = PyPDF2.PdfReader(self.book)
        self.voice = self.comboBox.currentText()
        if self.voice == "Male voice": self.voice_num = 0
        else: self.voice_num = 1
        self.thread = Thread(self.lineEdit_5, self.lineEdit_8, self.pdfreader, self.book, self.save_path, self.voice_num)
        self.thread.start()
        self.thread.signal.connect(self.listen)

class Thread(QThread):
    signal = pyqtSignal(int, int)
    def __init__(self, lineEdit_5, lineEdit_8, pdfreader, book, save_path, voice_num):
        QThread.__init__(self)
        self.lineEdit_5 = lineEdit_5
        self.lineEdit_8 = lineEdit_8
        self.pdfreader = pdfreader
        self.book = book
        self.save_path = save_path
        self.voice_num = voice_num

    def run(self):
        self.start_page = int(self.lineEdit_5.text())
        self.end = int(self.lineEdit_8.text())
        self.page_weight = 100 / (self.end - self.start_page)
        speaker = pyttsx3.init()
        speaker.setProperty("rate", 140)
        voices = speaker.getProperty('voices')
        speaker.setProperty('voice', voices[self.voice_num].id)
        for num, i in enumerate(range(self.start_page-1, self.end+1)):
                perecent = num * self.page_weight
                page = self.pdfreader.getPage(i)
                text = page.extractText().replace("\n", " ")
                speaker.runAndWait()
                speaker.save_to_file(text, f'{self.save_path}\\page {i+1}.mp3')
                self.signal.emit(int(perecent), i+1 if i < self.end else self.end)
        self.book.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
