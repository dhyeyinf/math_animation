from manim import *
import numpy as np

class HilbertCurve(Scene):
    def construct(self):
        # High-quality settings
        self.camera.background_color = "#1e1e1e"  # Dark background
        self.camera.frame_rate = 60  # Smoother animation
        
        # Parameters
        order = 7  # More complex curve
        size = 8   # Larger size for better detail
        
        # Generate Hilbert curve points
        points = self.generate_hilbert(order, size)
        
        # Create the path with better anti-aliasing
        path = VMobject()
        path.set_points_as_corners(points)
        path.set_stroke(width=4, color=BLUE_C, opacity=1)  # Thicker, brighter curve
        
        # Animation with smoother interpolation
        self.play(
            Create(path, run_time=8, rate_func=linear),  # Smooth, constant speed
            lag_ratio=0.01  # Less lag between segments
        )
        self.wait(2)
    
    def generate_hilbert(self, order, size):
        def hilbert(n, angle=PI/2):
            if n == 0:
                return []
            cmds = []
            cmds += [angle]
            cmds += hilbert(n-1, -angle)
            cmds += [None]
            cmds += [-angle]
            cmds += hilbert(n-1, angle)
            cmds += [None]
            cmds += hilbert(n-1, angle)
            cmds += [-angle]
            cmds += [None]
            cmds += hilbert(n-1, -angle)
            cmds += [angle]
            return cmds

        cmds = hilbert(order)
        points = [np.array(ORIGIN)]
        direction = np.array(RIGHT) * size / (2**order)
        angle = 0

        for cmd in cmds:
            if cmd is None:
                rotation_matrix = np.array([
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]
                ])
                rotated = rotation_matrix @ direction[:2]
                if len(direction) > 2:
                    rotated = np.append(rotated, direction[2])
                new_point = points[-1] + rotated
                points.append(new_point)
            else:
                angle += cmd
        
        # Center the curve
        points = np.array(points)
        points -= (np.max(points, axis=0) + np.min(points, axis=0)) / 2
        
        return [np.array([p[0], p[1], 0]) for p in points]

# Render in high quality
if __name__ == "__main__":
    config.quality = "high_quality"  # 1080p, anti-aliased
    config.frame_rate = 60  # Smoother motion
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.output_file = "HilbertCurve_HD"