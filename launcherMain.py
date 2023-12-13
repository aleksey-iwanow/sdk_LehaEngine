import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QWidget, QGraphicsOpacityEffect
from qt.launcher import Ui_MainWindow
import sqlite3
import datetime
from os import listdir, path
from qt.create_project import Ui_Form
import subprocess


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image_back = QPixmap('icon.ico')
        self.image_back = self.image_back.scaled(self.back_image.width(), self.back_image.height())
        self.back_image.setPixmap(self.image_back)
        self.padx = self.tabWidget.x() * 2
        self.padx2 = self.tableWidget.x() * 2
        self.pady = self.tabWidget.y() * 2
        self.pady2 = self.tableWidget.y() + 45
        self.conn = None
        self.cur = None
        self.titles = []
        self.projects = []
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.7)
        opacity_effect2 = QGraphicsOpacityEffect()
        opacity_effect2.setOpacity(0.7)
        opacity_effect3 = QGraphicsOpacityEffect()
        opacity_effect3.setOpacity(0.7)
        opacity_effect4 = QGraphicsOpacityEffect()
        opacity_effect4.setOpacity(0.7)

        self.pushButton_Add.clicked.connect(self.add_project)
        self.pushButton_Add.setGraphicsEffect(opacity_effect)
        self.pushButton_Open.clicked.connect(self.open_project)
        self.pushButton_Open.setGraphicsEffect(opacity_effect2)
        self.pushButton_Remove.clicked.connect(self.delete_project)
        self.pushButton_Remove.setGraphicsEffect(opacity_effect3)
        self.pushButton_Create.clicked.connect(self.create_project)
        self.pushButton_Create.setGraphicsEffect(opacity_effect4)
        self.tableWidget.doubleClicked.connect(self.open_project)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setStyleSheet("""QHeaderView::section { background-color: rgb(48,144,145); color: rgb(0,0,0); border: 0px; font-family: 'CatV 6x12 9'; font-size: 26px; }
    QTableWidget::item:pressed,QTableWidget::item:selected{color: rgb(240,240,240); background-color: rgb(130,130,130)}; """)
        self.textBrowser.setSource(QUrl.fromLocalFile('learnHtml.html'))
        self.create_project_ex = CreateUiWidget()
        self.create_db()
        self.update_db()

        self.tabWidget.setCurrentIndex(0)

    def open_project(self):
        if self.tableWidget.currentRow() != -1:
            pr = self.projects[self.tableWidget.currentRow()]

            with open('current_scene.settings', 'w', encoding='utf-8') as settings:
                settings.write(f'{pr[0]}\n{pr[1]}\n{pr[2]}')
            subprocess.Popen(f"C:\\Users\\aleks\\PycharmProjects\\python39\\Scripts\\python.exe main.py", shell=True)

    def create_project(self):
        self.create_project_ex.show()

    def add_project(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if dirlist.strip():
            self.cur.execute("SELECT * FROM projects;")
            id_ = len(self.cur.fetchall())
            dirlist = dirlist.replace('/', '\\')
            name = dirlist.split('\\')[-1]
            scenefiles = [f for f in listdir(dirlist) if
                         path.isfile(path.join(dirlist, f)) and len(f.split('.')) > 1 and f.split('.')[-1] == 'scenes']
            runfiles = [f for f in listdir(dirlist) if
                         path.isfile(path.join(dirlist, f)) and len(f.split('.')) > 1 and f.split('.')[-2].endswith('(run)')]
            if len(scenefiles) >= 1:
                scenes_fl = scenefiles[0]
                self.add_value(id_, name,
                               {'path': dirlist,
                                'db_scenes': scenes_fl,
                                'run_file': 'None' if len(runfiles) == 0 else runfiles[0]
                                })

    def delete_project(self):
        index = self.tableWidget.currentRow()
        if index != -1:
            self.cur.execute(f"DELETE from projects where id = {index}")
            self.cur.execute(f"UPDATE projects SET id=id-1 WHERE id > {index}")
            self.conn.commit()
            self.update_db()

    def create_db(self):
        self.conn = sqlite3.connect(r'projects.db')
        conn2 = sqlite3.connect(r'projects.db')
        self.cur = self.conn.cursor()
        curr = conn2.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS projects(
           id INT PRIMARY KEY,
           project TEXT,
           datec TEXT,
           descript TEXT);
        """)
        curr.execute("""CREATE TABLE IF NOT EXISTS settings(
                   id INT PRIMARY KEY,
                   project TEXT,
                   datec TEXT,
                   descript TEXT);
                """)
        self.conn.commit()

    def add_value(self, id1, name, descript):
        now = datetime.datetime.now()
        des = ''
        for item_ in descript:
            des += f'{item_}{" " * (11 - len(item_))}-->  {descript[item_]}\n'
        print(('0' * (5 - len(str(id1))) + str(id1)))
        project = (('0' * (5 - len(str(id1))) + str(id1)), name, now.strftime("%d-%m-%Y %H:%M"), des)
        self.cur.execute("INSERT INTO projects VALUES(?, ?, ?, ?);", project)
        self.conn.commit()
        self.update_db()

    def update_db(self):
        self.cur.execute("SELECT * FROM projects;")
        results = self.cur.fetchall()
        self.tableWidget.clear()
        self.projects.clear()
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(4)
        self.titles = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        if results:

            for i, elem in enumerate(results):
                self.tableWidget.setRowHeight(i, 150)
                ls = []
                for j, val in enumerate(elem):
                    it = QTableWidgetItem(str(val))

                    it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                    ls.append(str(val))
                    self.tableWidget.setItem(i, j, it)
                    ls = [a.split('-->')[-1].strip() for a in ls[-1].split('\n') if a.split('-->')[-1].strip()]
                self.projects.append(ls)

    def resizeEvent(self, event):
        self.tabWidget.resize(self.width() - self.padx, self.height() - self.pady - 30)
        self.tableWidget.resize(self.tabWidget.width() - self.padx2, self.tabWidget.height() - self.pady2)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 300)
        self.back_image.move(self.width() // 2 - self.back_image.width() // 2, self.back_image.y())

        w = 0
        for i in range(self.tableWidget.columnCount() - 1):
            w += self.tableWidget.columnWidth(i)
        self.tableWidget.setColumnWidth(self.tableWidget.columnCount() - 1, self.tableWidget.width() - w - 2)
        self.textBrowser.resize(self.tabWidget.width(), self.tabWidget.height() - 30)


class CreateUiWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\create_project.ui', self)
        self.pushButton.clicked.connect(self.create_pr)

    def create_pr(self):
        nm = self.lineEdit_3.text()
        run = self.lineEdit_2.text()
        set = self.lineEdit_4.text()
        os.mkdir(nm)
        with open(f'{nm}\\{run}(run).py', 'w+', encoding='utf-8') as fl:
            fl.write(f'''
from framework_LehaEngine import *
# импортируем все элементы фреймворка


class Game:
    def __init__(self):
        self.win = Window([1000, 600], "{nm}")  # создание окна

        while check_run():  # цикл работает пока приложение запущено
            # заливка окна
            self.win.fill_window()
            # обновление всех объектов
            self.win.update_game_objects()
            # устанавливаем заголовок окна с текущим FPS
            set_caption("fps:" + str(round(self.win.get_fps(), 2)))
            # обновление окна
            self.win.update_window()

        # выход
        quit_app()


if __name__ == "__main__":
    game = Game()
''')

        with open(f'{nm}\\main.scene', 'w+', encoding='utf-8') as fl:
            fl.write('')

        with open(f'{nm}\\{set}.scenes', 'w+', encoding='utf-8') as fl:
            fl.write('main.scene')

        with open(f'{nm}\\fps.settings', 'w+', encoding='utf-8') as fl:
            fl.write('')

        ex.create_project_ex.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    ex.setWindowTitle('hub-LehaEngine')
    ex.setMinimumSize(1000, 600)
    ex.setWindowIcon(QIcon("images/ICONHUB.png"))
    ex.setIconSize(QSize(190, 190))
    sys.exit(app.exec_())