import sys, os, subprocess, time
from xml.etree.ElementTree import parse, Element, ElementTree, SubElement, dump
from Quartz import (CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog, QGroupBox
from PyQt5.QtWidgets import QFormLayout, QBoxLayout, QHBoxLayout
from pynput import mouse
from pynput.mouse import Button, Controller

class window(QWidget):

    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle('Game Recording Launcher')
        self.setFixedWidth(640)
        self.setFixedHeight(480)
        
        self.layout_base = None

        self.current_game_location = None
        self.current_game = None
        self.group_game = None
        self.list_game = None
        self.btn_reload_gamelist = None
        self.btn_open_games_folder = None
        self.btn_hand_images = None

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
        self.current_game = app
        execute_file_folder = os.getcwd() + '/games/' + text + "/Contents/MacOS/"
        files = os.listdir(execute_file_folder)
        self.current_game_location = os.getcwd()+'/games/'+text+'/Contents/MacOS/'+files[0]
        print 'current item : '+text
        print 'current app location : '+self.current_game_location

    def reload_gamelist(self):
        files = os.listdir(os.getcwd()+'/games/')
        valid_games = self.validate_games(files)
        if len(valid_games) == 0:
            self.open_popup('Warning!', "Any games are not in /games folder!\n Please insert games in the folder")
            return

        self.list_game.clear()
        self.list_game.addItems(valid_games)
        app = valid_games[0].split('.app')[0]
        self.current_game = app
        execute_file_folder = os.getcwd() + '/games/' + valid_games[0] + "/Contents/MacOS/"
        files = os.listdir(execute_file_folder)
        self.current_game_location = os.getcwd()+'/games/'+valid_games[0]+'/Contents/MacOS/'+files[0]
        print 'current item : '+files[0]
        print 'current app location : '+self.current_game_location
    
    def validate_games(self, files):
        games = []
        for f in files:
            name = f.split('.app')[0]
            execute_file_folder = os.getcwd() + '/games/' + f + '/Contents/MacOS/'
            if not os.path.isdir(execute_file_folder):
                continue

            files = os.listdir(execute_file_folder)
            if len(files) != 0:
                path = os.getcwd()+'/games/'+f+'/Contents/MacOS/'+files[0]
                print name
                print path
                if os.path.isfile(path):
                    games.append(f)
        return games
   
    def open_dir_games(self):
        folder_location = os.getcwd() + '/games/'
        subprocess.call(["open", "-R", folder_location])

    def open_dir_handimages(self):
        if self.current_game == None:
            self.open_popup('Warning!', "You didn't select any game.\nPlease select game first")
            return
        
        folder_location = os.getcwd() + '/games/' + self.current_game + '.app/Contents/Data/HandTextures/' 
        if os.path.isdir(folder_location) is False:
            self.open_popup('Invalid!', "This game doesn't have 'HandTextures' folder.\nPlease insert the folder")
            return
        
        subprocess.call(["open", "-R", folder_location])


    def onClickGameStart(self):
        if self.current_game_location != None and self.lb_width.text().isdigit() and self.lb_height.text().isdigit():
            self.width = float(self.lb_width.text())
            self.height = float(self.lb_height.text())
            command = self.current_game_location + ' -screen-width '+self.lb_width.text()+' -screen-height '+self.lb_height.text()
            #os.system(command)
            subprocess.Popen([command], shell=True)
            return True
        else:
            self.open_popup("Warning!!!", "Please set up resolution of game")
            return False

    def onClickRecordStart(self):
        applescript = os.getcwd() + '/AppleScripts/recorder_fullscreen.scpt'
        command = 'osascript ' + applescript
        os.system(command)

    def record_start(self):
        command = "pgrep -l %s | awk '{print $1}'" %(self.current_game)
        child = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        result = child.communicate()[0].strip()
        
        game_started = False
        options = kCGWindowListOptionOnScreenOnly
        geometry = None
        while game_started == False:
            window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
            for window in window_list:
                pid = window['kCGWindowOwnerPID']
                if str(result) == str(pid):
                    geometry = window['kCGWindowBounds']
                    print geometry
                    game_started = True
        
        applescript = os.getcwd()+'/AppleScripts/recorder_gameframe.scpt'
        command = 'osascript '+applescript
        os.system(command)
        mouse =Controller()
        time.sleep(0.3)
        mouse.position = (geometry['X'], geometry['Y']+(geometry['Height']-self.height))
        time.sleep(0.3)
        print 'start : ('+str(geometry['X'])+', '+str(geometry['Y']+(geometry['Height']-self.height))+')'
        mouse.press(Button.left)
        time.sleep(0.3)
        mouse.position = (geometry['X']+geometry['Width'], geometry['Y']+geometry['Height'])
        print 'start : ('+str(geometry['X']+geometry['Width'])+', '+str( geometry['Y']+geometry['Height'])+')'
        time.sleep(0.3)
        mouse.release(Button.left)
        time.sleep(0.3)
        mouse.position = ((2*geometry['X']+geometry['Width'])/2, (2*geometry['Y']+2*geometry['Height']-self.height)/2)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        

    def onClickAllRun(self):
        ret = self.onClickGameStart()
        if ret:
            self.record_start()
    
    def open_popup(self, title, text):
        QMessageBox.warning(self, title, text)

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
        self.btn_open_games_folder = QPushButton('open games folder')
        self.btn_open_games_folder.clicked.connect(self.open_dir_games)
        self.btn_hand_images = QPushButton('hand images')
        self.btn_hand_images.clicked.connect(self.open_dir_handimages)

        layout.addWidget(QLabel("Game : "))
        layout.addWidget(self.list_game)
        layout.addWidget(self.btn_reload_gamelist)
        layout.addWidget(self.btn_open_games_folder)
        layout.addWidget(self.btn_hand_images)

        self.group_resolution = QGroupBox("Resolution")
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
