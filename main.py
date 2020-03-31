#!/usr/bin/env python
import sys, os

from PyQt5.QtWidgets import QApplication

from Visualisation.game_window import GameWindow
from game import Game


def main():
    with open(os.path.join('Levels', '2.txt'), 'r') as f:
        level = [i.strip() for i in f.readlines()]
    game = Game(level)
    app = QApplication(sys.argv)
    window = GameWindow(game)
    # menu_window = MenuWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
