import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('D:/haarcascade_frontalface_default.xml')
  
image = cv2.imread('D:/Data Projects/Faces in Movies/posters/EdgeofDoom - tt0042428/poster_3.jpeg')
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
faces = face_cascade.detectMultiScale(grayImage)

# Show percentage of area of faces to total area
totalArea = image.shape[0] * image.shape[1]
faceArea = 0

faceCount = 0
for (x, y, w, h) in faces:
    faceArea += w * h
percentage = (faceArea * 100) / totalArea

if len(faces) == 0:
    faceCount = 0
else:
    faceCount = faces.shape[0]
print("{faceCount} faces detected in the image.\n".format(faceCount=faceCount))
print("{:.2f}% of the image is covered by faces.\n".format(percentage))

folder = "D:/Data Projects/Faces in Movies/posters/"
# Count number of images in the folder and subdirectories
import os
imageCount = 0
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".jpeg"):
            imageCount += 1

# Count number of folders in folder
folderCount = 0
for root, dirs, files in os.walk(folder):
    folderCount += 1
perc = (folderCount/85000)*100
print("{perc} of the dataset is complete".format(perc=perc))
print("{imageCount} images scrapped".format(imageCount=imageCount))

emptyFolder = 0
for root, dirs, files in os.walk(folder):
    # Counter empty folders
    if len(files) == 0:
        emptyFolder += 1
print("{emptyFolder} empty folders".format(emptyFolder=emptyFolder))