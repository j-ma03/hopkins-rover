import predict_live
import cv2
from gpiozero import Robot, Motor


rovers = Robot(left=(7, 8), right=(10, 9))

if __name__ == "__main__":
    model_path = 'best.pt'  # Replace with your model path
    predictor = predict_live.YOLOLivePredictor(model_path)
    
    while True:
        ret, frame = predictor.cap.read()
        height, width, channels = frame.shape
        if not ret:
            break
        # result = predictor.get_highest_confidence_bounding_box_area(frame)
        # print('Area:', result)
        # x1, y1, x2, y2 = map(int, box)
        # cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        # cv2.imshow('YOLO Live Feed', frame)
        # cv2.waitKey(0)


        box = predictor.get_highest_confidence_bounding_box(frame)
        x1, y1, x2, y2 = map(int, box)
        
        center = predictor.get_box_center_point(box)
        if(x1 < 0):
            continue
            
        third = width / 3

        if(center < third):
            print("Turn left")
        elif(center < third * 2):
            print("In center")
        elif(center < width):
            print("Turn right")
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
#
    predictor.cap.release()
    cv2.destroyAllWindows()
        