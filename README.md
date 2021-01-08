# Exif-Viewer

# Overview

- **Academic Year**: 2020-2021
- **Student**: Kevin Grasso
- **CFUs**: 9

In this assignment it was implemented an Image and EXIF Metadata Viewer using python.

# Requirements

- **Python version**: Python 3.8.3  \[\1]
- **Pyqt5**: Pyqt 5.15.2  \[\2]
- **Pillow**: Pillow 7.2.0  \[\3]


# Summary
I used pyqt5 for the implementation of the interface and Pillow library to retrieve the information regarding Exif Metadata of an image, and to make operations with images, like rotation and resizing.

# Files
```bash
|---model
|   |---Model.py
|   |---TableModel.py
|---views
|   |---Ui_Dialog.py
|   |---UiMainWindow.py
|   |---MainView.py
|   |---dialog.ui
|   |---mainWindow.ui
|   |---style.qss
|-Exif_app.py
```


# Bibliography

\[1\] https://www.python.org/

\[2\] https://www.riverbankcomputing.com/static/Docs/PyQt5/

\[3\] https://pillow.readthedocs.io/en/stable/

\[4\]https://github.com/ianare/exif-samples/tree/master/jpg/gps


## Install the dependencies
```bash
pip install PyQt5
pip install Pillow
```
## Run
```bash
python Exif_app.py
```

