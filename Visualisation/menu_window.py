import os

from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QPixmap, QMouseEvent, QFocusEvent, QDragEnterEvent
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.h = 500
        self.w = 350
        self.title_label = GameTitle(self, 25, 50)
        self.play_button = MainMenuButton(self, 25, 150)
        self.settings_button = MainMenuButton(self, 25, 250)
        self.exit_button = MainMenuButton(self, 25, 350)
        self.setGeometry(300, 100, self.w, self.h)
        self.setStyleSheet('''background-color: #0f0f0f''')
        self.show()

    def eventFilter(self, o: QObject, e: QEvent):
        if isinstance(o, MainMenuButton) and e.type() == QEvent.HoverEnter:
            print(f'hovered {o}')
        return super(self).eventFilter(o, e)


class MainMenuButton(QPushButton):
    def __init__(self, father: MenuWindow, x, y):
        super().__init__()
        self.setParent(father)
        self.setGeometry(x, y, father.w - 50, father.h // 6)
        self.show()

    def mousePressEvent(self, e: QMouseEvent):
        print('kek')

    def focusInEvent(self, e: QFocusEvent):
        print('lol')


class GameTitle(QLabel):
    def __init__(self, father: MenuWindow, x, y):
        super().__init__()
        self.setParent(father)
        self.setGeometry(x, y, father.w - 50, father.h // 6)
        self.img = QPixmap(os.path.join('../Resources', 'game_title.png'))
        self.setPixmap(self.img.scaled(father.w - 50, father.h // 6))
        self.show()
