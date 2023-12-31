import cv2
import numpy as np
from Image_Processing.image_methods import *
from Image_Processing.solving_Algorithm import *
from tensorflow.python.keras.models import load_model
from typing import List, Tuple, Optional
import os

#path_To_Image = "./Test_Images/Sudoku.png" #To Do

def solve_image(path_To_Image):
    height_Image = 450 
    width_Image = 450
    #
    #parameters -> filepath maybe file name?
    #return inverse_perspective, or return Errors when steps cant be run
    model = load_model('C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/Number_Model/my_model2.keras', compile=False)
    #print(model.summary())
    img = cv2.imread(path_To_Image)
    img = cv2.resize(img,(width_Image, height_Image))
    blank_img = np.zeros((height_Image, width_Image, 3), np.uint8)

    imgThreshold = preProcessing(img)

    imgContours = imgThreshold.copy()
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

    imgBigContours = img.copy()
    biggest, max_Area = biggestContour(contours)

    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(imgBigContours, biggest, -1, (0, 255, 0), 15)
        
        points1 = np.float32(biggest)
        points2 = np.float32([[0,0], [width_Image,0], [0, height_Image], [width_Image, height_Image]])
        matrix = cv2.getPerspectiveTransform(points1, points2)
        imgWarpColoured = cv2.warpPerspective(img, matrix, (width_Image, height_Image))
        imgWarpColoured = cv2.cvtColor(imgWarpColoured, cv2.COLOR_BGR2GRAY)

        boxes = split_Boxes(imgWarpColoured)
        #cv2.imshow("Test", boxes[1])
        numbers = getPrediction(boxes, model)
        #print(numbers)
        
        img_detected_Digits = blank_img.copy()
        img_detected_Digits = displayNumbers(img_detected_Digits, numbers, color=(255, 0 , 255))
        
        solved_number = listProcessing(numbers)
        

        numbers = np.asarray(numbers)
        posArray = np.where(numbers >0,0,1)

        try:
            solve(solved_number)
        except: 
            print("SUDOKU CANT BE SOLVED")
            pass

        
        solved_number = reverse_listProcessing(solved_number)
        solved_number = solved_number*posArray
        imgSolvedDigits= blank_img.copy()
        imgSolvedDigits = displayNumbers(imgSolvedDigits, solved_number)

        points2 = np.float32(biggest)
        points1 = np.float32([[0,0], [width_Image,0], [0, height_Image], [width_Image, height_Image]])
        matrix = cv2.getPerspectiveTransform(points1, points2)
        imgInverseWarpColoured = img.copy()
        imgInverseWarpColoured = cv2.warpPerspective(imgSolvedDigits, matrix, (width_Image, height_Image))
        inverse_perspective = cv2.addWeighted(imgInverseWarpColoured, 1, img, 0.5, 1)
        modified_path = 'C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/uploads/modified_' + os.path.basename(path_To_Image)
        cv2.imwrite(modified_path, inverse_perspective)
        print("done")
        return modified_path
        #new_img_detected_Digits = img_detected_Digits.copy()
        #new_imgSolvedDigits = imgSolvedDigits.copy()
        #new_img_detected_Digits = drawGrid(new_img_detected_Digits)
        #new_imgSolvedDigits = drawGrid(new_imgSolvedDigits)

    else: 
        print("SUDOKU NOT FOUND")
        return None

#result = solve_image(path_To_Image)
#print(result)
#image_Array = ([img,imgThreshold, imgContours, imgBigContours], [imgWarpColoured, img_detected_Digits, imgSolvedDigits, imgInverseWarpColoured])
#stack = stackImages(1, image_Array)
#cv2.imshow("OpenCV Process", stack)
#cv2.waitKey(0)

#image_Array = ([new_img_detected_Digits,new_imgSolvedDigits, inverse_perspective, blank_img], [blank_img, blank_img, blank_img, blank_img])
#stack = stackImages(1, image_Array)
#cv2.imshow("OpenCV Process", stack)
#cv2.waitKey(0)

