import sys, os, subprocess
from xml.etree.ElementTree import parse, Element, ElementTree, SubElement, dump
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog, QGroupBox
from PyQt5.QtWidgets import QFormLayout, QBoxLayout, QHBoxLayout

class window(QWidget):

    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle('Game Recording Launcher')
        self.setFixedWidth(640)
        self.setFixedHeight(480)
        
        self.layout_base = None

        self.current_game_location = None
        self.group_game = None
        self.list_game = None
        self.btn_reload_gamelist = None

        self.group_resolution = None
        self.width = None
        self.height = None
        self.lb_width = None
        self.lb_height = None


        self.group_btn = None
        self.btn_game_start = None
        self.btn_record_start = None
        self.btn_play_game_and_record = None

        self.home()
    
    def onTextEditWidth(self):
        if self.lb_width.text().isdigit():
            self.width = self.lb_width.text()

    def onTextEditHeight(self):
        if self.lb_height.text().isdigit() :
            self.height = self.lb_height.text()

    def onActivated(self, text):
        app = text.split('.app')[0]
        self.current_game_location = os.getcwd()+'/games/'+text+'/Contents/MacOS/'+app
        print 'current item : '+text
        print 'current app location : '+self.current_game_location

    def reload_gamelist(self):
        files = os.listdir(os.getcwd()+'/games/')
        self.list_game.clear()
        self.list_game.addItems(files)
        app = files[0].split('.app')[0]
        self.current_game_location = os.getcwd()+'/games/'+files[0]+'/Contents/MacOS/'+app
        print 'current item : '+files[0]
        print 'current app location : '+self.current_game_location

    def onClickGameStart(self):
        if self.current_game_location != None and self.lb_width.text().isdigit() and self.lb_height.text().isdigit():
            command = self.current_game_location + ' -screen-width '+self.lb_width.text()+' -screen-height '+self.lb_height.text()
            #os.system(command)
            subprocess.Popen([command], shell=True)
            return True

    def onClickRecordStart(self):
        applescript = os.getcwd()+'/AppleScripts/recorder.scpt'
        command = 'osascript '+applescript
        os.system(command)

    def onClickAllRun(self):
        ret = self.onClickGameStart()
        if ret:
            self.onClickRecordStart()

    def home(self):
        
        self.layout_base = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(self.layout_base)

        self.group_game = QGroupBox("Game")
        self.layout_base.addWidget(self.group_game)
        layout = QHBoxLayout()
        self.group_game.setLayout(layout)
        self.list_game = QComboBox()
        self.reload_gamelist()
        self.list_game.activated[str].connect(self.onActivated)
        self.btn_reload_gamelist = QPushButton('reload list')
        self.btn_reload_gamelist.clicked.connect(self.reload_gamelist)
        layout.addWidget(QLabel("Game : "))
        layout.addWidget(self.list_game)
        layout.addWidget(self.btn_reload_gamelist)

        self.group_resolution = QGroupBox()
        layout = QHBoxLayout()
        self.layout_base.addWidget(self.group_resolution)
        self.group_resolution.setLayout(layout)
        self.lb_width = QLineEdit()
        self.lb_width.returnPressed.connect(self.onTextEditWidth)
        layout.addWidget(QLabel("Width : "))
        layout.addWidget(self.lb_width)
        self.lb_height = QLineEdit()
        self.lb_height.returnPressed.connect(self.onTextEditHeight)
        layout.addWidget(QLabel("Height : "))
        layout.addWidget(self.lb_height)
        
        self.buttonGrp = QGroupBox()
        self.layout_base.addWidget(self.buttonGrp)
        layout = QHBoxLayout()
        self.btn_game_start = QPushButton('play game')
        self.btn_game_start.clicked.connect(self.onClickGameStart)
        self.btn_record_start = QPushButton('start recording')
        self.btn_record_start.clicked.connect(self.onClickRecordStart)
        self.btn_play_game_and_record = QPushButton("run game and recoding")
        self.btn_play_game_and_record.clicked.connect(self.onClickAllRun)
        layout.addWidget(self.btn_game_start)
        layout.addWidget(self.btn_record_start)
        layout.addWidget(self.btn_play_game_and_record)
        self.buttonGrp.setLayout(layout)
         

        self.show()


if __name__ == "__main__":  # had to add this otherwise app crashed

    def run():
        app = QApplication(sys.argv)
        Gui = window()
        sys.exit(app.exec_())

run()
