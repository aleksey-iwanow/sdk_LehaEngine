import os
from pyspectator import Cpu
from time import sleep
from PyQt5.QtWidgets import QFileDialog
# pyuic5 -x image_engine.ui -o image_engine.py

def getDirectory(self):  # <-----
    dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
    self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))


def getFileName(self):
    filename, filetype = QFileDialog.getOpenFileName(self,
                                                     "Выбрать файл",
                                                     ".",
                                                     "Text Files(*.txt);;JPEG Files(*.jpeg);;\
                                                     PNG Files(*.png);;GIF File(*.gif);;All Files(*)")
    self.plainTextEdit.appendHtml("<br>Выбрали файл: <b>{}</b> <br> <b>{:*^54}</b>"
                                  "".format(filename, filetype))


def getFileNames(self):
    filenames, ok = QFileDialog.getOpenFileNames(self,
                                                 "Выберите несколько файлов",
                                                 ".",
                                                 "All Files(*.*)")
    self.plainTextEdit.appendHtml("""<br>Выбрали несколько файлов: 
                                   <b>{}</b> <br> <b>{:*^80}</b>"""
                                  "".format(filenames, ok))

    folder = os.path.dirname(filenames[0])
    print("folder =", folder)
    self.plainTextEdit.appendHtml("""<br>пути файлов, которые я выбираю: 
                                   <b>{}</b> """
                                  "".format(folder))


def saveFile(self):
    filename, ok = QFileDialog.getSaveFileName(self,
                                               "Сохранить файл",
                                               ".",
                                               "All Files(*.*)")
    self.plainTextEdit.appendHtml("<br>Сохранить файл: <b>{}</b> <br> <b>{:*^54}</b>"
                                  "".format(filename, ok))