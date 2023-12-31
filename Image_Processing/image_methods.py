import cv2
import numpy as np

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold


def listProcessing(list):
    result = []
    for index in range(0, len(list), 9):
        result.append(list[index:index + 9])
    return result

def reverse_listProcessing(list_of_lists):
    result = []
    for sublist in list_of_lists:
        result.extend(sublist)
    return result

def getPrediction(boxes, model):
    result = []
    for image in boxes: 
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
        img = cv2.resize(img, (32, 32))
        img = img / 255
        img = img.reshape(1, 32, 32, 1)

        predictions = model.predict(img)
        class_index = np.argmax(predictions, axis = -1)
        probaility_value = np.max(predictions)
        #print(class_index, probaility_value)
        if probaility_value > 0.6:
            result.append(class_index[0])
        else:  #set it 0 if empty
            result.append(0)
    return result

def biggestContour(contours):
    biggest = np.array([])
    max_area = 0

    for index in contours:
        area = cv2.contourArea(index)
        if area > 50:
            perimeter = cv2.arcLength(index, True) 
            approximate = cv2.approxPolyDP(index, 0.02*perimeter, True) 
            if area > max_area and len(approximate) == 4:
                biggest = approximate
                max_area = area
    
    return biggest, max_area

def reorder(original_Points):
    original_Points = original_Points.reshape((4,2))
    new_Points = np.zeros((4,1,2), np.int32)
    add = original_Points.sum(1)
    diff = np.diff(original_Points, axis=1)

    new_Points[0] = original_Points[np.argmin(add)]
    new_Points[3] = original_Points[np.argmax(add)]

    new_Points[1] = original_Points[np.argmin(diff)]
    new_Points[2] = original_Points[np.argmax(diff)]

    return new_Points

def split_Boxes(image):
    rows = np.vsplit(image,9)
    boxes = []
    for row in rows:
        columns = np.hsplit(row, 9)
        for box in columns:
            boxes.append(box)
    return boxes
        
def displayNumbers(img,numbers,color =(0,255,0)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for x in range(0,9):
        for y in range(0,9):
            if numbers[(y*9) +x] != 0:
                cv2.putText(img, str(numbers[(y*9)+x]),(x*secW+int(secW/2)-10, int((y+0.8)*secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv2.LINE_AA)
    return img

def drawGrid(img):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)
    return img

#TESTING METHODS
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale,scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver