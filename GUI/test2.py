from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #widget for dif pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 600, 600))
        
        #creating pages
        self.page_main = QtWidgets.QWidget()
        self.page_positioning = QtWidgets.QWidget()
        self.page_status = QtWidgets.QWidget()
        self.page_file_uploader = QtWidgets.QWidget()
        self.page_calibration = QtWidgets.QWidget()
        
        #putting pages on stacked widget
        self.stackedWidget.addWidget(self.page_main)
        self.stackedWidget.addWidget(self.page_positioning)
        self.stackedWidget.addWidget(self.page_status)
        self.stackedWidget.addWidget(self.page_file_uploader)
        self.stackedWidget.addWidget(self.page_calibration)
        
        #initializing page
        self.stackedWidget.setCurrentIndex(0)
        
        #declaring/positioning buttons for main menu
        self.positioning_button = QtWidgets.QPushButton(self.page_main)
        self.positioning_button.setGeometry(QtCore.QRect(210, 100, 200, 50))
        self.positioning_button.setObjectName("positioning_button")
        self.status_button = QtWidgets.QPushButton(self.page_main)
        self.status_button.setGeometry(QtCore.QRect(210, 200, 200, 50))
        self.status_button.setObjectName("status_button")
        self.file_uploader_button = QtWidgets.QPushButton(self.page_main)
        self.file_uploader_button.setGeometry(QtCore.QRect(210, 300, 200, 50))
        self.file_uploader_button.setObjectName("file_uploader_button")
        self.calibration_button = QtWidgets.QPushButton(self.page_main)
        self.calibration_button.setGeometry(QtCore.QRect(210, 400, 200, 50))
        self.calibration_button.setObjectName("calibration_button")
        self.help_button = QtWidgets.QPushButton(self.page_main)
        self.help_button.setGeometry(QtCore.QRect(525, 475, 75, 35))
        self.help_button.setObjectName("help_button")
        
        #"Back" button on all pages
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 10, 75, 35))
        self.back_button.setObjectName("back_button")
        self.back_button.setText("Back")
        
        #buttons will switch to respective pages
        self.positioning_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.status_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.file_uploader_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.calibration_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        
        #help button function 
        self.help_button.clicked.connect(self.show_help_popup)
        
        #labels, other functions
        self.title_label = QtWidgets.QLabel(self.page_positioning)
        self.title_label.setGeometry(QtCore.QRect(200, 20, 200, 50))
        self.title_label.setObjectName("title_label")
        
        self.file_selector_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.file_selector_button.setGeometry(QtCore.QRect(200, 100, 200, 50))
        self.file_selector_button.setObjectName("file_selector_button")
        self.file_selector_button.clicked.connect(self.select_file)
        
        self.check_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.check_button.setGeometry(QtCore.QRect(200, 200, 200, 50))
        self.check_button.setObjectName("check_button")
        
        self.upload_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.upload_button.setGeometry(QtCore.QRect(200, 300, 200, 50))
        self.upload_button.setObjectName("upload_button")
        
        self.start_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.start_button.setGeometry(QtCore.QRect(200, 400, 200, 50))
        self.start_button.setObjectName("start_button")
        
        self.prompt_textbox = QtWidgets.QTextEdit(self.page_file_uploader)
        self.prompt_textbox.setGeometry(QtCore.QRect(300, 500, 250, 60))
        self.prompt_textbox.setObjectName("prompt_textbox")
        self.prompt_textbox.setReadOnly(True)
        self.prompt_textbox.setPlaceholderText("Select a File")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 495, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #defining menu functions
        self.actionPositioning = QtWidgets.QAction(MainWindow)
        self.actionPositioning.setObjectName("actionPositioning")
        self.actionStatus = QtWidgets.QAction(MainWindow)
        self.actionStatus.setObjectName("actionStatus")
        self.actionFile_Uploader = QtWidgets.QAction(MainWindow)
        self.actionFile_Uploader.setObjectName("actionFile_Uploader")
        self.actionCalibration = QtWidgets.QAction(MainWindow)
        self.actionCalibration.setObjectName("actionCalibration")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMain_Menu = QtWidgets.QAction(MainWindow)
        self.actionMain_Menu.setObjectName("actionMain_Menu")

        #putting actions to functions
        self.menuFile.addAction(self.actionPositioning)
        self.menuFile.addAction(self.actionStatus)
        self.menuFile.addAction(self.actionFile_Uploader)
        self.menuFile.addAction(self.actionCalibration)
        self.menuHelp.addAction(self.actionHelp)
        
        #connecting actions to switch pages
        self.actionPositioning.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionStatus.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionFile_Uploader.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.actionCalibration.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        
        #connect help action to pages
        self.actionHelp.triggered.connect(self.show_help_popup)

        #translateing ui texts
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.positioning_button.setText(_translate("MainWindow", "Positioning"))
        self.status_button.setText(_translate("MainWindow", "Status"))
        self.file_uploader_button.setText(_translate("MainWindow", "File Uploader"))
        self.calibration_button.setText(_translate("MainWindow", "Calibration"))
        self.help_button.setText(_translate("MainWindow", "Help"))
        self.back_button.setText(_translate("MainWindow", "Back"))
        self.title_label.setText(_translate("MainWindow", "Positioning"))
        self.file_selector_button.setText(_translate("MainWindow", "File Selector"))
        self.check_button.setText(_translate("MainWindow", "Check"))
        self.upload_button.setText(_translate("MainWindow", "Upload to System"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionPositioning.setText(_translate("MainWindow", "Positioning"))
        self.actionStatus.setText(_translate("MainWindow", "Status"))
        self.actionFile_Uploader.setText(_translate("MainWindow", "File Uploader"))
        self.actionCalibration.setText(_translate("MainWindow", "Calibration"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionMain_Menu.setText(_translate("MainWindow", "Main Menu"))

    #help function popup
    def show_help_popup(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Help")
        msgBox.setText("THIS IS FOR HELP - -" 
                       "\nedit later!!~")
        msgBox.exec()

    #select file option - - - searching for .txt files
    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


#run the app
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
