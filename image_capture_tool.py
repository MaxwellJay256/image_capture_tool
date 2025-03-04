import cv2
import os
import sys

os.environ.update({"QT_QPA_PLATFORM_PLUGIN_PATH": \
                   "/home/jetson/anaconda3/envs/trashcan_2025/plugins/platforms"})
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
from Ui_image_capture_tool import Ui_ImageCaptureTool
from qfluentwidgets import *

class ImageCaptureTool(QWidget, Ui_ImageCaptureTool):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor("#ff6f4e")

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Unable to open camera")
            exit()
        
        self.label_camera.setScaledContents(True)
        
        # Connect signals and slots
        self.lineEdit_tag.textChanged.connect(self.updateFileName)
        self.spinBox_FileNumber.valueChanged.connect(self.updateFileName)
        self.pushButton_Reset.clicked.connect(self.resetFileNumber)
        self.button_capture.clicked.connect(self.saveImage)
        self.button_exit.clicked.connect(self.exit)

        # Bind shortcut keys
        self.shortcut_capture = QShortcut(QKeySequence("S"), self)
        self.shortcut_capture.activated.connect(self.saveImage)
        self.shortcut_exit = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut_exit.activated.connect(self.exit)

        self.save_dir_default = os.path.join(os.path.expanduser("~"), "Pictures")

        self.updatePeriod = 10 # ms
        self.updateFileName()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerUpdateEvent)
        self.timer.start(self.updatePeriod)


    def timerUpdateEvent(self):
        # Capture image from camera and display
        ret, frame = self.cap.read()
        if not ret:
            print("Unable to capture image")
            return
        # Convert cv image to Qt image
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Resize image to fit label size (maintain aspect ratio)
        label_width = self.label_camera.width()
        label_height = self.label_camera.height()
        qt_image = qt_image.scaled(label_width, label_height, Qt.KeepAspectRatio)

        self.label_camera.setPixmap(QPixmap.fromImage(qt_image))


    def updateFileName(self):
        self.fileName = self.lineEdit_tag.text() + '_' + str(self.spinBox_FileNumber.value()) + '.jpg'
        self.lineEdit_preview.setText(self.fileName)


    def resetFileNumber(self):
        self.spinBox_FileNumber.setValue(1)


    def saveImage(self):
        self.save_dir = self.lineEdit_savedir.text()
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        ret, frame = self.cap.read()
        if not ret:
            print("Unable to capture image")
            return

        self.imageAbsolutePath = os.path.join(self.save_dir, self.fileName)
        cv2.imwrite(self.imageAbsolutePath, frame)
        print(f"Image saved: {self.imageAbsolutePath}")

        self.spinBox_FileNumber.setValue(self.spinBox_FileNumber.value() + 1)  # Increment file number


    def exit(self):
        self.cap.release()
        self.close()


if __name__ == "__main__":
    # Enable DPI scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    image_capture_tool = ImageCaptureTool()
    image_capture_tool.show()
    sys.exit(app.exec_())
