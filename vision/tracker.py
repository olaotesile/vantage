import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os

class VisionTracker:
    def __init__(self):
        # Path to the model file
        model_path = os.path.join(os.getcwd(), 'face_landmarker.task')
        
        # Configure Landmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
        
        self.cap = cv2.VideoCapture(0)
        self.coords = (0, 0, 0) # x, y, z

    def get_eye_midpoint(self):
        success, image = self.cap.read()
        if not success:
            return None, None
        
        # Image needs to be RGB and a MediaPipe Image object for detection
        image_flipped = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image_flipped, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        # Detect landmarks
        detection_result = self.detector.detect(mp_image)
        
        viz_image = image_flipped.copy()
        
        if detection_result.face_landmarks:
            face_landmarks = detection_result.face_landmarks[0]
            nose_bridge = face_landmarks[168]
            
            # Normalize coordinates to [-1, 1]
            x = (nose_bridge.x - 0.5) * 2
            y = (nose_bridge.y - 0.5) * -2 
            
            # Depth proxy
            left_eye = face_landmarks[263]
            right_eye = face_landmarks[33]
            eye_dist = np.sqrt((left_eye.x - right_eye.x)**2 + (left_eye.y - right_eye.y)**2)
            z = -1 / (eye_dist + 0.0001) 
            
            self.coords = (x, y, z)
            
            # Draw tracked point for preview
            h, w, _ = viz_image.shape
            cx, cy = int(nose_bridge.x * w), int(nose_bridge.y * h)
            cv2.circle(viz_image, (cx, cy), 5, (0, 255, 0), -1)
            
            return self.coords, viz_image
            
        return None, viz_image

    def release(self):
        self.cap.release()
