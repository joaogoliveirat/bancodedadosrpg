from PyQt5.QtWidgets import QApplication
from main_menu import MainMenu

if __name__ == '__main__':
    app = QApplication([])
    main_menu = MainMenu()
    main_menu.show()
    app.exec_()
