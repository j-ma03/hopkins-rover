import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO # Assuming you have a YOLO class in yolov5 module




class YOLOLivePredictor:
    def __init__(self, model_path, camera_index=0):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(camera_index)

    def getFrame(self):
        ret, frame = self.cap.read()
        return frame
    
#    def predict_and_display(self, frame):
#        ret, frame = self.cap.read()
#        # if not ret:
#        #     break
#
#        # Predict using YOLO model
#        results = self.model.predict(frame)
#
#        for result in results:
#            boxes = result.boxes
#            for box in boxes:
#                x1, y1, x2, y2 = map(int, box.xyxy[0])
#                confidence = box.conf[0]
#                class_id = int(box.cls[0])
#
#                class_name = self.model.names[class_id]
#
#                cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
#                cv2.putText(frame, f'Class: {class_name}, Conf: {confidence:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
#
#        # Display the frame
#        cv2.imshow('YOLO Live Feed', frame)
#
#        # Break the loop if 'q' is pressed
#        # if cv2.waitKey(1) & 0xFF == ord('q'):
#        #     break
#
#        # Release the camera and close all OpenCV windows
#        self.cap.release()
#        cv2.destroyAllWindows()





    def get_highest_confidence_bounding_box_area(self, frame):
        highest_confidence = 0
        best_box = None

        ret, frame = self.cap.read()
        
        results = self.model.predict(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                confidence = box.conf[0]
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    best_box = box

        if best_box is not None:
            x1, y1, x2, y2 = map(int, best_box.xyxy[0])
            width = x2 - x1
            height = y2 - y1
            return width * height
        else:
            return 0
        

    def displayBox(self, frame, box):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.imshow('YOLO Live Feed', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    model_path = 'best.pt'  # Replace with your model path
    predictor = YOLOLivePredictor(model_path)
    
    while True:
        # ret, frame = predictor.cap.read()
        frame = predictor.getFrame()
        cv2.imshow('YOLO Live Feed', frame)
        result = predictor.get_highest_confidence_bounding_box_area(frame)
        print('Area:', result)
        

