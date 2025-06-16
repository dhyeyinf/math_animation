from manim import *
import numpy as np

class PeanoCurve(Scene):
    def construct(self):
        # Scene setup
        self.camera.background_color = "#1e1e1e"
        title = Text("Peano Curve", font_size=48).to_edge(UP)
        self.add(title)

        # Parameters
        order = 3  # Keep order low (3 or 4 max)
        size = 6   # Size of the curve

        # Generate Peano curve points
        points = self.generate_peano(order, size)

        # Create the path
        path = VMobject()
        path.set_points_as_corners(points)
        path.set_stroke(color=BLUE_C, width=4, opacity=1)

        # Animate
        self.play(Create(path, run_time=8, rate_func=linear))
        self.wait(3)

    def generate_peano(self, order, size):
        def peano(n, angle=PI/2, direction=1):
            if n == 0:
                return []
            
            cmds = []
            cmds += peano(n-1, -angle, direction)
            cmds += [None]  # Draw line
            cmds += [angle * direction]
            cmds += peano(n-1, angle, direction)
            cmds += [None]
            cmds += [angle * direction]
            cmds += peano(n-1, angle, -direction)
            cmds += [None]
            cmds += [-angle * direction]
            cmds += peano(n-1, -angle, -direction)
            cmds += [None]
            cmds += [-angle * direction]
            cmds += peano(n-1, -angle, direction)
            cmds += [None]
            cmds += [angle * direction]
            cmds += peano(n-1, angle, direction)
            cmds += [None]
            cmds += [angle * direction]
            cmds += peano(n-1, angle, -direction)
            cmds += [None]
            cmds += [-angle * direction]
            cmds += peano(n-1, -angle, -direction)
            return cmds

        cmds = peano(order)
        points = [np.array([0, 0, 0])]  # Start at origin
        step_size = size / (3**order)
        direction = np.array([step_size, 0, 0])  # 3D vector
        angle = 0

        for cmd in cmds:
            if cmd is None:
                # Create rotation matrix (2D rotation in xy-plane)
                rot_matrix = np.array([
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]
                ])
                # Apply rotation to direction
                new_dir = rot_matrix @ direction
                new_point = points[-1] + new_dir
                points.append(new_point)
            else:
                # Update angle
                angle += cmd

        # Center the curve
        points = np.array(points)
        points -= (points.max(axis=0) + points.min(axis=0)) / 2
        return points.tolist()  # Convert back to list of arrays

# Render in high quality
if __name__ == "__main__":
    config.quality = "high_quality"
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60