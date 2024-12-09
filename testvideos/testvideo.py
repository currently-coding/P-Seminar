from manim import *
from manim_physics import *


class MagneticFieldExample(ThreeDScene):
    def construct(self):
        def FieldUpdater(mob):
            mob.become(
                MagneticField(
                    *wires, x_range=[-10, 10], y_range=[-10, 10]
                )  # Unpack list
            )

        # Define the number of wires
        num_wires = 6  # Example with 6 wires; change to any number
        radius = 2  # Distance from the origin for each wire

        # Create all wires at the origin initially
        wires = [
            Wire(Circle(2)).rotate(PI / 2, UP).move_to(ORIGIN) for _ in range(num_wires)
        ]

        # Calculate target positions in a circular layout
        spacing = 2  # Base distance factor for spacing, can be adjusted as needed
        target_positions = [
            np.array(
                [(i - (num_wires - 1) / 2) * spacing, 0, 0]
            )  # Position along x-axis
            for i in range(num_wires)
        ]

        # Create the magnetic field using all wires
        mag_field = MagneticField(
            *wires, x_range=[-10, 10], y_range=[-10, 10]
        )  # Unpack list
        mag_field.add_updater(FieldUpdater)
        self.set_camera_orientation(PI / 4, PI / 3)

        # Animate each wire moving to its circular target position
        self.play(Create(mag_field), *[Create(wire) for wire in wires])
        self.wait(4)
        self.play(
            *[
                wire.animate.move_to(target)
                for wire, target in zip(wires, target_positions)
            ],
        )

        self.wait(10)


# error: https://github.com/Matheart/manim-physics/issues/34
# fixed in venv
