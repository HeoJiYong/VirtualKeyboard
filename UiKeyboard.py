'''
# Name : keyboard.py
# Version : ver1.0
# Developer : HeoJiYong
# Modify Date : 2020. 02. 26   15:08
# Description : 라즈베리용 가상키보드
# 변경사항 : 1. 한/영, 쉬프트, 특수문자 전환방식 변경,
#           2. & 출력오류 해결
#           3. 언어, 특수문자를 리스트 형태로 재정의
#           4. 키 입력시 효과 추가
# ----To Do----
# 1. 취소 = 12폰트, Cancel = 10폰트 상태, 추후 업데이트 필요해보임
# 2. TextBox 위에 라벨추가
# 3. 창의 테두리(?) 없애기 (라즈베리에서 실행시엔 안보일 수 도 있음)
# 4. 커서표시도 되면 좋을것 같음
# 5. 지우기버튼 누르고있을때 계속지우기

# 메모 : languages[is_shift][] 형태로 한/영 전환, 특수문자도 special[is_shift][] 형태로, 나중에 특수문자에도 shift 기능 추가가능.
        shift는 현재 bool 형식이므로 int 변환시 (0,1) 로만 사용가능, 추후에 자료형만 바꾸면 특수문자+shift 로 3가지 이상 조합가능

        버튼에 아이콘 등의 설정 : https://editor752.tistory.com/44
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
import Hangul
#
import time

#INPUT_TXT = ""

'''
#------------ 쓸모없어보여서 지웠지만 혹시나해서 놔둔 부분 ------------
class VKQLineEdit(QLineEdit):
    def __init__(self, parent=None, name=None, mainWindowObj=None):
        super(VKQLineEdit, self).__init__(parent)
        self.name = name
        self.setFixedHeight(40)
        self.mainWindowObj = mainWindowObj
        self.setFocusPolicy(Qt.ClickFocus)

    def focusInEvent(self, e):
        self.mainWindowObj.keyboardWidget.currentTextBox = self
        self.mainWindowObj.keyboardWidget.show()

        #self.setStyleSheet("border: 1px solid red;")
        super(VKQLineEdit, self).focusInEvent(e)

    def mousePressEvent(self, e):
        # print(e)
        # self.setFocusPolicy(Qt.ClickFocus)
        super(VKQLineEdit, self).mousePressEvent(e)
'''

#--------------------------------------[ 클래스 정의 ]-----------------------------------------
#class Keyboard(QWidget):
class Keyboard(QDialog):
    
    def __init__(self, parent, title):
        super(Keyboard , self).__init__(parent)
        self.HangulCombinater = Hangul.HangulCombination()
        #
        self.result = 0 # Cancel 
        self.inputData = ''
        #
        self.font = "Arial"
        self.font_size = 12
        self.window_width = 550
        self.window_heigh = 380
        self.key_width = 44
        self.key_height = 44

        self.setAutoFillBackground(True)
        self.layout = QGridLayout()
        self.setGeometry(120, 50, self.window_width, self.window_heigh)
        self.setMinimumSize(self.window_width, self.window_heigh)
        self.setMaximumSize(self.window_width, self.window_heigh)
        self.setWindowTitle("keyboard")
        #
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint) # 20200416 KHK - delete Title
        self.setWindowFlags(Qt.Window|Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint) # 20200416 KHK -> delete Title
        self.setStyleSheet("border:2px solid black; background-color:white")          # 20200416 KHK
        #
        self.setAutoFillBackground(True)

        self.titleLabel = QLabel()
        self.titleLabel.setMinimumSize(520,40)
        self.titleLabel.setMaximumSize(520,40)
        #self.titleLabel.setFont(QFont(self.font, self.font_size+4))
        self.titleLabel.setFont(QFont(self.font, self.font_size))
        self.titleLabel.setText(title)
        #self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        #self.titleLabel.setStyleSheet("QLabel{color:black; font:bold; border-radius:1px; border-width:1px; border-color:darkgray; border-style:solid;}")
        self.titleLabel.setStyleSheet("QLabel{border-width:0px color:gray;}")
        self.layout.addWidget(self.titleLabel, 0, 0, 1, 9)

        #self.text_box = QTextEdit()
        self.text_box = QLineEdit()
        self.text_box.setMinimumSize(520,40)
        self.text_box.setMaximumSize(520,40)
        self.text_box.setFont(QFont(self.font, self.font_size))
        #self.text_box.setStyleSheet("QLineEdit {background-color:white; color:black; border-radius:10px;}")
        self.text_box.setStyleSheet("QLineEdit {background-color:white; color:black; border-radius:1px;}")
        #self.layout.addWidget(self.text_box, 1, 0, 1, 9)
        self.layout.addWidget(self.text_box, 1, 0, 1, 1)

        #self.language_mode=[[],[],[]]-
        self.languages={
            "english":[["1","2","3","4","5","6","7","8","9","0","←",
                  "q","w","e","r","t","y","u","i","o","p","/",
                  "a","s","d","f","g","h","j","k","l","(",")",
                  "Shift","z","x","c","v","b","n","m","-","_","."],

                       ["1","2","3","4","5","6","7","8","9","0","←",
                      "Q","W","E","R","T","Y","U","I","O","P","/",
                      "A","S","D","F","G","H","J","K","L","(",")",
                      "Shift","Z","X","C","V","B","N","M","-","_","."]],

            "korean":[["1","2","3","4","5","6","7","8","9","0","←",
                      "ㅂ","ㅈ","ㄷ","ㄱ","ㅅ","ㅛ","ㅕ","ㅑ","ㅐ","ㅔ","/",
                      "ㅁ","ㄴ","ㅇ","ㄹ","ㅎ","ㅗ","ㅓ","ㅏ","ㅣ","(",")",
                      "Shift","ㅋ","ㅌ","ㅊ","ㅍ","ㅠ","ㅜ","ㅡ","-","_","."],

                      ["1","2","3","4","5","6","7","8","9","0","←",
                      "ㅃ","ㅉ","ㄸ","ㄲ","ㅆ","ㅛ","ㅕ","ㅑ","ㅐ","ㅔ","/",
                      "ㅁ","ㄴ","ㅇ","ㄹ","ㅎ","ㅗ","ㅓ","ㅏ","ㅣ","(",")",
                      "Shift","ㅋ","ㅌ","ㅊ","ㅍ","ㅠ","ㅜ","ㅡ","-","_","."]
                      ]
        }
        self.special={"special":[
            ["1","2","3","4","5","6","7","8","9","0","←",
                      "!","@","#","$","%","^","＆","*","<",">","?",
                      "\\","□","■","◎","○","●",":",";","=","{","}",
                      "Shift","☆","★","♡","♥","※","§","|","+","[","]"],
            []
        ]}
        self.present_language="english"
        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.pressKey)

        self.positions = [(i + 2, j) for i in range(6) for j in range(11)]
        #self.language = self.english
        self.is_special=False
        self.is_shift=False

        self.button = list()
        #self.key_shift = None
        self.key_special = None
        self.key_changelanguage=None
        self.key_space = None
        self.key_enter = None
        self.key_cancel = None
        #self.key_backspace = None

        self.printKey(self.languages[self.present_language][self.is_shift],self.positions,False)

        #self.show() # 20200416 khk

    def __del__(self):
        print("키보드 객체 소멸")


    #------------------------------------{ 클래스의 함수부분 }---------------------------------

    #--------------------------------------키출력
    def printKey(self, language,positions,is_change=True):

        '''키보드 처음 호출할 때'''
        if not is_change:
            self.setLayout(self.layout)
            for position, name in zip(positions, language):
                if name == '':
                    continue
                button = QPushButton(name)
                button.setFont(QFont(self.font, self.font_size))
                button.setFixedHeight(self.key_height)
                button.setFixedWidth(self.key_width)
                button.setStyleSheet("QPushButton{ border-radius:5px;"
                                                    "border-width: 1px;"
                                                    #"border-color:beige;"
                                                    "border-color:darkgray;"
                                                    "border-style:solid;"
                                                    "color:black;"
                                                    "background-color:white;}"
                                     "QPushButton:pressed{background-color:gray; color:white}")

                #문자키 인경우
                if (len(name) == 1)and (name != '←'):
                    button.KEY_CHAR = ord(name)
                    button.clicked.connect(self.signalMapper.map)
                    self.signalMapper.setMapping(button, button.KEY_CHAR)
                    self.layout.addWidget(button, *position)
                #그 외 키 인경우
                else:
                    if (name=='Shift'):
                        button.KEY_CHAR = Qt.Key_Shift
                        button.clicked.connect(self.pressShift)

                    elif (name=='←'):
                        button.KEY_CHAR = Qt.Key_Backspace
                        button.clicked.connect(self.pressBackspace)
                    self.layout.addWidget(button, *position, 1, 2)
                self.button.append(button)
                #self.button = button

            # 특문키 생성
            key_special = QPushButton('!#?')
            key_special.setFont(QFont(self.font, self.font_size))
            key_special.setFixedHeight(self.key_height)
            #key_special.setFixedWidth(self.key_width*(1.6))
            key_special.setFixedWidth(self.key_width)
            self.layout.addWidget(key_special, 7, 0, 1, 2)
            key_special.clicked.connect(self.pressSpecial)
            if not self.is_special:
                key_special.setStyleSheet("QPushButton { border-radius:1px; border-width: 1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
            else:
                key_special.setStyleSheet("QPushButton { border-radius:1px; border-width: 1px; border-color:darkgray; color:white; background-color:gray;} QPushButton:pressed{background-color:gray; color:white}")
            self.key_special = key_special

            # 한/영키 생성
            if self.present_language == "korean":
                key_changelanguage = QPushButton('English')
            elif self.present_language == "english":
                key_changelanguage = QPushButton('한글')
            key_changelanguage.setFixedHeight(self.key_height)
            key_changelanguage.setFont(QFont(self.font, self.font_size))
            self.layout.addWidget(key_changelanguage, 7, 1, 1, 2)
            key_changelanguage.clicked.connect(self.pressChangeLanguage)
            key_changelanguage.setStyleSheet("QPushButton { border-radius:1px; border-width:1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
            self.key_changelanguage = key_changelanguage

            # 스페이스바 생성
            key_space = QPushButton('SPACE')
            key_space.setFixedHeight(self.key_height)
            key_space.setFont(QFont(self.font, self.font_size))
            key_space.KEY_CHAR = Qt.Key_Space
            self.layout.addWidget(key_space, 7, 3, 1, 5)
            key_space.clicked.connect(self.pressSpace)
            self.signalMapper.setMapping(key_space, key_space.KEY_CHAR)
            key_space.setStyleSheet("QPushButton { border-radius:1px; border-width:1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
            self.key_space = key_space

            # 취소 생성
            key_cancel = QPushButton('Cancel')
            key_cancel.setFixedHeight(self.key_height)
            key_cancel.setFont(QFont(self.font, self.font_size-2))
            self.layout.addWidget(key_cancel, 7, 8, 1, 2)
            key_cancel.clicked.connect(self.pressCancel)
            key_cancel.setStyleSheet("QPushButton { border-radius:1px; border-width:1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
            #key_clear.setFixedWidth(self.key_width*(1.6))
            key_cancel.setFixedWidth(self.key_width)
            self.key_cancel = key_cancel

            # 확인 생성
            key_enter = QPushButton('Enter')
            key_enter.setFixedHeight(self.key_height)
            key_enter.setFont(QFont(self.font, self.font_size))
            #key_enter.KEY_CHAR = Qt.Key_Home
            self.layout.addWidget(key_enter, 7, 9, 1, 2)
            key_enter.clicked.connect(self.pressEnter)
            #self.signalMapper.setMapping(key_enter, done_button.KEY_CHAR)
            key_enter.setStyleSheet("QPushButton { border-radius:1px; border-width:1px; border-color:darkgray; color:black; background-color:white; } QPushButton:pressed{background-color:gray; color:white}")
            key_enter.setFixedWidth(self.key_width*2.2)
            self.key_enter = key_enter


            '''키보드를 처음 호출한게 아니라면 버튼의 값만 바꾸면 된다.'''
        else:
            for btn,name in zip(self.button, language):
                if name == '':
                    continue
                #문자키 인경우
                if (len(name) == 1)and (name != '←'):
                    btn.setText(name)               #버튼의 글자
                    #btn.KEY_CHAR = ord(name)
                    #self.signalMapper.setMapping(btn, btn.KEY_CHAR)
                    self.signalMapper.setMapping(btn, ord(name))    #버튼속 값 (위의 두줄 합친것)
                    if (name == "＆"):
                        self.signalMapper.setMapping(btn,ord("&"))

                #그 외 키 인경우
                else:
                    if (name=='Shift'):
                        if not self.is_shift:
                            btn.setStyleSheet("QPushButton { border-radius:5px; border-width: 1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
                        else:
                            btn.setStyleSheet("QPushButton { border-radius:5px; border-width: 1px; border-color:darkgray; color:white; background-color:gray;} QPushButton:pressed{background-color:gray; color:white}")
                  #  elif(name=="&"):
                  #      print("asfawfwafawf")
                

            #특수한 키에대한 버튼액션
            if not self.is_special:
                self.key_special.setStyleSheet("QPushButton { border-radius:5px; border-width: 1px; border-color:darkgray; color:black; background-color:white;} QPushButton:pressed{background-color:gray; color:white}")
            else:
                self.key_special.setStyleSheet("QPushButton { border-radius:5px; border-width: 1px; border-color:darkgray; color:white; background-color:gray;} QPushButton:pressed{background-color:gray; color:white}")

            if self.present_language == "korean":
                self.key_changelanguage.setText("ABC")
                self.key_enter.setText("확인")
                self.key_space.setText("띄어쓰기")
                self.key_cancel.setText("취소")
                self.key_cancel.setFont(QFont(self.font, self.font_size))
                
            elif self.present_language == "english":
                self.key_changelanguage.setText("가나다")
                self.key_enter.setText("Enter")
                self.key_space.setText("SPACE")
                self.key_cancel.setText("Cancel")
                self.key_cancel.setFont(QFont(self.font, self.font_size-2))



    #--------------------------------------쉬프트
    def pressShift(self):
        #print("Shift 입력\n",)
        #한/영 : Q
        #shift : Toggle
        #특문   : Reset
        self.is_special = False
        self.is_shift = not(self.is_shift)  #Shift 토글
        self.printKey(self.languages[self.present_language][int(self.is_shift)],self.positions)
        pass

    #--------------------------------------특문키
    def pressSpecial(self):
        #print("특수문자 입력")
        #한/영 : Q
        #shift : Reset
        #특문   : Toggle
        self.is_shift = False
        self.is_special = not(self.is_special)

        if self.is_special:
            self.printKey(self.special["special"][int(self.is_shift)],self.positions)
        else:
            self.printKey(self.languages[self.present_language][self.is_shift],self.positions)
        pass

    #--------------------------------------한영키
    def pressChangeLanguage(self):
        #print("한영키 입력")
        #한/영 : Toggle
        #shift : Reset
        #특문   : Reset
        self.is_shift = False
        self.is_special = False
        if self.present_language == 'english':
            self.present_language = 'korean'
        elif self.present_language == 'korean':
            self.present_language = 'english'
        else:
            print("알 수 없는 언어값")
        self.printKey(self.languages[self.present_language][int(self.is_shift)], self.positions)
        pass

    #--------------------------------------스페이스바
    def pressSpace(self):
        #print("스페이스바 입력")
        #txt = self.text_box.toPlainText()
        txt = self.text_box.text()
        txt += ' '
        self.text_box.setText(txt)
        #기존 스페이스바 기능 이용
        pass

    #--------------------------------------클리어
    def pressCancel(self):
        '''
        print("클리어 입력")
        txt = self.text_box.toPlainText()
        txt = ""
        self.text_box.setText(txt)
        #기존 클리어 이용
        '''
        self.result = 0 # Cancel
        self.close()    # 20200416 -Khk
        pass

    #--------------------------------------엔터
    def pressEnter(self):
        #print("엔터 입력")
        self.result = 1 # Enter 
        self.inputData = self.text_box.text()

        #QCoreApplication.quit()

        self.close()    # 20200416 -Khk
        #기존 엔터키 이용
        pass

    #--------------------------------------백스페이스
    def pressBackspace(self):
        #print("백스페이스 입력")
        #txt = self.text_box.toPlainText()
        txt = self.text_box.text()
        txt = txt[:-1]
        self.text_box.setText(txt)
        #기존 백스페이스 이용
        pass

    #--------------------------------------문자키
    def pressKey(self, char_ord):
        #print("문자키 입력")
        #txt = self.text_box.toPlainText() #현재까지 입력된 문자열을 txt에 저장
        txt = self.text_box.text()          #txt에 새로 입력된 문자를 추가 -> 한글 계산 (한글모드이면 ~~)
        txt = self.HangulCombinater.smoothString(txt,chr(char_ord))
        #txt += chr(char_ord)                 #textBox 로 반환
        self.text_box.setText(txt)
        #기존 키입력 이용
        pass

#-------------------------------------------------------------------------------------------
# 20200416 khk
#--------------------------------------[ KeyBoard ]-----------------------------------------
# QMainWindow 에서는 QHBoxLayout, QVBoxLayout 같은 layout 사용못함
# -- QMainWindow 자체의 layout 사용한다. 
# 출처: https://freeprog.tistory.com/326 [취미로 하는 프로그래밍 !!!]
#-------------------------------------------------------------------------------------------
#class UiKeyboard(QMainWindow):
class UiKeyboard():
    def __init__(self, parent, title):
        try:
            #------------------------------------
            # DialogBox 생성
            #------------------------------------
            dlg = Keyboard(parent, title)
            dlg.exec_()
            #------------------------------------
            self.result = dlg.result # Enter 
            self.inputData = dlg.inputData
            #print('>>>>>>>>>>>>>>>>>>>>> result[%d], input Data[%s]', self.result, self.inputData) 

        except Exception as e:
            print('UiKeyboard Happened the exception > ', e)


#--------------------------------------[ 메인함수 ]-----------------------------------------
if __name__ == '__main__':
    app = QApplication([])
    ex = Keyboard(None,'키보드')
    ex.show()
    app.exec_()

    print("키보드 결과값 :", INPUT_TXT)
    sys.exit()
