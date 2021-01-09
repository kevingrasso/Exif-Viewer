import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPixmap
from model.TableModel import TableModel


""" max dimension that an image can have"""
MAX_WIDTH = 512
MAX_HEIGHT = 512


def _convert_to_degrees(value):
    """Convert the gps data of the exif to format searchable on google maps"""
    deg = float(value[0])
    minute = float(value[1])
    sec = float(value[2])
    return deg + (minute / 60.0) + (sec / 3600.0)


def get_exif(img):
    """return all exif data of an image"""
    return [[ExifTags.TAGS[k], v]  for k, v in img._getexif().items() if k in ExifTags.TAGS]


class Model(QObject):
    def __init__(self):
        super().__init__()

        self._current_index = None
        self._filenames = None
        self._pixmap = None
        self._current_image = None
        self.imgQ = None


    def filenames(self):
        """Return the filename of the image"""
        return self._filenames

    def set_filenames(self, val):
        """Set the filename of the image"""
        if len(val) != 0:
            self._filenames = val
            self._current_index = 0

    def gen_pixmap(self, width, height, index=0, angle=0, resize=False):
        """return the pixmap of the image"""
        if self._current_index is not None:
            if index == 1:
                self._current_index = (self._current_index + 1) % (len(self._filenames))
            elif index == -1 and self._current_index > 0:
                self._current_index = self._current_index - 1
            elif index == -1 and self._current_index == 0:
                self._current_index = len(self._filenames) - 1

            if angle != 0:
                """rotate the image by an 'angle'  """
                self._current_image = self._current_image.rotate(angle=angle, expand=True)

            if not resize and angle == 0:
                self._current_image = Image.open(self._filenames[self._current_index])

            self.imgQ = ImageQt.ImageQt(self._current_image)
            pixmap = QPixmap.fromImage(self.imgQ)
            size = QtCore.QSize(min(width, MAX_WIDTH), min(height, MAX_HEIGHT))         
            self._pixmap = pixmap.scaled(size, Qt.KeepAspectRatio)                  #resize the pixmap of the image mantaining aspect ratio
        return self._pixmap, self._filenames[self._current_index].split('/')[-1]

    def get_data(self):
        """return the model to be loaded on table"""
        if self._current_image is not None:
            self._current_image.load()
            exif = get_exif(self._current_image)
            return TableModel(exif)

    def get_gps_info(self):
        """return gps info from exif data in the form 'latitude,longitude' """
        gps = {}
        for k, v in self._current_image._getexif().items():
            for k1, v1 in ExifTags.TAGS.items():
                if k == k1 and v1 == 'GPSInfo':
                    gps = v
        gps_info = {}
        for key in gps.keys():
            decode = ExifTags.GPSTAGS.get(key, key)
            gps_info[decode] = gps[key]
        if len(gps_info) >= 4:
            lat = _convert_to_degrees(gps_info['GPSLatitude'])
            long = _convert_to_degrees(gps_info['GPSLongitude'])
            return str(lat) + ',' + str(long)
        else:
            return None

    def open_location(self):
        """This function shows the location on google maps on the browser"""
        gps = self.get_gps_info()
        if gps is not None:
            webbrowser.open_new('https://www.google.com/maps/search/?api=1&query=' + gps)
