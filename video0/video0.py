import numpy as np
from manim import *
import math


class MyScene(ThreeDScene):
    angular_speed = PI
    carousel_radius = 2
    num_chains = 8
    chain_length = 1.5
    theta = 0
    angle = 0
    t = 0

    def create_chain_and_seat_template(self):
        chain_start = np.array([self.carousel_radius, 0, 0])
        chain_end = chain_start * (1 + math.sin(self.theta) * self.chain_length / self.carousel_radius) + np.array([0, 0, -math.cos(self.theta) * self.chain_length])
        direc = chain_end - chain_start
        chain = Cylinder(radius=0.02, height=self.chain_length, direction=direc, color=WHITE).move_to(chain_start + direc / 2)
        seat = Sphere(radius=0.1, color=RED).move_to(chain_end)
        return VGroup(chain, seat)

    def create_carousel(self):
        # Create the carousel base (circular platform)
        base = Circle(radius=self.carousel_radius, color=BLUE).set_fill(WHITE, opacity=0.3)

        chains_and_seats = VGroup()
        template = self.create_chain_and_seat_template().rotate(self.angle, about_point=ORIGIN, axis=OUT)

        for _ in range(self.num_chains):
            chains_and_seats.add(template.copy())
            template.rotate(2 * math.pi / self.num_chains, about_point=ORIGIN, axis=OUT)

        return VGroup(base, chains_and_seats)

    def change_theta(self, dt):
        # TODO change this
        self.t += dt

        if self.t <= 2:
            pass
        elif self.t <= 3:
            self.theta = PI/6 * (1-math.cos(PI*(self.t-2)))
        elif self.t <= 5:
            pass
        else:
            self.theta = PI/6 * (1-math.cos(PI*(self.t-4)))

    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        swing_carousel = self.create_carousel()

        # Add carousel to the scene
        self.add(swing_carousel)

        # Define an updater to continuously change the angle `self.theta` over time
        def update_carousel(mob, dt):
            self.change_theta(dt)  # Oscillating change in angle
            seat_radius = self.carousel_radius + self.chain_length * math.sin(self.theta)
            self.angular_speed = (9.81*math.tan(self.theta)/seat_radius)**0.5

            self.angle += dt * self.angular_speed  # Increase angle gradually
            updated_carousel = self.create_carousel()
            mob.become(updated_carousel)

        # Apply the updater to the carousel group
        swing_carousel.add_updater(update_carousel)

        # Animate the carousel rotating around a vertical axis through its center
        self.wait(7)

# To run this, save the file and use the following command:
# manim -pql your_file_name.py SwingCarousel3D

