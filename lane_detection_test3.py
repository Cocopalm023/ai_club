import cv2
import numpy as np 
import math

cap = cv2.VideoCapture("test_video02.mp4")

min_slope = -0.1
max_slope = 0.1






def slope_weight(slope,y1):

    max_distance_weight = 1
    min_distance_weight = 0
    max_distance = 0
    min_distance = 480
    slope = ((max_distance_weight-min_distance_weight)/(min_distance-max_distance)*(y1-max_distance))

    return slope


def pwm(sum_slope):
    max_pwm = 255
    min_pwm = 60
    if sum_slope > 0:
        right_pwm = right_pwm*sum_slope
    elif sum_slope < 0:
        left_pwm = left_pwm*sum_slope
    return right_pwm,left_pwm


def main():

#crop img
    x=0
    y=0
    w=640
    h=480
#adjust size
    x_size = 640
    y_size = 480
    path_list = []
    

    while True:
        ret,frame = cap.read()

        if not cap.isOpened():
          print("Cannot open camera")
          exit()

        if not ret :
            print("error")
            break

        if ret:
            crop_frame = frame[y:h-y, x:w-x]
            size = cv2.resize(crop_frame, (x_size,y_size), interpolation=cv2.INTER_AREA)
            #pts1 = np.float32(([135,10],[40,70],[520,70],[435,10]))
            #pts2 = np.float32(([0,0],[0,480],[640,480],[640,0]))
            #matrix = cv2.getPerspectiveTransform(pts1, pts2)
            #frameoutput = cv2.warpPerspective(size, matrix, (w-x,h-y))
            gray = cv2.cvtColor(size, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            edges = cv2.Canny(blur, 75, 100)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 25, maxLineGap=5, minLineLength=40)

            sum_slope = 0
            count = 0
            final_slope = 0
            right_pwm = 255
            left_pwm = 255
            if lines is None: 
                continue
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(size, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    if(x2-x1) == 0:
                        continue  
                    else:
                        slope = float((y1-y2)/(x2-x1))
                        if(max_slope > slope > min_slope):
                            continue
                        #print("x:",x2-x1)
                        #print("y",y1-y2)
                        if slope == float("inf") or slope == float("nan"):
                            continue
                        else:
                            count = count + 1
                            sum_slope = sum_slope + slope  
                        
            
            if count != 0:
                sum_slope = sum_slope/count
            
                path_list.append(sum_slope)

                for i in range(len(path_list)):
                    final_slope = final_slope + path_list[i]

                final_slope = final_slope/len(path_list)

                if len(path_list) == 60:
                    path_list.pop(0)

            if 0.1 > final_slope > -0.1:
                print("straight")
            elif 0.2 > final_slope > 0.1:
                print("right")
            elif final_slope > 0.2:
                print("BIG right")
            elif -0.2 < final_slope < -0.1:
                print("left")
            elif final_slope < -0.2:
                print("BIG left")
            #print("final_slope:",final_slope)
            cv2.imshow("frame",size)

        if cv2.waitKey(30) == ord('q'):
            break
            
            
if __name__ == '__main__':
    main()           

            

    

