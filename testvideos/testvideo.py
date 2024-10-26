from manim import *

from manim_physics import *


class MagneticFieldExample(ThreeDScene):
    def construct(self):
        wire = Wire(Circle(2).rotate(PI / 2, UP))
        mag_field = MagneticField(
            wire,
            x_range=[-5, 5],
            y_range=[-5, 5],
        )
        self.set_camera_orientation(PI / 3, PI / 5)
        self.add(wire, mag_field)
