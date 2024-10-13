from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolov8s.pt')
    model.to('cuda')


    results = model.train(
        data='data.yaml',
        imgsz=640,
        epochs=50,
        batch=8,
        name='yolov8s_mallet'
    )

