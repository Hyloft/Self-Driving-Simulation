import numpy as np
import cv2
import math
import functools
from datetime import datetime

sign = functools.partial(math.copysign, 1) # either of these
sign = lambda x: math.copysign(1, x)

class CustomController:
    def __init__(self, waypoints, lookahead_distance,stop_seconds_on_destination=30):
        self.waypoints = waypoints
        self.lookahead_distance = lookahead_distance
        self.target_index = None
        self.current_index = None
        
        self.speed = 1
        self.brake = 0
        
        self.sleep_time = 0
        self.stop_start = datetime.now()
        self.stop_seconds_on_destination = stop_seconds_on_destination # seconds
        self.stop_handled = True
        
        
    def prepare_start(self,x,y):
        self.current_index = self.find_closest_point_index(x,y)
        self.target_index = self.find_closest_point_index(x,y)
    
    
    def handle_destination(self):
        self.sleep_time = self.stop_seconds_on_destination
        self.stop_start = datetime.now()
        self.brake = 1
        self.speed =0
        self.stop_handled = False
        
    def tick(self):
        if self.sleep_time>0:
            self.sleep_time = self.stop_seconds_on_destination - (datetime.now()-self.stop_start).seconds
        else:
            self.brake = 0
            self.speed = 1
        
    def get_current_road_segment(self)->str:
        return self.waypoints[self.current_index].segment
    
    def get_current_road_eigen(self):
        cx,cy = self.waypoints[self.current_index][0],self.waypoints[self.current_index][1]
        tx,ty = self.waypoints[self.target_index][0],self.waypoints[self.target_index][1]
        if abs(cx-tx)>abs(cy-ty):
            return 90 * sign(tx-cx)
        else:
            return 0 if sign(ty-cy) else 180
    
    def change_waypoints(self,waypoints):
        self.waypoints = waypoints

    def find_closest_point_index(self, x, y):
        distances = [np.sqrt((px - x)**2 + (py - y)**2) for px, py in self.waypoints]
        return np.argmin(distances)

    def find_lookahead_point(self, x, y):
        if self.target_index == None:
            self.prepare_start(x,y)
            
        for i in range(self.target_index, len(self.waypoints)):
            distance = np.sqrt((self.waypoints[i][0] - x)**2 + (self.waypoints[i][1] - y)**2)
            if distance >= self.lookahead_distance:
                if i != self.target_index:
                    self.current_index = self.target_index
                self.target_index = i
                if i == (len(self.waypoints)-1):
                    self.handle_destination()
                return self.waypoints[i]
            
        return self.waypoints[-1]

    def compute_steering_angle(self, x, y, theta,degrees = False):
        if degrees == False:
            theta = math.degrees(theta)
        x_a,y_a = self.find_lookahead_point(x,y)
        self.tick()
        print(f'looking to x:{x_a} y:{y_a}')
        # Calculate the angle to the aim point in degrees
        theta_a = math.degrees(math.atan2(y_a - y, x_a - x))
        
        # Calculate the relative angle and normalize it to [-180, 180] degrees
        steering = theta_a - theta
        steering = (steering + 180) % 360 - 180
        
        steering = sign(steering) * 45 if abs(steering) > 45 else steering
        
        return steering

    def update_position(self, x, y, theta, velocity, steering_angle, dt):
        x += velocity * np.cos(theta) * dt
        y += velocity * np.sin(theta) * dt
        steering_angle = math.radians(steering_angle)
        theta += (velocity / self.lookahead_distance) * np.tan(steering_angle) * dt
        return x, y, theta
    
def main():
    pp = CustomController([(-3,-5),(1,2),(2,2),(2,33)],2)
    pp.prepare_start(2,3)
    wheel = pp.compute_steering_angle(2,3,0)
    print(wheel)
    
def test():
    path = [(0, 20), (10, 20), (20, 5), (15, 20),(10, 5)]  # Define your path here
    # path = [(-17.0,-30.75),(-14.6,-30.75),(-12.3,-30.75),(-10.0,-30.75)]
    # path = [(px * 10, py * 10) for (px, py) in path]
    lookahead_distance = 2.0
    add = 0
    pure_pursuit = CustomController(path, lookahead_distance)
    # pure_pursuit.prepare_start(0,20)
    x, y = 0, 20  # Initial position in meters

    # Initial position and orientation of the car
    initial_angle_degrees = 90
    initial_angle_radians = initial_angle_degrees * (math.pi / 180)
    theta = math.pi / 2 - initial_angle_radians  # Initial heading angle in radians
    velocity = 1.0  # m/s
    dt = 0.1  # time step in seconds

    # Visualization setup
    scale = 10  # Scale factor to fit path in the visualization window
    window_size = 500  # Size of the window
    frame_delay = 50  # Delay between frames in milliseconds

    # Create a blank image
    image = np.zeros((window_size, window_size, 3), dtype=np.uint8)

    # Draw the path
    for (px, py) in path:
        cv2.circle(image, (int((px+add) * scale), window_size - int((py+add) * scale)), 3, (0, 255, 0), -1)

    # Simulation loop with visualization
    for _ in range(650):
        # Copy the original image to draw on
        img = image.copy()

        # Compute steering angle and update position
        steering_angle = pure_pursuit.compute_steering_angle(x, y, theta)
        steering_angle_degrees = steering_angle
        look = pure_pursuit.find_lookahead_point(x,y)
        x, y, theta = pure_pursuit.update_position(x, y, theta, velocity, steering_angle, dt)

        # Draw the car
        car_position = (int((x+add) * scale), window_size - int((y+add) * scale))
        cv2.circle(img, car_position, 5, (0, 0, 255), -1)

        # Draw the heading direction
        heading_end = (int((x+add + 2 * np.cos(theta)) * scale), window_size - int((y+add + 2 * np.sin(theta)) * scale))
        cv2.line(img, car_position, heading_end, (255, 0, 0), 2)

        # Display the steering angle
        cv2.putText(img, f"Steering Angle: {steering_angle_degrees:.2f} degrees", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(img, f"Look: {look}", (10, 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Show the image
        cv2.imshow('Pure Pursuit', img)
        if cv2.waitKey(frame_delay) & 0xFF == 27:  # Press 'ESC' to exit
            break

    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
    main()
    test()