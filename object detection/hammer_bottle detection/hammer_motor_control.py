import predict_live
import cv2
from gpiozero import Robot, Motor


rovers = Robot(left=(7, 8), right=(10, 9))

if __name__ == "__main__":
    model_path = 'best.pt'  # Replace with your model path
    predictor = predict_live.YOLOLivePredictor(model_path)
    
    while True:
        # ret, frame = predictor.cap.read()
        frame = predictor.getFrame()
        cv2.imshow('YOLO Live Feed', frame)
        result = predictor.get_highest_confidence_bounding_box_area(frame)
        print('Area:', result)

        if(result > 5000):
            rovers.forward()
        else:
            rovers.stop()
        