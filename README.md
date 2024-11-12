
# Attendance 2.0 - Python and OpenCV

### Steps:
- Download or clone my Repository to your device
- type `pip install -r requirements.txt` in command prompt (to install required packages to run the program).
- Create a `TrainingImage` folder in a project folder.
- Open `attendance.py` & `automaticAttendance.py` and change paths accoriding to your system.
- Run `attandance.py` file.

### Project flow & explaination
- Register your face after you run the project so that system can identify you, click on register new student.
- A small window pops up where you have to enter you Roll Number and Name and then click on `Take Image` button.
- After clicking `Take Image` button, a camera window will pop up and will detect your Face and take upto 50 Images (You can easily change the number of images clicked) and stored in  `TrainingImage` folder. The more you give the image to system, the better it will perform while recognising the face.
- Click on `Train Image` button, it will train the model and convert all the images into numeric format so that computer can understand. Training is done so that next time when we will show the same face to the computer it will easily identify the face.
- It might take some time (depends on you system).
- After training model click on `Automatic Attendance`, you have to enter the subject name and then it can fill attendace by your face using our trained model.
- A `.csv` file for every subject you enter is created and a seperate `.csv` file accoriding the subject
- You can view the attendance after clicking `View Attendance` button. It will show record in tabular format.
