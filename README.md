# Sudoku Image Solver

![ezgif-2-510eec4329](https://github.com/NicholasTerek/Sudoku_Image_Solver/assets/139080309/474b9cfb-6cce-4312-a436-ce119a8d4763)


## How To Run

If you wish, you can create a subdirectory and invoke configure from there.
For example::

    mkdir debug
    cd debug
    ../configure --with-pydebug
    make
    make test

   ''pip install numpy''
   ''pip install OpenCV''
   ::
   pip install tensorflow
   pip install flask
   pip install flask_uploads flask_wtf

  

Than run app.py file in terminal
Finally go to http://127.0.0.1:5000/


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














