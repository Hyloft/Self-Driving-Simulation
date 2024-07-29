from flask import Flask, render_template
from flask_sock import Sock
from io import BytesIO
from PIL import Image
from base64 import b64decode
import time
import numpy as np
import cv2
import json


app = Flask(__name__)
sock = Sock(app)

last_time = time.time()
is_responsed = True

@sock.route('/echo')
def echo(ws):
    global last_time
    global is_responsed
    while True:
        data = ws.receive()
        # ws.send(6)
        if(data):
            
            if 'reward:' in data: # if message is reward
                is_responsed = True
                reward = float(data.split('reward:')[1].replace(',','.'))
                print('got reward:',reward)
            
            else: # if message is image data
                if(is_responsed): # dont run too fast and before get reward
                    is_responsed = False
                    image = getDecodedImage(data)
                    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    last_time = time.time()
                    
                    # code here to write after
                    d,s = read_settings_from_json()
                    
                    # send message
                    ## string type: '{speed(-1 to 1)}:{wheel(-30 to 30)}:{brake(0 or 1)}'
                    ws.send(f'{s/3}:{d}:{0 if s is not 0 else 1}')
                    print('image processed and output sended')
                    cv2.imshow('video',opencvImage)
                    cv2.waitKey(1)
                    # cv2.waitKey(1)

def getDecodedImage(str):
    return Image.open(BytesIO(b64decode(str)))


def read_settings_from_json():
    """
    Reads the degree and speed values from the JSON file and returns them as a tuple.
    
    Returns:
        tuple: A tuple containing the degree and speed values read from the JSON file.
    """
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            degree = data.get('degree', None)
            speed = data.get('speed', None)
            return degree, speed
    except FileNotFoundError:
        print("JSON file not found.")
        return 0, 0    

if __name__ == '__main__':
    app.run('localhost','8080')