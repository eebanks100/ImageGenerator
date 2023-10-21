import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QCheckBox, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from makeImgs import imgGen, wipeData

# Elisha - created a GUI for the image generator, easy to adjust resolution, number of images, add/remove augmentations, etc to all the images for dataset creation
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
# left side content
        #resolution label
        self.lbl_resolution = QLabel('Resolution', self)
        self.lbl_resolution.move(50, 0)
        #width label
        self.lbl_width = QLabel('Width:', self)
        self.lbl_width.move(10, 25)
        #width text box
        self.le_width = QLineEdit(self)
        self.le_width.setGeometry(50, 30, 50, 20)
        self.le_width.setText("800")
        self.le_width.editingFinished.connect(self.validate_width)
        #height label
        self.lbl_height = QLabel('Height:', self)
        self.lbl_height.move(10, 60)
        #height text box
        self.le_height = QLineEdit(self)
        self.le_height.setGeometry(50, 60, 50, 20)
        self.le_height.setText("600")
        self.le_height.editingFinished.connect(self.validate_height)
        #number of images label
        self.lbl_number = QLabel('Number of images:', self)
        self.lbl_number.move(10, 100)
        #number of images text box
        self.le_number = QLineEdit(self)
        self.le_number.setGeometry(110, 110, 60, 20)
        self.le_number.setText("5")
        self.le_number.editingFinished.connect(self.validate_numImgs)
        #clear data checkbox
        self.chkb_cleardata= QCheckBox('Clear previous data', self)
        self.chkb_cleardata.setGeometry(10, 150, 300, 20)
        self.chkb_cleardata.setEnabled(True)
        self.chkb_cleardata.setChecked(False)
        self.chkb_cleardata.setToolTip('Enabling this will clear all the images for the selected Image Type')
        # lbl_cleardata_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_cleardata_qmark.setGeometry(135, 150, 300, 20)
        # lbl_cleardata_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_cleardata_qmark.setToolTip('Enabling this will clear all the images for the selected Image Type')

    #Image augmentations label
        self.lbl_aug = QLabel('Image augmentations:', self)
        self.lbl_aug.setGeometry(10, 200, 300, 20)
        #Random head size
        self.chkb_headsize= QCheckBox('Random head size', self)
        self.chkb_headsize.setGeometry(10, 225, 300, 20)
        self.chkb_headsize.setEnabled(True)
        self.chkb_headsize.setChecked(False)
        self.chkb_headsize.stateChanged.connect(self.headsize_enabled)
        self.chkb_headsize.setToolTip('Randomly changes the size of the head for each image')
        # lbl_headsize_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_headsize_qmark.setGeometry(135, 225, 300, 20)
        # lbl_headsize_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_headsize_qmark.setToolTip('Randomly changes the size of the head for each image')
        #Random image tilt
        self.chkb_tilt= QCheckBox('Tilt', self)
        self.chkb_tilt.setGeometry(10, 250, 300, 20)
        self.chkb_tilt.setEnabled(True)
        self.chkb_tilt.setChecked(False)
        self.chkb_tilt.stateChanged.connect(self.tilt_enabled)
        self.chkb_tilt.setToolTip('Apply a random degree of tilt in the image to simulate viewing the background from an angle')
        # lbl_tilt_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_tilt_qmark.setGeometry(135, 250, 300, 20)
        # lbl_tilt_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_tilt_qmark.setToolTip('Apply a random degree of tilt in the image to simulate viewing the background from an angle')
        #Randomize mosaic effect
        self.chkb_mosaic= QCheckBox('Mosaic', self)
        self.chkb_mosaic.setGeometry(10, 275, 300, 20)
        self.chkb_mosaic.setEnabled(True)
        self.chkb_mosaic.setChecked(False)
        self.chkb_mosaic.stateChanged.connect(self.mosaic_enabled)
        self.chkb_mosaic.setToolTip('Crop various background images together to simulate viewing the foreground object with multiple background images in the scene')
        # lbl_mosaic_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_mosaic_qmark.setGeometry(135, 275, 300, 20)
        # lbl_mosaic_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_mosaic_qmark.setToolTip('Crop various background images together to simulate viewing the foreground object with multiple background images in the scene')
        # brightness variation
        self.chkb_brightness= QCheckBox('Brightness', self)
        self.chkb_brightness.setGeometry(170, 225, 300, 20)
        self.chkb_brightness.setEnabled(True)
        self.chkb_brightness.setChecked(False)
        self.chkb_brightness.stateChanged.connect(self.brightness_enabled)
        self.chkb_brightness.setToolTip('Randomly adjust the brightness of the image to simulate different lighting conditions')
        # lbl_brightnes_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_brightnes_qmark.setGeometry(250, 225, 300, 20)
        # lbl_brightnes_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_brightnes_qmark.setToolTip('Randomly adjust the brightness of the image to simulate different lighting conditions')
        # blur variation
        self.chkb_blur= QCheckBox('Blur', self)
        self.chkb_blur.setGeometry(170, 250, 300, 20)
        self.chkb_blur.setEnabled(True)
        self.chkb_blur.setChecked(False)
        self.chkb_blur.stateChanged.connect(self.blur_enabled)
        self.chkb_blur.setToolTip('Adds a level of blur to the image to simulate the image being of lower quality or focusing on the object')
        # lbl_blur_qmark = QLabel('<span style="color: blue;"><u>?</u></span>', self)
        # lbl_blur_qmark.setGeometry(250, 250, 300, 20)
        # lbl_blur_qmark.setCursor(Qt.PointingHandCursor)
        # lbl_blur_qmark.setToolTip('Adds a level of blur to the image to simulate the image being of lower quality or focusing on the object')
        



# right side content
        #image type label
        self.lbl_imgtype = QLabel('Image Type', self)
        self.lbl_imgtype.move(350, 0)
        #Positive BG_img checkbox
        self.chkb_posBGimgs= QCheckBox('Positive Background Images', self)
        self.chkb_posBGimgs.setEnabled(True)
        self.chkb_posBGimgs.setGeometry(300, 30, 300, 20)
        self.chkb_posBGimgs.setChecked(True)
        self.chkb_posBGimgs.stateChanged.connect(self.posBGimgs_enabled)
        #Positive GT_img checkbox
        self.chkb_posGTimgs= QCheckBox('Positive Ground Truth Images', self)
        self.chkb_posGTimgs.setEnabled(True)
        self.chkb_posGTimgs.setGeometry(300, 60, 300, 20)
        self.chkb_posGTimgs.setChecked(True)
        self.chkb_posGTimgs.stateChanged.connect(self.posGTimgs_enabled)
        #Negative BG_img checkbox
        self.chkb_negBGimgs= QCheckBox('Negative Background Images', self)
        self.chkb_negBGimgs.setEnabled(True)
        self.chkb_negBGimgs.setGeometry(300, 90, 300, 20)
        self.chkb_negBGimgs.setChecked(True)
        self.chkb_negBGimgs.stateChanged.connect(self.negBGimgs_enabled)
        #Negative GT_img checkbox
        self.chkb_negGTimgs= QCheckBox('Negative Ground Truth Images', self)
        self.chkb_negGTimgs.setEnabled(True)
        self.chkb_negGTimgs.setGeometry(300, 120, 300, 20)
        self.chkb_negGTimgs.setChecked(True)
        self.chkb_negGTimgs.stateChanged.connect(self.negGTimgs_enabled)



#bottom content
        #generate button
        self.btn_generate = QPushButton('Generate', self)
        self.btn_generate.setGeometry(200, 325, 100, 30)
        self.btn_generate.clicked.connect(self.generateImgs)

#main window
        #window settings
        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('Image Generator')
        self.show()



#textbox value validation for number of images
    def validate_numImgs(self):
        value = self.le_number.text()
        if value:
            value = int(value)
            if value > 50000:
                value = 50000
        self.le_number.setText(str(value))
#textbox value validation for width
    def validate_width(self):
        value = self.le_width.text()
        if value:
            value = int(value)
            if value < 800:
                value = 800
            elif value > 8000:
                value = 8000
        self.le_width.setText(str(value))
#textbox value validation for height
    def validate_height(self):
        value = self.le_height.text()
        if value:
            value = int(value)
            if value < 600:
                value = 600
            elif value > 8000:
                value = 8000
        self.le_height.setText(str(value))

# set flags for checkboxes
    def posBGimgs_enabled(self, state):
        self.posBGimgs = state == Qt.Checked
    def posGTimgs_enabled(self, state):
        self.posGTimgs = state == Qt.Checked
    def negBGimgs_enabled(self, state):
        self.negBGimgs = state == Qt.Checked
    def negGTimgs_enabled(self, state):
        self.negGTimgs = state == Qt.Checked
    def headsize_enabled(self, state):
        self.headsize = state == Qt.Checked
    def tilt_enabled(self, state):
        self.tilt = state == Qt.Checked
    def mosaic_enabled(self, state):
        self.mosaic = state == Qt.Checked
    def brightness_enabled(self, state):
        self.brightness = state == Qt.Checked
    def blur_enabled(self, state):
        self.blur = state == Qt.Checked



    def generateImgs(self):
    # will not proceed if textboxes are left empty
        if not self.le_width.text() or not self.le_height.text() or not self.le_number.text():
            return
        
    # store user input from GUI into variables
        new_res_x = int(self.le_width.text())
        new_res_y = int(self.le_height.text())
        imgNum = self.le_number.text()
        self.posBGimgs = self.chkb_posBGimgs.isChecked()
        self.posGTimgs = self.chkb_posGTimgs.isChecked()
        self.negBGimgs = self.chkb_negBGimgs.isChecked()
        self.negGTimgs = self.chkb_negGTimgs.isChecked()
        self.headsize = self.chkb_headsize.isChecked()
        self.tilt = self.chkb_tilt.isChecked()
        self.mosaic = self.chkb_mosaic.isChecked()
        self.brightness = self.chkb_brightness.isChecked()
        self.blur = self.chkb_blur.isChecked()

        cmd = ["python", "./makeImgs.py"]  

    # Elisha - clears data before generating if clear data is checked
        if self.chkb_cleardata.isChecked():   
            wipeData(cmd)
    # Elisha - call imgGen from makeImgs.py passing all the values that were entered in from the GUI
        imgGen(int(imgNum), cmd, new_res_x, new_res_y, self.posBGimgs, self.posGTimgs, self.negBGimgs, self.negGTimgs, self.headsize, self.tilt, self.mosaic, self.brightness, self.blur)    #call makeImgs.imgGen with user input parameters

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())