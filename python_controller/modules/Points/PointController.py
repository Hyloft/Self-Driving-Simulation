import pandas as pd
import numpy as np
try:
    from Waypoint import Waypoint
except:
    from .Waypoint import Waypoint
from typing import List

import math
import functools

sign = functools.partial(math.copysign, 1) # either of these
sign = lambda x: math.copysign(1, x)

class WaypointController:
    def __init__(self,csv_name,avoid_distance,offset,initial_road,variance_offset=0.5) -> None:
        self.csv_name = csv_name
        self.avoid_distance = avoid_distance
        self.offset = offset
        self.variance_offset = variance_offset
        self.initial_road = initial_road
        
        # self.df = pd.read_csv(csv_name)
        # self.waypoints = self.get_coordinates()
        self.all_waypoints = self._read_coordinates_from_csv(self.csv_name)
        self.waypoints = []
        self.set_waypoints_by_road(initial_road)
        self.obstacles = []
    
    def get_waypoints(self):
        return self.waypoints
    
    def set_waypoints_by_road(self,road:str):
        # i.e: ABUTSLMW
        paths = [road[i]+road[i+1] for i in range(len(road)-1)]
        
        arr = []
        
        for item in [self._get_points_by_segments(p) for p in paths]:
            arr+=item
        
        self.waypoints = arr
        return arr
    
    # def get_coordinates(self):
    #     coordinates = list(zip(self.df['X'], self.df['Y']))
    #     return coordinates
    
    def find_close_point_indexes(self,x,y,distance):
        close_points_indexes = []
        for i in range(len(self.waypoints)):
            d = np.sqrt((self.waypoints[i][0] - x)**2 + (self.waypoints[i][1] - y)**2)
            if d <= distance:
                close_points_indexes.append(i)
                print(i)
        return close_points_indexes
    
    def get_road_eigen_by_segment(self,name):
        wps = self._get_points_by_segments(name)
        s = wps[0]
        e = wps[-1]
        cx,cy = self.waypoints[s][0],self.waypoints[s][1]
        tx,ty = self.waypoints[e][0],self.waypoints[e][1]
        if abs(cx-tx)>abs(cy-ty):
            return 90 * sign(tx-cx)
        else:
            return 0 if sign(ty-cy) else 180
    
    def handle_obstacle(self,x,y):
        if (x,y) in self.obstacles: return self.waypoints
        indexes_in_avoid_range = self.find_close_point_indexes(x,y,self.avoid_distance)
        
        if len(indexes_in_avoid_range)<1:
            return self.waypoints
        
        x_mean = sum([self.waypoints[i][0] for i in indexes_in_avoid_range]) / len(indexes_in_avoid_range)
        y_mean = sum([self.waypoints[i][1] for i in indexes_in_avoid_range]) / len(indexes_in_avoid_range)
        
        x_var = sum([(self.waypoints[i][0] - x_mean)**2 for i in indexes_in_avoid_range]) / len(indexes_in_avoid_range)
        y_var = sum([(self.waypoints[i][1] - y_mean)**2 for i in indexes_in_avoid_range]) / len(indexes_in_avoid_range)
        
        for i in indexes_in_avoid_range:
            new_x = self.waypoints[i][0] + ((-1 if x_mean < x else 1 if x_mean > x else 0) * self.offset if x_var<self.variance_offset or (x_var>self.variance_offset or y_var>self.variance_offset)  else 0)
            new_y = self.waypoints[i][1] + ((-1 if y_mean < y else 1 if y_mean > y else 0) * self.offset if y_var<self.variance_offset or (x_var>self.variance_offset or y_var>self.variance_offset) else 0)
            self.waypoints[i] = (new_x,new_y)
            print((new_x,new_y))
        
        self.obstacles.append((x,y))
        return self.waypoints
    
    def _read_coordinates_from_csv(self,csv_file):
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Check if the required columns exist
        if 'Segment' not in df.columns or 'X' not in df.columns or 'Y' not in df.columns:
            raise ValueError("CSV file must contain 'Segment', 'X', and 'Y' columns")
        
        # Extract the 'Segment', 'X', and 'Y' columns and create Waypoint instances
        waypoints = [Waypoint(row['Segment'], row['X'], row['Y']) for _, row in df.iterrows()]
        
        return waypoints

    def _get_points_by_segments(self,segment):
        all_segments = self._get_unique_segments()
        if segment not in all_segments:
            segment = segment[::-1]
            return reversed([w for w in self.all_waypoints if w.segment == segment])
            
        return [w for w in self.all_waypoints if w.segment == segment]
    
    def _get_unique_segments(self):
        unique_segments = set()
        for waypoint in self.all_waypoints:
            unique_segments.add(waypoint.segment)
        return unique_segments
    
def main():
    pc = WaypointController('points.csv',3,2.5,'ABUTSLMW')
    
    print(pc.get_waypoints())

if __name__ == '__main__':
    main()
    
    