from ursina import *

class SceneManager:
    def __init__(self):
        self.app = Ursina()
        self.setup_scene()
        
    def setup_scene(self):
        # Create a "room" or box
        Entity(model='cube', color=color.gray, scale=(10, 10, 1), position=(0, 0, 5)) # Back wall
        Entity(model='cube', color=color.dark_gray, scale=(1, 10, 10), position=(-5, 0, 0)) # Left wall
        Entity(model='cube', color=color.dark_gray, scale=(1, 10, 10), position=(5, 0, 0)) # Right wall
        
        # Some objects inside
        self.target = Entity(model='cube', color=color.orange, scale=(1,1,1), position=(0,0,0))
        
        # Initial camera setup
        camera.position = (0, 0, -10)
        camera.look_at(self.target)

    def update_camera(self, x, y, z):
        # x and y are in range [-1, 1], z is depth proxy (negative)
        
        # Physical scaling factors (adjust based on monitor size)
        scale_x = 5.0
        scale_y = 3.0
        
        # Position the camera in world space
        camera.x = x * scale_x
        camera.y = y * scale_y
        camera.z = z # depth
        
        # Off-axis projection: shift the lens in the opposite direction
        # to keep the "window" (screen) centered.
        # Panda3D's film_offset is in normalized units.
        camera.lens.set_film_offset((-x, -y))

    def run(self):
        self.app.run()
