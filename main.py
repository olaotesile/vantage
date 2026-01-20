from vision.tracker import VisionTracker
from render.scenemanager import SceneManager
import ursina

# Initialize these as None; they'll be set in main()
tracker = None
scene = None

def update():
    # Ursina automatically looks for a global 'update' function in the main script
    if tracker and scene:
        coords, frame = tracker.get_eye_midpoint()
        if coords:
            scene.update_camera(coords[0], coords[1], coords[2])
        if frame is not None:
            scene.update_preview(frame)

def main():
    global tracker, scene
    tracker = VisionTracker()
    scene = SceneManager()
    
    # We don't need to manually assign ursina.update if it's defined globally here
    scene.run()
    tracker.release()

if __name__ == "__main__":
    main()
