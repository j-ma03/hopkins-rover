# import a utility function for loading Roboflow models
from inference import get_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2

# define the image url to use for inference
#dir_path = "/Users/vicki/Downloads/hopkins-rover-main/object_detection/orange hammer training/IMG_421"
# directory = os.fsencode(dir_path)
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".asm") or filename.endswith(".py"): 
#         image = cv2.imread(filename)
#         continue
#     else:
#         continue

#for (int i = 0; )
image_file = "/Users/vicki/Downloads/hopkins-rover-main/object_detection/orange hammer training/IMG_0414.JPG"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
api_key = "bskz71LU7ndpmIJu4bE8"  # Replace with your actual API key
model = get_model(model_id="mallet-and-water-bottle/5", api_key=api_key)

# run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
results = model.infer(image)

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

# create supervision annotators
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with our inference results
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# display the image
sv.plot_image(annotated_image)

