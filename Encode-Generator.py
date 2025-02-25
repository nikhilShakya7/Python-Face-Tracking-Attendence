import cv2
import face_recognition
import pickle
import os

#from main import modePath

#modePath = "Images"
modePath="Database/Images"
modePathList = os.listdir(modePath)
imgList = []
studentId = []

# Load images and corresponding student IDs
for path in modePathList:
    img_path = os.path.join(modePath, path)
    img = cv2.imread(img_path)

    # Append image to imgList
    imgList.append(img)

    # Extract student ID from the image filename (without the extension)
    studentId.append(os.path.splitext(path)[0])

print(studentId)


# Function to find encodings of faces in images
def findEncodings(imagesLists):
    encodeList = []
    for img in imagesLists:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB
        encodings = face_recognition.face_encodings(img)  # Get encodings for all faces in the image
        if encodings:  # Check if at least one face was found
            encodeList.append(encodings[0])  # Use the encoding of the first face (assumes one face per image)
    return encodeList


# Encode known faces and associate with student IDs
encodeListKnown = findEncodings(imgList)
encodeListKnownWithId = [encodeListKnown, studentId]

# Print encoded list and complete message
print(encodeListKnownWithId)
print("Encoding complete")

file=open("Encode_File.p",'wb')
pickle.dump(encodeListKnownWithId,file)
file.close()