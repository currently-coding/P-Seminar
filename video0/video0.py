import numpy as np
from manim import *
import math


class MyScene(ThreeDScene):
    angular_speed = PI
    carousel_radius = 2
    seat_radius = carousel_radius
    num_chains = 8
    chain_length = 1.5
    theta = ValueTracker(0)
    angle = 0
    t = 0
    info_tex = MathTex(r"\tan{\theta}=",r"\frac{F_z}{F_G}")

    def create_chain_and_seat_template(self):
        chain_start = np.array([self.carousel_radius, 0, 0])
        chain_end = chain_start * (1 + math.sin(self.theta.get_value()) * self.chain_length / self.carousel_radius) + np.array([0, 0, -math.cos(self.theta.get_value()) * self.chain_length])
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


    def adjust_tex(self, tex: MathTex):
        tex.rotate(PI/2, axis=IN)
        tex.rotate(-self.camera.get_phi(), axis=UP)
        tex.rotate(PI, axis=IN)
        tex.shift(2*OUT)
        return tex


    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=0)
        swing_carousel = self.create_carousel()

        # Add carousel to the scene
        self.add(swing_carousel)

        # Define an updater to continuously change the angle `self.theta` over time
        def update_carousel(mob, dt):
            self.seat_radius = self.carousel_radius + self.chain_length * math.sin(self.theta.get_value())
            self.angular_speed = (9.81*math.tan(self.theta.get_value())/self.seat_radius)**0.5

            self.angle += dt * self.angular_speed  # Increase angle gradually
            updated_carousel = self.create_carousel()
            mob.become(updated_carousel)

        # Apply the updater to the carousel group
        swing_carousel.add_updater(update_carousel)


        self.adjust_tex(self.info_tex)
        self.play(Write(self.info_tex))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\tan{\theta}=\frac{m\omega^2r}{mg}"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\tan{\theta}=\frac{\omega^2r}{g}"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"g\tan{\theta}=\omega^2r"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\frac{g\tan{\theta}}{r}=\omega^2"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\sqrt{\frac{g\tan{\theta}}{r}}=\omega"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\omega=\sqrt{\frac{g\tan{\theta}}{r}}"))))
        self.play(Transform(self.info_tex, self.adjust_tex(MathTex(r"\omega=",r"\sqrt{\frac{9.81\cdot\tan{" + f"{self.theta.get_value():.5f}" + "}}{" + f"{self.seat_radius:.5f}" + "}}=" + f"{self.angular_speed:.5f}"))))
        self.info_tex.add_updater(lambda tex: tex.become(self.adjust_tex(MathTex(r"\omega=\sqrt{\frac{9.81\cdot\tan{" + f"{self.theta.get_value():.5f}" + "}}{" + f"{self.seat_radius:.5f}" + "}}=" + f"{self.angular_speed:.5f}"))))


        # Animate the carousel rotating around a vertical axis through its center
        self.play(self.theta.animate.set_value(PI/3), run_time=2)
        self.wait(3)
        self.play(self.theta.animate.set_value(PI / 6), run_time=2)
        self.wait(3)
        self.play(self.theta.animate.set_value(0), run_time=2)

# To run this, save the file and use the following command:
# manim -pql your_file_name.py SwingCarousel3D
