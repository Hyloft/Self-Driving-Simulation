from typing import Any, Callable
from flask import Flask
from flask_sock import Sock
from io import BytesIO
from PIL import Image
from base64 import b64decode
import time
import numpy as np
import cv2
import json

class SocketHandler:
    def __init__(self) -> None:
        self.events = {
        }
        self.state = {}
        self._set_socket()
    
    def add_event(self,name,fn:Callable[[Any,str], Any]):
        self.events[name] = fn
    
    def run(self):
        self.app.run('localhost','8080')
    
    def _handle_events(self,ws,data):
        event = data.split(':')[0]
        if event in self.events:
            self.events[event](ws,data.split(event+':')[1])
    
    def _set_socket(self):
        self.app = Flask(__name__)
        sock = Sock(self.app)
    
        @sock.route('/echo')
        def echo(ws):
            global last_time
            global is_responsed
            while True:
                data = ws.receive()
                # ws.send(6)
                if(data): self._handle_events(ws,data)
                    
## EXAMPLE USAGE                 
def get_decoded_image(str):
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

def handle_reward(ws,data):
    #data.split('reward:')[1]
    reward = float(data.replace(',','.'))
    print('got reward:',reward)\

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))


def handle_image(ws,data):
    image = get_decoded_image(data)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # code here to write after
    d,s = read_settings_from_json()
    if s!=0:out.write(opencvImage)
    
    # send message
    ## string type: '{speed(-1 to 1)}:{wheel(-30 to 30)}:{brake(0 or 1)}'
    ws.send(f'{s/3}:{d}:{0 if s is not 0 else 1}')
    print(f'image processed and output sended {s/3}:{d}:{0 if s is not 0 else 1}')
    cv2.imshow('video',opencvImage)
    cv2.waitKey(1)
    # cv2.waitKey(1)
    if s==0: 
        out.release()
        print('ended')



if __name__ == '__main__':
    socket = SocketHandler()
    socket.add_event('image',handle_image)
    socket.add_event('reward',handle_reward)
    socket.run()
    