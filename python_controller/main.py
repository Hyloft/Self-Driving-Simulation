from utils.SocketHandler import SocketHandler,get_decoded_image
from modules.ObstacleDetection import ObstacleDetection
import cv2
import numpy as np
import math
from modules.Nav.Navigator import Navigator,Path
from modules.Controllers.CustomController import CustomController
from modules.Points.PointController import WaypointController

obstacle_detector = ObstacleDetection()


multiply = 1

## SET ROADS
A=Path('A',right='B',straight='N')
B=Path('B',right='C',left='A',straight='U')
C=Path('C',right='D',left='B',straight='P')
D=Path('D',left='C',straight='E')
E=Path('E',straight='F',back='D',right='X',left='P')
X=Path('X',straight='G',back='E')
F=Path('F',left='O',straight='G',back='E')
G=Path('G',left='I',back='F',right='X',straight='Y')
Y=Path('Y',right='G',left='J')
I=Path('I',right='G',left='J',back='O') 
J=Path('J',right='I',left='K',back='R',straight='Y')
K=Path('K',right='J',back='L')
L=Path('L',right='S',straight='K',back='M')
M=Path('M',left='W',straight='L',back='N')
N=Path('N',right='U',straight='M',back='A')
P=Path('P',right='E',left='U',straight='O',back='C')
O=Path('O',right='F',left='Q',straight='I',back='P')
U=Path('U',right='P',left='N',straight='T',back='B')
W=Path('W',right='M',left='1')
T=Path('T',back='U',right='Q',left='S')
Q=Path('Q',right='O',straight='R',back='T')
S=Path('S',back='T',left='L',straight='R')
R=Path('R',straight='J',left='S',right='Q')
P1=Path('1',right='W')

aims=['X','Y','1']

nav = Navigator([A,B,C,D,E,X,F,G,Y,I,J,K,L,M,N,P,O,U,W,T,Q,S,R,P1],aims,'AB')
last_path = nav.get_next_path()
waypoint_controller = WaypointController('points.csv',3.5,1.76,last_path)
controller = CustomController(waypoint_controller.get_waypoints(),3.0*multiply,stop_seconds_on_destination=5)



def handle_image(ws,data):
    image = get_decoded_image(data)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def handle_reward(ws,reward):
    pass

def handle_coords(ws,data):
    print(data)
    x=float(data.split(':')[0].replace(',','.'))*multiply
    y=float(data.split(':')[1].replace(',','.'))*multiply
    theta = float(data.split(':')[2].replace(',','.'))

    print('theta:',theta)
    print(f'car x:{x} y:{y}')
    steering = controller.compute_steering_angle(x,y,theta,degrees=True)
    steering = int(steering)
    print('steering:',steering)

    ws.send(f'{controller.speed}:{(-steering)}:{controller.brake}')
    
    if controller.stop_handled == False:
        new_path = nav.get_next_path()
        wps = waypoint_controller.set_waypoints_by_road(new_path)
        controller.change_waypoints(wps)
        controller.stop_handled = True
        
        

def handle_obstacles(ws,data):
    print("HEARED OBSTACLE",data)
    x=float(data.split(':')[0].replace(',','.'))*multiply
    y=float(data.split(':')[1].replace(',','.'))*multiply
    wp = waypoint_controller.handle_obstacle(x,y)
    controller.change_waypoints(wp)

if __name__ == '__main__':
    socket = SocketHandler()
    # socket.add_event('image',handle_image)
    # socket.add_event('reward',handle_reward)
    socket.add_event('coords',handle_coords)
    socket.add_event('obstacle',handle_obstacles)
    socket.run()