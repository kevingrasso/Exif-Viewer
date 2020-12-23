import sys
from PyQt5.QtWidgets import QApplication
from views.MainView import MainWindow
from model.Model import Model
# from pyqt5_material import apply_stylesheet


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.model = Model()
        self.view = MainWindow(self.model)

        self.view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    css = "views/style.qss"
    with open(css, "r") as fh:
        app.setStyleSheet(fh.read())

    # apply_stylesheet(app, theme='dark_blue.xml')
    sys.exit(app.exec_())

