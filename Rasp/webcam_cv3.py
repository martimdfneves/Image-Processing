import cv2
import sys
import datetime as dt
import os
from os.path import basename
from time import sleep
import subprocess

def main():
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    
    video_capture = cv2.VideoCapture(0)

    previousfaces = 0 # previous do ciclo! xd
    timestart = ''
    timestop = ''
    interactiontime = ''
    previouscontent = '' # previous do ciclo! xd
    hours = 0
    minutes = 0
    seconds = 0
    count = 0

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        if ret == False:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        f=open("/home/pi/Desktop/Webcam-Face-Detect-master/log.txt","r")
        for line in f:
            content = line

        if previousfaces == 0 and len(faces) != 0:
            timestart = dt.datetime.now()
        if (previousfaces != 0 and len(faces) == 0) or (previouscontent != content and len(faces) != 0):
            timestop = dt.datetime.now()
            interactiontime = timestop - timestart
            interactiontime = str(interactiontime)
            auxtime = interactiontime.split(".")
            interactiontime = auxtime[0]
            auxtime = interactiontime.split(":")
            hours = int(auxtime[0]) * 3600
            minutes = int(auxtime[1]) * 60
            seconds = int(auxtime[2])
            interactiontime = hours + minutes + seconds
            # enviar o script 2
            command1 = "./authpost1.sh %s %s" %(interactiontime, content)
            process1 = subprocess.Popen(command1.split(), stdout=subprocess.PIPE)
            output1, error1 = process1.communicate()

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Display the resulting frame
        cv2.imshow('Video', frame)

        time = str(dt.datetime.now())
        aux = time.split(".")
        time = aux[0]
        aux = time.split(" ")
        time = aux[0]+"-"+aux[1]
        aux = time.split(":")
        time = aux[0]+"-"+aux[1]+"-"+aux[2]

        
        os.chdir("/home/pi/Desktop/Webcam-Face-Detect-master")
        if len(faces) != 0:
            cv2.imwrite("Captures/%s.jpg" % time, frame)
            count += 1
            os.chdir("/home/pi/Desktop/Webcam-Face-Detect-master")
            command2 = "./authpost.sh %s %s" %(time, content)
            process2 = subprocess.Popen(command2.split(), stdout=subprocess.PIPE)
            output2, error2 = process2.communicate()
        
        if count == 10:
            dir = "/home/pi/Desktop/Webcam-Face-Detect-master/Captures"
            for f in os.listdir(dir):
                os.remove(os.path.join(dir,f))
            count = 0

        previousfaces = len(faces)
        previouscontent = content

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

    
main()
