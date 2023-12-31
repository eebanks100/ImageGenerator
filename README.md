# CamoTectV2 Image Generator Overview:
ImageGen is a Python script designed to simplify the process of creating image datasets used specifically for CamoTectV2. ImageGen provides users the ability to choose the number of images they wish to generate, which image types they want to generate, a list of augmentations that can be applied to each image, as well as allowing users to change the width and height of the images created.

The image generator makes use of background and foreground images, which are stored under the `./planeImages` folder labeled as bg and fg folders respectively. The object used for the foreground is stored in the foregroundObjects folder. The output for the four different image types generated by the script are stored under `./outputFiles`.

ImageGen provides users with a variety of options for customizing the image generation process. These options include head size variation (foreground object size variation), applying a random degree of tilt to the image, creating a mosaic effect (multiple background images cropped together), random brightness adjustment, and adding blur to the image. Users can also choose whether or not they wish to generate images for one or more of the image types under `./outputFiles`.


## Installation:
1) Navigate to the ImageGen project directory

2) Run the following command to install all required dependencies: `pip install -r requirements.txt`
   
3) Run via command line



# Usage
Ensure all the required dependencies have been properly installed.

## How to Use:
1) Navigate to the ImageGen project directory

2) Open the `start.bat` file

3) The desired output files can be selected under `Image Type` section
-   a) `Positive Background Images`: Original background image with the foreground object

    b) `Positive Ground Truth Images`: Ground truth image corresponding to the positive background image

    c) `Negative Background Images`: Original background image without the foreground object

    d) `Negative Ground Truth Images`: Ground truth image corresponding to the negative background image

4) Width and height of the images produced can be changed under `Resolution` (max width and height is 8000)

5) `Number of images` can be changed (max number of images is 50000)

6) When checked, `Clear previous data` will clear all files under the selected image type under the `Image Type` section

7) Image augmentations can be added to the images to add noise to the images under `Image augmentations`
-   a) `Random head size`: randomly adjust the size of the foreground object (head object)

    b) `Tilt`: apply a random degree of tilt to the whole image

    c) `Mosaic`: crop various background images together (uses images under `./planeImages/bgFruit/cropFruit`, `./planeImages/bgTrees/cropTrees`, `./planeImages/fgFruit/cropFruit`, `./planeImages/fgTrees/cropTrees`)

    d) `Brightness`: randomly adjust the brightness of the image to be brighter or darker

    e) `Blur`: adds a random level of blur to the image

8) When all desired options have been selected, click on the `Generate` button and images for each of the selected `Image Types` will be created



### Creating Datasets For CamoTectV2
When generating datasets for CamoTectV2, it is best to simply leave all the `Image Type` checkboxes checked since the negatives will eventually need to be used together with the positive images. In the context of training using CamoTectV2, a minimum of 5000 images (positive or negative) should be enough to train.

[Using CamoTectV2 With Generated Dataset](https://github.com/eebanks100/CamoTectV2)


#### Developers
- Elisha Ebanks
- Jacob Doby
- Atabey Abbasi