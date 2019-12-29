#import threading
import time
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadManager(QThread):
    progress = pyqtSignal((int, int))
    message = pyqtSignal(str)
    enableStart = pyqtSignal(bool)

    def __init__(self,client):
        super(DownloadManager,self).__init__()

        self.client = client


    def run(self):
        time.sleep(5)
        i = 0
        completed = False
        while i < 3:
            try:
                c = self.client
                self.message.emit("Connecting To Server")
                c.connect()

                self.message.emit("Checking Files")
                update_files = c.get_updates(self.progress)
                self.message.emit("Performing Upgrade")
                print("Performing_Update")
                c.do_upgrades(update_files, self.progress)
                print("Update Compileted")
                self.message.emit("Completed")
                self.enableStart.emit(True)
                completed = True
            except WindowsError:
                i += 1
                self.message.emit("Failed To Connect, Trying Again...")
                time.sleep(5)
                completed = False
            except:
                i += 1
                self.message.emit("Update Failed, Trying Again...")
                time.sleep(5)
                completed = False

            if completed:
                break

        if not completed:
            self.message.emit("Update Failed!!! Try Again Later")
            self.enableStart.emit(True)

