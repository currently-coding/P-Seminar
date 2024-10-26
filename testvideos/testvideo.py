from manim import *
from manim_physics import *


class ElectricFieldExample(Scene):
    def construct(self):
        def FieldUpdater(mob):
            mob.become(ElectricField(charge1, charge2))

        charge1 = Charge(-1, LEFT)
        charge2 = Charge(+1, RIGHT)
        field = ElectricField(charge1, charge2)

        field.add_updater(FieldUpdater)
        self.play(Create(charge1), Create(charge2))
        self.play(Create(field))
        self.play(charge1.animate().shift(LEFT))
        self.wait()
