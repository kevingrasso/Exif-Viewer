import sys
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QShortcut, QAbstractItemView
from views.Ui_MainWindow import Ui_MainWindow
from PIL import Image, ImageQt
from PIL import ExifTags
from model.TableModel import TableModel
from FileDialog import FileDialog
from pyqt5_material import apply_stylesheet

MAX_WIDTH = 512
MAX_HEIGHT = 512


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.filenames = []
        self.current_image = None
        self.current_index = -1
        self.ui.img_name.setText('No files selected')
        self.current_gps_data = None
        self.ui.bt_next.setEnabled(False)
        self.ui.bt_prev.setEnabled(False)
        self.ui.bt_right.setEnabled(False)
        self.ui.bt_left.setEnabled(False)
        self.ui.gps_button.setEnabled(False)

        self.ui.gps_button.clicked.connect(self._open_google)

        self.ui.bt_next.clicked.connect(self.next_image)
        self.quick_next = QShortcut(QKeySequence('right'), self)
        self.quick_next.activated.connect(self.next_image)
        self.ui.bt_prev.clicked.connect(self.prev_image)
        self.quick_prev = QShortcut(QKeySequence('left'), self)
        self.quick_prev.activated.connect(self.prev_image)

        self.ui.bt_right.clicked.connect(self.right_rotate)
        self.quick_rt = QShortcut(QKeySequence('Ctrl+right'), self)
        self.quick_rt.activated.connect(self.right_rotate)

        self.ui.bt_left.clicked.connect(self.left_rotate)
        self.quick_lt = QShortcut(QKeySequence('Ctrl+left'), self)
        self.quick_lt.activated.connect(self.left_rotate)

        self.ui.actionOpen_file.triggered.connect(self.load_files)
        self.ui.actionExit.triggered.connect(self.close)

    def resizeEvent(self, event):
        self.load_image()
        QMainWindow.resizeEvent(self, event)

    def next_image(self):
        if len(self.filenames) != 0 and self.current_index == -1:
            self.current_index = 0
            self.current_image = Image.open(self.filenames[self.current_index])
            self.load_image()
            self.show_data()
            self.ui.img_name.setText(self.filenames[self.current_index].split('/')[-1])
        elif len(self.filenames) != 0 and self.current_index != -1:
            self.current_index = (self.current_index + 1) % (len(self.filenames))
            self.current_image = Image.open(self.filenames[self.current_index])
            self.load_image()
            self.show_data()
            self.ui.img_name.setText(self.filenames[self.current_index].split('/')[-1])
        else:
            print('No files selected')

    def prev_image(self):
        if len(self.filenames) != 0 and (self.current_index == -1 or self.current_index == 0):
            self.current_index = len(self.filenames) - 1
            self.current_image = Image.open(self.filenames[self.current_index])
            self.load_image()
            self.show_data()
            self.ui.img_name.setText(self.filenames[self.current_index].split('/')[-1])
        elif len(self.filenames) != 0 and self.current_index != -1:
            self.current_index = self.current_index -1
            self.current_image = Image.open(self.filenames[self.current_index])
            self.load_image()
            self.show_data()
            self.ui.img_name.setText(self.filenames[self.current_index].split('/')[-1])
        else:
            print('No files selected')

    def load_image(self):
        img = self.current_image
        if img is not None:
            self.imgQ = ImageQt.ImageQt(img)  # we need to hold reference to imgQ, or it will crash

            pix_map = QPixmap.fromImage(self.imgQ)
            size = QtCore.QSize(min(self.ui.img_label.width(), MAX_WIDTH), min(self.ui.img_label.height(), MAX_HEIGHT))
            pix_map = pix_map.scaled(size, Qt.KeepAspectRatio)

            self.ui.img_label.setPixmap(pix_map)

    def right_rotate(self):
        if self.current_image is not None:
            self.current_image = self.current_image.rotate(angle=-90, expand=True)
            self.load_image()
        else:
            print('No files selected')

    def left_rotate(self):
        if self.current_image is not None:
            self.current_image = self.current_image.rotate(angle=90, expand=True)
            self.load_image()
        else:
            print('No files selected')

    def show_data(self):
        self.current_image.load()

        exif = [
            [ExifTags.TAGS[k], v]
            for k, v in self.current_image._getexif().items()
            if k in ExifTags.TAGS
        ]
        self.current_gps_data = self.get_gps_info()

        model = TableModel(exif)
        self.ui.tableView.setModel(model)
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def get_gps_info(self):
        for k, v in self.current_image._getexif().items():
            for k1, v1 in ExifTags.TAGS.items():
                if k == k1 and v1 == 'GPSInfo':
                    gps = v
        gpsinfo = {}
        for key in gps.keys():
            decode = ExifTags.GPSTAGS.get(key, key)
            gpsinfo[decode] = gps[key]
        if len(gpsinfo)>=4:
            lat = self._convert_to_degrees(gpsinfo['GPSLatitude'])
            long = self._convert_to_degrees(gpsinfo['GPSLongitude'])
            self.ui.gps_button.setEnabled(True)
            self.ui.gps_button.setText('View Location')
            return str(lat) + ',' +str(long)
        else:
            self.ui.gps_button.setEnabled(False)
            self.ui.gps_button.setText('No GPS data available')
            print('No data available')
            return None

    def _convert_to_degrees(self, value):
        deg = float(value[0])
        minute = float(value[1])
        sec = float(value[2])
        return deg + (minute / 60.0) + (sec / 3600.0)

    def _open_google(self):
        if self.current_gps_data is not None:
            webbrowser.open('https://www.google.com/maps/search/?api=1&query=' + self.current_gps_data)

    @QtCore.pyqtSlot()
    def load_files(self):
        caption = 'Open files'
        directory = './'
        filter_mask = "JPEG File Interchange Format (*.jpg *.jpeg *jfif)|" + "*.jpg;*.jpeg;*.jfif"
        filenames = FileDialog.getOpenFileNames(None, caption, directory, filter_mask)[0]
        self.filenames = filenames

        if len(filenames) == 1:
            self.ui.bt_next.setEnabled(False)
            self.ui.bt_prev.setEnabled(False)
            self.ui.bt_right.setEnabled(True)
            self.ui.bt_left.setEnabled(True)
        elif len(filenames) > 1:
            self.ui.bt_next.setEnabled(True)
            self.ui.bt_prev.setEnabled(True)
            self.ui.bt_right.setEnabled(True)
            self.ui.bt_left.setEnabled(True)

        self.next_image()

    def show(self):
        window = MainWindow()
        apply_stylesheet(app, theme='dark_blue.xml')
        window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_blue.xml')

    window.show()
    sys.exit(app.exec_())

