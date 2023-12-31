import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 

import tensorflow as tf
import keras
from keras.preprocessing.image import ImageDataGenerator 
from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras.layers import Dropout, Flatten, Dense
from tensorflow.python.keras.layers.convolutional import Conv2D, MaxPooling2D


path = 'C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/Number_Model/myData'

myList = os.listdir(path)

number_of_folders = len(myList)
images = []
class_number = []
image_dimension = [32, 32, 3]
for folder in range(0, number_of_folders):
    number_folder = os.listdir(path + "/" + str(folder))

    for png in number_folder:
        current_png = cv2.imread(path + "/" + str(folder) + "/" + png)
        current_png = cv2.resize(current_png, (image_dimension[0],image_dimension[1])) #Note to self: its 180 x 180, so we make it 32 x 32 for easier processing but can change
        images.append(current_png)
        class_number.append(folder)
    print(f"Folder {folder} Done")
#print(len(images)) Total number of images 

images = np.array(images)
class_number = np.array(class_number)

#print(images.shape, ' | ', class_number.shape)

#Ratio of what % we want to use in training
test_ratio = 0.2
validation_ratio = 0.2

X_train, X_test, Y_train, Y_test = train_test_split(images, class_number, test_size=test_ratio)

X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=validation_ratio)

np.where(Y_train == 0)
sample_distribution = []
for number in range(0, number_of_folders):
    sample_distribution.append(len(np.where(Y_train == number)[0]))

#print(sample_distribution)
#plt.figure(figsize=(10,5))
#plt.bar(range(0,number_of_folders), sample_distribution)
#plt.title("Number of Image Distribution")
#plt.xlabel("Digit")
#plt.ylabel("Number of PNG's")
#plt.show()
    
def preProcessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img/255
    return img

X_train = np.array(list(map(preProcessing, X_train)))
X_test = np.array(list(map(preProcessing, X_test)))
X_validation = np.array(list(map(preProcessing, X_validation)))

X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1)
X_validation = X_validation.reshape(X_validation.shape[0],X_validation.shape[1],X_validation.shape[2],1)

dataGen = ImageDataGenerator(width_shift_range=0.1, height_shift_range=0.1, zoom_range=0.2, shear_range=0.1, rotation_range=10)
dataGen.fit(X_train)

Y_train = to_categorical(Y_train, number_of_folders)
Y_test = to_categorical(Y_test, number_of_folders)
Y_validation = to_categorical(Y_validation, number_of_folders)

def myModel(): #LeNet model
    noOfFilters = 60
    sizeOfFliter1 = (5,5)
    sizeOfFliter2 = (3,3)
    sizeOfPool = (2,2)
    noOfNode = 500

    model = Sequential()
    model.add((Conv2D(noOfFilters, sizeOfFliter1, input_shape=(image_dimension[0],image_dimension[1], 1),activation='relu')))
    model.add((Conv2D(noOfFilters, sizeOfFliter1,activation='relu')))
    model.add(MaxPooling2D(pool_size=sizeOfPool))
    model.add((Conv2D(noOfFilters//2, sizeOfFliter2,activation='relu')))
    model.add((Conv2D(noOfFilters//2, sizeOfFliter2,activation='relu')))
    model.add(MaxPooling2D(pool_size=sizeOfPool))
    
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(noOfNode, activation='relu'))
    model.add(Dense(number_of_folders, activation='softmax'))
    model.compile(optimizer=adam_v2.Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = myModel()
#print(model.summary())

#SETTING FOR MODEL FITTING
batchSizeVal = 50
epochsVal = 5
stepsPerEpochVal = 2000

history = model.fit(x=X_train, y=Y_train, batch_size=batchSizeVal, steps_per_epoch=len(X_train)//batchSizeVal, epochs=epochsVal, validation_data=(X_validation, Y_validation))

plt.figure(1)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training','validation'])
plt.title('Loss')
plt.xlabel('epoch')
plt.show()

plt.figure(2)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training','validation'])
plt.title('accuracy')
plt.xlabel('epoch')
plt.show()

score = model.evaluate(X_test,Y_test,verbose=0)
print("Test Score = ", score[0])
print("Test Accuracy = ", score[1])

model.save('C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/Number_Model/my_model2.keras')
model.save('C:/Users/nicky/OneDrive/Desktop/Sudoku_Solver/Number_Model/my_model1.h5')