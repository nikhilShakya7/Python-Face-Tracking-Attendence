import os
import pickle
import numpy as np
import cv2
import cvzone
import face_recognition

# Index 0 for the default camera
cap = cv2.VideoCapture(0)

# Set the resolution to 640x480
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

#Load background images
imgBackground = cv2.imread("Resources/background.png")
modePath = "Resources/Modes"
modePathList = os.listdir(modePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(modePath, path)))

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

#Load face encodings from the saves file
file = open('Encode_File.p', 'rb')
encodeListKnownWithId = pickle.load(file)
file.close()

#Unpaxk the encodings and student id and prints the id
encodeListKnown, studentId = encodeListKnownWithId
print(studentId)

# Capture frame-by-frame
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally

    #resize the image so that face is only visible for detection
    resize_img=cv2.resize(img,(0,0),None,0.25,0.25)

    #converts the resized image to RGB
    resize_img=cv2.cvtColor(resize_img,cv2.COLOR_BGR2RGB)

    #detect face in resized frame
    faceFrame=face_recognition.face_locations(resize_img)

    #Encode the detected face
    encodeFrame=face_recognition.face_encodings(resize_img,faceFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[1]

   #Loop through all the faces and finds the correct face
    for encodeFace ,faceLoc in zip(encodeFrame,faceFrame):
        #Compare the face with the encodings
        match=face_recognition.compare_faces(encodeListKnown,encodeFace)
        #Compute face distance(lower distance = better match)
        faceDistance=face_recognition.face_distance(encodeListKnown,encodeFace)
        print("matches",match)
        print("Distance", faceDistance)
        #Get the best match index
        matchIndex=np.argmin(faceDistance)
        print("Match Index",matchIndex)
        #if match is found prints the id
        if match[matchIndex]:
            print("Face matched")
            print(studentId[matchIndex])
            #Extract face location coordinates
            #y1=top point of the face
            #y2=bottom point of the face
            #x2=right point of the face
            #x1=left point of the face
            y1,x2,y2,x1=faceLoc
            #Scale the coordinates. Multiplied by 4 because the image was resized. Coordinates are being scaled back to its original size.
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            #bbox library for bounding box for the face.
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground= cvzone.cornerRect(imgBackground,bbox ,rt=0)




    cv2.imshow("Face Attendance", imgBackground)

    # If frame is read correctly, success will be True
    if not success:
        print("Error: Failed to capture image.")
        break

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
