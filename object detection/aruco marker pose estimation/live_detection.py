import cv2
import cv2.aruco as aruco

class ArucoTagDetector:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters()

    def get_aruco_tag_number(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = aruco.ArucoDetector(self.aruco_dict, self.parameters)
            corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

            if ids is not None:
                for i in range(len(ids)):
                    cv2.polylines(frame, [corners[i].astype(int)], True, (0, 255, 0), 2)
                    cv2.putText(frame, str(ids[i][0]), (corners[i][0][0][0], corners[i][0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    print(f"Aruco tag detected: {ids[i][0]}")

            cv2.imshow('Aruco Tag Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = ArucoTagDetector()
    detector.get_aruco_tag_number()