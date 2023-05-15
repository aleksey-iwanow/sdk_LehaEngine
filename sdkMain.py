import os
import shutil
import sys
import subprocess
from os import listdir, path, getcwd
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5 import uic, QtGui, QtMultimedia  # Импортируем uic
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QAction

from qt.create import Ui_Form
from qt.addComponent import Ui_Form as Add_Form
from qt.settings import Ui_Form as Settings_Form
from qt.textRedactor import Ui_MainWindow as Redactor_Form
from FramelessWindow import FramelessWindow
from pydub import AudioSegment

from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QWidget, QFileDialog, \
    QGraphicsOpacityEffect, QLabel
from PyQt5 import QtCore, QtWidgets
from qt.textRedactor import Ui_MainWindow
import subprocess as sp
import ctypes
import platform, socket, re, uuid, json, psutil, logging


def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


commands = {
    'cd': ['cd',
           'Переходит по указанной директории'],
    'systeminfo': ['systeminfo',
                   'Системная информация'],
    'clear': ['clear',
              'Очищает консоль'],
    'help': ['help',
             'Выводит все команды'],
    'ls': ['ls',
           'Выводит все файлы и папки в текущей директории'],
    'nano': ['nano',
             'текстовый редактор'],
    'ls.dirs': ['ls.dirs',
                'Выводит только папки в текущей директории'],
    'ls.files': ['ls.files',
                 'Выводит только файлы в текущей директории'],
    'system': ['system',
               'Выполняет системную команду'],
}

errorFormat = '<font color="red">{}</font>'
warningFormat = '<font color="orange">{}</font>'
validFormat = '<font color="green">{}</font>'
darkgreenFormat = '<font color="#80CF0C";">{}</font>'
whiteFormat = '<font color="#A1A1A1">{}</font>'
titleFormat = '<font style="color:#010101; background-color: #1F4D3C">{}</font>'


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()


class TerminalWidget:
    def __init__(self, pushButton, label_2, textEdit, pushButton_2, pushButton_3, pushButton_4, lineEdit, pushButtonEnter, label):
        self.pushButton, self.label_2, self.textEdit, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.lineEdit, self.pushButtonEnter, self.label = \
            pushButton, label_2, textEdit, pushButton_2, pushButton_3, pushButton_4, lineEdit, pushButtonEnter, label

        self.timer = QTimer()
        self.timer.setInterval(503)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()

        self.pushButton.clicked.connect(self.close_nano)
        self.lineEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.textEdit.setStyleSheet(f"border: 2px solid #121C16; "
                                    f"background: #162e22")
        self.textEdit.setReadOnly(True)
        self.pushButton_2.clicked.connect(self.terminate_file)
        self.pushButton_4.clicked.connect(self.save_file)
        self.pushButton_3.clicked.connect(self.open_file_1)

        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton.hide()
        self.pushButtonEnter.clicked.connect(self.send_command)
        self.fl = ""
        self.fl_is_run = False
        self.function_set_txt = None
        self.label.setText(f'┌{os.getcwd()}┐')
        self.set_cursor()
        self.text_main = f'''<span style="color:green;">НАЧАЛО РАБОТЫ!</span><br>'''

    # слот для таймера
    def timeStep(self):
        pass

    def send_command(self):
        cp = os.getcwd()
        def set_txt(out=""):
            self.textEdit.setText(
                f'{self.text_main}{titleFormat.format(cp + "~")} {command}<br><span style="background-color: #AB274F">#</span> {out if out else output}')
            self.text_main = self.textEdit.toHtml()
            self.set_cursor()
            self.label.setText(f'┌{os.getcwd()}┐')

        if not self.function_set_txt:
            self.function_set_txt = set_txt

        command = self.lineEdit.text()
        if not command:
            return
        output = ""
        fcm = command.split()[0]
        fcms = command.split()[0].split('.')
        arg = command[len(fcm) + 1:]

        ch = "<font color='#162e22'>&nbsp;</font>"
        path_ = ''

        if fcm in commands:
            if fcm == commands['cd'][0]:
                try:
                    os.chdir(arg if ":" in arg else (os.getcwd() + '\\' + arg))
                    output = os.getcwd()
                except Exception as ex:
                    output += errorFormat.format(ex)
            if fcm == commands['system'][0]:
                try:
                    data = subprocess.check_output(arg)
                    print(data.decode(encoding='ascii'))

                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcm == commands['clear'][0]:
                self.text_main = ''
                output = 'Консоль очищена.'
            elif fcm == commands['nano'][0]:
                try:
                    path_ = arg if ":" in arg else (os.getcwd() + '\\' + arg)

                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcms[0] == commands['ls'][0]:
                onlyfiles = ''
                if len(fcms) > 1:
                    if fcms[1] == 'DIRS':
                        onlyfiles = [f for f in listdir(cp) if not os.path.isfile(os.path.join(cp, f))]
                    elif fcms[1] == 'FILES':
                        onlyfiles = [f for f in listdir(cp) if os.path.isfile(os.path.join(cp, f))]
                else:
                    # if os.path.isfile(os.path.join(cp, f))
                    onlyfiles = [f for f in listdir(cp)]

                output = f",{ch * 2}".join(onlyfiles)
            elif fcm == commands['help'][0]:
                try:
                    for i in commands:
                        name = f"{i}:"
                        ln = 20 - len(name)
                        output += '<br>' + f'{validFormat.format(name)}{ln * ch}{darkgreenFormat.format(commands[i][1])}</span>'
                except Exception as ex:
                    output += errorFormat.format(ex)
            elif fcm == commands['systeminfo'][0]:
                inf = json.loads(get_system_info())

                for i in inf:
                    name = f"{i}:"
                    ln = 20 - len(name)
                    output += f'<br>{validFormat.format(name)}{ln * ch}{darkgreenFormat.format(inf[i])}</span>'

        else:
            output = warningFormat.format("Команда не обнаружена! (help - список команд)")

        if path_:
            ex = self.active_nano(path_)
            if ex:
                set_txt(ex)
        else:
            set_txt()

    def active_nano(self, pt):
        try:
            self.open_file(pt)
            self.textEdit.setReadOnly(False)
            self.lineEdit.hide()
            self.pushButtonEnter.hide()
            self.pushButton_4.show()
            self.pushButton_3.show()
            self.pushButton_2.show()
            self.pushButton.show()
            return ""
        except Exception as ex:
            print(ex)
            return errorFormat.format(ex)

    def close_nano(self):
        self.textEdit.setReadOnly(True)
        self.lineEdit.show()
        self.pushButtonEnter.show()
        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton.hide()
        self.function_set_txt("nano exit")
        return ""

    def set_cursor(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def run_file(self):
        if self.fl:
            self.fl_is_run = True
            os.system(f'python {self.fl}')

    def open_file_1(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "Text Files(*.txt);;Python File(*.py);;All Files(*)")
        if filename.strip():
            self.open_file(filename)

    def save_file(self):
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл",
                                                   ".",
                                                   "All Files(*.*)")
        if ok:
            with open(filename, 'w', encoding="utf-8") as fl:
                fl.write(self.textEdit.toPlainText())

    def terminate_file(self):
        if self.fl_is_run:
            self.fl_is_run = False
            ext_proc = sp.Popen(['python', self.fl.split('\\')[-1]])
            sp.Popen.terminate(ext_proc)

    def open_file(self, file_):
        fl = sys.argv[0]
        fl = fl.replace('/', '\\')
        nm = file_.split("\\")[-1]
        self.fl = ""
        if file_ != fl:
            if file_.endswith('.py') or file_.endswith('.pyr'):
                self.fl = file_
            self.label.setText(f'┌{nm}┐')

            with open(file_, 'r', encoding="utf-8") as fl__:
                tx = fl__.read()
                self.textEdit.setPlainText(tx)
                self.textEdit.setText(f'<a style="color:#95CBBF;">{self.textEdit.toHtml()}</a>')

                count = len(tx.split("\n"))
                self.label_2.setText(f'┌{count}┐')
        self.set_cursor()

    def key_press_event_term(self, e):
        count = len(self.textEdit.toPlainText().split("\n"))
        self.label_2.setText(f'┌{count}┐')
        if e.key() == Qt.Key_Escape:
            self.send_command()


StyleSheet = """
/* Панель заголовка */
TitleBar {
    background-color: rgb(54, 157, 180);
}
/* Минимизировать кнопку `Максимальное выключение` Общий фон по умолчанию */
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonMy {
    border: none;
    background-color: rgb(54, 157, 180);
}
/* Зависание */
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}
#buttonMy:hover {
    color: white;
    background-color: green;   /* rgb(232, 17, 35) */
}
/* Мышь удерживать */
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""


def booled(arg):
    if not arg or str(arg).lower().strip() == 'false' or str(arg).lower().strip() == 'none':
        return False
    else:
        return True


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\sdk.ui', self)

        with open('current_scene.settings', 'r', encoding='utf-8') as settings:
            sett = settings.read().split('\n')
            pr_p = sett[0]
            scenes = sett[1]
            rn_fl = sett[2]
        self.sizeWindow = [1707, 1067]

        self.lines_center = []
        self.but_vec_resize = 0
        self.player = Player()
        self.project_path = pr_p

        self.icon_obj = QIcon(QPixmap('./images/icon_obj.png'))
        self.icon_func = QIcon(QPixmap('./images/settingsIcon.png'))
        self.icon_script = QIcon(QPixmap('./images/script_icon.png'))
        self.pixmap_func = QPixmap('./images/settingsIcon.png')
        self.icon_warning = QIcon(QPixmap('./images/icon_warning.png'))
        self.icon_sett = QIcon(QPixmap('./images/icon_func.png'))
        self.icon_image = QIcon(QPixmap('./images/image_icon.png'))
        self.icon_folder = QIcon(QPixmap('./images/folder_icon.png'))
        self.icon_act_exit = QIcon(QPixmap('./images/exit-full-screen.png'))
        self.icon_act_create = QIcon(QPixmap('./images/free-icon-dead-blow-hammer-1105682.png'))
        self.icon_act_run = QIcon(QPixmap('./images/free-icon-check-mark-4225683.png'))
        self.icon_act_update = QIcon(QPixmap('./images/icons8-параметры-синхронизации-96.png'))
        self.icon_act_save = QIcon(QPixmap('./images/icons8-сохранить-48.png'))
        self.icon_act_settings = QIcon(QPixmap('./images/icons8-шестерни-80.png'))
        self.icon_doc = QIcon(QPixmap('./images/icon_doc.png'))
        self.image_doc = QtGui.QPixmap('./images/icon_doc.png')
        self.audio_icon = QtGui.QPixmap('./images/icon_audio.png')
        self.audio_icon2 = QIcon(QPixmap('./images/icon_audio.png'))
        self.icon_py = QIcon(QPixmap('./images/icon_py2.png'))
        self.icon_py2 = QIcon(QPixmap('./images/python_icon1.png'))
        self.image_py = QtGui.QPixmap('./images/icon_py2.png')
        self.project_file = self.project_path + '\\' + scenes
        self.game_ = open(self.project_file).read().split('\n')
        self.game_ = [self.project_path + '\\' + a for a in self.game_]
        self.path_ = self.game_[0]
        self.add_tab_scene(0)

        self.widget0 = self.findChild(QtWidgets.QWidget, f'widget_0')

        self.list_game_objects = []
        self.delta_list_game_objects = []
        self.widgets_ = []
        self.items_tree = []
        self.list_line_edits_for_gm = []
        self.list_grid_layout_files = []
        self.list_components = []
        self.list_components_values = []
        self.height_grid_layout_proj = 0
        self.current_file_index = 0
        self.current_file_path = ''

        self.scale_factor = 1.0

        self.sizeStartWindow = self.size()
        self.sizeTabInspector = [self.width() - self.tabWidgetInspector.x(), self.height() - self.tabWidgetInspector.y()]
        self.sizeProjectTree = [self.width() - self.treeWidget_Project.x(), self.height() - self.treeWidget_Project.y()]
        self.sizeProjectTreeTit1 = [self.width() - self.label_6.x(), self.height() - self.label_6.y()]
        self.sizeProjectTreeTit2 = [self.width() - self.pushButtonUpdateproject.x(), self.height() - self.pushButtonUpdateproject.y()]
        self.sizeProjectTreeTit3 = [self.width() - self.radioButton.x(), self.height() - self.radioButton.y()]
        self.sizeProjectTreeTit4 = [self.width() - self.radioButton_2.x(), self.height() - self.radioButton_2.y()]
        self.sizeButSave = [self.width() - self.pushButtonSave.x(), self.height() - self.pushButtonSave.y()]
        self.sizeButDelete = [self.width() - self.pushButtonDelete.x(), self.height() - self.pushButtonDelete.y()]
        self.sizeButPlus = [self.width() - self.pushButtonPlus.x(), self.height() - self.pushButtonPlus.y()]
        self.sizeDebug = [self.width() - self.listWidget.x(), self.height() - self.listWidget.y()]
        self.sizeDebugTit2 = [self.width() - self.pushButtonClear.x(), self.height() - self.pushButtonClear.y()]
        self.sizeScrollArea = [self.width() - self.scrollArea.width(), self.height() - self.scrollArea.y()]
        self.sizeScrollArea2 = [self.width() - self.scrollArea_2.width(), self.height() - self.scrollArea_2.height()]
        self.sizeTreeWidget = self.height() - self.treeWidget.height()
        self.sizelistWidget = self.width() - self.listWidget.width()
        self.hTabInspector = self.height() - self.tabWidgetInspector.height()
        self.sizeScrollAreaTit = [0, self.height() - self.label_Project.y()]
        self.sizeTabW = self.size() - self.tabWidget.size()
        self.index_gm_now = -9999999
        self.index_sel_gm = -9999999

        self.old_sel_item = []

        self.treeWidget.setHeaderHidden(True)
        self.treeWidget_Project.setHeaderHidden(True)
        self.list_settings_parameters = ['image       => ',
                                         'pos         => ',
                                         'size        => ',
                                         'angle       => ',
                                         'opacity     => ',
                                         'collision   => ',
                                         'add to list => ']

        self.font_main = self.treeWidget.font()
        self.gridLayout.setAlignment(Qt.AlignTop)
        self.gridLayout_files.setAlignment(Qt.AlignTop)

        self.cam_pos = [0, 0]
        self.cam_pos_now = [0, 0]
        self.old_pos_mouse = [0, 0]
        self.button_click = ''
        self.lineEditPosX.setText(str(self.cam_pos_now[0]))
        self.lineEditPosY.setText(str(self.cam_pos_now[1]))

        self.create_ex = CreateWidget()
        self.add_ex = AddComponentWidget()
        self.set_ex = SettingsWidget()
        self.redactor_ex = TextRedactorWidget()
        self.f_ex = CreateFolderWidget()
        self.paint_ex = PaintWidget()

        self.current_path_project = ''

        self.labels_in_scene = []
        self.labels_in_scene_debugs = []
        self.copy_game_object = []

        self.run_file = f'{self.project_path}\\{rn_fl}'
        self.image_background = 'None'
        self.path_opening = ""
        self.list_exceptions = ['venv', '.idea', '__pycache__']
        self.movement = 10
        self.r1, self.r2 = 0, 0
        self.r1obj, self.r2obj = 0, 0
        self.main_k_szs = 0
        self.mouse_pos = [0, 0]
        self.lineEditMove.setText(str(self.movement))

        self.update_()
        self.lineEditScale.setText(str(self.scale_factor))

        self.update_scene()
        self.but_for_object = QLabel(self.widget0)
        self.but_for_object.resize(15, 15)
        self.but_for_object.setStyleSheet("background-color: #FF7E0A")
        self.but_for_object2 = QLabel(self.widget0)
        self.but_for_object2.resize(15, 15)
        self.but_for_object2.setStyleSheet("background-color: #FF7E0A")
        self.but_for_object3 = QLabel(self.widget0)
        self.but_for_object3.resize(15, 15)
        self.but_for_object3.setStyleSheet("background-color: #FF7E0A")
        self.but_for_object4 = QLabel(self.widget0)
        self.but_for_object4.resize(15, 15)
        self.but_for_object4.setStyleSheet("background-color: #FF7E0A")

        self.but_for_object.hide()
        self.but_for_object2.hide()
        self.but_for_object3.hide()
        self.but_for_object4.hide()
        self.send_debug_message(f'общее количество обьектов => {len(self.list_game_objects)}')

        self.menuFile.setTitle("#File")
        self.menuEdit.setTitle("#Edit")
        self.menuHelp.setTitle("#Help")

        self.actionGameObject.triggered.connect(self.create_new_game_object)
        self.actionRun.triggered.connect(self.run_engine)
        self.actionUpdate_scene.triggered.connect(self.update_scene)
        self.actionSave_scene.triggered.connect(self.save_scene)
        self.actionExit.triggered.connect(self.exit)
        self.actionSettings.triggered.connect(self.active_setting_panel)
        self.actionOpen_project.triggered.connect(self.open_project)

        self.actionExit.setIcon(self.icon_act_exit)
        self.menuCreate.setIcon(self.icon_act_create)
        self.actionRun.setIcon(self.icon_act_run)
        self.actionUpdate_scene.setIcon(self.icon_act_update)
        self.actionSave_scene.setIcon(self.icon_act_save)
        self.actionSettings.setIcon(self.icon_act_settings)

        self.pushButtonSave.clicked.connect(self.save_gm)
        self.pushButtonSave_4.clicked.connect(self.update_scene)
        self.pushButtonDelete.clicked.connect(self.delete)
        self.pushButtonPlus.clicked.connect(self.add_)
        self.pushButtonUpdateproject.clicked.connect(self.update_tree_widget_project)
        self.pushButtonCopy.clicked.connect(self.copy_gm)
        self.pushButtonPaste.clicked.connect(self.paste_gm)
        self.pushButtonClear.clicked.connect(self.listWidget.clear)
        self.radioButton.clicked.connect(self.update_tree_widget_project)
        self.radioButton_2.clicked.connect(self.update_tree_widget_project)

        w.titleBar.signalButtonMy.connect(self.active_setting_panel)

        self.pushButtonPlus.hide()
        self.pushButtonSave.hide()
        self.pushButtonDelete.hide()
        self.choose_object = False
        self.run_bool = True
        # self.check_click()
        self.update_tree_widget_project()
        self.treeWidget_Project.setIconSize(QSize(30, 30))

        self.scrollArea.setStyleSheet(f"background-color: rgb(102, 126, 120, 90)")
        self.scrollArea_2.setStyleSheet("background-color: rgb(102, 126, 120, 0);}")

        '''self.timer = QTimer()
        self.timer.setInterval(1000)  # 100мс
        self.timer.timeout.connect(lambda : self.get_message())
        self.timer.start()'''
        tree_wid_style = """QTreeView::branch:open:has-children:!has-siblings{image:url(images/minus-square-outlined-button.png)}
                                          QTreeView::branch:closed:has-children:!has-siblings{image:url(images/free-icon-instagram-post-5705604.png)}
                                          QTreeView::branch:open:has-children{image:url(images/minus-square-outlined-button.png)}
                                          QTreeView::branch:closed:has-children{image:url(images/free-icon-instagram-post-5705604.png)}
                                          QTreeView::branch:open:{image:url(images/minus-square-outlined-button.png)}
                                          QTreeView::branch:closed:{image:url(images/free-icon-instagram-post-5705604.png)}
                                          ;"""

        self.treeWidget_Project.setStyleSheet(tree_wid_style)
        self.treeWidget.setStyleSheet(tree_wid_style)

        self.update_statistic()
        self.tabWidget.setCurrentIndex(0)
        self.components_all = ['Animation', 'Function', 'Script', 'Collider', 'Rigidbody', 'UI', 'Button', 'Text', 'Particle system', 'Audio source', 'Color box', 'Activeself']
        self.create_component('Animation', ['int=frames', 'list:frames', 'bool=looping', 'int=speed(ms)', 'bool=active', 'bool=deleted', 'string=tag'])
        self.create_component('Function', ['bool=update', 'string=function'])
        self.create_component('Script', ['bool=update', 'string=script', 'int=arguments', 'list:arguments'])
        self.create_component('Rigidbody', ['bool=gravity', 'int=power', 'bool=active'])
        self.create_component('Audio source', ['string=sound_track', 'int=volume', 'bool=active', 'bool=looping', 'string=type'])
        self.create_component('Color box', ['string=color'])
        self.create_component('Text', ['string=text', 'int=sizef', 'string=colorf'])
        self.create_component('Button', ['string=function', 'string=color_click', 'string=color_loc'])
        self.create_component('UI', ['bool=active'])
        self.create_component('Activeself', ['bool=active'])
        self.create_component('Particle system', ['bool=active', 'bool=looping', 'int=count', 'int=time'])
        self.create_component('Collider', ['int=x', 'int=y', 'int=width', 'int=height'])
        self.dockWidget.setTitleBarWidget(QWidget(self.dockWidget))
        self.dockWidget_open.setTitleBarWidget(QWidget(self.dockWidget_open))
        self.dockWidget_Project.setTitleBarWidget(QWidget(self.dockWidget_Project))
        self.dockWidget_inspector.setTitleBarWidget(QWidget(self.dockWidget_inspector))
        self.dockWidget_debug.setTitleBarWidget(QWidget(self.dockWidget_inspector))

        self.dockWidget.installEventFilter(self)
        self.dockWidget_open.installEventFilter(self)
        self.dockWidget_Project.installEventFilter(self)
        self.dockWidget_inspector.installEventFilter(self)
        self.dockWidget_debug.installEventFilter(self)

        self.twidget = TerminalWidget(self.pushButton, self.label_3, self.textEdit, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.lineEdit, self.pushButtonEnter, self.label_4)

    def update_statistic(self):
        self.graphicsView.clear()

        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView.setLabel('left', 'Fps', units='f')
        self.graphicsView.setLabel('bottom', 'Time', units='sec')
        self.graphicsView.setWindowTitle('pyqtgraph plot')
        # self.graphicsView.setBackground('')
        with open(f'{self.project_path}/fps.settings') as fl:
            fps_ = [int(e) for e in fl.readlines()]
            self.graphicsView.plot([i for i in range(len(fps_))], fps_, pen='r')

    def set_current_scene(self, el):
        self.path_ = el
        self.tabWidget.setCurrentIndex(0)
        self.widget0 = self.findChild(QtWidgets.QWidget, f'widget_{0}')
        self.zeroing_values()

        self.update_()
        self.update_scene()
        self.clear_inspector()

    def exit(self):
        w.close()

    def open_project(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")

        if dirlist.strip():
            onlyfiles = [f for f in listdir(dirlist) if path.isfile(path.join(dirlist, f)) and len(f.split('.')) > 1 and f.split('.')[-1] == 'scenes']
            scenes_fl = onlyfiles[0]

            dirlist = dirlist.replace('/', '\\')
            print(getcwd())
            with open('current_scene.settings', 'w', encoding='utf-8') as settings:
                settings.write(f'{dirlist}\n{scenes_fl}\nNone')
            subprocess.Popen(f"python {getcwd()}\\sdkMain.py", shell=True)

    def zeroing_values(self):
        self.cam_pos = [0, 0]
        self.cam_pos_now = [0, 0]
        self.old_pos_mouse = [0, 0]
        self.index_gm_now = -9999999
        self.index_sel_gm = -9999999
        self.lineEditPosY.setText('0')
        self.lineEditPosX.setText('0')

    def add_tab_scene(self, index):
        wid = QWidget(self.tab_scene)
        wid.resize(self.tabWidget.width(), self.tabWidget.height() - 30)
        wid.move(0, 0)
        line_center_x = QtWidgets.QLabel(wid)
        line_center_y = QtWidgets.QLabel(wid)
        line_center_x.setStyleSheet(f"border: 0px solid blue; "
                                    f"background-color: #636363;")
        line_center_y.setStyleSheet(f"border: 0px solid blue; "
                                    f"background-color: #636363;")
        line_up = QtWidgets.QLabel(wid)
        line_down = QtWidgets.QLabel(wid)
        line_left = QtWidgets.QLabel(wid)
        line_right = QtWidgets.QLabel(wid)
        line_left.setStyleSheet(f"border: 0px solid blue; "
                                f"background-color: #636363;")
        line_right.setStyleSheet(f"border: 0px solid blue; "
                                 f"background-color: #636363;")
        line_down.setStyleSheet(f"border: 0px solid blue; "
                                f"background-color: #636363;")
        line_up.setStyleSheet(f"border: 0px solid blue; "
                              f"background-color: #636363;")
        self.lines_center.append([line_center_x, line_center_y, line_up, line_down, line_left, line_right])
        wid.setObjectName(f'widget_{index}')

    def create_scene(self):
        nm = f'gamescene{len(self.game_)}.scene'
        with open(self.project_file, 'a', encoding='utf-8') as fl:
            fl.write(f'\n{nm}')

        my_file = open(f'{self.project_path}\\{nm}', "w+")
        my_file.write("")
        my_file.close()

        self.game_.append(f'{self.project_path}\\{nm}')

    def update_(self):
        if self.path_ != '':
            self.list_game_objects.clear()
            with open(self.path_, 'r') as fl:
                tx = fl.read()
                if tx.strip('\n') != '':
                    h = tx.split('(~&~)')
                    for i in h[0].split('~'):
                        elements = i.split('\n')
                        elements = [a for a in elements if a]

                        if len(elements) > 1:
                            index_childes = 9 if len(elements) > 9 else 8
                            ch = elements[index_childes][1:-2]
                            if ch:
                                pass  # отложено -=-=-=-=-=-=-=-=-=-=-=

                            self.list_game_objects.append(elements)

                self.treeWidget.clicked.connect(self.upd)
                self.treeWidget.setIconSize(QSize(30, 30))
        self.update_treeview()

    def update_tree_widget_project(self):
        self.treeWidget_Project.clear()
        item1 = QTreeWidgetItem(self.treeWidget_Project)
        item1.setText(0, self.project_path.split('\\')[-1] + f"   ~   ({self.project_path})")
        item1.setIcon(0, self.icon_folder)
        item1.setForeground(0, QtGui.QBrush(QtGui.QColor("#FF9142")))
        item1.setExpanded(True)
        item1.setFont(0, QFont('Times', 10))
        self.treeWidget_Project.setCurrentItem(item1)
        self.rec_dir(f'{self.project_path}', item1, self.radioButton.isChecked())
        self.update_project_opening()
        self.treeWidget_Project.clicked.connect(self.update_project_opening)

    def update_project_opening(self):
        tx = self.treeWidget_Project.currentItem().text(0)
        path_ = tx.split('~')[-1].strip()[1:-1]
        nm = self.project_path.split('\\')[-1]
        p_copy = path_[path_.find(nm) - 1:]
        p = p_copy.split("\\")
        self.current_path_project = path_

        if path.isdir(path_):
            self.height_grid_layout_proj = 0
            self.label_Project.setText(f'┌({" -> ".join(p)[4:]})┐')
            for l in self.list_grid_layout_files:
                self.gridLayout_files.removeWidget(l)
            self.list_grid_layout_files.clear()
            col = 0
            row = 0
            self.path_opening = path_
            old_h = [0, 0]
            for fl in listdir(path_):
                if not path.isdir(f'{path_}\\{fl}'):
                    lbl = ClickedLabel(self)
                    pix = QtGui.QPixmap(f'{path_}\\{fl}') if self.file_is_image(f'{path_}\\{fl}') \
                        else self.image_py if fl.endswith('py') or fl.endswith('pyr') else QPixmap('images/settings (1).png') if fl.endswith('.scene') or fl.endswith('.scenes') or fl.endswith('.settings') else self.image_doc
                    if fl.endswith('ogg') or fl.endswith('mp3') or fl.endswith('.wav'):
                        pix = self.audio_icon
                    if pix.width() > pix.height():
                        k = pix.height() / pix.width()
                        pix = pix.scaled(110, int(110 * k))
                    else:
                        try:
                            k = pix.width() / pix.height()
                            pix = pix.scaled(int(110 * k), 110)
                        except ZeroDivisionError:
                            pass
                    lbl.setPixmap(pix)
                    lbl.setAutoFillBackground(True)
                    lbl.setStyleSheet("background-color: #96a69e")

                    lbl.resize(110, 110)
                    lbl.clicked.connect(lambda x=f'{path_}\\{fl}', y=len(self.list_grid_layout_files): self.open_file_in_project(x, y))
                    lbl2 = QtWidgets.QLineEdit(self)
                    lbl2.setStyleSheet("background-color: #96a69e")
                    lbl2.setAutoFillBackground(True)
                    lbl2.setText(fl)
                    lbl2.setMinimumWidth(30)
                    lbl2.setFont(QFont('OCR A Extended', 8))
                    lbl2.resize(110, 30)
                    lbl2.setReadOnly(True)

                    self.gridLayout_files.addWidget(lbl, col, row)
                    self.gridLayout_files.addWidget(lbl2, col + 1, row)
                    self.list_grid_layout_files.append(lbl)
                    self.list_grid_layout_files.append(lbl2)
                    row += 1
                    if row == 6:
                        bl = QtWidgets.QLabel(self)
                        bl.setText('____')
                        bl.setStyleSheet("color: #e6fff3")
                        bl.resize(54, 30)
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(0.0)
                        bl.setGraphicsEffect(opacity_effect)
                        self.gridLayout_files.addWidget(bl, col, row + 1)
                        self.list_grid_layout_files.append(bl)
                        col += 2
                        row = 0
                        self.height_grid_layout_proj += \
                            lbl.height() + lbl2.height() + self.gridLayout_files.verticalSpacing() * 2
                    old_h = [lbl.height(), lbl2.height()]
            if row != 0:
                self.height_grid_layout_proj += \
                    old_h[0] + old_h[1] + self.gridLayout_files.verticalSpacing() * 2
            if not col:
                for i in range(6 - row):
                    pix = QtGui.QPixmap(f'icon_main.ico')
                    pix = pix.scaled(110, 110)
                    lbl1 = QLabel(self)
                    lbl1.setPixmap(pix)
                    lbl1.setAutoFillBackground(True)
                    lbl1.resize(110, 110)
                    opacity_effect = QGraphicsOpacityEffect()
                    opacity_effect.setOpacity(0.0)
                    lbl1.setGraphicsEffect(opacity_effect)

                    self.gridLayout_files.addWidget(lbl1, col, row + i)
                    self.list_grid_layout_files.append(lbl1)
                bl = QtWidgets.QLabel(self)
                bl.setText('____')
                bl.setStyleSheet("color: #e6fff3")
                bl.resize(54, 30)
                opacity_effect = QGraphicsOpacityEffect()
                opacity_effect.setOpacity(0.0)
                bl.setGraphicsEffect(opacity_effect)
                self.gridLayout_files.addWidget(bl, col, 7)
                self.list_grid_layout_files.append(bl)

            self.frame.setMinimumHeight(self.height_grid_layout_proj)

    def file_is_text(self, path_):
        try:
            with open(path_, 'r', encoding='utf-8') as file:
                text = file.read()

            return True
        except UnicodeDecodeError:
            return False

    def file_is_audio(self, path_):
        sp = path_.split('.')[-1]
        if sp == "mp3" or sp == "wav" or sp == "ogg":
            return True
        return False

    def open_file_in_project(self, path_, index_):
        if self.current_file_path and self.current_file_path == path_:
            self.current_file_path = ''
            self.current_file_index = -9999999
            if len(path_.split('.')) > 1 and path_.split('.')[-1] == 'scene':
                for i in self.game_:
                    if path_ == i and self.path_ != path_:
                        self.set_current_scene(i)
                return

            if self.file_is_text(path_):
                self.redactor_ex.hide()
                self.redactor_ex.show()
                self.redactor_ex.open_file(path_)
            elif self.file_is_image(path_):
                self.paint_ex.show()
                self.paint_ex.open_image(path_)
            elif self.file_is_audio(path_):
                self.player.show()
                self.player.load_mp3(path_)
        else:
            self.current_file_path = path_
            self.current_file_index = index_
            self.list_grid_layout_files[index_].setStyleSheet("background-color: #A1D4BD")
            self.list_grid_layout_files[index_ + 1].setStyleSheet("background-color: #A1D4BD")

    def move_object_of_index(self, idx):
        gm = self.list_game_objects[self.index_gm_now]
        name = gm[0]
        self.list_game_objects.remove(gm)
        self.list_game_objects.insert(idx, gm)

        self.send_debug_message(f'GameObject <{name}> перемещен\n new_index = {idx}')

    def move_ui_of_index(self, idx):
        gm = self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)]
        name = gm[0]
        self.list_ui_objects.remove(gm)
        self.list_ui_objects.insert(idx, gm)

        self.send_debug_message(f'GameObject <{name}> перемещен\n new_index = {idx}')

    def file_is_image(self, p):
        try:
            im = Image.open(f'{p}')
            return True
        except IOError:
            return False

    def rec_dir(self, path_, item_, ischeck):
        for i in listdir(path_):
            if i not in self.list_exceptions:
                if (ischeck and path.isdir(f'{path_}\\{i}')) or not ischeck:
                    icon_ = self.icon_py if i.endswith('.py') or i.endswith('.pyr') else QIcon('images/settings (1).png') if i.endswith('.scene') or i.endswith('.scenes') or i.endswith('.settings') else self.icon_doc
                    try:
                        im = Image.open(f'{path_}\\{i}')
                        icon_ = self.icon_image
                    except IOError:
                        pass
                    if i.endswith('.ogg') or i.endswith('.mp3') or i.endswith('.wav'):
                        icon_ = self.audio_icon2

                    item1 = QTreeWidgetItem(item_)
                    item1.setText(0, f'{i}')
                    item1.setIcon(0, self.icon_folder if path.isdir(f'{path_}\\{i}') else icon_)
                    item1.setExpanded(False)
                    item1.setFont(0, QFont('Times', 10))
                    ii2 = i.split('.')

                    if path.isdir(f'{path_}\\{i}'):
                        item1.setText(0, f'{i}   ~   ({path_}\\{i})')
                        item1.setForeground(0, QtGui.QBrush(QtGui.QColor("#FF9142")))
                        self.rec_dir(f'{path_}\\{i}', item1, ischeck)
                    elif len(ii2) > 1 and (ii2[1] == 'py' or ii2[1] == 'pyr'):
                        item1.setForeground(0, QtGui.QBrush(QtGui.QColor("#00F5E5")))
                    elif len(ii2) > 1 and (ii2[1] == 'scene' or ii2[1] == 'scenes'):
                        item1.setForeground(0, QtGui.QBrush(QtGui.QColor("#FCFCFC")))

    def eventFilter(self, obj, event):
        if obj in [self.dockWidget_debug, self.dockWidget_Project, self.dockWidget, self.dockWidget_inspector, self.dockWidget_open] and event.type() == QEvent.Resize:
            self.treeWidget_Project.resize(self.dockWidget_open.width() - 10, self.dockWidget_open.height() - 30)
            self.scrollArea.resize(self.dockWidget_Project.width(), self.dockWidget_Project.height() - 30)
            w0 = self.findChild(QtWidgets.QWidget, f'widget_0')
            w0.resize(self.width() - self.dockWidget.width() - self.dockWidget_inspector.width() - 30, self.height() - 120 - self.dockWidget_open.height())
            self.tabWidget.resize(self.width() - self.dockWidget.width() - self.dockWidget_inspector.width() - 30, self.height() - 120 - self.dockWidget_open.height())
            self.graphicsView.resize(self.tabWidget.width(), self.tabWidget.height() - 40 - self.graphicsView.y())
            self.treeWidget.resize(self.dockWidget.width() - 10, self.dockWidget.height() - 30)
            self.listWidget.resize(self.dockWidget_debug.width() - 10, self.dockWidget_debug.height() - 50)
            self.tabWidgetDebug.resize(self.dockWidget_debug.width() - 10, self.dockWidget_debug.height())
            self.tabWidgetInspector.resize(self.dockWidget_inspector.width() - 10, self.dockWidget_inspector.height())
            self.scrollArea_2.resize(self.dockWidget_inspector.width() - 10, self.dockWidget_inspector.height() - 90)
            self.pushButtonSave.move(self.pushButtonSave.x(), self.tabWidgetInspector.height() - 70)
            self.pushButtonPlus.move(self.pushButtonPlus.x(), self.tabWidgetInspector.height() - 70)
            self.pushButtonDelete.move(self.pushButtonDelete.x(), self.tabWidgetInspector.height() - 70)
            self.groupBoxSceneSett.resize(self.tabWidget.width(), self.groupBoxSceneSett.height())

            self.textEdit.resize(self.dockWidget_debug.width() - 10, self.dockWidget_debug.height() - 30 - self.lineEdit.height() - self.label_3.height())
            self.lineEdit.resize(self.dockWidget_debug.width() - 10 - self.pushButtonEnter.width(), self.lineEdit.height())
            self.lineEdit.move(0, self.dockWidget_debug.height() - self.lineEdit.height() - 30)
            self.pushButtonEnter.move(self.dockWidget_debug.width() - 10 - self.pushButtonEnter.width(), self.dockWidget_debug.height() - self.pushButtonEnter.height() - 30)

        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        self.update_lines_center()
        # self.treeWidget_Project.move(self.treeWidget_Project.x(), self.height() - self.sizeProjectTree[1])
        # self.label_6.move(self.label_6.x(), self.height() - self.sizeProjectTreeTit1[1])
        # self.pushButtonUpdateproject.move(self.pushButtonUpdateproject.x(), self.height() - self.sizeProjectTreeTit2[1])
        # self.radioButton.move(self.radioButton.x(), self.height() - self.sizeProjectTreeTit3[1])
        # self.radioButton_2.move(self.radioButton_2.x(), self.height() - self.sizeProjectTreeTit4[1])

        '''self.tabWidgetInspector.move(self.width() - self.sizeTabInspector[0], self.tabWidgetInspector.y())

        self.listWidget.move(self.listWidget.x(), self.height() - self.sizeDebug[1])
        self.label_3.move(self.label_3.x(), self.height() - self.sizeDebugTit1[1])

        self.pushButtonSave.move(self.pushButtonSave.x(), self.height() - self.sizeButSave[1])
        self.pushButtonDelete.move(self.pushButtonDelete.x(), self.height() - self.sizeButDelete[1])
        self.pushButtonPlus.move(self.pushButtonPlus.x(), self.height() - self.sizeButPlus[1])

        self.pushButtonClear.move(self.pushButtonClear.x(), self.height() - self.sizeDebugTit2[1])
        # self.scrollArea.move(self.scrollArea.x(), self.height() - self.sizeScrollArea[1])
        self.scrollArea_2.resize(self.scrollArea_2.width(), self.height() - self.sizeScrollArea2[1])
        self.listWidget.resize(self.width() - self.sizelistWidget, self.listWidget.height())
        # self.label_Project.move(self.label_Project.x(), self.height() - self.sizeScrollAreaTit[1])
        self.tabWidget.resize(self.size() - self.sizeTabW)
        # self.treeWidget.resize(self.treeWidget.width(), self.height() - self.sizeTreeWidget)
        self.tabWidgetInspector.resize(self.tabWidgetInspector.width(), self.height() - self.hTabInspector)
        w0 = self.findChild(QtWidgets.QWidget, f'widget_0')
        w0.resize(self.size() - self.sizeTabW)

        self.graphicsView.resize(self.tabWidget.width(), self.tabWidget.height() - 40 - self.graphicsView.y())
        self.groupBoxSceneSett.resize(self.width() - 18, self.groupBoxSceneSett.height())'''

    def wheelEvent(self, event):
        x_pos, y_pos = event.x(), event.y() - 30
        if self.widget0 and self.tabWidget.x() + 4 + self.dockWidget.width() < x_pos < self.tabWidget.x() + 4 + self.dockWidget.width() + self.widget0.width() and \
                self.tabWidget.y() < y_pos < self.tabWidget.y() + self.widget0.height():
            delta = event.angleDelta().y()
            if self.scale_factor > 0:
                if delta < 0:
                    self.scale_factor = round(self.scale_factor - 0.1, 2)
            if self.scale_factor < 100:
                if delta > 0:
                    self.scale_factor = round(self.scale_factor + 0.1, 2)
            self.lineEditScale.setText(str(self.scale_factor))
            self.update_scene()

    def collision_object(self, x, y, w, h, x_pos, y_pos):
        if x + self.tabWidget.x() + 4 + self.dockWidget.width() < x_pos < x + self.tabWidget.x() + 4 + self.dockWidget.width() + w and y + self.tabWidget.y() + 30 < y_pos < y + self.tabWidget.y() + 30 + h:
            return True
        return False

    def remove_component_(self, num):
        num = int(num)
        ls_components = self.list_game_objects[self.index_gm_now][8].split('$')
        ls_components.remove(ls_components[num])
        self.list_game_objects[self.index_gm_now][8] = '$'.join(ls_components)
        self.update_inspector(self.index_gm_now)

    def clicked_rm_but(self, but, index):
        but.clicked.connect(lambda: self.remove_component_(index))

    def update_components_in_inspector(self, el):
        ls_components = [[i.split('^;^') for i in a.split('^,^')] for a in el.split('$')]
        self.list_components_values.clear()
        index_main = 0
        for list_values in ls_components:
            if len(list_values) > 1:
                lbl2 = QtWidgets.QLabel(self)
                lbl2.setText(f'{str(list_values[0]).replace("[", "").replace("]", "")[1:-1]} =>')
                lbl2.resize(200, 70)
                self.font_main.setPointSize(12)
                lbl2.setFont(self.font_main)
                lbl2.setStyleSheet("color: #ceecde")

                wid1 = QtWidgets.QGroupBox(self)
                but = QtWidgets.QPushButton(wid1)

                but.move(5, 5)
                but.resize(100, 25)
                but.setText('remove')
                but.setStyleSheet('''QPushButton
                                    {
                                        background-color: rgb(70,118,66,190);
                                        color: rgb(255,255,255)
                                    }
                                    
                                    QPushButton:hover
                                    {
                                        background-color: rgb(40,88,36,190);
                                        color: rgb(255,255,255)
                                    }''')
                self.clicked_rm_but(but, ls_components.index(list_values))
                ls_vl = []
                pad_y = 35
                for i in list_values[1]:
                    sp_ = i.split(':')
                    if len(sp_) <= 1:
                        lbl3 = QtWidgets.QLabel(wid1)
                        tx_ = i.split("=")[1] if len(i.split("=")) > 1 else i
                        lbl3.setText(f' {tx_}' + ' ' * (12 - len(tx_)) + '= ')
                        lbl3.resize(200, 30)

                        lbl3.move(0, pad_y)

                        self.font_main.setPointSize(8)
                        lbl3.setFont(self.font_main)
                        lbl3.setStyleSheet("color: #ceecde")

                        ln_ed3 = QtWidgets.QLineEdit(wid1)
                        ln_ed3.setText('0' if list_values[2][list_values[1].index(i)].lower() == 'none' and i.split('=')[0] == 'int' else ('False' if list_values[2][list_values[1].index(i)].lower() == 'none' and i.split('=')[0] == 'bool' else list_values[2][list_values[1].index(i)]))
                        ln_ed3.resize(200, 30)
                        ln_ed3.move(200, pad_y)
                        pad_y += 30
                        ln_ed3.setStyleSheet("background-color: #77D4C5")
                        self.font_main.setPointSize(8)
                        ln_ed3.setFont(self.font_main)

                        ls_vl.append(ln_ed3)
                    else:
                        curr_count = ['', 0]
                        for i2 in list_values[1]:
                            try:
                                sp_cop = i2.split('=')[1]
                            except IndexError:
                                sp_cop = i2
                            if sp_cop == sp_[1]:
                                curr_count = (list_values[2][list_values[1].index(i2)], list_values[1].index(i2))
                        ls_ed = []
                        curr_count = curr_count if curr_count[0].isdigit() else ['0', curr_count[1]]
                        pad_y += 5
                        for j in range(int(curr_count[0])):
                            ln_ed_ = QtWidgets.QLineEdit(wid1)
                            txt_ = list_values[2][list_values[1].index(i)].split('*&*')
                            if len(txt_) > j and txt_[j] and txt_[j].lower() != 'none':
                                ln_ed_.setText(txt_[j])
                            else:
                                ln_ed_.setText('None')
                            ln_ed_.resize(380, 30)
                            ln_ed_.move(20, pad_y)
                            pad_y += 30
                            ln_ed_.setStyleSheet("background-color: #77D4C5")
                            self.font_main.setPointSize(8)
                            ln_ed_.setFont(self.font_main)

                            ls_ed.append(ln_ed_)
                        pad_y += 5
                        ls_vl.append(ls_ed)

                self.list_components_values.append(ls_vl)
                wid1.setMinimumHeight(pad_y + 5)

                self.widgets_.append(lbl2)
                self.widgets_.append(wid1)
                index_main+=1

    def create_component(self, name, list_values):
        self.list_components.append([name, list_values, ['None' for a in list_values]])

    def mousePressEvent(self, event):
        self.button_click = str(event.button())
        self.choose_object = False
        self.update_statistic()
        x_pos, y_pos = event.x(), event.y() - 30
        bl = True
        if self.button_click != '2':
            for i in range(len(self.list_grid_layout_files)):
                if self.list_grid_layout_files[i].styleSheet() != "background-color: #96a69e;":
                    self.list_grid_layout_files[i].setStyleSheet("background-color: #96a69e;")
                    bl = False
            if bl:
                self.current_file_index = -9999999
                self.current_file_path = ''
        if self.button_click == '1':
            if self.but_for_object.isActiveWindow() and \
                    self.collision_object(self.but_for_object.x(),
                                          self.but_for_object.y(),
                                          self.but_for_object.width(),
                                          self.but_for_object.height(),
                                          x_pos,
                                          y_pos):
                self.f_set_vec(1)
            elif self.but_for_object2.isActiveWindow() and \
                    self.collision_object(self.but_for_object2.x(),
                                          self.but_for_object2.y(),
                                          self.but_for_object2.width(),
                                          self.but_for_object2.height(),
                                          x_pos,
                                          y_pos):
                self.f_set_vec(2)
            elif self.but_for_object3.isActiveWindow() and \
                    self.collision_object(self.but_for_object3.x(),
                                          self.but_for_object3.y(),
                                          self.but_for_object3.width(),
                                          self.but_for_object3.height(),
                                          x_pos,
                                          y_pos):
                self.f_set_vec(3)
            elif self.but_for_object4.isActiveWindow() and \
                    self.collision_object(self.but_for_object4.x(),
                                          self.but_for_object4.y(),
                                          self.but_for_object4.width(),
                                          self.but_for_object4.height(),
                                          x_pos,
                                          y_pos):
                self.f_set_vec(4)
            elif self.widget0 and self.tabWidget.x() + 4 + self.dockWidget.width() < x_pos < self.tabWidget.x() + self.dockWidget.width() + 4 + self.widget0.width() and \
                    self.tabWidget.y() < y_pos < self.tabWidget.y() + self.widget0.height():
                if self.tabWidget.currentIndex() == 0:
                    self.select_item(x_pos, y_pos)

            if self.index_gm_now != -9999999:
                if self.index_gm_now < len(self.list_game_objects):
                    obj = self.list_game_objects[self.index_gm_now]
                self.old_sel_item = [int(obj[2].split(',')[0]),
                                     int(obj[2].split(',')[1]),
                                     int(obj[3].split(',')[0]),
                                     int(obj[3].split(',')[1]),
                                     self.labels_in_scene[self.index_gm_now].x(),
                                     self.labels_in_scene[self.index_gm_now].y()]
        elif self.button_click == '4':
            self.old_pos_mouse = [0, 0]
        elif self.button_click == '2':
            if self.index_gm_now == -9999999:
                if self.widget0 and self.tabWidget.x() + self.dockWidget.width() + 4 < x_pos < self.tabWidget.x() + self.dockWidget.width() + 4 + self.widget0.width() and \
                        self.tabWidget.y() < y_pos < self.tabWidget.y() + self.widget0.height():
                    menu = QtWidgets.QMenu(self)

                    # removeSceneAction = menu.addAction(QIcon('images/delete.png'), "Remove this scene")
                    # removeSceneAction.triggered.connect(lambda: self.remove_scene(self.tabWidget.currentIndex()))

                    innewtabAction = menu.addAction(self.icon_act_create, "Create empty GameObject")
                    innewtabAction.triggered.connect(lambda: create_game_object('empty_gameobject',
                                                                                'None',
                                                                                f'{self.sizeWindow[0] // 2},{self.sizeWindow[1] // 2}',
                                                                                '100,100',
                                                                                '0',
                                                                                '1',
                                                                                'False',
                                                                                'True',
                                                                                '',
                                                                                'None'))

                    menu.exec_(event.globalPos())
            else:
                x, y = self.labels_in_scene[self.index_sel_gm].x() + self.tabWidget.x() + self.dockWidget.width() + 4, self.labels_in_scene[
                    self.index_sel_gm].y() + self.tabWidget.y()
                if x < event.x() < x + self.labels_in_scene[self.index_sel_gm].width() and y < event.y() - 60 < y + self.labels_in_scene[self.index_sel_gm].height():
                    self.choose_object = True
                    self.r1, self.r2 = event.x() - self.tabWidget.x() - self.labels_in_scene[self.index_sel_gm].x(), event.y() - self.tabWidget.y() - 60 - self.labels_in_scene[self.index_sel_gm].y()

                    self.r1obj, self.r2obj = round((event.x() - self.tabWidget.x() - self.labels_in_scene[self.index_sel_gm].x()) / self.scale_factor), round((event.y() - self.tabWidget.y() - 60 - self.labels_in_scene[self.index_sel_gm].y()) / self.scale_factor)

            if self.dockWidget_Project.x() < x_pos < self.dockWidget_Project.x() + self.dockWidget_Project.width() and \
                        self.dockWidget_Project.y() < y_pos < self.dockWidget_Project.y() + self.dockWidget_Project.height():
                    menu = QtWidgets.QMenu(self)
                    createFolderAction = menu.addAction(QIcon('images/free-icon-dead-blow-hammer-1105682.png'), "Create folder")
                    self.mouse_pos = [x_pos + 50, y_pos]
                    createFolderAction.triggered.connect(lambda: self.active_window_create_folder())
                    createSceneAction = menu.addAction(QIcon('images/free-icon-plus-1828575.png'), "Add new scene")
                    createSceneAction.triggered.connect(lambda: self.create_scene())
                    removeFolderAction = menu.addAction(QIcon('images/delete.png'), "Remove folder")
                    removeFolderAction.triggered.connect(lambda: self.remove_folder())

                    menu.addSeparator()
                    menu.exec_(event.globalPos())

    def select_item(self, px, py, ixx=-999999):
        x, y = px, py
        index_ = -999999
        self.f_set_vec(0)

        for ix in range(len(self.labels_in_scene)):
            i = self.labels_in_scene[ix]
            if ix < len(self.list_game_objects):
                cmp = ''
                cmpt = ''
                if len(self.list_game_objects[ix]) > 9:
                    comps = [a.split('^,^') for a in self.list_game_objects[ix][8].split('$')]
                    for c in comps:
                        if c[0] == 'Color box':
                            cmp = c
                        elif c[0] == 'Text':
                            cmpt = c
                if not cmp:
                    self.labels_in_scene[ix].setStyleSheet("border: 0px solid blue;"
                                                           f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'}")
                else:
                    self.labels_in_scene[ix].setStyleSheet("border: 0px solid blue;"
                                                           f"background-color: {cmp[2]};"
                                                           f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'}")
            else:
                self.labels_in_scene[ix].setStyleSheet(
                    f"border: 0px solid blue; "
                    f"background-color: {self.list_ui_objects[ix - len(self.list_game_objects)][7]}; "
                    f"color: {self.list_ui_objects[ix - len(self.list_game_objects)][10]}")
            if ixx == -999999:
                x2 = i.x() + self.tabWidget.x() + self.dockWidget.width() + 4
                y2 = self.tabWidget.y() + 30 + i.y()
                if x2 <= x <= x2 + i.width() \
                        and y2 <= y <= y2 + i.height() \
                        and self.tabWidget.x() + self.dockWidget.width() + 4 <= x <= self.tabWidget.x() + self.dockWidget.width() + 4 + self.tabWidget.width() \
                        and self.tabWidget.y() + 30 <= y <= self.tabWidget.y() + self.tabWidget.height():
                    index_ = ix
            else:
                index_ = ixx
        if index_ != -999999:
            self.index_sel_gm = index_
            self.index_gm_now = index_
            self.update_inspector(index_)

            if self.index_gm_now < len(self.list_game_objects):
                obj = self.list_game_objects[self.index_gm_now]
                cmp = ''
                cmpt = ''
                if len(self.list_game_objects[self.index_gm_now]) > 9:
                    comps = [a.split('^,^') for a in self.list_game_objects[self.index_gm_now][8].split('$')]
                    for c in comps:
                        if c[0] == 'Color box':
                            cmp = c
                        elif c[0] == 'Text':
                            cmpt = c
                if not cmp:
                    self.labels_in_scene[index_].setStyleSheet("border: 2px solid blue;"
                                                               f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'}")
                else:
                    self.labels_in_scene[index_].setStyleSheet("border: 2px solid blue;"
                                                               f"background-color: {cmp[2]};"
                                                               f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'}")
            else:
                obj = self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)]
                self.labels_in_scene[index_].setStyleSheet(
                    f"border: 2px solid blue; "
                    f"background-color: {obj[7]}; "
                    f"color: {obj[10]}")

            self.but_for_object.show()
            self.but_for_object2.show()
            self.but_for_object3.show()
            self.but_for_object4.show()
            self.move_buttons_choose_object(index_)
        else:
            self.index_sel_gm = -9999999
            self.index_gm_now = -9999999
            self.clear_inspector()
            self.but_for_object.hide()
            self.but_for_object2.hide()
            self.but_for_object3.hide()
            self.but_for_object4.hide()

    def movement_set(self, vec, x_p, y_p):
        if vec == 0:
            mv1, mv2 = round(self.old_sel_item[0] - ((self.old_sel_item[4] - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())) / 2) / self.scale_factor), \
                       round(self.old_sel_item[2] + (self.old_sel_item[4] - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())) / self.scale_factor)
            mv22 = round(self.old_sel_item[2] * self.scale_factor + (self.old_sel_item[4] - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())))

            if mv22 > 0 and mv2 > 0:
                if self.index_gm_now < len(self.list_game_objects):
                    self.list_game_objects[self.index_gm_now][2] = f'{mv1},{self.old_sel_item[1]}'
                    self.list_game_objects[self.index_gm_now][3] = f'{mv2},{self.old_sel_item[3]}'
                else:
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][2] = f'{mv1},{self.old_sel_item[1]}'
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][3] = f'{mv2},{self.old_sel_item[3]}'
                self.labels_in_scene[self.index_gm_now].move(x_p - self.tabWidget.x() - 4 - self.dockWidget.width(), self.old_sel_item[5])
                self.labels_in_scene[self.index_gm_now].resize(mv22, self.labels_in_scene[self.index_gm_now].height())
                self.move_buttons_choose_object(self.index_sel_gm)
        elif vec == 1:
            mv1, mv2 = round(self.old_sel_item[1] - ((self.old_sel_item[5] - (y_p - self.tabWidget.y() - 30)) / 2) / self.scale_factor), \
                       round(self.old_sel_item[3] + (self.old_sel_item[5] - (y_p - self.tabWidget.y() - 30)) / self.scale_factor)
            mv22 = round(self.old_sel_item[3] * self.scale_factor + (self.old_sel_item[5] - (y_p - self.tabWidget.y() - 30)))
            if mv22 > 0 and mv2 > 0:
                if self.index_gm_now < len(self.list_game_objects):
                    self.list_game_objects[self.index_gm_now][2] = f'{self.old_sel_item[0]},{mv1}'
                    self.list_game_objects[self.index_gm_now][3] = f'{self.old_sel_item[2]},{mv2}'
                else:
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][
                        2] = f'{self.old_sel_item[0]},{mv1}'
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][
                        3] = f'{self.old_sel_item[2]},{mv2}'
                self.labels_in_scene[self.index_gm_now].move(self.old_sel_item[4], y_p - self.tabWidget.y() - 30)
                self.labels_in_scene[self.index_gm_now].resize(self.labels_in_scene[self.index_gm_now].width(), mv22)
            self.move_buttons_choose_object(self.index_sel_gm)
        elif vec == 2:
            mv1, mv2 = round(self.old_sel_item[0] - ((self.old_sel_item[4] + self.old_sel_item[2] * self.scale_factor - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())) / 2) / self.scale_factor), \
                       round(self.old_sel_item[2] - (self.old_sel_item[4] + self.old_sel_item[2] * self.scale_factor - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())) / self.scale_factor)
            mv22 = round(self.old_sel_item[2] * self.scale_factor - (self.old_sel_item[4] + self.old_sel_item[2] * self.scale_factor - (x_p - self.tabWidget.x() - 4 - self.dockWidget.width())))
            if mv22 > 0 and mv2 > 0:
                if self.index_gm_now < len(self.list_game_objects):
                    self.list_game_objects[self.index_gm_now][2] = f'{mv1},{self.old_sel_item[1]}'
                    self.list_game_objects[self.index_gm_now][3] = f'{mv2},{self.old_sel_item[3]}'
                else:
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][2] = f'{mv1},{self.old_sel_item[1]}'
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][3] = f'{mv2},{self.old_sel_item[3]}'
                self.labels_in_scene[self.index_gm_now].resize(mv22, self.labels_in_scene[self.index_gm_now].height())
            self.move_buttons_choose_object(self.index_sel_gm)
        elif vec == 3:
            mv1, mv2 = round(self.old_sel_item[1] - ((self.old_sel_item[5] + self.old_sel_item[3] * self.scale_factor - (y_p - self.tabWidget.y() - 30)) / 2) / self.scale_factor), \
                       round(self.old_sel_item[3] - (self.old_sel_item[5] + self.old_sel_item[3] * self.scale_factor - (y_p - self.tabWidget.y() - 30)) / self.scale_factor)
            mv22 = round(self.old_sel_item[3] * self.scale_factor - (self.old_sel_item[5] + self.old_sel_item[3] * self.scale_factor - (y_p - self.tabWidget.y() - 30)))
            if mv22 > 0 and mv2 > 0:
                if self.index_gm_now < len(self.list_game_objects):
                    self.list_game_objects[self.index_gm_now][2] = f'{self.old_sel_item[0]},{mv1}'
                    self.list_game_objects[self.index_gm_now][3] = f'{self.old_sel_item[2]},{mv2}'
                else:
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][
                        2] = f'{self.old_sel_item[0]},{mv1}'
                    self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][
                        3] = f'{self.old_sel_item[2]},{mv2}'
                self.labels_in_scene[self.index_gm_now].resize(self.labels_in_scene[self.index_gm_now].width(), mv22)
            self.move_buttons_choose_object(self.index_sel_gm)
        self.update_inspector(self.index_gm_now)
        if self.index_gm_now < len(self.list_game_objects):
            size = self.list_game_objects[self.index_gm_now][3].split(',')
            pix = QtGui.QPixmap(f'{self.project_path}\\{self.list_game_objects[self.index_gm_now][1]}')
            pix = pix.scaled(round(int(size[0]) * self.scale_factor), round(int(size[1]) * self.scale_factor))
            self.labels_in_scene[self.index_gm_now].setPixmap(pix)

    def move_buttons_choose_object(self, ix):
        self.but_for_object.move(self.labels_in_scene[ix].x()
                                 - int(self.but_for_object2.width() / 2),
                                 self.labels_in_scene[ix].y()
                                 + int(self.labels_in_scene[ix].height() / 2) - int(self.but_for_object2.height() / 2))
        self.but_for_object2.move(self.labels_in_scene[ix].x()
                                  + self.labels_in_scene[ix].width()
                                  - int(self.but_for_object2.width() / 2),
                                  self.labels_in_scene[ix].y()
                                  + int(self.labels_in_scene[ix].height() / 2) - int(self.but_for_object2.height() / 2))
        self.but_for_object3.move(self.labels_in_scene[ix].x()
                                  + int(self.labels_in_scene[ix].width() / 2)
                                  - int(self.but_for_object2.width() / 2),
                                  self.labels_in_scene[ix].y()
                                  - int(self.but_for_object2.height() / 2))
        self.but_for_object4.move(self.labels_in_scene[ix].x()
                                  + int(self.labels_in_scene[ix].width() / 2)
                                  - int(self.but_for_object2.width() / 2),
                                  self.labels_in_scene[ix].y()
                                  + self.labels_in_scene[ix].height()
                                  - int(self.but_for_object2.height() / 2))

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y() - 30

        if self.button_click == '4':
            self.update_lines_center()
            pos_wx, pos_wy = self.tabWidget.x() + 4 + self.dockWidget.width(), self.tabWidget.y() + 30
            sz_wx, sx_wy = self.tabWidget.width(), self.tabWidget.height() - 30
            if pos_wx <= x <= pos_wx + sz_wx \
                    and pos_wy <= y <= pos_wy + sx_wy:
                self.cam_pos = [self.cam_pos[0] + x - self.old_pos_mouse[0], self.cam_pos[1] + y - self.old_pos_mouse[1]] \
                    if self.old_pos_mouse[0] != 0 or self.old_pos_mouse[1] != 0 else [0, 0]
                self.cam_pos_now = [self.cam_pos_now[0] + self.cam_pos[0], self.cam_pos_now[1] + self.cam_pos[1]]
            self.old_pos_mouse = [x, y]
            for ix in range(len(self.labels_in_scene)):
                i = self.labels_in_scene[ix]
                i.move(i.x() + self.cam_pos[0], i.y() + self.cam_pos[1])
            self.cam_pos = [0, 0]
            if self.index_gm_now != -9999999:
                self.move_buttons_choose_object(self.index_gm_now)
                if self.index_gm_now < len(self.list_game_objects):
                    obj = self.list_game_objects[self.index_gm_now]
                else:
                    obj = self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)]
                self.old_sel_item = [int(obj[2].split(',')[0]),
                                     int(obj[2].split(',')[1]),
                                     int(obj[3].split(',')[0]),
                                     int(obj[3].split(',')[1]),
                                     self.labels_in_scene[self.index_gm_now].x(),
                                     self.labels_in_scene[self.index_gm_now].y()]
            self.lineEditPosX.setText(str(self.cam_pos_now[0]))
            self.lineEditPosY.setText(str(self.cam_pos_now[1]))

        elif self.button_click == '2':
            if self.index_sel_gm != -9999999 and self.choose_object:
                self.update_inspector(self.index_sel_gm)
                obj = self.list_game_objects[self.index_gm_now]
                x_m, y_m = event.x() - self.tabWidget.x() - ((4 + self.dockWidget.width()) if not self.radioButton_5.isChecked() else 0), event.y() - self.tabWidget.y() - 60
                x_mm, y_mm = event.x() - self.cam_pos_now[0] - self.tabWidget.x() - ((4 + self.dockWidget.width()) if not self.radioButton_5.isChecked() else 0), event.y() - self.cam_pos_now[1] - self.tabWidget.y() - 60
                x_m2 = x_m - int((x_m - self.cam_pos_now[0]) % (self.movement * self.scale_factor)) - (self.r1 if self.radioButton_5.isChecked() else self.labels_in_scene[self.index_sel_gm].width() // 2 if self.radioButton_3.isChecked() else 0)
                y_m2 = y_m - int((y_m - self.cam_pos_now[1]) % (self.movement * self.scale_factor)) - (self.r2 if self.radioButton_5.isChecked() else self.labels_in_scene[self.index_sel_gm].height() // 2 if self.radioButton_3.isChecked() else 0)

                x_m3 = round((x_mm - x_mm % (self.movement * self.scale_factor)) / self.scale_factor) - (self.r1obj if self.radioButton_5.isChecked() else int(obj[3].split(',')[0]) // 2 if self.radioButton_3.isChecked() else 0)
                y_m3 = round((y_mm - y_mm % (self.movement * self.scale_factor)) / self.scale_factor) - (self.r2obj if self.radioButton_5.isChecked() else int(obj[3].split(',')[1]) // 2 if self.radioButton_3.isChecked() else 0)

                self.labels_in_scene[self.index_sel_gm].move(x_m2, y_m2)
                self.move_buttons_choose_object(self.index_sel_gm)

                sz = obj[3].split(',')
                self.list_game_objects[self.index_sel_gm][2] = f'{x_m3 + int(int(sz[0]) / 2)},{y_m3 + int(int(sz[1]) / 2)}'

                self.old_sel_item = [int(obj[2].split(',')[0]),
                                     int(obj[2].split(',')[1]),
                                     int(obj[3].split(',')[0]),
                                     int(obj[3].split(',')[1]),
                                     self.labels_in_scene[self.index_gm_now].x(),
                                     self.labels_in_scene[self.index_gm_now].y()]

        elif self.button_click == '1':
            if self.but_vec_resize == 1:
                self.movement_set(0, x, y)
            elif self.but_vec_resize == 2:
                self.movement_set(2, x, y)
            elif self.but_vec_resize == 3:
                self.movement_set(1, x, y)
            elif self.but_vec_resize == 4:
                self.movement_set(3, x, y)

    def active_window_create_folder(self):
        self.f_ex.show()

    def remove_folder(self):
        if self.current_path_project != self.project_path:
            shutil.rmtree(self.current_path_project)
            self.update_tree_widget_project()
        else:
            self.send_debug_message('ошибка! нельзя удалить папку проекта!')

    def create_folder(self, name):
        os.mkdir(f'{self.current_path_project}\\{name}')
        self.update_tree_widget_project()

    def active_setting_panel(self):
        win = self.set_ex
        win.active_wid()
        win.show()

    def remove_component(self):
        list_items = self.listWidget_2.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def copy_gm(self):
        if self.index_gm_now != -9999999:
            tx = 'GameObject'
            if self.index_gm_now < len(self.list_game_objects):
                self.copy_game_object = self.list_game_objects[self.index_gm_now]
            else:
                tx = 'UI'
                self.copy_game_object = self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)]
            self.send_debug_message(f'{tx} <{self.copy_game_object[0]}> скопирован.')
        else:
            self.send_debug_message(f'обьект не выбран!')

    def paste_gm(self):
        if len(self.copy_game_object) > 0:
                cmp = ''
                if len(self.copy_game_object) > 9:
                    cmp = self.copy_game_object[8]

                create_game_object(self.copy_game_object[0],
                                   self.copy_game_object[1],
                                   self.copy_game_object[2],
                                   self.copy_game_object[3],
                                   self.copy_game_object[4],
                                   self.copy_game_object[5],
                                   self.copy_game_object[6],
                                   self.copy_game_object[7],
                                   cmp, self.copy_game_object[9] if len(self.copy_game_object) > 9 else self.copy_game_object[8], index_=self.list_game_objects.index(self.copy_game_object) + 1)
        else:
            self.send_debug_message(f'нет скопированного обьекта!')

    def create_new_game_object(self):
        self.create_ex.show()

    def add_(self):
        self.add_ex.show()
        self.add_ex.is_show()

    def keyPressEvent(self, event):
        self.twidget.key_press_event_term(event)
        if int(event.modifiers()) == Qt.CTRL:
            if event.key() == Qt.Key_V:
                self.paste_gm()
            if event.key() == Qt.Key_C:
                self.copy_gm()
            if event.key() == Qt.Key_S:
                self.save_scene()

    def add_component(self, component):
        if component.strip() != '' and self.index_gm_now != -9999999:
            for i in self.list_components:
                if i[0] == component:
                    component = f'{i[0]}^,^{"^;^".join(i[1])}^,^{"^;^".join(i[2])}'
            if len(self.list_game_objects[self.index_gm_now]) > 9:
                self.list_game_objects[self.index_gm_now][8] += f'${component}'
            else:
                self.list_game_objects[self.index_gm_now].insert(8, f'{component}')
            self.update_inspector(self.index_gm_now)
            self.send_debug_message(f'добавлен новый компонент для <{self.list_game_objects[self.index_gm_now][0]}>'
                                    f'\n--> {component}')

        else:
            self.send_debug_message('ошибка, компонент не может быть добавлен!')

    def run_engine(self):
        self.save_scene()
        os.chdir(self.project_path)
        subprocess.Popen(f"C:\\Users\\aleks\\PycharmProjects\\python39\\Scripts\\python.exe {self.run_file}", shell=True)

    def update_lines_center(self):
        self.lines_center[0][0].resize(self.widget0.width(), 2)
        self.lines_center[0][0].move(0, self.cam_pos_now[1] + int(self.sizeWindow[1] / 2 * self.scale_factor))
        self.lines_center[0][1].resize(2, self.widget0.height())
        self.lines_center[0][1].move(self.cam_pos_now[0] + int(self.sizeWindow[0] / 2 * self.scale_factor), 0)

        self.lines_center[0][2].move(self.cam_pos_now[0], self.cam_pos_now[1])
        self.lines_center[0][2].resize(2, int(self.sizeWindow[1] * self.scale_factor))
        self.lines_center[0][3].move(self.cam_pos_now[0] + int(self.sizeWindow[0] * self.scale_factor), self.cam_pos_now[1])
        self.lines_center[0][3].resize(2, int(self.sizeWindow[1] * self.scale_factor))
        self.lines_center[0][4].move(self.cam_pos_now[0], self.cam_pos_now[1])
        self.lines_center[0][4].resize(int(self.sizeWindow[0] * self.scale_factor), 2)
        self.lines_center[0][5].move(self.cam_pos_now[0], self.cam_pos_now[1] + int(self.sizeWindow[1] * self.scale_factor))
        self.lines_center[0][5].resize(int(self.sizeWindow[0] * self.scale_factor), 2)

    def update_scene(self):
        if is_float(self.lineEditScale.text()):
            self.scale_factor = float(self.lineEditScale.text())
        if self.lineEditPosX.text().isdigit() and self.lineEditPosY.text().isdigit():
            self.cam_pos_now = [int(self.lineEditPosX.text()), int(self.lineEditPosY.text())]
        if self.lineEditMove.text().isdigit():
            self.movement = int(self.lineEditMove.text())

        for lk in self.labels_in_scene:
            lk.deleteLater()

        for lk in self.labels_in_scene_debugs:
            lk.deleteLater()

        self.labels_in_scene.clear()
        self.labels_in_scene_debugs.clear()

        self.update_lines_center()

        for i in self.list_game_objects:
                cmp = ''
                cmpt = ''
                active = True
                if len(i) > 9:
                    comps = [a.split('^,^') for a in i[8].split('$')]
                    for c in comps:
                        if c[0] == 'Color box':
                            cmp = c
                        elif c[0] == 'Text':
                            cmpt = c
                        elif c[0] == 'Activeself':
                            active = booled(c[2].split('^;^')[0])
                opacity_effect = QGraphicsOpacityEffect()
                opacity_effect.setOpacity(float(i[5]))
                size = i[3].split(',')
                pos = i[2].split(',')
                lbl = QtWidgets.QLabel()
                lbl.move(9999, 9999)
                lbl.resize(0, 0)

                if active:
                        lbl.resize(round(int(size[0]) * self.scale_factor), round(int(size[1]) * self.scale_factor))
                        lbl.move(self.cam_pos_now[0] + (round(int(pos[0]) * self.scale_factor) - int(lbl.width() / 2)),
                             self.cam_pos_now[1] + (round(int(pos[1]) * self.scale_factor) - int(lbl.height() / 2)))
                        lbl.setStyleSheet(f"border: 0px solid blue; "
                                          f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'};")
                        if not cmp and i[1] != 'None':
                            pix = QtGui.QPixmap(f'{self.project_path}\\{i[1]}')
                            pix = pix.scaled(round(int(size[0]) * self.scale_factor), round(int(size[1]) * self.scale_factor))
                            lbl.setPixmap(pix)

                        elif cmp:
                            lbl.setStyleSheet(f"border: 0px solid blue; "
                                              f"background-color: {cmp[2]};"
                                              f"color: {cmpt[2].split('^;^')[2] if cmpt else '#000000'};")

                        if cmpt:
                            lbl.setText(cmpt[2].split('^;^')[0])
                            lbl.setFont(QFont('Times', int(int(cmpt[2].split('^;^')[1]) / 2 * self.scale_factor)))
                        lbl.setGraphicsEffect(opacity_effect)
                lbl.setParent(self.widget0)
                lbl.show()
                self.labels_in_scene.append(lbl)

        try:
            self.but_for_object.hide()
            self.but_for_object2.hide()
            self.but_for_object3.hide()
            self.but_for_object4.hide()
            self.but_for_object = QLabel(self.widget0)
            self.but_for_object.resize(15, 15)
            self.but_for_object2 = QLabel(self.widget0)
            self.but_for_object2.resize(15, 15)
            self.but_for_object3 = QLabel(self.widget0)
            self.but_for_object3.resize(15, 15)
            self.but_for_object4 = QLabel(self.widget0)
            self.but_for_object4.resize(15, 15)
            self.but_for_object.setStyleSheet("background-color: #FF7E0A")
            self.but_for_object2.setStyleSheet("background-color: #FF7E0A")
            self.but_for_object3.setStyleSheet("background-color: #FF7E0A")
            self.but_for_object4.setStyleSheet("background-color: #FF7E0A")
            self.but_for_object.hide()
            self.but_for_object2.hide()
            self.but_for_object3.hide()
            self.but_for_object4.hide()
            '''
            self.but_for_object.clicked.connect(lambda: self.f_set_vec(1))
            self.but_for_object2.clicked.connect(lambda: self.f_set_vec(2))
            self.but_for_object3.clicked.connect(lambda: self.f_set_vec(3))
            self.but_for_object4.clicked.connect(lambda: self.f_set_vec(4))'''
        except AttributeError:
            pass
        if self.index_gm_now != -9999999:
            self.select_item(0, 0, self.index_gm_now)
        self.send_debug_message('сцена обновлена!')

    def f_set_vec(self, v):
        self.but_vec_resize = v

    def send_debug_message(self, message_):
        mess = QListWidgetItem(self.listWidget)
        if 'ошибк' in message_.lower():
            mess.setForeground(QtGui.QColor(120, 18, 24))
            mess.setBackground(QtGui.QColor(92, 92, 92))
        elif 'сохранены' in message_.lower():
            mess.setForeground(QtGui.QColor(51, 184, 0))
            mess.setBackground(QtGui.QColor(74,112,62))
        mess.setText(message_)
        mess.setIcon(self.icon_warning)

    def delete(self):
        if self.index_gm_now != -9999999:
            if self.index_gm_now < len(self.list_game_objects):
                nm = self.list_game_objects[self.index_gm_now][0]
                self.list_game_objects.pop(self.index_gm_now)
            else:
                nm = self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)][0]
                self.list_ui_objects.pop(self.index_gm_now - len(self.list_game_objects))
            self.index_gm_now = -9999999
            self.index_sel_gm = -9999999
            self.update_treeview()
            self.update_scene()
            self.clear_inspector()
            self.send_debug_message(f'обьект <{nm}> удален.')

    def get_name_recur(self, ls, name_, num=0, nm=''):
        for i in ls:
            nm = name_ if num == 0 else (f'{name_[:-2]}_{num}' if name_[-2] == '_' and name_[-1].isdigit() else f'{name_}_{num}')
            if i[0] == nm:
                return self.get_name_recur(ls, name_, num + 1, nm)

        return nm

    def save_gm(self):
        if self.index_gm_now != -9999999:
            el = []
            for wd in range(len(self.list_line_edits_for_gm) - 2):
                el.append(self.list_line_edits_for_gm[wd].text())

            for e in el:
                if not e.strip():
                    self.send_debug_message(f'ошибка! \nизменения для <{el[0]}> не могут быть сохранены! \n(есть пустые строки)')
                    return

            if self.index_gm_now < len(self.list_game_objects):
                if len(self.list_game_objects[self.index_gm_now]) > 9:
                    ln = ''
                    coms = self.list_game_objects[self.index_gm_now][8].split('$')

                    for i in range(len(self.list_components_values)):
                        ls = []
                        for a in self.list_components_values[i]:
                            if type(a) == list:
                                ls.append("*&*".join([a2.text() for a2 in a]))
                            else:
                                ls.append(a.text())

                        ln2 = '^;^'.join(ls)
                        ln += (('$' if i != 0 else '') + f'{coms[i].split("^,^")[0]}^,^{"^;^".join(coms[i].split("^,^")[1].split("^;^"))}^,^{ln2}')
                    if ln:
                        el.append(ln)
                el.append(self.list_line_edits_for_gm[-1].text())
                self.list_game_objects[self.index_gm_now] = el

                if self.index_gm_now != int(self.list_line_edits_for_gm[-2].text()):
                    self.move_object_of_index(int(self.list_line_edits_for_gm[-2].text()))

            else:
                self.list_ui_objects[self.index_gm_now - len(self.list_game_objects)] = el
                if self.index_gm_now - len(self.list_game_objects) != int(self.list_line_edits_for_gm[-2].text()):
                    self.move_ui_of_index(int(self.list_line_edits_for_gm[-2].text()))
            self.update_treeview()
            self.update_scene()
            self.update_inspector(self.index_gm_now)
            self.send_debug_message(f'изменения для <{el[0]}> сохранены.')

    def save_scene(self):
        with open(self.path_, 'w') as fl:
            st = ""
            for i in self.list_game_objects:
                for j in i:
                    if j.strip() != "":
                        st += f'{j}\n'
                    else:
                        st += 'None\n'
                if i != self.list_game_objects[-1]:
                    st += '~\n'
            st += "(~&~)\n"

            fl.write(st)

            self.send_debug_message('=:сцена сохранена:=')

    def upd(self):
        indexes = self.treeWidget.selectedIndexes()[0]
        name_ = indexes.data(Qt.DisplayRole)
        idx = -999999
        element = None
        element_ui = None
        for el in self.list_game_objects:
            if name_ == el[0]:
                idx = self.list_game_objects.index(el)
                element = self.list_game_objects[idx]
        if idx == -999999:
            for el in self.list_ui_objects:
                if name_ == el[0]:
                    idx = self.list_ui_objects.index(el)
                    element_ui = self.list_ui_objects[idx]
        if element:
            self.index_gm_now = idx

            self.select_item(0, 0, self.index_gm_now)
            self.update_inspector(self.index_gm_now)
        elif element_ui:
            self.index_gm_now = idx + len(self.list_game_objects)

            self.select_item(0, 0, self.index_gm_now)
            self.update_inspector(self.index_gm_now)

    def rec_tree(self, name, item):
        for el in self.list_game_objects:
            nm = el[9] if len(el) > 9 else el[8]
            if nm == name:
                item_ = QTreeWidgetItem(item)
                # s = f"<{index_}> "
                item_.setText(0, el[0])
                item_.setIcon(0, self.icon_obj)
                item_.setFont(0, QFont('Times', 10))
                self.items_tree.append(item_)
                self.delta_list_game_objects.append(el)
                for el_ in self.list_game_objects:
                    nm2 = el_[9] if len(el_) > 9 else el_[8]
                    if nm2 == el[0]:
                        self.rec_tree(el[0], item_)

    def update_treeview(self):
        self.treeWidget.clear()
        self.items_tree.clear()
        item_2 = QTreeWidgetItem(self.treeWidget)
        item_2.setText(0, '<GameObjects>')
        item_2.setIcon(0, self.icon_py2)
        item_2.setExpanded(True)
        item_2.setForeground(0, QtGui.QBrush(QtGui.QColor("#37B98D")))
        item_2.setFont(0, QFont('Times', 12))

        index_ = 0
        self.delta_list_game_objects.clear()
        for i in self.list_game_objects:
            nm = i[9] if len(i) > 9 else i[8]
            if nm == '[]' or nm == 'None':
                item_ = QTreeWidgetItem(item_2)
                # s = f"<{index_}> "
                item_.setText(0, i[0])
                item_.setIcon(0, self.icon_obj)
                item_.setFont(0, QFont('Times', 10))
                self.items_tree.append(item_)
                index_ += 1
                self.delta_list_game_objects.append(i)
                self.rec_tree(i[0], item_)

            '''for j in range(1, len(i) - 2):
                item_s = QTreeWidgetItem(item_)
                item_s.setText(0, self.list_settings_parameters[j - 1] + i[j])
                item_s.setIcon(0, self.icon_sett)
                item_s.setExpanded(True)
                item_s.setForeground(0, QtGui.QBrush(QtGui.QColor("#4EE3E9")))
                item_s.setFont(0, QFont('Times', 10))'''
        self.list_game_objects.clear()
        for elem in self.delta_list_game_objects:
            self.list_game_objects.append(elem)
        '''item_3 = QTreeWidgetItem(self.treeWidget)
        item_3.setText(0, '<UI>')  # └
        item_3.setIcon(0, self.icon_py2)
        item_3.setExpanded(True)
        item_3.setForeground(0, QtGui.QBrush(QtGui.QColor("#37B98D")))
        item_3.setFont(0, QFont('Times', 12))

        index_ = 0
        for i in self.list_ui_objects:
            item_ = QTreeWidgetItem(item_3)
            s = f"<{index_}> "
            item_.setText(0, s + i[0])
            item_.setIcon(0, self.icon_obj)
            item_.setFont(0, QFont('Times', 10))

            for j in range(1, len(i)):
                item_s = QTreeWidgetItem(item_)
                item_s.setText(0, self.list_settings_parameters_ui[j - 1] + i[j])
                item_s.setIcon(0, self.icon_sett)
                item_s.setExpanded(True)
                item_s.setForeground(0, QtGui.QBrush(QtGui.QColor("#4EE3E9")))
                item_s.setFont(0, QFont('Times', 10))
            self.items_tree_ui.append(item_)
            index_ += 1'''

    def clear_inspector(self):
        for i in self.widgets_:
            self.gridLayout.removeWidget(i)
        self.pushButtonPlus.hide()
        self.pushButtonDelete.hide()
        self.pushButtonSave.hide()
        self.widgets_.clear()
        self.listWidget_script.clear()
        self.listWidget_script_2.clear()

    def update_inspector(self, ix):
        for i in self.widgets_:
            self.gridLayout.removeWidget(i)

        self.listWidget_script.clear()
        self.listWidget_script_2.clear()

        self.pushButtonSave.show()
        self.pushButtonDelete.show()

        if ix < len(self.list_game_objects):
            self.pushButtonPlus.show()

            el = self.list_game_objects[ix]
            size = el[3].split(',')

            # k2 = int(size[1]) / int(size[0])
            lbl = QtWidgets.QLabel(self)
            pix = QtGui.QPixmap(f'{self.project_path}\\{el[1]}')
            if int(size[1]) > int(size[0]):
                k = int(size[0]) / int(size[1])
                pix = pix.scaled(int(400 * k), 400)
            else:
                k = int(size[1]) / int(size[0])
                pix = pix.scaled(400, int(400 * k))
            lbl.setPixmap(pix)
            lbl.resize(pix.width(), pix.height())
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(float(el[5]))
            lbl.setGraphicsEffect(opacity_effect)

            # Transform =>
            lbl2 = QtWidgets.QLabel(self)
            lbl2.setText('Transform =>')
            lbl2.resize(200, 70)
            self.font_main.setPointSize(12)
            lbl2.setFont(self.font_main)

            wid1 = QtWidgets.QGroupBox(self)
            wid1.setMinimumHeight(130)

            lbl3 = QtWidgets.QLabel(wid1)
            lbl3.setText(' position    = ')
            lbl3.resize(200, 30)
            lbl3.move(0, 5)
            self.font_main.setPointSize(8)
            lbl3.setFont(self.font_main)

            ln_ed3 = QtWidgets.QLineEdit(wid1)
            ln_ed3.setText(el[2])
            ln_ed3.resize(200, 30)
            ln_ed3.move(200, 5)
            ln_ed3.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed3.setFont(self.font_main)

            lbl4 = QtWidgets.QLabel(wid1)
            lbl4.setText(' size        = ')
            lbl4.resize(200, 30)
            lbl4.move(0, 35)
            self.font_main.setPointSize(8)
            lbl4.setFont(self.font_main)

            ln_ed4 = QtWidgets.QLineEdit(wid1)
            ln_ed4.setText(el[3])
            ln_ed4.resize(200, 30)
            ln_ed4.move(200, 35)
            ln_ed4.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed4.setFont(self.font_main)

            lbl5 = QtWidgets.QLabel(wid1)
            lbl5.setText(' angle       = ')
            lbl5.resize(200, 30)
            lbl5.move(0, 65)
            self.font_main.setPointSize(8)
            lbl5.setFont(self.font_main)

            ln_ed5 = QtWidgets.QLineEdit(wid1)
            ln_ed5.setText(el[4])
            ln_ed5.resize(200, 30)
            ln_ed5.move(200, 65)
            ln_ed5.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed5.setFont(self.font_main)

            lbl6 = QtWidgets.QLabel(wid1)
            lbl6.setText(' index       = ')
            lbl6.resize(200, 30)
            lbl6.move(0, 95)
            self.font_main.setPointSize(8)
            lbl6.setFont(self.font_main)

            ln_ed6 = QtWidgets.QLineEdit(wid1)
            ln_ed6.setText(str(self.index_gm_now))
            ln_ed6.resize(200, 30)
            ln_ed6.move(200, 95)
            ln_ed6.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed6.setFont(self.font_main)

            # Name
            lbl1 = QtWidgets.QLabel(self)
            lbl1.setText(f'<{el[0]}>\ntype:=GameObject')
            lbl1.resize(200, 70)
            self.font_main.setPointSize(12)
            lbl1.setFont(self.font_main)

            # Image =>
            lbl21 = QtWidgets.QLabel(self)
            lbl21.setText('Image =>')
            lbl21.resize(200, 70)
            self.font_main.setPointSize(12)
            lbl21.setFont(self.font_main)

            wid2 = QtWidgets.QGroupBox(self)
            wid2.setMinimumHeight(70)

            lbl31 = QtWidgets.QLabel(wid2)
            lbl31.setText(' file        = ')
            lbl31.resize(200, 30)
            lbl31.move(0, 5)
            self.font_main.setPointSize(8)
            lbl31.setFont(self.font_main)

            ln_ed31 = QtWidgets.QLineEdit(wid2)
            ln_ed31.setText(el[1])
            ln_ed31.resize(200, 30)
            ln_ed31.move(200, 5)
            ln_ed31.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed31.setFont(self.font_main)

            lbl41 = QtWidgets.QLabel(wid2)
            lbl41.setText(' opacity     = ')
            lbl41.resize(200, 30)
            lbl41.move(0, 35)
            self.font_main.setPointSize(8)
            lbl41.setFont(self.font_main)

            ln_ed41 = QtWidgets.QLineEdit(wid2)
            ln_ed41.setText(el[5])
            ln_ed41.resize(200, 30)
            ln_ed41.move(200, 35)
            ln_ed41.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed41.setFont(self.font_main)

            # Other settings =>
            lbl22 = QtWidgets.QLabel(self)
            lbl22.setText('Other settings =>')
            lbl22.resize(200, 70)
            self.font_main.setPointSize(12)
            lbl22.setFont(self.font_main)

            wid3 = QtWidgets.QGroupBox(self)
            wid3.setMinimumHeight(130)

            lbl_nm = QtWidgets.QLabel(wid3)
            lbl_nm.setText(' name        = ')
            lbl_nm.resize(200, 30)
            lbl_nm.move(0, 5)
            self.font_main.setPointSize(8)
            lbl_nm.setFont(self.font_main)

            ln_ed_nm = QtWidgets.QLineEdit(wid3)
            ln_ed_nm.setText(el[0])
            ln_ed_nm.resize(200, 30)
            ln_ed_nm.move(200, 5)
            ln_ed_nm.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed_nm.setFont(self.font_main)

            lbl32 = QtWidgets.QLabel(wid3)
            lbl32.setText(' collision   = ')
            lbl32.resize(200, 30)
            lbl32.move(0, 35)
            self.font_main.setPointSize(8)
            lbl32.setFont(self.font_main)

            ln_ed32 = QtWidgets.QLineEdit(wid3)
            ln_ed32.setText(el[6])
            ln_ed32.resize(200, 30)
            ln_ed32.move(200, 35)
            ln_ed32.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed32.setFont(self.font_main)

            lbl42 = QtWidgets.QLabel(wid3)
            lbl42.setText(' add to list = ')
            lbl42.resize(200, 30)
            lbl42.move(0, 65)
            self.font_main.setPointSize(8)
            lbl42.setFont(self.font_main)

            ln_ed42 = QtWidgets.QLineEdit(wid3)
            ln_ed42.setText(el[7])
            ln_ed42.resize(200, 30)
            ln_ed42.move(200, 65)
            ln_ed42.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed42.setFont(self.font_main)

            lbl_par = QtWidgets.QLabel(wid3)
            lbl_par.setText(' parent      = ')
            lbl_par.resize(200, 30)
            lbl_par.move(0, 95)
            self.font_main.setPointSize(8)
            lbl_par.setFont(self.font_main)

            ln_ed_par = QtWidgets.QLineEdit(wid3)
            ln_ed_par.setText(('None' if el[9] == '[]' else el[9]) if len(el) > 9 else ('None' if el[8] == '[]' else el[8]))
            ln_ed_par.resize(200, 30)
            ln_ed_par.move(200, 95)
            ln_ed_par.setStyleSheet("background-color: #77D4C5")
            self.font_main.setPointSize(8)
            ln_ed_par.setFont(self.font_main)

            lbl_s = [lbl1, lbl2, lbl31, lbl41, lbl3, lbl_nm, lbl4, lbl42, lbl5, lbl6, lbl21, lbl22, lbl32, lbl_par]

            for e in lbl_s:
                e.setStyleSheet("color: #ceecde")

            self.widgets_ = [lbl1, lbl, lbl2, wid1, lbl21, wid2, lbl22, wid3]
            if len(el) > 9:
                self.update_components_in_inspector(el[8])
            for e in self.widgets_:
                self.gridLayout.addWidget(e)

            self.list_line_edits_for_gm = [ln_ed_nm, ln_ed31, ln_ed3, ln_ed4, ln_ed5, ln_ed41, ln_ed32, ln_ed42, ln_ed6, ln_ed_par]
            self.frame_3.setMinimumHeight(5000)


def create_game_object(name_, image, pos, size, angle, opacity, collision, add_in_list, components, parent, index_=-1):
    if index_ == -1:
        index_ = len(ex.list_game_objects)
    name = name_
    if ex.list_game_objects:
        name = ex.get_name_recur(ex.list_game_objects, name_, (int(name_[-1]) if name_[-2] == '_' and name_[-1].isdigit() else 0))

    if components == "":
        ex.list_game_objects.insert(index_, [name, image, pos, size, angle, opacity, collision, add_in_list, parent])
    else:
        ex.list_game_objects.insert(index_, [name, image, pos, size, angle, opacity, collision, add_in_list, components, parent])
    ex.send_debug_message(f'создан новый GameObject\n-->{name}')
    ex.update_scene()
    ex.update_treeview()


# создает gameObject
class CreateWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\create.ui', self)
        self.openImageButton.clicked.connect(self.get_file_name_image)
        self.pushButton.clicked.connect(self.create_gm)
        self.openImageButton_2.clicked.connect(self.line_ed_set)

    def get_file_name_image(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "JPEG Files(*.jpeg);;\
                                                         PNG Files(*.png);;GIF File(*.gif);;All Files(*)")
        self.lineEdit_2.setText(f'{filename}')

    def line_ed_set(self):
        if self.lineEdit_11.text() == "":
            self.lineEdit_11.setText(self.lineEdit_10.text())
        else:
            self.lineEdit_11.setText(f'{self.lineEdit_11.text()}${self.lineEdit_10.text()}')

    def create_gm(self):
        nm = self.lineEdit_3.text()
        img = self.lineEdit_2.text()
        pos = f'{self.lineEdit_4.text()},{self.lineEdit_5.text()}'
        sz = f'{self.lineEdit_6.text()},{self.lineEdit_7.text()}'
        ang = self.lineEdit_8.text()
        opc = self.lineEdit_9.text()
        components = self.lineEdit_11.text()
        coll = 'True' if self.checkBox.checkState() else 'False'
        add = 'True' if self.checkBox_2.checkState() else 'False'
        create_game_object(nm, img, pos, sz, ang, opc, coll, add, components, 'None')


# добавляет компонент для gameObject
class AddComponentWidget(QWidget, Add_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\addComponent.ui', self)
        self.AddButton_1.clicked.connect(self.add_comp)

    def is_show(self):
        self.comboBox.clear()
        self.comboBox.addItems(ex.components_all)

    def add_comp(self):
        ex.add_component(self.comboBox.currentText())


class CreateFolderWidget(QWidget, Add_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\addComponent2.ui', self)
        self.setWindowTitle('Create folder')
        self.label_7.setText('Name: ')
        self.lineEdit_1.setText('folder')
        self.AddButton_1.setText('+')
        self.AddButton_1.clicked.connect(self.create_folder)

    def create_folder(self):
        ex.create_folder(self.lineEdit_1.text())


# текстовый редактор для файлов
class TextRedactorWidget(QMainWindow, Redactor_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\textRedactor.ui', self)
        self.pushButton.clicked.connect(self.run_file)
        self.setMinimumSize(700, 400)
        self.pushButton_2.clicked.connect(self.terminate_file)
        self.pushButton_4.clicked.connect(self.save_file)
        self.pushButton_3.clicked.connect(self.open_file_1)
        self.fl = ""
        self.fl_is_run = False

    def resizeEvent(self, event):
        self.textEdit.resize(self.size().width() - 26, self.size().height() - 83)
        self.pushButton_4.move(self.size().width() - 190, 10)
        self.pushButton_3.move(self.size().width() - 100, 10)
        self.pushButton_2.move(self.size().width() - 280, 10)
        self.pushButton.move(self.size().width() - 370, 10)

    def run_file(self):
        if self.fl:
            self.fl_is_run = True
            os.system(f'python {self.fl}')

    def open_file_1(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "Text Files(*.txt);;Python File(*.py);;All Files(*)")
        if filename.strip():
            self.open_file(filename)

    def save_file(self):
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл",
                                                   ".",
                                                   "All Files(*.*)")
        if ok:
            with open(filename, 'w', encoding="utf-8") as fl:
                fl.write(self.textEdit.toPlainText())

    def terminate_file(self):
        if self.fl_is_run:
            self.fl_is_run = False
            ext_proc = sp.Popen(['python', self.fl.split('\\')[-1]])
            sp.Popen.terminate(ext_proc)

    def open_file(self, file_):
        fl = sys.argv[0]
        fl = fl.replace('/', '\\')
        nm = file_.split("\\")[-1]
        self.fl = ""
        if file_ != fl and file_ != getcwd() + '\\FramelessWindow.py':
            if file_.endswith('.py') or file_.endswith('.pyr'):
                self.pushButton.show()
                self.pushButton_2.show()
                self.fl = file_
            else:
                self.pushButton.hide()
                self.pushButton_2.hide()
            self.label.setText(f'┌{nm}┐')

            with open(file_, 'r', encoding="utf-8") as fl__:
                tx = fl__.read()
                self.textEdit.setPlainText(tx)
                count = len(tx.split("\n"))
                self.label_2.setText(f'┌{count}┐')
        else:
            self.pushButton.hide()
            self.pushButton_2.hide()


class Player(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(400, 400, 200, 150)
        self.setWindowTitle("<audio-player>")

        self.playBtn = QPushButton(self)
        self.playBtn.move(15, 20)
        self.playBtn.setText("play")
        self.playBtn.resize(60, 60)
        self.playBtn.show()
        self.pauseBtn = QPushButton(self)
        self.pauseBtn.move(90, 20)
        self.pauseBtn.setText("pause")
        self.pauseBtn.resize(60, 60)
        self.pauseBtn.show()
        self.stopBtn = QPushButton(self)
        self.stopBtn.move(165, 20)
        self.stopBtn.setText("stop")
        self.stopBtn.resize(60, 60)
        self.stopBtn.show()

        self.playBtn.clicked.connect(self.play)
        self.pauseBtn.clicked.connect(self.pause)
        self.stopBtn.clicked.connect(self.stop)

    def load_mp3(self, filename):
        given_audio = AudioSegment.from_file(f"{filename}", format=filename.split(".")[-1])
        os.remove("current_audio.mp3")
        given_audio.export("current_audio.mp3", format="mp3")
        media = QtCore.QUrl.fromLocalFile("current_audio.mp3")
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()


# paint
class PaintWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 800, 600)
        self.left = 50
        self.pos_ = []
        self.size_ = []
        self.path_ = ""
        self.pixmap = None
        self.widget_1 = QWidget(self)
        self.widget_1.resize(self.width(), self.height() - 60)
        self.widget_1.move(0, 60)

        self.ot = 60
        self.image = QImage(QSize(self.widget_1.size()), QImage.Format_ARGB32)

        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.red
        self._createMenuBar()
        self.lastPoint = QPoint()

    def _createMenuBar(self):
        mainMenu = self.menuBar()

        # creating file menu for save and clear action
        fileMenu = mainMenu.addMenu("File")

        # adding brush size to main menu
        b_size = mainMenu.addMenu("Brush Size")

        # adding brush color to ain menu
        b_color = mainMenu.addMenu("Brush Color")

        # creating save action
        saveAction = QAction("Save", self)
        # adding save to the file menu
        fileMenu.addAction(saveAction)
        # adding action to the save
        saveAction.triggered.connect(self.save)

        saveAction = QAction("Save as", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save_as)

        clearAction = QAction("Clear", self)
        # adding short cut to the clear action
        clearAction.setShortcut("Ctrl + C")
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(self.clear)

        pix_4 = QAction("1px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(lambda: self.set_pixel(1))

        pix_7 = QAction("4px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(lambda: self.set_pixel(4))

        pix_9 = QAction("7px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(lambda: self.set_pixel(7))

        pix_12 = QAction("9px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(lambda: self.set_pixel(9))

        black = QAction("Black", self)
        b_color.addAction(black)
        black.triggered.connect(lambda: self.set_color(Qt.black))

        white = QAction("White", self)
        b_color.addAction(white)
        white.triggered.connect(lambda: self.set_color(Qt.white))

        green = QAction("Green", self)
        b_color.addAction(green)
        green.triggered.connect(lambda: self.set_color(Qt.green))

        yellow = QAction("Yellow", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(lambda: self.set_color(Qt.yellow))

        red = QAction("Red", self)
        b_color.addAction(red)
        red.triggered.connect(lambda: self.set_color(Qt.red))

    def clear(self):
        self.image.fill(QColor(0, 0, 0, 0))
        self.update()

    def set_pixel(self, px):
        self.brushSize = px

    def set_color(self, color):
        self.brushColor = color

    def open_image(self, image):
        self.path_ = image
        self.setWindowTitle(f"<image-engine> - {self.path_}")
        self.pixmap = QPixmap()
        self.pixmap.load(image)
        img = QImage(QSize(self.pixmap.size()), QImage.Format_ARGB32)
        img.load(image)
        if int(self.pixmap.height()) > int(self.pixmap.width()):
            k = int(self.pixmap.width()) / int(self.pixmap.height())
            self.resize(int(1200 * k), 1200 + self.ot)
        else:
            k = int(self.pixmap.height()) / int(self.pixmap.width())
            self.resize(1200, int(1200 * k) + self.ot)
        self.image = QImage(QSize(self.pixmap.size()), QImage.Format_ARGB32)
        for i in range(self.image.width()):
            for j in range(self.image.height()):
                if QColor(img.pixelColor(i, j)).alpha():
                    self.image.setPixelColor(i, j, QColor(img.pixelColor(i, j)))
                else:
                    self.image.setPixelColor(i, j, QColor(232, 232, 232, 0))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            k = self.width() / self.image.width()
            self.lastPoint = QPoint(int(event.x() / k), int(event.y() / k) - int(self.ot / k))
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            painter.drawPoint(self.lastPoint)

    def mouseMoveEvent(self, event):
        k = self.width() / self.image.width()
        mouse_pos = QPoint(int(event.x() / k), int(event.y() / k) - int(self.ot / k))
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            painter.drawLine(self.lastPoint, mouse_pos)
            self.lastPoint = mouse_pos
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(QRect(0, self.ot, self.width(), self.height() - self.ot), self.image, self.image.rect())

    def save_as(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def save(self):
        self.image.save(self.path_)


# настройки
class SettingsWidget(QWidget, Settings_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\settings.ui', self)
        self.setMinimumSize(self.width() - 200, self.height() - 100)
        self.pushButtonUse.clicked.connect(self.use_settings)
        self.setWindowIcon(QIcon('images/settings (1).png'))
        self.oldButtonPos = self.pushButtonUse.pos()
        self.oldSize = self.size()

    def active_wid(self):
        self.lineEditScene.setText(ex.path_)
        self.lineEditRun.setText(ex.run_file)
        self.lineEditImage.setText(ex.image_background)
        self.lineEditWidth.setText(str(ex.sizeWindow[0]))
        self.lineEditHeight.setText(str(ex.sizeWindow[1]))

    def resizeEvent(self, event):
        self.tabWidget.resize(self.width() - 18, self.height() - 18)
        for el in [self.frame, self.frame_2, self.frame_3]:
            el.resize(self.width() - 18, self.height() - 39)
        self.pushButtonUse.move(self.oldButtonPos.x() + (self.width() - self.oldSize.width()), self.oldButtonPos.y() + (self.height() - self.oldSize.height()))
        for el in [self.groupBox, self.groupBox_2, self.groupBox_3, self.groupBox_4, self.groupBox_5]:
            el.resize(self.frame.width() - 40, el.height())

    def use_settings(self):
        ex.path_ = self.lineEditScene.text()
        ex.run_file = self.lineEditRun.text()
        ex.image_background = self.lineEditImage.text()

        try:
            ex.sizeWindow = [int(self.lineEditWidth.text()), int(self.lineEditHeight.text())]
        except ValueError:
            pass

        if ex.image_background and ex.image_background != 'None':
            w.setStyleSheet("#MainWindow{border-image:url(" + ex.image_background + ")}")
        else:
            w.setStyleSheet("#MainWindow{border-image:url("")}")
            palette = ex.palette()
            palette.setColor(palette.Window, QColor(1, 25, 23))
            ex.setPalette(palette)
        ex.update_()
        ex.update_tree_widget_project()
        ex.update_scene()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = FramelessWindow()
    ex = MyWidget()
    ex.show()
    user32 = ctypes.windll.user32
    scz = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    ex.setMinimumSize(ex.width() - 500, ex.height() - 300)
    w.setWindowTitle('SDK-LehaEngine')
    w.setIconSize(60)
    w.setWindowIcon(QIcon('icon_main.ico'))
    w.setWidget(ex)  # Добавить свое окно
    w.move(QPoint(100, 100))
    w.setStyleSheet("#MainWindow{background-color: rgb(1,25,23)}")  # border-image:url(images/fon1.jpg)
    w.showMaximized()
    w.show()

    sys.exit(app.exec_())
