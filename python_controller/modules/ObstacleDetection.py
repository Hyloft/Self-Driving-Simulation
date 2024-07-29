import cv2
import numpy as np
import math

def calculate_hypotenuse(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

class ObstacleDetection:
    def __init__(self, min_area=8000):
        self.MIN_AREA = min_area
        self.barriers = []

    def process_image(self, img, print=False):
        img = cv2.imread(img) if type(img) == str else img
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv_img,(170, 50, 50), (180, 255, 255))
        mask2 = cv2.inRange(hsv_img,(0, 50, 50), (10, 255, 255))
        final_mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.detect_objects(contours, img)

        if print:
            cv2.imshow("Orijinal görüntü", img)
            cv2.imshow("Sonuç", final_mask)
            cv2.waitKey(1)
        return final_mask

    def detect_objects(self, contours, img):
        for contour in contours:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            try:
                first_corner = approx[0][0]
                x1, y1 = first_corner
                second_corner = approx[1][0]
                x2, y2 = second_corner
                if len(approx) != 4:continue
                distances = []
                for i in range(2):
                    x1, y1 = approx[i*(i+1)][0]
                    x2, y2 = approx[i*(i+1)+1][0]
                    d = calculate_hypotenuse(x1,y1,x2,y2)
                    distances.append(d)
                print(distances)
                
                if min(distances)/max(distances) <0.75 :
                    cv2.circle(img, (x1, y1), 5, (0, 255, 0), -1)
                    print('FOUND ONE')
                
            except:
                pass

            #print("Köşe koordinatları:", approx)

            if cv2.contourArea(contour) > self.MIN_AREA:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    center_x = int(M['m10'] / M['m00'])
                    center_y = int(M['m01'] / M['m00'])
                    weightCenter = (center_x, center_y)

                    #cv2.circle(img, weightCenter, 5, (0, 0, 255), -1)

                    downLeftPoint = np.amax(approx, axis=0)
                    upRightPoint = np.amin(approx, axis=0)

                    self.barriers.append([weightCenter, (downLeftPoint, upRightPoint)])
                    #print(self.barriers)
                    #x, y, w, h = cv2.boundingRect(contour)
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

def main():
    processor = ObstacleDetection()
    processor.process_image("den.png")

if __name__ == "__main__":
    main()