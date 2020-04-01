from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from constants import Bullets
from tank import Bullet


class BulletVisualisation(QWidget):
    def __init__(self, father, bullet: Bullet):
        super().__init__(father, bullet)
