import cv2
import numpy as np
from Image_Processing.image_methods import *
from Image_Processing.solving_Algorithm import *
from tensorflow.python.keras.models import load_model
from typing import List, Tuple, Optional
import os

def solve_image(path_To_Image):
    height_Image = 450
    width_Image = 450

    model = load_model("./Number_Model/my_model2.keras", compile=False)
    img = cv2.imread(path_To_Image)
    img = cv2.resize(img, (width_Image, height_Image))
    blank_img = np.zeros((height_Image, width_Image, 3), np.uint8)

    img_threshold = preProcessing(img)

    img_contours = img_threshold.copy()
    contours, hierarchy = cv2.findContours(
        img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

    img_biggest_contour = img.copy()
    biggest, max_Area = biggestContour(contours)

    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(img_biggest_contour, biggest, -1, (0, 255, 0), 15)

        points1 = np.float32(biggest)
        points2 = np.float32(
            [[0, 0], [width_Image, 0], [0, height_Image], [width_Image, height_Image]]
        )
        matrix = cv2.getPerspectiveTransform(points1, points2)
        img_warp_coloured = cv2.warpPerspective(img, matrix, (width_Image, height_Image))
        img_warp_coloured = cv2.cvtColor(img_warp_coloured, cv2.COLOR_BGR2GRAY)

        boxes = split_Boxes(img_warp_coloured)
        numbers = getPrediction(boxes, model)

        img_detected_Digits = blank_img.copy()
        img_detected_Digits = displayNumbers(
            img_detected_Digits, numbers, color=(255, 0, 255)
        )

        solved_number = listProcessing(numbers)
        numbers = np.asarray(numbers)
        position_array = np.where(numbers > 0, 0, 1)

        try:
            solve(solved_number)
        except:
            print("SUDOKU CANT BE SOLVED")
            pass

        solved_number = reverse_listProcessing(solved_number)
        solved_number = solved_number * position_array
        img_solved_digits = blank_img.copy()
        img_solved_digits = displayNumbers(img_solved_digits, solved_number)

        points2 = np.float32(biggest)
        points1 = np.float32(
            [[0, 0], [width_Image, 0], [0, height_Image], [width_Image, height_Image]]
        )
        matrix = cv2.getPerspectiveTransform(points1, points2)
        img_inverse_warp_coloured = img.copy()
        img_inverse_warp_coloured = cv2.warpPerspective(
            img_solved_digits, matrix, (width_Image, height_Image)
        )
        img_final = cv2.addWeighted(img_inverse_warp_coloured, 1, img, 0.5, 1)
        modified_path = (
            "C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/uploads/modified_"
            + os.path.basename(path_To_Image)
        )
        cv2.imwrite(modified_path, img_final)
        print("done")
        return modified_path

    else:
        print("SUDOKU NOT FOUND")
        return None


