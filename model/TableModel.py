from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class TableModel(QStandardItemModel):
    """Reimplementation of Table Model to adapt to our data"""

    def __init__(self, data):
        super(TableModel, self).__init__(len(data), len(data[0]))
        self._data = data
        self.populate()

    def populate(self):
        for value in self._data:
            row = []
            for item in value:
                cell = QStandardItem(str(item))
                row.append(cell)
            self.appendRow(row)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            value = str(value)
            return value

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
