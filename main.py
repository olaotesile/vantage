from vision.tracker import VisionTracker
from render.scenemanager import SceneManager
from ursina import update

def main():
    tracker = VisionTracker()
    scene = SceneManager()

    # Define the update function for Ursina
    def update():
        coords = tracker.get_eye_midpoint()
        if coords:
            # We add a bit of smoothing or scaling here if needed
            scene.update_camera(coords[0], coords[1], coords[2])

    # Assign the update function to Ursina's global update
    import ursina
    ursina.update = update

    scene.run()
    tracker.release()

if __name__ == "__main__":
    main()
