class Waypoint:
    def __init__(self, segment, x, y):
        self.segment = segment
        self.x = x
        self.y = y

    def __call__(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Waypoint(segment={self.segment}, x={self.x}, y={self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 'segment':
            return self.segment
        elif key == 'x':
            return self.x
        elif key == 'y':
            return self.y
        else:
            raise IndexError("Invalid key. Use 0 for x, 1 for y, 'segment' for segment, 'x' for x, and 'y' for y.")
    
    
def main():
    wp = Waypoint('AB',1,1)
    w = wp
    print(w)
    print(wp[0])
    print(wp[1])
    print(wp.segment)
    
if __name__ == '__main__':
    main()