from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #different pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 600, 600))
        
        #create pages
        self.page_main = QtWidgets.QWidget()
        self.page_positioning = QtWidgets.QWidget()
        self.page_status = QtWidgets.QWidget()
        self.page_file_uploader = QtWidgets.QWidget()
        self.page_calibration = QtWidgets.QWidget()
        
        #pages for buttons
        self.stackedWidget.addWidget(self.page_main)
        self.stackedWidget.addWidget(self.page_positioning)
        self.stackedWidget.addWidget(self.page_status)
        self.stackedWidget.addWidget(self.page_file_uploader)
        self.stackedWidget.addWidget(self.page_calibration)
        
        #initializing
        self.stackedWidget.setCurrentIndex(0)
        
        #file uploader apge
        self.file_selector_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.file_selector_button.setGeometry(QtCore.QRect(200, 100, 200, 50))
        self.file_selector_button.setObjectName("file_selector_button")
        self.file_selector_button.setText("Select File")
        self.file_selector_button.clicked.connect(self.select_file)

        self.check_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.check_button.setGeometry(QtCore.QRect(200, 200, 200, 50))
        self.check_button.setObjectName("check_button")
        self.check_button.setText("Check")
        self.check_button.clicked.connect(lambda: self.update_file_uploader_display("Checked"))

        self.upload_button = QtWidgets.QPushButton(self.page_file_uploader)
        self.upload_button.setGeometry(QtCore.QRect(200, 300, 200, 50))
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setText("Upload")
        self.upload_button.clicked.connect(lambda: self.update_file_uploader_display("Uploaded"))

        self.prompt_textbox = QtWidgets.QTextEdit(self.page_file_uploader)
        self.prompt_textbox.setGeometry(QtCore.QRect(50, 400, 500, 100))
        self.prompt_textbox.setObjectName("prompt_textbox")
        self.prompt_textbox.setReadOnly(True)
        self.prompt_textbox.setPlaceholderText("Select a file to analyze")
        
        #positioning page
        self.up_button = QtWidgets.QPushButton(self.page_positioning)
        self.up_button.setGeometry(QtCore.QRect(250, 150, 100, 50))
        self.up_button.setObjectName("up_button")
        self.up_button.setText("Up")
        self.up_button.clicked.connect(lambda: self.update_position("Up"))

        self.down_button = QtWidgets.QPushButton(self.page_positioning)
        self.down_button.setGeometry(QtCore.QRect(250, 250, 100, 50))
        self.down_button.setObjectName("down_button")
        self.down_button.setText("Down")
        self.down_button.clicked.connect(lambda: self.update_position("Down"))

        self.position_textbox = QtWidgets.QLineEdit(self.page_positioning)
        self.position_textbox.setGeometry(QtCore.QRect(200, 350, 200, 50))
        self.position_textbox.setObjectName("position_textbox")
        self.position_textbox.setReadOnly(True)
        self.position_textbox.setPlaceholderText("Current Position")
        
        #start and stop buttons
        pages = [self.page_positioning, self.page_status, self.page_file_uploader, self.page_calibration]
        for i, page in enumerate(pages):
            start_button = QtWidgets.QPushButton(page)
            start_button.setGeometry(QtCore.QRect(400, 500, 100, 50))
            start_button.setText("Start")
            start_button.clicked.connect(lambda _, b=i: self.update_start_stop_display("Start", b))

            stop_button = QtWidgets.QPushButton(page)
            stop_button.setGeometry(QtCore.QRect(510, 500, 100, 50))
            stop_button.setText("Stop")
            stop_button.clicked.connect(lambda _, b=i: self.update_start_stop_display("Stop", b))

            display_box = QtWidgets.QLineEdit(page)
            display_box.setGeometry(QtCore.QRect(50, 500, 340, 50))
            display_box.setReadOnly(True)
            display_box.setObjectName(f"display_box_{i}")
        
        #creating main menu buttons/positions
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
        
        #back button
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 10, 75, 35))
        self.back_button.setObjectName("back_button")
        self.back_button.setText("Back")
        
        #button actions (main menu)
        self.positioning_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.status_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.file_uploader_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.calibration_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        
        #help button funct.
        self.help_button.clicked.connect(self.show_help_popup)
        
        #functions
        self.title_label = QtWidgets.QLabel(self.page_positioning)
        self.title_label.setGeometry(QtCore.QRect(200, 20, 200, 50))
        self.title_label.setObjectName("title_label")
        
        #placeholder function
        self.placeholder_function()  # Example of where to place other placeholder functions
        
        MainWindow.setCentralWidget(self.centralwidget)

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

    def show_help_popup(self):
        # Help function popup
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Help")
        msgBox.setText("Help information for the application.")
        msgBox.exec()

    def placeholder_function(self):
        # Placeholder functions for additional functionality
        pass
    
    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select File", "", "Text Files (*.txt)", options=options)
        if fileName:
            self.prompt_textbox.setText(f"Selected file: {fileName}")
            
    def update_position(self, direction):
        # Update the position display based on the button pressed
        self.position_textbox.setText(direction)
        
    def update_file_uploader_display(self, text):
        self.prompt_textbox.setText(text)
        
    def update_start_stop_display(self, text, page_index):
        display_box = self.stackedWidget.widget(page_index).findChild(QtWidgets.QLineEdit, f"display_box_{page_index}")
        if display_box:
            display_box.setText(text)

#run app
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
