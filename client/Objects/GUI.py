#GUI

from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtCore import Qt
import os
import json
from subprocess import Popen
from Client import Client
from DownloadManager import DownloadManager
import webbrowser

class GUI(QWidget):
    def __init__(self, title, url, local_minecraft_dir, server_host, server_port, skip_files, extra_buttons,mc_server_details,mc_files_only_download):
        super().__init__()
        self.setWindowTitle(title)

        self.local_minecraft_folder = local_minecraft_dir
        self.user_settings_file = "user_settings.json"
        self.launcher_path = None

        self.default_launcher_value = os.path.expanduser("~") + os.sep + "AppData"+os.sep+"Roaming"+os.sep+".minecraft"+os.sep+"minecraft launcher"+os.sep+"Minecraft Launcher.exe"
        self.client = Client(server_host, server_port, local_minecraft_dir, skip_files,mc_files_only_download)
        self.dm = DownloadManager(self.client)

        layout = QGridLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        browser = QWebView()
        browser.setUrl(QUrl(url))
        browser.setMaximumHeight(10000)

        self.startButton = QPushButton("Start")

        extra_buttons_widgets = []

        for button_id in range(len(extra_buttons)):
            button = extra_buttons[button_id]
            extra_buttons_widgets.append(QPushButton(button["name"]))
            if button["type"] == "link":
                url = button["url"][:]
                extra_buttons_widgets[-1].clicked.connect(lambda e=False,url=url: webbrowser.open(url))

        clipboard = QApplication.clipboard()

        labelA = QPushButton(mc_server_details)
        labelA.clicked.connect(lambda: (clipboard.setText(mc_server_details)==92 or labelA.setText("Copied!")))

        configButton = QPushButton("Config")

        configButton.clicked.connect(self.fix_minecraft_folder)
        self.startButton.clicked.connect(self.start_minecraft)
        self.startButton.setEnabled(False)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)

        self.progressBar.setFormat("Checking For Updates")
        self.progressBar.setStyleSheet("color:black;font-weight:bold;")
        self.progressBar.setAlignment(Qt.AlignCenter)



        layout.addWidget(browser,0,0,10,10)
        layout.addWidget(self.startButton,0,10)

        btnPos = 1
        for button in extra_buttons_widgets:
            layout.addWidget(button, btnPos, 10)
            btnPos += 1


        layout.addWidget(labelA,7,10)
        layout.addWidget(configButton,9,10)
        layout.addWidget(self.progressBar,10,0,1,11)

        self.dm.progress.connect(self.update_progress_bar_value)
        self.dm.message.connect(self.update_progress_bar_text)
        self.dm.enableStart.connect(self.enableStart_tracker)
        self.show()

        if not os.path.isfile(self.user_settings_file):
            self.ask_for_config_fix()
        else:
            try:
                user_settings = json.loads(open(self.user_settings_file).read())
                self.launcher_path = user_settings["launcher_path"]
            except:
                self.ask_for_config_fix()

        self.dm.setTerminationEnabled(False)
        self.dm.start()
    def enableStart_tracker(self,val):
        self.startButton.setEnabled(val)

    def update_progress_bar_value(self,current,max):
        self.progressBar.setValue(current)
        self.progressBar.setMaximum(max)

    def update_progress_bar_text(self,text):
        self.progressBar.setFormat(text)

    def ask_for_config_fix(self):
        buttonReply = QMessageBox.question(self, 'Configuration Needed',
                                           "Minecraft Launcher Path Is Not Set, Would you like ti set the path to the minecraft launcher folder now?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.fix_minecraft_folder()


    def fix_minecraft_folder(self):
        file = QFileDialog.getOpenFileName(self, "Select Minecraft Launcher",self.default_launcher_value,"*.exe")[0]
        if file == "":
            return

        user_settings = {
            "launcher_path":file
        }

        serializedSettings = json.dumps(user_settings)
        fl = open(self.user_settings_file,"w")
        fl.write(serializedSettings)
        fl.close()

        self.launcher_path = file


    def start_minecraft(self):
        if self.launcher_path == None:
            buttonReply = QMessageBox.question(self, 'Configuration Needed',
                                               "Minecraft Launcher Path Is Not Set, Would you like ti set the path to the minecraft launcher folder now?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.fix_minecraft_folder()
            else:
                return

            if self.launcher_path == "":
                return

        if os.path.isfile(self.launcher_path):
            Popen([self.launcher_path, "--workDir="+os.getcwd()+os.sep+self.local_minecraft_folder])
            QCoreApplication.instance().quit()
        else:
            buttonReply = QMessageBox.question(self, 'Configuration Needed',
                                               "Unable to find minecraft launcher, would you like to set the path now?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.fix_minecraft_folder()
                self.start_minecraft()
            else:
                return









if __name__ == "__main__":
    app = QApplication([])
    g = GUI("sdadsa","300x600","https://www.riverbankcomputing.com/static/Docs/PyQt5/introduction.html#module-PyQt5.QtWebEngineWidgets")
    app.exec_()
