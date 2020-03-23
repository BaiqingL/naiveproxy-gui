# Quick prototype of the looks for the gui written in Python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from subprocess import Popen, PIPE, STDOUT
import json, time, os, signal, requests, socket, struct

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.localProxyEntry = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localProxyEntry.sizePolicy().hasHeightForWidth())
        self.localProxyEntry.setSizePolicy(sizePolicy)
        self.localProxyEntry.setMaximumSize(QtCore.QSize(16777215, 40))
        self.localProxyEntry.setObjectName("localProxyEntry")
        self.gridLayout.addWidget(self.localProxyEntry, 3, 1, 1, 1)
        self.serverAddr = QtWidgets.QLabel(self.centralwidget)
        self.serverAddr.setObjectName("serverAddr")
        self.gridLayout.addWidget(self.serverAddr, 0, 0, 1, 1)
        self.passwd = QtWidgets.QLabel(self.centralwidget)
        self.passwd.setObjectName("passwd")
        self.gridLayout.addWidget(self.passwd, 2, 0, 1, 1)
        self.serverEntry = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverEntry.sizePolicy().hasHeightForWidth())
        self.serverEntry.setSizePolicy(sizePolicy)
        self.serverEntry.setMaximumSize(QtCore.QSize(16777215, 40))
        self.serverEntry.setObjectName("serverEntry")
        self.gridLayout.addWidget(self.serverEntry, 0, 1, 1, 1)
        self.localProxyPort = QtWidgets.QLabel(self.centralwidget)
        self.localProxyPort.setObjectName("localProxyPort")
        self.gridLayout.addWidget(self.localProxyPort, 3, 0, 1, 1)
        self.passwdEntry = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwdEntry.sizePolicy().hasHeightForWidth())
        self.passwdEntry.setSizePolicy(sizePolicy)
        self.passwdEntry.setMaximumSize(QtCore.QSize(16777215, 40))
        self.passwdEntry.setObjectName("passwdEntry")
        self.gridLayout.addWidget(self.passwdEntry, 2, 1, 1, 1)
        self.usrName = QtWidgets.QLabel(self.centralwidget)
        self.usrName.setObjectName("usrName")
        self.gridLayout.addWidget(self.usrName, 1, 0, 1, 1)
        self.userEntry = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userEntry.sizePolicy().hasHeightForWidth())
        self.userEntry.setSizePolicy(sizePolicy)
        self.userEntry.setMaximumSize(QtCore.QSize(16777215, 40))
        self.userEntry.setObjectName("userEntry")
        self.gridLayout.addWidget(self.userEntry, 1, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setObjectName("connect")
        self.gridLayout_2.addWidget(self.connect, 0, 0, 1, 1)
        self.disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect.setObjectName("disconnect")
        self.gridLayout_2.addWidget(self.disconnect, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 576, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen_Config = QtWidgets.QAction(MainWindow)
        self.actionOpen_Config.setObjectName("actionOpen_Config")
        self.actionOpen_Config.setShortcut("Ctrl+O")
        self.actionSave_Config = QtWidgets.QAction(MainWindow)
        self.actionSave_Config.setObjectName("actionSave_Config")
        self.actionSave_Config.setShortcut("Ctrl+S")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen_Config)
        self.menuFile.addAction(self.actionSave_Config)
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect all buttons with functions
        self.actionExit.triggered.connect(self.exitOnClick)
        self.actionSave_Config.triggered.connect(self.saveConfig)
        self.actionOpen_Config.triggered.connect(self.loadConfig)
        self.connect.clicked.connect(self.connectToNaive)
        self.disconnect.clicked.connect(self.disconnectFromNaive)
        self.CONNECTED = False

        # System tray
        self.trayIcon = QSystemTrayIcon(QIcon('icon.png'), parent = app)
        self.trayIcon.setToolTip("Naive Proxy")
        self.trayIcon.show()
        self.trayIcon.setContextMenu(self.menuFile)
        

        self.defaultConfig()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "naiveProxy"))
        self.localProxyEntry.setPlainText(_translate("MainWindow", "1080"))
        self.serverAddr.setText(_translate("MainWindow", "Server Address"))
        self.passwd.setText(_translate("MainWindow", "Password"))
        self.serverEntry.setPlainText(_translate("MainWindow", "example.org"))
        self.localProxyPort.setText(_translate("MainWindow", "SOCKS Port"))
        self.passwdEntry.setPlainText(_translate("MainWindow", "password"))
        self.usrName.setText(_translate("MainWindow", "Username"))
        self.userEntry.setPlainText(_translate("MainWindow", "username"))
        self.connect.setText(_translate("MainWindow", "Connect"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Config.setText(_translate("MainWindow", "Open Config"))
        self.actionSave_Config.setText(_translate("MainWindow", "Save Config"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def overrideConfig(self):
        serverAddress = self.serverEntry.toPlainText()
        username = self.userEntry.toPlainText()
        password = self.passwdEntry.toPlainText()
        SOCKSPort = self.localProxyEntry.toPlainText()
        with open("config.json", 'w') as output:
            json.dump({
            "listen": "socks://127.0.0.1:" + SOCKSPort,
            "proxy":"https://"+username+":"+password+"@"+serverAddress,
            "padding" : True
            }, output)
    
    def saveConfig(self):
        serverAddress = self.serverEntry.toPlainText()
        username = self.userEntry.toPlainText()
        password = self.passwdEntry.toPlainText()
        SOCKSPort = self.localProxyEntry.toPlainText()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Save Naive Configuration","","Naive Configuration File (*.json)", "")
        if(fileName):
            with open(fileName, 'w') as output:
                json.dump({
                "listen": "socks://127.0.0.1:" + SOCKSPort,
                "proxy":"https://"+username+":"+password+"@"+serverAddress,
                "padding" : True
                }, output)

    def defaultConfig(self):
        try:
            with open("config.json") as f:
                data = json.load(f)
            listen = data['listen']
            proxy = data['proxy'][8:]
            self.serverEntry.setPlainText(proxy[proxy.rfind('@')+1:])
            self.userEntry.setPlainText(proxy[:proxy.find(':')])
            self.passwdEntry.setPlainText(proxy[proxy.find(self.userEntry.toPlainText()) + len(self.userEntry.toPlainText()) + 1:proxy.rfind('@')])
            self.localProxyEntry.setPlainText(listen[-4:])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please place in proper config.json")
            msg.setWindowTitle("Error")
            msg.exec_()
            quit()

    def loadConfig(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Open Naive Configuration","","Naive Configuration File (*.json)", "")
        try:
            with open(fileName) as f:
                data = json.load(f)
            listen = data['listen']
            proxy = data['proxy'][8:]
            self.serverEntry.setPlainText(proxy[proxy.rfind('@')+1:])
            self.userEntry.setPlainText(proxy[:proxy.find(':')])
            self.passwdEntry.setPlainText(proxy[proxy.find(self.userEntry.toPlainText()) + len(self.userEntry.toPlainText()) + 1:proxy.rfind('@')])
            self.localProxyEntry.setPlainText(listen[-4:])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Not a valid configuration")
            msg.setWindowTitle("Error")
            msg.exec_()
    
    def testConnection(self):
        self.progressBar.setProperty("value", 50)
        try:
            proxyPort = int(self.localProxyEntry.toPlainText())
            proxies = {'https': "socks5://localhost:"+str(proxyPort)}
            try:
                response = int(requests.get('https://skylantern.social/success', proxies=proxies).content.decode('utf-8'))
                self.progressBar.setProperty("value", 70)
            except:
                self.p.kill()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Credential Error")
                msg.setWindowTitle("Wrong username / password")
                msg.exec_()
                self.progressBar.setProperty("value", 0)
                return
            if(response):
                self.CONNECTED = True
                self.progressBar.setProperty("value", 100)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Naive connected")
                msg.setWindowTitle("Connection Established")
                msg.exec_()
            else:
                self.p.kill()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Credential Error")
                msg.setWindowTitle("Wrong username / password")
                msg.exec_()
                self.progressBar.setProperty("value", 0)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Naive not connected")
            msg.setWindowTitle("No connection")
            msg.exec_()
            self.progressBar.setProperty("value", 0)

    def connectToNaive(self):
        if self.CONNECTED:
            msg = QMessageBox()
            msg.setText("Reconnect with current credentials?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg = msg.exec()

            if msg == QMessageBox.Yes:
                self.progressBar.setProperty("value", 0)
                self.p.kill()
                pass
            else:
                return
        self.overrideConfig()
        CURRENT_OS = os.name
        if CURRENT_OS == "nt":
            args = ["naive.exe", "config.json"]
            self.p = Popen(["naive.exe", "config.json"], stderr=STDOUT, stdout=PIPE)
            self.testConnection()
        elif CURRENT_OS == "postfix":
            args = ["naive", "config.json"]
            self.p = Popen(["naive.exe", "config.json"], stderr=STDOUT, stdout=PIPE)
            self.testConnection()
    
    def disconnectFromNaive(self):
        if self.CONNECTED:
            self.p.kill()
            self.progressBar.setProperty("value", 0)
            self.CONNECTED = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Naive disconnected")
            msg.setWindowTitle("Connection Terminated")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Naive not connected")
            msg.setWindowTitle("No connection")
            msg.exec_()

    def exitOnClick(self):
        if(self.CONNECTED):
            self.p.kill()
        quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
