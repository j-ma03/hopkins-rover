from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

imgPath = "/Users/noahm/Documents/MalletDetection/MalletDetection/orange hammer training/IMG_0432.jpg"

modelPath = "/Users/noahm/Documents/MalletDetection/MalletDetection/Mallet/runs/detect/yolov8s_mallet116/weights/best.pt"

model = YOLO(modelPath)

results = model.predict(imgPath)

img = cv2.imread(imgPath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


for result in results:
   boxes = result.boxes
   for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0]
        class_id = int(box.cls[0])

        class_name = model.names[class_id]
        

        formatted_result = {
            'class': class_name,
            'confidence': confidence.item(),
            'bbox': [x1, y1, x2, y2]
        }
        cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=6)
        cv2.putText(img, f'Class: {class_name}, Conf: {confidence:.2f}', (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 255, 0), 2)
        

plt.imshow(img)
plt.axis('off')
plt.show()

print(formatted_result)
    