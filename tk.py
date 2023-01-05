#import all the libraries that we need
#1. tkinter is used to create the GUI
#2. Pillow/PIL is used to manage the video data and image
#3. openCV/cv2 is used to identify objects, faces and others
#4. imutils are a series of convinient functions to make basic image processing finctions like rotation, rezising images
#5. GPIO activate the inputs and outputs of the RPi 

from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)#relay VFD 240VAC
GPIO.setup(18, GPIO.OUT)#number of steps the steppermotor
GPIO.setup(23, GPIO.OUT)#Enavel or desable the drive // it prevent the motor from overheating
GPIO.setup(24, GPIO.OUT)#Direction of the stepperMotor   
GPIO.setup(25, GPIO.OUT)#change relay between screw and camera 
#add to the camera axis
GPIO.setup(21, GPIO.OUT)#number of steps the steppermotor   Blanco
GPIO.setup(16, GPIO.OUT)#Enavel or desable the drive // it prevent the motor from overheating    cafe
GPIO.setup(20, GPIO.OUT)#Direction of the stepperMotor     negro
#add to the camera axis

GPIO.output(17, GPIO.HIGH) #is used to start the VFD OFF position
# is not going to be use the relay #GPIO.output(25, GPIO.HIGH)


#function to setup the video
def visualizar():
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame,width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
    else:
        lblVideo.image = ""
        cap.release()

#funtion link to the btnIniciar
#start the camera by calling visualizar()
def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    visualizar()
    
#funtion link to the btnFinalizar
#Stop the camera
def finalizar():
    global cap
    cap.release()

cap = None

#function to activate contactor VFD 240v
#same button turn on and off
"""vfdON = False
def vfdON():
    # change the state of the contactor. if it is On turn Off and viseversa
    global vfdON
    vfdON = not vfdON
    GPIO.output(17, GPIO.HIGH if vfdON else GPIO.LOW)
    
    '''if (17, GPIO.HIGH):                         <-- Testing different backgorund
        buttonVFD["bg"]="green"                        but it is not working
    else:
        buttonVFD["bg"]="red"            '''
"""
#el codigo de arriba prende y apaga el VFD con el mismo boton

#Turn on the pin 17 and activate the VFD
def vfdON():
    print('VFD ON')
    GPIO.output(17, GPIO.LOW)
    
#Turn off the pin 17 and diactivate the VFD
def vfdOFF():
    print('VFD Off')
    GPIO.output(17, GPIO.HIGH)


#create funtion to rotate to the screw to the right   
def Screwright():
        
    GPIO.output(24, GPIO.HIGH)#input to the stepper drive to change direction 
    GPIO.output(23, GPIO.LOW)#enable stepper drive
    
    for step in range (1500) :  #every time you click advance 1500 steps
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.0001)
    GPIO.output(23, GPIO.HIGH)#disable stepper drive
 
 
    
#create funtion to rotate to the screw to the left
def Screwleft():
    
    GPIO.output(24, GPIO.LOW)# change direction in stepper drive
    GPIO.output(23, GPIO.LOW)#enable stepper drive
    
    for step in range (1500) :
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.0001)
    GPIO.output(23, GPIO.HIGH)#disable stepper drive
    
def RotateCameraRight():       
    GPIO.output(20, GPIO.LOW)# change direction in stepper drive
    GPIO.output(16, GPIO.LOW)#enable stepper drive
    
    for step in range (100) :
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(21, GPIO.LOW)
        time.sleep(0.0001)
    #GPIO.output(16, GPIO.HIGH)#disable stepper drive


def RotateCameraLeft():       
    GPIO.output(20, GPIO.HIGH)# change direction in stepper drive
    GPIO.output(16, GPIO.LOW)#enable stepper drive
    
    for step in range (100) :
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(21, GPIO.LOW)
        time.sleep(0.0001)
    #GPIO.output(16, GPIO.HIGH)#disable stepper drive

#Start the tkinter part
root = Tk()

#Window name
root.title("Troubleshooting")

#create button iniciar camera
btnIniciar = Button(root, text="Start Camera", width = 45, command = iniciar)
btnIniciar.grid(column=0, row=0, pady=5)

#create button finalizar camera
btnFinalizar = Button(root, text="Stop Camera", width = 45, command = finalizar)
btnFinalizar.grid(column=1, row=0, pady=5)

#create a space for the camera in column0-row1
lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)

#call function start vfd contactor ->> high pin 17
buttonVFD = Button(root, text= "Start VFD", width=25 , bg="Green", command= vfdON)
buttonVFD.grid(column=0, row=10)

#call function stop vfd contactor ->> low pin 17
buttonVFD = Button(root, text= "Stop VFD", width=25 , bg="red", command= vfdOFF)
buttonVFD.grid(column=1, row=10)

#create button to rotate the screw to the left (1axis)
btnTLeft = Button(root, text="<< Screw", width=25, command= Screwleft)
btnTLeft.grid(column=0, row=11)

#create button to rotate the screw to the right (1axis)
btnTRight = Button(root, text='Screw >>', width=25,command= Screwright)
btnTRight.grid(column=1, row=11)

#create button to rotate the screw to the right (2axis)
buttonCameraRight = Button(root, text= "<< Camera", width=25, command= RotateCameraLeft)
buttonCameraRight.grid(column=0, row=12)

#create button to rotate the screw to the right (2axis)
buttonCameraLeft = Button(root, text= "Camera >>", width=25, command= RotateCameraRight)
buttonCameraLeft.grid(column=1, row=12)


root.mainloop()

