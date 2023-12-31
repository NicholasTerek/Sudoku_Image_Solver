# Sudoku Image Solver

![ezgif-2-510eec4329](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/474b9cfb-6cce-4312-a436-ce119a8d4763)


## How To Run

### Packages Needed
    pip install numpy
-----------------------------------
    pip install OpenCV
-----------------------------------

    pip install tensorflow
-----------------------------------

    pip install flask
-----------------------------------

    pip install flask_uploads flask_wtf
-----------------------------------

- Than run app.py file in terminal
- Finally go to http://127.0.0.1:5000/


## Technology stack:
<div><b>Frontend:</b> (HTML/CSS, BootStrap)</div> 
<div><b>Backend:</b> (Python, Flask, OpenCV, os, numpy)</div> 
<div><b>CNN-Model:</b> (Python, TensorFlow Keras, Sklearn, numpy, MatPlotLib, OpenCV) </div> 



## Image Processing:
Using OpenCV I processed any given sudoku puzzle, using this process

1. Converting it to GrayScale
2. Gaussian Blurring the Image 
3. Adaptive Thresholding to contrast the image 
4. Finding the contour to find the corners of the Sudoku 
5. Warped the perspective of an image to give just the Sudoku grid
6. Using a created split_Boxes() method to divide the image into 81 even images
7. Using CNN to detect the numbers and place them into an array
8. Overlay the array onto a blank image
9. Using a created drawGrid() method to draw a grid around each number
10. Warp the perspective back to how the photo is originally given
11. Overlay the numbers onto the original image


![image](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/697618bc-7bd9-4ffd-80b4-aaf9297900fc)
![image](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/ff757b23-c984-49ee-a041-86aeb41962d0)


## Convolutional Neural Network

### Training Data:
The training data used for this CNN is from Kaggle, it contains just over 1000 unique images for each digit for over 10,000 total images. Additionally to improve accuracy of CNN, i implemented an attempt at even distribution 

![image](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/e7f0be9b-da33-4f59-8eb6-8e54a5de0da9)


### Model:
The model is a classical CNN inspired by the LeNet-5 architecture developed by Yann LeCun.

<div>
  <img src="https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/9fe9f111-23a1-4b6f-908b-f0f40b4f2096" alt="Image 2" width="400"/>
  <img src="https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/400b922f-b6c3-4a40-8268-b17e10873c8d" alt="Image 1" width="400"/>
</div>

### Training:
The model was trained over 10 epochs with a batch size of  130 images. Next time i would try and acquire more computational power as this was near the limits for my computer 
- Test Accuracy =  99.2125988007%

![image](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/2915cf3a-2b41-41f2-9045-285d85ead26e)


### Graphs:
Here are some graphs to show how the training went for my CNN
<div>
  <img src="https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/e8dea320-0875-464b-98c6-ada44dc84e47" alt="Image 2" width="400"/>
  <img src="https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/e04c8118-d70d-496b-a922-bf152d720051" alt="Image 1" width="400"/>
</div>


## Sudoku Algorithm
 
After extracting a numerical array representing the numbers from the Sudoku grid image, we employ a backtracking algorithm to solve the puzzle. This recursive approach systematically attempts to place valid numbers in empty grid cells. If the algorithm encounters a dead end or an unsolvable puzzle, it backtracks to the last empty cell and explores alternative options. This process continues until the Sudoku puzzle is successfully solved.

## Flask Server

This Flask server is designed to facilitate Sudoku puzzle solving through image processing and a backtracking algorithm. The structure of the code is organized as follows:

1. **Uploads Configuration:** Utilizes Flask-Uploads to handle uploaded images, configuring the upload destination.

2. **Form Definition:** Defines a FlaskForm using Flask-WTF, which includes a FileField for image uploads and a SubmitField.

3. **Routes:**
   - `/uploads/<filename>`: Serves uploaded images.
   - `/`: Main route for handling image uploads, processing, and displaying the results.

4. **Image Processing Integration:** Imports image processing methods for solving Sudoku puzzles from `Image_Processing.main` and supporting methods from `Image_Processing.image_methods`.

5. **Flask App Configuration:** Configures Flask app settings, including the secret key and template folder location.

6. **App Initialization:** Initializes the Flask app with the specified template folder.

7. **Form and Upload Configuration:** Creates an instance of the `UploadForm` and configures image uploads using Flask-Uploads.

8. **Route Definitions:**
   - `/uploads/<filename>`: Returns uploaded images.
   - `/`: Handles image uploads, initiates processing, and renders the results on the HTML template.






