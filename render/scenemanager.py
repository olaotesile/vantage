from ursina import *
import PIL.Image
import cv2

class SceneManager:
    def __init__(self):
        self.app = Ursina()
        self.setup_scene()
        
    def setup_scene(self):
        # Create a "room" using grids to show off perspective
        # Floor & Ceiling (Smaller Room)
        Entity(model=Grid(10, 10, thickness=2), rotation_x=90, position=(0,-2,0), color=color.white33)
        Entity(model=Grid(10, 10, thickness=2), rotation_x=90, position=(0,2,0), color=color.white33)
        
        # Walls
        Entity(model=Grid(10, 10, thickness=2), rotation_y=90, position=(-2,0,0), color=color.white33)
        Entity(model=Grid(10, 10, thickness=2), rotation_y=90, position=(2,0,0), color=color.white33)
        Entity(model='cube', color=color.dark_gray, scale=(4,4,1), position=(0,0,2)) # Back wall

        # Add a real-life object: A Shoe
        self.target = Entity(model='shoe.glb', scale=1, position=(0,-0.5,0), rotation_y=180)
        # Small marker cube to verify rendering
        Entity(model='cube', color=color.red, scale=0.1, position=(0.5,0,0))

        # Lights to emphasize depth and details
        self.point_light = PointLight(position=(0, 5, -5), color=color.white)
        self.ambient_light = AmbientLight(color=color.rgba(180, 180, 180, 255))
        
        # Camera Preview in the corner
        self.preview = Entity(parent=camera.ui, model='quad', scale=(0.3, 0.2), position=(0.7, -0.4))
        self.preview.texture = Texture(PIL.Image.new('RGB', (100, 100), (0, 0, 0)))

        # Initial camera setup
        camera.position = (0, 0, -15)

    def update_camera(self, x, y, z):
        # x and y are in range [-1, 1], z is depth proxy (negative)
        
        # Physical scaling factors (adjust based on monitor size)
        scale_x = 8.0
        scale_y = 5.0
        
        # Position the camera in world space
        camera.x = x * scale_x
        camera.y = y * scale_y
        
        # Map z (which is around -5 to -20) to a stable viewing range
        # We'll use a base offset plus the eye tracking delta
        camera.z = z * 2.0 # Scale the depth effect
        
        # Off-axis projection: shift the lens in the opposite direction
        # to keep the "window" (screen) centered.
        camera.lens.set_film_offset((-x, -y))
        
        # Keep looking at the center
        camera.look_at(self.target)

    def update_preview(self, frame):
        if frame is not None:
            # Convert CV2 BGR to PIL RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = PIL.Image.fromarray(frame_rgb)
            # Update the texture
            self.preview.texture = Texture(pil_img)

    def run(self):
        self.app.run()
