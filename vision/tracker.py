import cv2
import mediapipe as mp
import numpy as np

class VisionTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)
        self.coords = (0, 0, 0) # x, y, z

    def get_eye_midpoint(self):
        success, image = self.cap.read()
        if not success:
            return None
        
        # Flip the image horizontally for a later selfie-view display
        # Convert the BGR image to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.face_mesh.process(image)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Landmark 168 is the bridge of the nose, between the eyes.
            # It's a stable point for head tracking.
            nose_bridge = face_landmarks.landmark[168]
            
            # Normalize coordinates to [-1, 1]
            x = (nose_bridge.x - 0.5) * 2
            y = (nose_bridge.y - 0.5) * -2 # Invert Y for screen coordinates
            
            # For Z, use the distance between eyes as a depth proxy.
            # Landmarks 33 (right outer) and 263 (left outer)
            left_eye = face_landmarks.landmark[263]
            right_eye = face_landmarks.landmark[33]
            
            eye_dist = np.sqrt(
                (left_eye.x - right_eye.x)**2 + 
                (left_eye.y - right_eye.y)**2 + 
                (left_eye.z - right_eye.z)**2
            )
            
            # Map eye_dist to a reasonable Z range. 
            # When close, eye_dist is larger. 
            # We'll use an inverse relationship or calibration later.
            z = -1 / (eye_dist + 0.0001) 
            
            self.coords = (x, y, z)
            return self.coords
            
        return None

    def release(self):
        self.cap.release()
