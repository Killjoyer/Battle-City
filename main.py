import sys

from PyQt5.QtWidgets import QApplication

from GUI import GameWindow
from game import Game


def main():
    level = ['           ',
             '#          ',
             ' # # # ### ',
             ' #         ',
             ' #         ',
             ' #         ',
             '    #      ',
             '           ']
    game = Game(8, 8, level)
    app = QApplication(sys.argv)
    window = GameWindow(game)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
