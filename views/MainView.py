from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAbstractItemView, \
    QHeaderView, QShortcut, QPushButton, QDialog
from views.Ui_MainWindow import Ui_MainWindow
from views.Ui_Dialog import Ui_Dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._aboutDialog = AboutDialog()

        self.initialize()
        
        self._open_btn.clicked.connect(self.open_slot)
        self._ui.actionOpen_file.triggered.connect(self.open_slot)
        self._ui.actionExit.triggered.connect(self.close)
        self._ui.actioninfo.triggered.connect(self._aboutDialog.exec_)
        self._quit = QShortcut(QKeySequence("esc"), self)
        self._quit.activated.connect(self.close)

        self._ui.bt_next.clicked.connect(lambda: self.refresh_images(index=1))
        self._next_sc = QShortcut(QKeySequence("right"), self)
        self._next_sc.activated.connect(lambda: self.refresh_images(index=1))

        self._ui.bt_prev.clicked.connect(lambda: self.refresh_images(index=-1))
        self._prev_sc = QShortcut(QKeySequence("left"), self)
        self._prev_sc.activated.connect(lambda: self.refresh_images(index=-1))

        self._ui.bt_right.clicked.connect(lambda: self.refresh_images(angle=-90))
        self._right_sc = QShortcut(QKeySequence("Ctrl+right"), self)
        self._right_sc.activated.connect(lambda: self.refresh_images(angle=-90))

        self._ui.bt_left.clicked.connect(lambda: self.refresh_images(angle=90))
        self._left_sc = QShortcut(QKeySequence("Ctrl+left"), self)
        self._left_sc.activated.connect(lambda: self.refresh_images(angle=90))

        self._ui.gps_button.clicked.connect(self._model.open_location)

    def initialize(self):
        """Set the buttons to not clickable when the application starts"""
        self._ui.img_name.setText('No files selected')
        self._ui.bt_next.setEnabled(False)
        self._ui.bt_prev.setEnabled(False)
        self._ui.bt_right.setEnabled(False)
        self._ui.bt_left.setEnabled(False)
        self._ui.gps_button.setEnabled(False)

        self._open_btn = QPushButton('Open File', self._ui.img_label)
        self.adjustSize()

    @QtCore.pyqtSlot()
    def open_slot(self):
        """This function open the file dialog and sets visibility of the buttons"""
        caption = 'Open files'
        directory = './'
        filter_mask = "JPEG File Interchange Format (*.jpg *.jpeg *jfif)|" + "*.jpg;*.jpeg;*.jfif"
        files = QFileDialog.getOpenFileNames(None, caption, directory, filter_mask)[0]
        self._model.set_filenames(files)
        if len(files) > 1:
            self._ui.bt_next.setEnabled(True)
            self._ui.bt_prev.setEnabled(True)
            self._ui.bt_right.setEnabled(True)
            self._ui.bt_left.setEnabled(True)
        elif len(files) == 1:
            self._ui.bt_left.setEnabled(True)
            self._ui.bt_right.setEnabled(True)
            self._ui.bt_next.setEnabled(False)
            self._ui.bt_prev.setEnabled(False)
        else:
            self._ui.bt_left.setEnabled(False)
            self._ui.bt_right.setEnabled(False)
            self._ui.bt_next.setEnabled(False)
            self._ui.bt_prev.setEnabled(False)

        self.refresh_images()

    @QtCore.pyqtSlot()
    def refresh_images(self, index=0, angle=0, resize=False):
        """This function reload the view of the image """
        if self._model.filenames() is None:
            """Set to visible the open button and centered it in the image_label"""
            self._open_btn.setVisible(True)
            x = (self._ui.img_label.width() / 2) - (self._open_btn.width() / 2)
            y = (self._ui.img_label.height() / 2) - (self._open_btn.height() / 2)
            self._open_btn.move(x, y)
        else:
            """Set open button visibility to false, and show the image in the image_label"""
            self._open_btn.setVisible(False)
            pixmap, name_file = self._model.gen_pixmap(self._ui.img_label.width(), \
                 self._ui.img_label.height(), index, angle, resize)
            self._ui.img_label.setPixmap(pixmap)
            self._ui.img_name.setText(name_file)

            if angle == 0 and resize is not True:
                self._ui.tableView.setModel(self._model.get_data())
                self._ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self._ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)

                for i in range(self._ui.tableView.model().columnCount(0)):
                    self._ui.tableView.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
                gps = self._model.get_gps_info()
                if gps is None:
                    self._ui.gps_button.setEnabled(False)
                    self._ui.gps_button.setText('No GPS data available')
                else:
                    self._ui.gps_button.setEnabled(True)
                    self._ui.gps_button.setText('View Location')

    def resizeEvent(self, event):
        """Reimplementation of the resize event with the call to refresh_images"""
        self.refresh_images(resize=True)
        QMainWindow.resizeEvent(self, event)


class AboutDialog(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Set up the user interface from Designer."""
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
