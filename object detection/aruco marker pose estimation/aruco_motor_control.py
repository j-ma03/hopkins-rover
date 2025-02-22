import live_detection
import cv2
from gpiozero import Robot, Motor


rovers = Robot(left=(7, 8), right=(10, 9))

if __name__ == "__main__":
    model_path = 'best.pt'  # Replace with your model path
    aruco_detector = live_detection.ArucoTagDetector()
    
    while True:
        area = aruco_detector.detect_aruco_area()
        
        

        if(area < 10000):
            rovers.forward()
        else:
            rovers.stop()

        if cv2.waitKey(1) & 0xFF == ord('q'):
           break