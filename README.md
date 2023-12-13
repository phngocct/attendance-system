<div align="center">
    <h2 align="center">
  Student Attendance System Based on Face Recognition Using HOG and Euclidean Distance: A case study in FPT Polytechnic
    </h2>
</div>


<details>
  <summary>Dataset is used in research</summary>
    <ol>
      <a >Data includes facial photos of FPT Polytechnic students</a>
      </br>
    <a href="https://mega.nz/file/NJATiDYC#Flio3w_yBewoe8M4xYSCeeXvO_UeJTxLSR1tAsUxfKE">Faces of students at FPT Polytechnic (click here)</a>
</ol>
</details>


# Method
</br>
<h2 align="center">
  <img src="/assets/images/method.png" alt="method" width="600">
</h2>

- ## In the task of adding a new student to the system.
    - 1: Taking pictures is the student’s face from an image file or webcam.
    - 2: Crop the image for face detection by 216 × 216 pixels 
    - 3: Face detection is based on the HOG feature.
    - 4: Use the pre-trained dlib model to extract important features from the face and store it in the database.
- ## In the student attendance task.
    - 1: Take a picture of the student’s face on the webcam.
    - 2: Just like in the task of adding new students: face cropping, feature
extraction and encoding.
    - 3: Face recognition by applying Euclidean distance to compare with the encoded and stored data

# Some face images in the dataset:
<br/>
<h2 align="center">
  <img src="/assets/images/imagefromstudents.png" alt="method" width="600">
</h2>

## Project Description

- Python (programming language): <a href="https://www.python.org/downloads/release/python-31010/" alt="Python"><img src="https://img.shields.io/badge/python-v3.8.8-blue?logo=python" /></a>

- The PyPA recommended tool for installing Python packages: <a href="https://pypi.org/project/pip/" alt="pip"><img src="https://img.shields.io/badge/pypi-v23.1.2-blue?logo=pypi" /></a>

- Fundamental package for array computing in Python: <a href="https://numpy.org/" alt="numpy"><img src="https://img.shields.io/badge/numpy-v1.24.3-blue?logo=numpy" /></a>

- Powerful data structures for data analysis, time series, and statistics: <a href="https://pandas.pydata.org/" alt="pandas"><img src="https://img.shields.io/badge/pandas-v2.0.2-blue?logo=pandas" /></a>

- Wrapper package for OpenCV python bindings: <a href="https://github.com/opencv/opencv-python" alt="opencv-python"><img src="https://img.shields.io/badge/opencv python-v4.7.0.72-blue?logo=opencv" /></a>

- Python Imaging Library (Fork): <a href="https://pypi.org/project/Pillow/" alt="PIL"><img src="https://img.shields.io/badge/PIL-v9.5.0-blue?logo=PIL" /></a>

- Recognize faces from Python or from the command line: <a href="https://github.com/ageitgey/face_recognition" alt="face_recognition"><img src="https://img.shields.io/badge/face_recognition-v1.3.0-blue?logo=face_recognition" /></a>

- Create modern looking GUIs with Python: <a href="https://customtkinter.tomschimansky.com/" alt="customtkinter"><img src="https://img.shields.io/badge/customtkinter-v5.1.3-blue?logo=customtkinter" /></a>

- Firebase Admin Python SDK: <a href="https://pypi.org/project/firebase-admin/" alt="firebase_admin"><img src="https://img.shields.io/badge/firebase_admin-v6.1.0-blue?logo=firebase_admin" /></a>

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Python](https://www.python.org/downloads/release/python-31010/)

## Environment

Create a virtual environment `venv` for the project:

```sh
python -m venv venv
```

Activate virtual environment:

```sh
venv\Scripts\activate
```

Update to the latest pip version:

```sh
python.exe -m pip install --upgrade pip
```

## Project Setup

Install the external dependencies needed for the project:

```sh
pip install -r requirements.txt
```

## Run Project

```sh
python FaceAttendance.py
```

## Deactivate env

Once you’re done working with this virtual environment, you can deactivate it:

```sh
deactivate
```



# Demo the application

[Watch the video](https://www.youtube.com/watch?v=lJmntWEeC9Y)
