from manim import *
import numpy as np

class SierpinskiArrowhead(Scene):
    def construct(self):
        # High-quality settings
        self.camera.background_color = "#1e1e1e"  # Dark background
        self.camera.frame_rate = 60  # Smoother animation

        # Parameters
        order = 7  # Increase for more complexity (7 is practical limit for smooth animation)
        size = 8   # Larger size for better detail

        # Generate Sierpiński arrowhead curve points
        points = self.generate_sierpinski(order, size)

        # Create the path with better anti-aliasing
        path = VMobject()
        path.set_points_as_corners(points)
        path.set_stroke(width=4, color=YELLOW_C, opacity=1)  # Thicker, bright curve

        # Animation with smoother interpolation
        self.play(
            Create(path, run_time=8, rate_func=linear),
            lag_ratio=0.01
        )
        self.wait(2)

    def generate_sierpinski(self, order, size):
        # L-system parameters for Sierpiński arrowhead curve
        axiom = "A"
        rules = {"A": "B-A-B", "B": "A+B+A"}
        angle = 60 * DEGREES

        # Generate the L-system string
        def lsystem(axiom, rules, iterations):
            path = axiom
            for _ in range(iterations):
                path = "".join(rules.get(c, c) for c in path)
            return path

        instructions = lsystem(axiom, rules, order)

        # Interpret the L-system string as drawing commands
        pos = np.array([0.0, 0.0, 0.0])
        direction = np.array([1, 0, 0])
        points = [pos.copy()]
        current_angle = 0

        # Calculate step length to fit the curve in the scene
        step = size / (2 ** order)

        for cmd in instructions:
            if cmd in "AB":
                # Move forward in current direction
                rotation_matrix = np.array([
                    [np.cos(current_angle), -np.sin(current_angle), 0],
                    [np.sin(current_angle),  np.cos(current_angle), 0],
                    [0,                     0,                    1]
                ])
                move_vec = rotation_matrix @ (direction * step)
                pos += move_vec
                points.append(pos.copy())
            elif cmd == "+":
                current_angle += angle
            elif cmd == "-":
                current_angle -= angle

        # Center the curve
        points = np.array(points)
        points -= (np.max(points, axis=0) + np.min(points, axis=0)) / 2

        return [np.array([p[0], p[1], 0]) for p in points]

# Render in high quality
if __name__ == "__main__":
    config.quality = "high_quality"
    config.frame_rate = 60
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.output_file = "SierpinskiArrowhead_HD"
