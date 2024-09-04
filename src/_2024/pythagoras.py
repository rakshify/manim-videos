from typing import List

from manim import *

class PythagoreanTheorem(Scene):
    def get_triangle(self, ptA, ptB, ptC, color, rotation=0, shift=0):
        # Create the right-angled triangle
        triangle = Polygon(ptB, ptC, ptA, color=color)
        
        # Label the sides
        a = MathTex("a").next_to(triangle, DOWN)
        b = MathTex("b").next_to(triangle, RIGHT)
        c = MathTex("c").next_to(triangle.get_center(), UP+LEFT)
        
        return {
            "figure": triangle,
            "sides": [a, b, c]
        }
    
    def get_square(self, side_length, color, label, rotation=0, shift=0):
        square = Square(side_length=side_length, color=color).rotate(
            rotation).shift(shift)
        label = MathTex(label).next_to(square, LEFT)
        
        return {"figure": square, "label": label}
    
    def state(self):
        st_text = ("Given a right angle triangle, "
                   "the sum of the squares of the base and the height "
                   "is equal to the square of the hypotenuse")
        eq_text = "a^2 + b^2 = c^2"
        self.statement = Tex(st_text).to_edge(UP)
        # Create the equation
        self.equation = MathTex(*(eq_text.split())).next_to(
            self.statement, DOWN)
        self.play(Write(self.statement))
        self.play(Write(self.equation))
        self.wait()
        
    def draw_triangle(self):
        ptB = 0.5 * self.base * LEFT
        ptC = 0.5 * self.base * RIGHT
        ptA = 0.5 * self.base * RIGHT + self.height * UP
        self.triangle = self.get_triangle(ptA, ptB, ptC, WHITE)
        # Show triangle and labels
        self.play(Create(self.triangle["figure"]))
        self.play(*([Write(side) for side in self.triangle["sides"]]))
        self.wait()
        
    def draw_squares(self):
        bx = 0.5 * (self.base + self.height) * RIGHT
        by = 0.5 * self.height * UP
        cx = 0.5 * self.height * LEFT
        cy = 0.5 * (self.base + self.height) * UP
        squares = {
            "a": {
                "side_length": self.base,
                "color": GREEN,
                "label": "a^2",
                "shift": 0.5 * self.base * DOWN
            },
            "b": {
                "side_length": self.height,
                "color": RED,
                "label": "b^2",
                "shift": bx + by
            },
            "c": {
                "side_length": self.hypotenuse,
                "color": BLUE,
                "label": "c^2",
                "rotation": np.arctan(self.height / self.base),
                "shift": cx + cy
            }
        }
        self.squares = {
            key: self.get_square(**value)
            for key, value in squares.items()
        }
        self.play(
            FadeOut(self.statement),
            self.equation.animate.move_to(3 * LEFT + 3 * UP)
        )
        self.play(*([Create(square["figure"]) for square in self.squares.values()]))
        self.wait()
        self.play(*([Write(square["label"]) for square in self.squares.values()]))
        self.wait()
        
        # Highlight squares
        for i, side in enumerate(["a", "b", "c"]):
            self.play(
                Indicate(self.equation[2 * i]),
                Indicate(self.squares[side]["label"]),
                Indicate(self.squares[side]["figure"]),
                run_time=2
            )
        
    def construct(self):
        # Initiate lengths
        self.base, self.height, self.hypotenuse = 4 / 2, 3 / 2, 5 / 2
        
        # State the theorem
        self.state()
        
        # Draw the triangle
        self.draw_triangle()
        
        
        # Draw squares
        self.draw_squares()
            
            
        # self.play(
        #     Indicate(equation[2]),
        #     Indicate(lbl_b),
        #     Indicate(sq_b),
        #     run_time=2
        # )
        # self.play(
        #     Indicate(equation[4]),
        #     Indicate(lbl_c),
        #     Indicate(sq_c),
        #     run_time=2
        # )
        
        # # Show final equality
        # final_equation = MathTex("9", "+", "16", "=", "25").next_to(equation, DOWN)
        # self.play(Write(final_equation))
        # self.wait(2)
        
        # # Fade out everything except the original equation
        # self.play(
        #     FadeOut(triangle),
        #     FadeOut(label_a), FadeOut(label_b), FadeOut(label_c),
        #     FadeOut(square_a), FadeOut(square_b), FadeOut(square_c),
        #     FadeOut(area_a), FadeOut(area_b), FadeOut(area_c),
        #     FadeOut(final_equation)
        # )
        # self.wait()
        
        # # Center and scale up the equation for a final emphasis
        # self.play(
        #     equation.animate.scale(1.5).move_to(ORIGIN)
        # )
        self.wait(2)



class PythagoreanTheoremProof(Scene):
    def construct(self):
        # Colors
        colors = {
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "red": "#FF0000",
            "green": "#00FF00",
            "blue": "#0000FF"
        }

        self.base, self.height, self.hypotenuse = 4 / 2, 3 / 2, 5 / 2
        ptB = np.array([-0.5 * self.base, 0, 0])#0.5 * self.base * LEFT
        ptC = np.array([0.5 * self.base, 0, 0])#0.5 * self.base * RIGHT
        ptA = np.array([0.5 * self.base, self.height, 0])
        triangle = Polygon(ptB, ptC, ptA, color=WHITE)
        labels = VGroup(
            MathTex("a").next_to(triangle, DOWN),
            MathTex("b").next_to(triangle, RIGHT),
            MathTex("c").next_to(triangle.get_center(), UP+LEFT)
        )

        # # Create the initial triangle
        # triangle = Polygon(
        #     np.array([0, 0, 0]),
        #     np.array([3, 0, 0]),
        #     np.array([0, 4, 0]),
        #     color=WHITE
        # )
        # labels = VGroup(
        #     Text("a").next_to(triangle, LEFT),
        #     Text("b").next_to(triangle, DOWN),
        #     Text("c").next_to(triangle.get_center(), UP+RIGHT)
        # )

        self.play(Create(triangle), Write(labels))
        self.wait()

        # Create 4 copies of the triangle with different colors
        triangles = VGroup(*[triangle.copy().set_fill(color, opacity=0.5) 
                             for color in [colors["yellow"], colors["orange"], colors["red"], colors["green"]]])

        self.play(Create(triangles))
        self.wait()

        # Arrange triangles to form a square
        square_side = triangle.get_width() + triangle.get_height()
        square = Square(side_length=square_side, color=WHITE)
        
        # Define the first arrangement positions and rotations
        first_arrangement = [
            {"pos": square.get_corner(DL), "rot": -PI/2, "aligned_edge": DL},
            {"pos": square.get_corner(UL), "rot": PI, "aligned_edge": UL},
            {"pos": square.get_corner(UR), "rot": PI/2, "aligned_edge": UR},
            {"pos": square.get_corner(DR), "rot": 0, "aligned_edge": DR}
        ]

        # Animate the triangles moving into the first arrangement
        self.play(
            ReplacementTransform(triangle, square),
            *[
                triangle.animate.rotate(arr["rot"]).move_to(
                    arr["pos"], aligned_edge=arr["aligned_edge"])
                for triangle, arr in zip(triangles, first_arrangement)
            ],
            run_time=2
        )

        # Update the current rotation of each triangle
        current_rotations = [arr["rot"] for arr in first_arrangement]

        center_square = Square(
            side_length=self.hypotenuse,
            color=colors["blue"],
            fill_opacity=0.5
        )
        ang = np.arctan(self.height / self.base)
        center_square.rotate(ang).move_to(square.get_center())

        c_squared = Text("c²").move_to(center_square.get_center())

        self.play(Create(center_square), Write(c_squared))
        self.wait()

        # Define the second arrangement positions and rotations
        second_arrangement = [
            {"pos": square.get_corner(UR), "rot": 0, "aligned_edge": UR},
            {"pos": square.get_corner(UR), "rot": -PI/2, "aligned_edge": UL},
            {"pos": square.get_corner(DL), "rot": 0, "aligned_edge": DL},
            {"pos": square.get_corner(DL), "rot": PI/2, "aligned_edge": DR}
        ]

        # Animate the triangles moving into the second arrangement
        self.play(
            *[
                triangle.animate.rotate(arr["rot"] - curr_rot).move_to(
                    arr["pos"], aligned_edge=arr["aligned_edge"])
                for triangle, arr, curr_rot in zip(
                    triangles, second_arrangement, current_rotations)
            ],
            FadeOut(center_square),
            FadeOut(c_squared),
            run_time=2
        )

        a_squared = Square(side_length=4, color=colors["blue"], fill_opacity=0.5)
        b_squared = Square(side_length=3, color=colors["blue"], fill_opacity=0.5)
        a_squared.move_to(square.get_corner(UL), aligned_edge=UL)
        b_squared.move_to(square.get_corner(DR), aligned_edge=DR)

        a_squared_text = Text("a²").move_to(a_squared.get_center())
        b_squared_text = Text("b²").move_to(b_squared.get_center())

        self.play(
            Create(a_squared),
            Create(b_squared),
            Write(a_squared_text),
            Write(b_squared_text)
        )
        self.wait()

        # Conclusion
        conclusion = Text("c² = a² + b²").scale(0.8).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

# class PythagoreanTheoremProof(Scene):
#     def construct(self):
#         # Colors
#         colors = {
#             "yellow": "#FFFF00",
#             "orange": "#FFA500",
#             "red": "#FF0000",
#             "green": "#00FF00",
#             "blue": "#0000FF"
#         }

#         self.base, self.height, self.hypotenuse = 4 / 2, 3 / 2, 5 / 2
#         ptB = np.array([-0.5 * self.base, 0, 0])#0.5 * self.base * LEFT
#         ptC = np.array([0.5 * self.base, 0, 0])#0.5 * self.base * RIGHT
#         ptA = np.array([0.5 * self.base, self.height, 0])
#         triangle = Polygon(ptB, ptC, ptA, color=WHITE)
#         labels = VGroup(
#             MathTex("a").next_to(triangle, DOWN),
#             MathTex("b").next_to(triangle, RIGHT),
#             MathTex("c").next_to(triangle.get_center(), UP+LEFT)
#         )

#         # # Create the initial triangle
#         # triangle = Polygon(
#         #     np.array([0, 0, 0]),
#         #     np.array([3, 0, 0]),
#         #     np.array([0, 4, 0]),
#         #     color=WHITE
#         # )
#         # labels = VGroup(
#         #     Text("a").next_to(triangle, LEFT),
#         #     Text("b").next_to(triangle, DOWN),
#         #     Text("c").next_to(triangle.get_center(), UP+RIGHT)
#         # )

#         self.play(Create(triangle), Write(labels))
#         self.wait()

#         # Create 4 copies of the triangle with different colors
#         triangles = VGroup(*[triangle.copy().set_fill(color, opacity=0.5) 
#                              for color in [colors["yellow"], colors["orange"], colors["red"], colors["green"]]])

#         self.play(Create(triangles))
#         self.wait()

#         # Arrange triangles to form a square
#         square_side = triangle.get_width() + triangle.get_height()
#         square = Square(side_length=square_side, color=WHITE)
        
#         # Rotate and position triangles
#         triangles[0].rotate(-PI/2).move_to(square.get_corner(UL), aligned_edge=UL)
#         triangles[1].rotate(PI).move_to(square.get_corner(UR), aligned_edge=UR)
#         triangles[2].rotate(PI/2).move_to(square.get_corner(DR), aligned_edge=DR)
#         triangles[3].move_to(square.get_corner(DL), aligned_edge=DL)

#         center_square = Square(side_length=3, color=colors["blue"], fill_opacity=0.5)
#         center_square.move_to(square.get_center())

#         c_squared = Text("c²").move_to(center_square.get_center())

#         self.play(
#             ReplacementTransform(triangle, square),
#             *[ReplacementTransform(triangle.copy(), target) for triangle, target in zip(triangles, triangles)],
#             Create(center_square),
#             Write(c_squared)
#         )
#         self.wait()

#         # Rearrange triangles
#         self.play(
#             triangles[0].animate.rotate(PI/2).move_to(square.get_corner(UR), aligned_edge=UR),
#             triangles[1].animate.rotate(-PI/2).move_to(square.get_corner(UR), aligned_edge=UL),
#             triangles[2].animate.rotate(-PI/2).move_to(square.get_corner(DL), aligned_edge=DL),
#             triangles[3].animate.rotate(PI/2).move_to(square.get_corner(DL), aligned_edge=DR),
#             FadeOut(center_square),
#             FadeOut(c_squared)
#         )

#         a_squared = Square(side_length=4, color=colors["blue"], fill_opacity=0.5)
#         b_squared = Square(side_length=3, color=colors["blue"], fill_opacity=0.5)
#         a_squared.move_to(square.get_corner(UL), aligned_edge=UL)
#         b_squared.move_to(square.get_corner(DR), aligned_edge=DR)

#         a_squared_text = Text("a²").move_to(a_squared.get_center())
#         b_squared_text = Text("b²").move_to(b_squared.get_center())

#         self.play(
#             Create(a_squared),
#             Create(b_squared),
#             Write(a_squared_text),
#             Write(b_squared_text)
#         )
#         self.wait()

#         # Conclusion
#         conclusion = Text("c² = a² + b²").scale(0.8).to_edge(DOWN)
#         self.play(Write(conclusion))
#         self.wait(2)