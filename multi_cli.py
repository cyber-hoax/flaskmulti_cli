import time
import argparse
import socketio
import cv2
import base64
from multiprocessing import Process
from cv import *


def _convert_image_to_jpeg(image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)
def data_tranfer(frame,msg):
    stream = _convert_image_to_jpeg(frame)
    sio.emit(
        'cv2server',
        {
            'image':stream,
            'text': msg,
            
        })
    time.sleep(1)
    #experiments
    
    
    stre = _convert_image_to_jpeg(frame)
    sio.emit(
        'cv3server',
        {
            'images':stre,
            'text': msg,
        })
    print("data emited")
    time.sleep(1)




#connectig camera url(urls) in parameter 
def streamer(uri):
    sio.connect('http://127.0.0.1:5000')
    print("connected")
    cap = cv2.VideoCapture(uri)
    print("process running")

    while(True):
        #get all opencv frame
        # Capture frame-by-frame
        ret, frame = cap.read()
        print(ret)
        frame=convert_gray_scale(frame)
        msg={'key':uri,
             'dst':10}
        
        #---------experiment block---------------------------#
        data_tranfer(frame,msg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    sio.disconnect()
sio = socketio.Client()


# sio.connect(
#                 'http://localhost:5001')
# #while True:

try:
    
    
    #call opencv vedio handler
    procs=1
    jobs=[]
    urs = [0,1]
    

    for i in range (len(urs)):
       # use Process tp use miltiprocess in streamer function passing parameter
        process=Process(target=streamer,args=(urs[i],))
        jobs.append(process)
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    
except Exception as e:
    print("cant connetc to server")
finally:
    

    print("disconnected")



