#!/usr/bin/env python
import sys, os

from PyQt5.QtWidgets import QApplication

from GUI import GameWindow
from menu_window import MenuWindow
from game import Game


def main():
    with open(os.path.join('Levels', '1.txt'), 'r') as f:
        level = [i.strip() for i in f.readlines()]
    game = Game(level)
    app = QApplication(sys.argv)
    window = GameWindow(game)
    # menu_window = MenuWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
