from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt


class PointCounter(QWidget):
    def __init__(self, father):
        super().__init__(father)
        self.setGeometry((father.width() - father.cell_size) // 2, 0,
                         father.cell_size, father.cell_size)
        self.label = QLabel(self)
        self.label.setStyleSheet(f'\
        background-color: rgb(59, 59, 59);\
        color: rgb(200, 200, 200);\
        font-size: {father.cell_size // 2}px;\
        ')
        self.label.show()
        self.label.resize(father.cell_size, father.cell_size)
        self.label.setNum(0)
        self.show()
        self.label.setAlignment(Qt.AlignCenter)

    def set_points(self, points: int) -> None:
        self.label.setNum(points)
