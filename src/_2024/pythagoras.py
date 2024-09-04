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
    def get_triangle(self, ptA, ptB, ptC, color, rotation=0, shift=0):
        # Create the right-angled triangle
        triangle = Polygon(ptB, ptC, ptA, color=color)
        
        # Label the sides
        # a = MathTex("a").next_to(triangle, DOWN)
        # b = MathTex("b").next_to(triangle, RIGHT)
        # c = MathTex("c").next_to(triangle.get_center(), UP+LEFT)
        labels = VGroup(
            MathTex("a").next_to(triangle, DOWN),
            MathTex("b").next_to(triangle, RIGHT),
            MathTex("c").next_to(triangle.get_center(), UP+LEFT)
        )
        
        return {"figure": triangle, "sides": labels}
        
    def draw_triangle(self, color):
        ptB = np.array([-0.5 * self.base, 0, 0])
        ptC = np.array([0.5 * self.base, 0, 0])
        ptA = np.array([0.5 * self.base, self.height, 0])
        self.triangle = self.get_triangle(ptA, ptB, ptC, color=color)
        # Show triangle and labels
        # self.play(Create(self.triangle["figure"]))
        # self.play(*([Write(side) for side in self.triangle["sides"]]))
        self.play(Create(self.triangle["figure"]), Write(self.triangle["sides"]))
        self.wait()
        
    def draw_triangle_copies(self, colors):
        # Create 4 copies of the triangle with different colors
        self.triangles = VGroup(
            *[
                self.triangle["figure"].copy().set_fill(color, opacity=0.5) 
                for color in colors.values()
            ]
        )
        a_labels = VGroup(*[self.triangle["sides"][0].copy() for _ in colors])
        b_labels = VGroup(*[self.triangle["sides"][1].copy() for _ in colors])
        c_labels = VGroup(*[self.triangle["sides"][2].copy() for _ in colors])
        self.lbl_copies = {"a": a_labels, "b": b_labels, "c": c_labels}
        #[colors["yellow"], colors["orange"], colors["red"], colors["green"]]])

        self.play(Create(self.triangles))
        self.wait()
    
    def draw_first_arrangement(self, square):
        # Define the first arrangement positions and rotations
        first_arrangement = [
            {"pos": square.get_corner(DL), "rot": -PI/2, "aligned_edge": DL},
            {"pos": square.get_corner(UL), "rot": PI, "aligned_edge": UL},
            {"pos": square.get_corner(UR), "rot": PI/2, "aligned_edge": UR},
            {"pos": square.get_corner(DR), "rot": 0, "aligned_edge": DR}
        ]

        # Animate the triangles moving into the first arrangement
        a_pos = [
            (UP, LEFT * (self.base / 2)),
            (RIGHT, UP * (self.base / 2)),
            (LEFT, DOWN * (self.base / 2)),
            (DOWN, RIGHT * (self.base / 2))
        ]
        b_pos = [
            (LEFT, UP * (self.height / 2)),
            (UP, RIGHT * (self.height / 2)),
            (DOWN, LEFT * (self.height / 2)),
            (RIGHT, DOWN * (self.height / 2))
        ]
        c_pos = [
            (UP, DOWN * (self.height / 1.2) + LEFT * (self.base / 3)),
            (UP, DOWN * (self.height / 1.2) + RIGHT * (self.base / 3)),
            (DOWN, UP * (self.height / 1.2) + LEFT * (self.base / 3)),
            (DOWN, UP * (self.height / 1.2) + RIGHT * (self.base / 3))
        ]
        self.play(
            ReplacementTransform(self.triangle["figure"], square),
            *[
                triangle.animate.rotate(arr["rot"]).move_to(
                    arr["pos"], aligned_edge=arr["aligned_edge"])
                for triangle, arr in zip(self.triangles, first_arrangement)
            ],
            FadeOut(self.triangle["sides"]),
            *[
                label.animate.next_to(square, pos[0]).shift(pos[1])
                for label, pos in zip(self.lbl_copies["a"], a_pos)
            ],
            *[
                label.animate.next_to(square, pos[0]).shift(pos[1])
                for label, pos in zip(self.lbl_copies["b"], b_pos)
            ],
            *[
                label.animate.next_to(square, pos[0]).shift(pos[1])
                for label, pos in zip(self.lbl_copies["c"], c_pos)
            ],
            run_time=2
        )

        # Update the current rotation of each triangle
        self.triangle_rotations = [arr["rot"] for arr in first_arrangement]

        self.center_square = Square(
            side_length=self.hypotenuse,
            color=BLUE,
            fill_opacity=0.5
        )
        ang = np.arctan(self.height / self.base)
        self.center_square.rotate(ang).move_to(square.get_center())

        self.c_squared = Text("c²").move_to(self.center_square.get_center())

        self.play(Create(self.center_square), Write(self.c_squared))
        self.wait()
        
    def draw_second_arrangement(self, square):
        # Define the second arrangement positions and rotations
        second_arrangement = [
            {"pos": square.get_corner(DL), "rot": -PI, "aligned_edge": DL},
            {"pos": square.get_corner(UR), "rot": 3 * PI / 2, "aligned_edge": UR},
            {"pos": square.get_corner(UR), "rot": PI/2, "aligned_edge": UR},
            {"pos": square.get_corner(DL), "rot": 0, "aligned_edge": DL}
        ]

        # Animate the triangles moving into the second arrangement
        a_pos = [
            (UP, LEFT * (self.base / 2)),
            (RIGHT, UP * (self.base / 2)),
            (LEFT, UP * (self.height / 2)),
            (DOWN, LEFT * (self.height / 2))
        ]
        b_pos = [
            (LEFT, DOWN * (self.base / 2)),
            (UP, RIGHT * (self.height / 2)),
            (DOWN, RIGHT * (self.base / 2)),
            (RIGHT, DOWN * (self.height / 2))
        ]
        self.play(
            *[
                triangle.animate.rotate(arr["rot"] - curr_rot).move_to(
                    arr["pos"], aligned_edge=arr["aligned_edge"])
                for triangle, arr, curr_rot in zip(
                    self.triangles, second_arrangement, self.triangle_rotations)
            ],
            FadeOut(self.center_square),
            FadeOut(self.c_squared),
            FadeOut(self.lbl_copies["c"]),
            *[
                label.animate.next_to(square, pos[0]).shift(pos[1])
                for label, pos in zip(self.lbl_copies["a"], a_pos)
            ],
            *[
                label.animate.next_to(square, pos[0]).shift(pos[1])
                for label, pos in zip(self.lbl_copies["b"], b_pos)
            ],
            run_time=2
        )

        a_squared = Square(
            side_length=self.base, color=BLUE, fill_opacity=0.5
        )
        b_squared = Square(
            side_length=self.height, color=BLUE, fill_opacity=0.5
        )
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
        
    def prove(self):
        # Colors
        colors = {
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "red": "#FF0000",
            "green": "#00FF00"
        }
        
        self.draw_triangle_copies(colors=colors)

        # Arrange triangles to form a square
        square_side = self.base + self.height
        square = Square(side_length=square_side, color=WHITE)
        
        self.draw_first_arrangement(square=square)

        self.draw_second_arrangement(square=square)

        # Conclusion
        conclusion = Text("c² = a² + b²").scale(0.8).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
        
    def construct(self):
        self.base, self.height, self.hypotenuse = 4 / 2, 3 / 2, 5 / 2
        
        self.draw_triangle(color=WHITE)
        
        self.prove()
