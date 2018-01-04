#!/usr/bin/python3
'''
Original code: https://github.com/PiSimo/PiCamNN
'''

import cv2
import time
import threading
import subprocess
import numpy as np
from sys import exit
from os import system
from keras import backend as K
from keras.models import load_model
from yad2k.models.keras_yolo import yolo_eval, yolo_head

'''
---# GLOBAL VARIABLES #---
'''
#USER SETTINGS :
maxDays = 7                      #The recorded videos will be destroyed after "maxDays" days
baseFolder = "/var/www/html/"    #Apache's base folder
scriptFolder = "/home/pi/PoochPak/yolo_picam/" #The folder which contains main script (picam.py)
num_cam = -1       #Number of the camera (if -1 it will be the first camera read by the system)
frame_check = 17   #Frames to check before quit
time_chunk = 15   #Time to consider for a new action

#IMAGES VARIABLES:
w = 0 #width
h = 0 #height
#Image processing vars:
blur1 = 2
blur2 = 1
erodeval = 7
#Volatile arrays:
frames = []
times  = []
#General Log file
flog = open(baseFolder+"logs","a")

'''
---# END #---
'''

#when an error occur
def printExit(out):
    print(out,"\nClosing....!")
    exit(-1)

#Updating index.html :
#       1 Opening index.html
#       2 Adding new link for the new video
#       3 If there are more then maxDays links removing oldest one
#       4 Removing also the oldest video
def handleFile(name):
    print("[PiCamNN] Updating file...")
    f = open(baseFolder+"index.html","r")
    cont = f.read()
    f.close()
    if cont.find(name) != -1:
        print("[PiCamNN] File has been update yet !")
        return False
    f = open(baseFolder+"index.html","w")
    lines = cont.split("\n")
    day = 0
    go = False
    for i in range(len(lines)-1):
        if lines[i].find("<!-- S -->") != -1:
            i += 1
            f.write("<!-- S -->\n <a href=\"{}.avi\" class=\"file\" >{}.avi</a><br />\n".format(name,name))
            day += 1
            go  =  True
        elif lines[i].find("<!-- E -->") != -1:
            f.write("{}\n".format(lines[i]))
            go = False
            if day > maxDays:
                rm = lines[i-1]
                rm = rm[rm.find("\"")+1:len(rm)]
                rm = rm[0:rm.find("\"")]
                try:
                    system("rm {}".format(baseFolder+rm))
                    print("[PiCamNN] Old file removed.")
                except:
                    print("[PiCamNN] An error occured while removing old file!")
        elif go:
            day +=1
            if day <= maxDays:f.write("{}\n".format(lines[i]))
        else:f.write("{}\n".format(lines[i]))
    f.close()
    print("[PiCamNN] index.html UPDATED")
    return True

# Some morphological operations on two input frames to check for movements
def movement(mat_1,mat_2):
    mat_1_gray     = cv2.cvtColor(mat_1.copy(),cv2.COLOR_BGR2GRAY)
    mat_1_gray     = cv2.blur(mat_1_gray,(blur1,blur1))
    _,mat_1_gray   = cv2.threshold(mat_1_gray,100,255,0)
    mat_2_gray     = cv2.cvtColor(mat_2.copy(),cv2.COLOR_BGR2GRAY)
    mat_2_gray     = cv2.blur(mat_2_gray,(blur1,blur1))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,100,255,0)
    mat_2_gray     = cv2.bitwise_xor(mat_1_gray,mat_2_gray)
    mat_2_gray     = cv2.blur(mat_2_gray,(blur2,blur2))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,70,255,0)
    mat_2_gray     = cv2.erode(mat_2_gray,np.ones((erodeval,erodeval)))
    mat_2_gray     = cv2.dilate(mat_2_gray,np.ones((4,4)))
    _, contours,__ = cv2.findContours(mat_2_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:return True #If there were any movements
    return  False                    #if not


#Pedestrian Recognition Thread
def yoloThread():
    global frames,times
    model_path =   scriptFolder+"tiny.h5"     #Model weights
    sess = K.get_session()                    
    print("[PiCam] Loading anchors file...")
    anchors = [1.08,1.19,3.42,4.41,6.63,11.38,9.42,5.11,16.62,10.52] #Tiny Yolo anchors' values 
    anchors = np.array(anchors).reshape(-1, 2)
    print("[PiCam] Loading yolo model ({})...".format(scriptFolder+"tiny.h5"))
    yolo_model = load_model(model_path)  #Loading Tiny YOLO
    num_anchors = len(anchors)      
    print('[PiCam] YOLO model loaded !'.format(model_path))

    model_image_size = yolo_model.layers[0].input_shape[1:3] #Get input shape
    yolo_outputs = yolo_head(yolo_model.output, anchors, 20) 
    input_image_shape = K.placeholder(shape=(2, ))
    boxes, scores, classes = yolo_eval(yolo_outputs,input_image_shape,score_threshold=0.1,iou_threshold=0.6)
    num = 0 #Starting Photo's name
    old_time = 0.0 #Latest time

    print("[PiCam] YOLO Thread started!")
### Loop:
    while True:
        if len(frames) != 0:
            try:
                cv2.waitKey(17) 
                mat = frames[0] #Get First frame with movements
                mat = cv2.resize(mat,(model_image_size[0],model_image_size[1]))
                in_mat = np.array(mat,dtype='float32')
                in_mat /= 255.  # Scaling 
                in_mat = np.expand_dims(in_mat, 0)
                if (times[0] - old_time) > time_chunk:
                    #Searching for detection:
                    out_boxes, out_scores, out_classes = sess.run([boxes, scores, classes],feed_dict={yolo_model.input: in_mat,input_image_shape: [mat.shape[1], mat.shape[0]],K.learning_phase(): 0})
                    print(out_classes)
                    if len(out_boxes) > 0:
                        writ = False
                        xs,ys = [],[]  #X's and Y's coordinate
                        out_classes = list(set(out_classes))
                        for i, c in reversed(list(enumerate(out_classes))):
                            if (c == 1) or (c == 14) or (c == 11) or (c == 6): # 14 is the label for persons
                                if c == 14:
                                    msg  =  'Person Detected'
                                    print('Sending Hologram Message')
                                    subprocess.call('/home/pi/PoochPak/hologram_msg.py "{}"'.format(msg), shell=True)
                                writ = True
                                box = out_boxes[i]
                                top, left, bottom, right = box
                                top = max(0, np.floor(top + 0.5).astype('int32'))
                                left = max(0, np.floor(left + 0.5).astype('int32'))
                                bottom = min(mat.shape[1], np.floor(bottom + 0.5).astype('int32'))
                                right = min(mat.shape[0], np.floor(right + 0.5).astype('int32'))
                                xs.append(left+i)
                                xs.append(right-i)
                                ys.append(top+i)
                                ys.append(bottom-i)
                        if writ:
                            img_name = scriptFolder+"imgs/{}.png".format(num)
                            cv2.imwrite(img_name,mat[min(ys):max(ys),min(xs):max(xs)]) #Only saving the rectangle in which persons' got detected
                            out_s = "[{}] Detected person (taken {}s)!\n".format(time.strftime("%H:%M:%S"),round(time.time()-times[0])) #Log output
                            print(out_s)
                            flog.write(out_s)
                            flog.flush()
                            num += 1
                            old_time = times[0] #Updating detection time
            except Exception as ex:
                print("[PiCam] Some error occured in YOLO Thread ({}) :".format(time.strftime("%H:%M:%S")),ex)
            del times[0]   #Deleting first Detection time
            del frames[0]  #Deleting first Frame
        cv2.waitKey(50)

'''
Main code from here :
'''

if __name__ == "__main__":
    print("Starting PiCam....")
    name = time.strftime("%c").replace(" ","_")[0:10]
#Camera Input
    cap = None
    try:
        cap = cv2.VideoCapture(num_cam) #Trying to open camera
        _,dim = cap.read()
        if not _ or dim.shape == (0,0,0) :
            printExit("[PiCam] Error occured when opening the camera stream!")
        h = dim.shape[0]
        w  = dim.shape[1]
        print("[PiCam] Height:{} | Width:{}".format(h,w))
    except:
        printExit("[PiCam] Error occured when opening the camera stream!")
#Video Output
    writer = None
    err = "[PiCam] Error occured when opening the output video stream!"
    load = handleFile(name) #Updating web_file
    if not load:system("mv {}.avi {}_.avi".format(baseFolder+name,baseFolder+name))
    writer = cv2.VideoWriter(baseFolder+name+".avi", cv2.VideoWriter_fourcc(*"MJPG"), 21,(w,h), True)
    if not writer.isOpened():
        printExit(err) #If output Stream is unavailable
#Loading video file of the same day:
    if not load:
        try:
            print("[PiCam] Loading old video File...",end="")
            read = cv2.VideoCapture(baseFolder+name+"_.avi")
            _,mat = read.read()
            while _ :
                if mat.shape == (0,0,0) or mat.shape[0] != h or mat.shape[1] != w:
                    print("[PiCam] Couldn't load old file skipping(shape {})...!".format(mat.shape))
                    break
                writer.write(mat)
                _,mat = read.read()
            del read,mat
            print("loaded!")
        except:
            print("\n[PiCam] Couldn't load old file skipping...!")
        system("rm {}_.avi".format(baseFolder+name)) #Removing old video file
        
#Starting Yolo thread
    yoloThread = threading.Thread(target=yoloThread)
    print("[PiCam] Starting Yolo Thread....")
    yoloThread.start()


    day = time.strftime("%d") #startin' day
    frc = 0 #Frame count
#Loop's start
    print("[PiCam] Starting main loop...")
    while True:
        try:
            _,a = cap.read()
            if a.shape == (0,0,0):
                #If Frame was empty trying frame_check times and then breaking program
                for i in range(frame_check):
                    _,a = cap.read()
                    if a.shape != (0,0,0):break
                    if i == frame_check-1:printExit("[PiCam] Error with camera stream!")

            cv2.waitKey(33)
            _,b = cap.read()
            move = movement(a,b)

            #if we have got a movement
            if move:
                print("[PiCam] Movement ({})".format(time.strftime("%H:%M:%S")))
                if frc % 2 == 0:   #Only each two frames with movement are passed to YOLO Thread
                    frames.append(b.copy())  #Frame with movement
                    times.append(time.time())#Detection Time
                frc += 1 #FrameCount +1
                cv2.putText(b,name.replace("_"," ")+" "+time.strftime("%H:%M:%S"),(50,h - 50),cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255))
                writer.write(cv2.resize(b,(w,h))) #Adding to File

            if time.strftime("%d") != day:
                writer.release() #Closing old video output
                frc = 0          
                print("[PiCam] Cleaning imgs dir...")
                system("rm {}".format(scriptFolder+"imgs/*"))
                #Handling FLOG:
                flog.close()
                system("echo '### PiCam Live Logs###' > {}".format(baseFolder+"logs")) #Cleaning Logs file
                flog = open(baseFolder+"logs","a") 
                #FLOG end
                print("[PiCam] New day! Restarting video output....")
                name = time.strftime("%c").replace(" ","_")[0:10]
                writer = cv2.VideoWriter(baseFolder+name+".avi", cv2.VideoWriter_fourcc(*"MJPG"), 21,(w,h), True)
                print("[PiCam] Updating index.html...")
                handleFile(name)
                day = time.strftime("%d")
                print("[PiCam] Done! Resuming main loop...")
        except Exception as ex:
            print("Some error occured : ",ex)
            sys.exit(-1)
