#!/usr/bin/env python
import sys

from PyQt5.QtWidgets import QApplication

from GUI import GameWindow
from game import Game


def main():
    level = ['           ',
             '#      x   ',
             ' # # # ### ',
             ' #     x   ',
             ' #     x   ',
             ' #     x   ',
             '    #      ',
             '           ']
    game = Game(level)
    app = QApplication(sys.argv)
    window = GameWindow(game)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
