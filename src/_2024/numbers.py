from manim import *

import numpy as np

from src.utils import get_coord_space

def setup_space():
    # Positions of the plane
    add_plane_shift = np.array([-4.5, 0.5, 0])
    mul_plane_shift = np.array([4.5, 0.5, 0])
    # Axes range and length
    scale = 1 / 3
    x_range, y_range = [-4, 4, 1], [-4, 4, 1]
    x_length = 12 * scale
    y_length = 12 * scale
    
    # Additive plane
    add_title = Tex(
        "Additive Universe", font_size=24, color=YELLOW
    ).move_to(np.array([-4.5, 3.5, 0]))
    add_plane = ComplexPlane(
        x_range=x_range, y_range=y_range,
        x_length=x_length, y_length=y_length,
        axis_config={"font_size": 48 * scale}
    ).add_coordinates().move_to(add_plane_shift)
    p1 = add_plane.x_axis.number_to_point(add_plane.x_range[0])[0]
    p2 = add_plane.x_axis.number_to_point(add_plane.x_range[0] + 1)[0]
    x_shift = p2 - p1
    p1 = add_plane.y_axis.number_to_point(add_plane.y_range[0])[1]
    p2 = add_plane.y_axis.number_to_point(add_plane.y_range[0] + 1)[1]
    y_shift = p2 - p1
    add_id = Dot(add_plane.get_origin(), radius=0.05, color=YELLOW)
    
    # Multiplicative plane
    mul_title = Tex(
        "Multiplicative Universe", font_size=24, color=GREEN
    ).move_to(np.array([4.5, 3.5, 0]))
    mul_plane = add_plane.copy().move_to(mul_plane_shift)
    mul_id_shift = np.array([x_length / (x_range[1] - x_range[0]), 0, 0])
    mul_id_shift += mul_plane.get_origin()
    mul_id = Dot(mul_id_shift, radius=0.05, color=GREEN)
    
    return (
        add_plane_shift, mul_plane_shift,
        add_title, add_plane, x_shift, y_shift, add_id,
        mul_title, mul_plane, mul_id
    )


class IntroductionScene(ThreeDScene):
    def get_hemisphere(self):
        def param_hemisphere(u, v):
            x = np.cos(u) * np.sin(v)
            y = np.sin(u) * np.sin(v)
            z = np.cos(v)
            return np.array([x, y, z])

        return Surface(
            param_hemisphere,
            u_range=[0, 2 * PI],
            v_range=[0, PI / 2],
            stroke_width=0.5,
        )

    def intro(self):
        # Scene 1: "What is a number?"
        title = Tex("What is a number?")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Scene 2: Number 3 with thought bubble
        number = MathTex("3", font_size=72)

        self.play(Write(number))
        self.wait(5)

        # Scene 3: Counting
        counting_text = Tex("counting", font_size=36).next_to(number, DOWN)
        self.play(Write(counting_text))

        count_numbers = VGroup(*[MathTex(str(i + 1), font_size=36) for i in range(3)])
        count_numbers.arrange(RIGHT).next_to(counting_text, RIGHT)

        self.wait(2)
        for num in count_numbers:
            self.play(Write(num))
        self.wait(1)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)
        
        fraction = MathTex(r"\frac{3}{2}", font_size=72).to_edge(UP)
        self.play(Write(fraction))
        self.wait(5)
        irrational = MathTex(r"\sqrt{2}", font_size=72).next_to(fraction, DOWN)
        self.play(Write(irrational))
        self.wait(7)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(17)
    
    def integer_counting(self):
        # Scene 1: Addition
        addition = MathTex("2", "+", "3")
        self.play(Write(addition))
        self.wait(3)

        # Scene 2: Visualize addition
        dots = VGroup()
        self.play(Indicate(addition[0]))
        for i in range(2):
            dot = Dot()
            dot.move_to([i*0.5 - 0.5, -0.5, 0])
            dots.add(dot)
            self.play(Create(dot))
        self.play(Indicate(addition[2]))
        for i in range(3):
            dot = Dot()
            dot.move_to([i*0.5 + 0.5, -0.5, 0])
            self.play(Create(dot))
            dots.add(dot)
        self.wait(4)

        dot_numbers = VGroup(*[MathTex(str(i+1), font_size=24) for i in range(5)])
        for i, num in enumerate(dot_numbers):
            num.next_to(dots[i], DOWN, buff=0.2)
            self.play(Indicate(dots[i]), Write(num))

        result = MathTex("=", "5").next_to(addition, RIGHT)
        self.play(Indicate(result))
        self.wait(2)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(5)

        # Scene 3: Multiplication
        multiplication = MathTex("3", "*", "4")
        self.play(Write(multiplication))
        self.wait(5)

        # Scene 4: Visualize multiplication
        dot_groups = VGroup()
        group = VGroup()
        self.play(Indicate(multiplication[0]))
        for i in range(3):
            dot = Dot()
            dot.move_to([i*0.5 - 4.5, -0.5, 0])
            group.add(dot)
            self.play(Create(dot))
        dot_groups.add(group)
        self.play(Indicate(multiplication[2]))
        for i in range(1, 4):
            ngroup = group.copy()
            ngroup.shift(i * 0.5 * DOWN)
            dot_groups.add(ngroup)
            self.play(Create(ngroup))

        numbers = VGroup(*[MathTex(str(i+1), font_size=24) for i in range(12)])
        numbers.arrange_in_grid(rows=4, cols=3, buff=0.5)
        numbers.next_to(dot_groups, RIGHT)
        
        for i, num in enumerate(numbers):
            r, c = i // 3, i % 3
            self.play(Indicate(dot_groups[r][c]), Write(num))

        result = MathTex("=", "12").next_to(multiplication, RIGHT)
        self.play(Indicate(result))
        
    def fraction_case(self):
        self.set_camera_orientation(phi=-PI/2)

        # Scene 1: Fraction example
        fraction = MathTex(r"\frac{3}{2}")
        self.add_fixed_in_frame_mobjects(fraction)
        self.play(Write(fraction))
        self.wait(1)

        # Scene 2: Sphere and hemisphere
        sphere = Sphere().scale(0.5).next_to(fraction, OUT, buff=1)
        hemisphere = self.get_hemisphere().scale(0.5).next_to(sphere, RIGHT, buff=1)
        self.play(Create(sphere), Create(hemisphere))
        self.wait(25)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.set_camera_orientation(phi=0)

        # Scene 3: Addition of fractions
        addition = MathTex(r"\frac{3}{2} + \frac{4}{3}")
        self.play(Write(addition))
        self.wait(17)

        # Scene 4: Indicate denominators
        self.play(Indicate(addition[0][2]), Indicate(addition[0][6]))
        self.wait(1)

        # Scene 5: Arrows and multiplication for 3/2
        arrow3 = Arrow(addition[0][6].get_bottom(), addition[0][0].get_top(), color=YELLOW)
        arrow4 = Arrow(addition[0][6].get_bottom(), addition[0][2].get_top(), color=YELLOW)
        self.play(Create(arrow3), Create(arrow4))
        new_fraction2 = MathTex(r"\frac{3 \cdot 3}{2 \cdot 3}").next_to(addition, LEFT)
        self.play(Write(new_fraction2))
        self.play(FadeOut(arrow3), FadeOut(arrow4))
        self.wait(5)

        # Scene 6: Arrows and multiplication for 4/3
        arrow1 = Arrow(addition[0][2].get_bottom(), addition[0][4].get_top(), color=YELLOW)
        arrow2 = Arrow(addition[0][2].get_bottom(), addition[0][6].get_top(), color=YELLOW)
        self.play(Create(arrow1), Create(arrow2))
        new_fraction = MathTex(r"\frac{4 \cdot 2}{3 \cdot 2}").next_to(addition, RIGHT)
        self.play(Write(new_fraction))
        self.wait(1)
        self.play(FadeOut(arrow1), FadeOut(arrow2))

        # Scene 7: Simplify fractions
        simplified = MathTex(r"\frac{9}{6} + \frac{8}{6}")
        self.play(
            Transform(addition, simplified), 
            FadeOut(new_fraction), 
            FadeOut(new_fraction2)
        )
        self.wait(15)

        # Scene 8: Final addition
        result = MathTex(r"= \frac{17}{6}").next_to(simplified, RIGHT)
        self.play(Indicate(simplified[0][0]), Indicate(simplified[0][4]), Indicate(simplified[0][3]))
        self.play(Write(result))
        self.wait(20)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(5)

        # Scene 9: Multiplication of fractions
        multiplication = MathTex(r"\frac{3}{2} \cdot \frac{5}{7}")
        self.play(Write(multiplication))
        self.wait(10)

        # Scene 10: Multiply numerators
        self.play(
            Indicate(multiplication[0][0]), 
            Indicate(multiplication[0][4]), 
            Indicate(multiplication[0][3])
        )
        result2 = MathTex(r"= 15").next_to(multiplication, RIGHT)
        self.play(Write(result2))
        self.wait(3)

        # Scene 11: Multiply denominators
        self.play(
            Indicate(multiplication[0][2]),
            Indicate(multiplication[0][6]),
            Indicate(multiplication[0][3])
        )
        final_result = MathTex(r"= \frac{15}{14}").next_to(multiplication, RIGHT)
        self.wait(2)
        self.play(Transform(result2, final_result))
        self.wait(2)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)
        
    def construct(self):
        # Introduce
        self.intro()
        
        # Scenes for integer counting
        self.integer_counting()
        
        # Fractional issues
        self.fraction_case()
        

class GroupTheoryScene(Scene):
    def ask_questions(self):
        # Issues with counting
        root2 = MathTex(r"\sqrt{2}").to_edge(UP)
        self.play(Write(root2), run_time=3)
        self.wait(30)

        i_number = MathTex("i").next_to(root2, DOWN, buff=0.5)
        self.play(Write(i_number))
        self.wait(5)
        
        complex_num = MathTex("3+i").next_to(i_number, DOWN, buff=0.5)
        self.play(Write(complex_num))
        self.wait(5)

        exponent = MathTex(r"e^3, e^{ix}").next_to(complex_num, DOWN, buff=0.5)
        self.play(Write(exponent))
        self.wait(1)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
    def group_theory_examples(self):
        # Scene 1: Display the text "Let's play a game"
        intro_text = Tex("Let's play a game")
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))

        # Scene 2: Create two dots, one green at the origin, and one blue at (0, -1, 0)
        green_dot = Dot(color=GREEN).move_to(ORIGIN)
        blue_dot = Dot(color=BLUE).move_to(DOWN)
        self.play(FadeIn(green_dot), FadeIn(blue_dot))
        self.wait(10)

        # Scene 3: Move the green dot along the described path
        green_path = [ORIGIN, RIGHT*2, LEFT, RIGHT*3]
        green_line = VMobject()
        green_line.set_points_as_corners([green_dot.get_center()])
        
        for target in green_path[1:]:
            self.play(
                MoveAlongPath(
                    green_dot, 
                    Line(green_dot.get_center(), target, color=GREEN)
                ), 
                run_time=3
            )
        self.add(Line(ORIGIN, RIGHT * 3, color=GREEN))
        
        # Scene 4: Move the blue dot to (3, -1, 0)
        blue_target = blue_dot.get_center() + RIGHT * 3
        blue_line = Line(blue_dot.get_center(), blue_target, color=BLUE)
        self.play(MoveAlongPath(blue_dot, blue_line), run_time=3)
        self.add(blue_line)
        self.wait(5)
        self.play(Indicate(green_dot), Indicate(blue_dot))
        self.wait(30)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)
        
        # Scene 5: Create a white square S1 at the center of the screen
        square_s1 = Square().set_color(WHITE)
        labels_s1 = VGroup(Tex("A").next_to(square_s1.get_corner(DL), DL, buff=SMALL_BUFF),
                           Tex("B").next_to(square_s1.get_corner(DR), DR, buff=SMALL_BUFF),
                           Tex("C").next_to(square_s1.get_corner(UR), UR, buff=SMALL_BUFF),
                           Tex("D").next_to(square_s1.get_corner(UL), UL, buff=SMALL_BUFF))
        self.play(FadeIn(square_s1), Write(labels_s1))
        self.wait(5)

        # Scene 6: Move the square S1 and create S2
        s1_target = square_s1.get_center() + 2 * UP + 2 * LEFT
        self.play(
            square_s1.animate.move_to(s1_target), 
            labels_s1.animate.move_to(s1_target)
        )

        square_s2 = square_s1.copy().set_color(GREEN).move_to(
            square_s1.get_center() + RIGHT * 4
        )
        labels_s2 = labels_s1.copy().move_to(square_s2.get_center())
        self.play(FadeIn(square_s2), Write(labels_s2))

        # Scene 7: Flip S2 over a vertical axis
        vertical_axis = DashedLine(
            (square_s2.get_corner(UL) + square_s2.get_corner(UR)) // 2,
            (square_s2.get_corner(DL) + square_s2.get_corner(DR)) // 2
        ).move_to(square_s2.get_center())
        self.play(Create(vertical_axis))
        
        # Perform the flip by scaling along the x-axis
        self.play(
            square_s2.animate.scale([-1, 1, 1], about_point=vertical_axis.get_center()),
            labels_s2[0].animate.move_to(square_s2.get_corner(DR), UL),
            labels_s2[1].animate.move_to(square_s2.get_corner(DL), UR),
            labels_s2[2].animate.move_to(square_s2.get_corner(UL), DR),
            labels_s2[3].animate.move_to(square_s2.get_corner(UR), DL),
            run_time=4
        )

        # Scene 8: Create S3 and rotate it
        square_s3 = square_s2.copy().move_to(square_s2.get_center() + DOWN * 4)
        labels_s3 = labels_s2.copy().move_to(square_s3.get_center())
        self.play(FadeIn(square_s3), Write(labels_s3))
        
        arrows = VGroup(
            CurvedArrow(
                square_s3.get_corner(DR) + DOWN * 1.0, 
                square_s3.get_corner(DR) + RIGHT * 1.0, angle=PI/2
            ),
            CurvedArrow(
                square_s3.get_corner(DL) + LEFT * 1.0,
                square_s3.get_corner(DL) + DOWN * 1.0, angle=PI/2
            ),
            CurvedArrow(
                square_s3.get_corner(UL) + UP * 1.0, 
                square_s3.get_corner(UL) + LEFT * 1.0, angle=PI/2
            ),
            CurvedArrow(
                square_s3.get_corner(UR) + RIGHT * 1.0, 
                square_s3.get_corner(UR) + UP * 1.0, angle=PI/2
            )
        )
        self.play(Create(arrows))
        self.play(
            Rotate(square_s3, angle=PI/2, about_point=square_s3.get_center()),
            labels_s3[0].animate.move_to(square_s3.get_corner(UR), DL),
            labels_s3[1].animate.move_to(square_s3.get_corner(DR), UL),
            labels_s3[2].animate.move_to(square_s3.get_corner(DL), UR),
            labels_s3[3].animate.move_to(square_s3.get_corner(UL), DR),
            run_time=4
        )
        self.wait(8)

        # Scene 9: Create S4 and flip it over diagonal BD
        square_s4 = square_s1.copy().set_color(BLUE).move_to(
            square_s1.get_center() + DOWN * 4
        )
        labels_s4 = labels_s1.copy().move_to(square_s4.get_center())
        self.play(FadeIn(square_s4), Write(labels_s4))

        diagonal_axis = DashedLine(square_s4.get_corner(UL), square_s4.get_corner(DR))
        self.play(Create(diagonal_axis), run_time=4)
        self.wait(2)
        
        # Manually map the corners after diagonal flip
        self.play(
            square_s4.animate.apply_function(
                lambda p: square_s4.get_center() - np.array([p[1], p[0], p[2]])
            ).shift(square_s4.get_center()),
            labels_s4[0].animate.move_to(square_s4.get_corner(UR), DL),
            labels_s4[2].animate.move_to(square_s4.get_corner(DL), UR),
            run_time=4
        )
        self.wait(20)

        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(6)
        
    def group_writeup(self):
        # First set of text
        text1 = Tex("Group").scale(0.7).to_edge(UP)
        text2 = Tex("Count Group").scale(0.5).next_to(text1, DOWN)
        self.play(Write(text1))
        self.wait(17)
        self.play(Write(text2))
        self.wait(15)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Third set of text
        text7 = Tex("What if we change the group?").scale(0.8).to_edge(UP)
        text9 = Tex(
            "Additive Group"
        ).scale(0.6).next_to(text7, DOWN).shift(RIGHT * 0.5)
        text10 = Tex(
            "Multiplicative Group"
        ).scale(0.6).next_to(text9, DOWN).align_to(text9, LEFT)

        self.play(Write(text7))
        self.play(Write(text9))
        self.play(Write(text10))
        self.wait(5)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)
        
    def construct(self):
        # Issues with counting
        self.ask_questions()
        
        # Group theory introduction
        self.group_theory_examples()
        self.group_writeup()


class GraphUniverseScene(Scene):
    def reset_space(self):
        self.add(self.x_lines)
        self.add(self.y_lines)
        self.add(self.number_line)
        self.play(FadeIn(self.dots), FadeIn(self.marks))
        
    def setup_coords(self):
        mx = 20
        left = lambda y: np.array([-mx, y, 0])
        right = lambda y: np.array([mx, y, 0])
        top = lambda x: np.array([x, mx, 0])
        bot = lambda x: np.array([x, -mx, 0])
        self.x_lines = VGroup(*[
            Line(
                left(y), right(y), color=LIGHT_GREY, stroke_width=0.1
            ) for y in range(-mx, mx + 1)
        ])
        self.y_lines = VGroup(*[
            Line(
                top(x), bot(x), color=LIGHT_GREY, stroke_width=0.1
            ) for x in range(-mx, mx + 1)
        ])
        self.add(self.x_lines)
        self.add(self.y_lines)
        
        self.number_line = Line(left(0), right(0), color=WHITE)
        self.add(self.number_line)
        self.wait()
        
        self.dots = VGroup()
        for i in range(41):
            dot = Dot()
            dot.move_to(np.array([i - 20, 0, 0]))
            self.dots.add(dot)
        self.marks = VGroup(*[
            Tex(str(i - 20)).next_to(self.dots[i], DOWN)
            for i in range(41)
        ])
        self.play(Create(self.dots), Write(self.marks))
        self.wait(17)
        
    def basic_graph(self):
        # Tex animations
        title1 = Tex("Plot cities?").to_edge(UP)
        subtitle1 = Tex("scale.").next_to(title1, DOWN)
        
        self.play(Write(title1))
        self.play(Write(subtitle1))
        
        # Scale number line
        scaled_marks = VGroup(*[
            Tex(str((i - 20) * 100)).next_to(self.dots[i], DOWN)
            for i in range(41)
        ])
        
        self.wait(9)
        self.play(FadeOut(self.marks), FadeIn(scaled_marks))
        self.wait(4)
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)
        self.reset_space()
        self.wait(7)
        
        # New text animations
        text = "Plot students ages?"
        title2 = Tex(text).to_edge(UP)
        subtitle2 = Tex("offset.").next_to(title2, DOWN)
        
        self.play(Write(title2))
        self.play(Write(subtitle2))
        
        # Offset number line
        offset_marks = self.marks.copy()
        for i in range(1, 9):
            offset_marks[-i].shift(LEFT * 12)
        
        self.play(
            FadeOut(self.marks), 
            FadeIn(offset_marks[:21]), 
            FadeIn(offset_marks[-8:])
        )
        self.wait(10)
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.reset_space()
        
    def graph_universes(self):
        shifting_text = Tex(
            "1. Additive Universe"
        ).to_edge(UP)
        stretching_text = Tex(
            "2. Multiplicative Universe"
        ).next_to(shifting_text, DOWN)
        self.play(Write(shifting_text))
        self.play(Write(stretching_text))
        self.wait(15)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(2)

    def define_number(self):
        number_3 = Tex("3", font_size=72).move_to(ORIGIN)
        self.play(Write(number_3))
        self.wait(10)
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.reset_space()
        adding = Tex(
            "1. Additive Universe"
        ).to_edge(UP)
        self.play(Write(adding))
        self.wait(16)
        
        # Animated graph shift
        shifted_y_lines = self.y_lines.copy().set_color(YELLOW)
        shifted_marks = self.marks.copy().set_color(YELLOW)
        num3 = Circle(radius=0.3, color=YELLOW).move_to(self.marks[20])
        self.play(Create(num3))
        self.play(
            shifted_y_lines.animate.shift(RIGHT * 3),
            shifted_marks.animate.shift(RIGHT * 3),
            num3.animate.shift(RIGHT * 3),
            FadeOut(self.marks),
            run_time=10
        )
        
        # Clear screen
        self.play(
            FadeOut(shifted_y_lines),
            FadeOut(shifted_marks),
            FadeIn(self.marks)
        )
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.reset_space()
        multiplying = Tex(
            "2. Multiplicative Universe"
        ).to_edge(UP)
        self.play(Write(multiplying))
        self.wait(15)
        
        # Animated graph stretch
        stretched_y_lines = self.y_lines.copy().set_color(YELLOW)
        stretched_marks = self.marks.copy().set_color(YELLOW)
        num3 = Circle(radius=0.3, color=YELLOW).move_to(stretched_marks[21])
        self.play(Create(num3))
        self.play(
            *[
                line.animate.shift((i - 20) * RIGHT * 2)
                for i, line in enumerate(stretched_y_lines)
            ],
            *[
                mark.animate.shift((i - 20) * RIGHT * 2) 
                for i, mark in enumerate(stretched_marks)
            ],
            num3.animate.shift(RIGHT * 2),
            FadeOut(self.marks),
            run_time=10
        )
        self.wait(2)
        
        # Clear screen
        self.play(
            FadeOut(stretched_y_lines),
            FadeOut(stretched_marks),
            FadeIn(self.marks)
        )
        self.wait(2)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.reset_space()
        self.wait(15)
        
    def addition_action(self):
        addition = MathTex("2", "+", "3").to_edge(UP)
        self.play(Write(addition))
        self.wait(40)
        
        # Animated graph shift
        shifted_y_lines = self.y_lines.copy().set_color(YELLOW)
        shifted_marks = self.marks.copy().set_color(YELLOW)
        num2 = Circle(radius=0.3, color=YELLOW).move_to(self.marks[20])
        self.play(Create(num2))
        self.play(
            Indicate(addition[0]),
            shifted_y_lines.animate.shift(RIGHT * 2),
            shifted_marks.animate.shift(RIGHT * 2),
            num2.animate.shift(RIGHT * 2),
            FadeOut(self.marks),
            run_time=4
        )
        self.wait(5)
        
        # Animated graph shift
        shifted_y_lines2 = shifted_y_lines.copy().set_color(GREEN)
        shifted_marks2 = shifted_marks.copy().set_color(GREEN)
        num5 = Circle(radius=0.3, color=GREEN).move_to(shifted_marks[20])
        self.play(Create(num5))
        self.play(
            Indicate(addition[2]),
            shifted_y_lines2.animate.shift(RIGHT * 3),
            shifted_marks2.animate.shift(RIGHT * 3),
            num5.animate.shift(RIGHT * 3),
            FadeOut(shifted_marks),
            FadeOut(num2),
            run_time=7
        )
        self.wait(8)
        
        # Clear screen
        self.play(
            FadeOut(shifted_y_lines2),
            FadeOut(shifted_marks2),
            FadeOut(shifted_y_lines),
            FadeOut(shifted_marks),
            FadeIn(self.marks)
        )
        result = MathTex("=", "5").next_to(addition, RIGHT)
        self.play(Indicate(result), Indicate(self.marks[25]), Indicate(num5))
        self.play(
            FadeOut(num5), 
            FadeOut(addition),
            FadeOut(result)
        )
        self.wait(5)
        
    def multiplication_action(self):
        multiplication = MathTex("3", "*", "2").to_edge(UP)
        self.play(Write(multiplication))
        self.wait(17)
        
        # Animated graph stretch
        stretched_y_lines = self.y_lines.copy().set_color(YELLOW)
        stretched_marks = self.marks.copy().set_color(YELLOW)
        num3 = Circle(radius=0.3, color=YELLOW).move_to(stretched_marks[21])
        self.play(Create(num3))
        self.play(
            Indicate(multiplication[0]),
            *[
                line.animate.shift((i - 20) * RIGHT * 2)
                for i, line in enumerate(stretched_y_lines)
            ],
            *[
                mark.animate.shift((i - 20) * RIGHT * 2) 
                for i, mark in enumerate(stretched_marks)
            ],
            num3.animate.shift(RIGHT * 2),
            FadeOut(self.marks),
            run_time=4
        )
        self.wait(6)
        
        # Animated graph stretch
        stretched_y_lines2 = stretched_y_lines.copy().set_color(GREEN)
        stretched_marks2 = stretched_marks.copy().set_color(GREEN)
        num6 = Circle(radius=0.3, color=GREEN).move_to(stretched_marks2[21])
        self.play(Create(num6))
        self.play(
            Indicate(multiplication[2]),
            *[
                line.animate.shift((i - 20) * RIGHT * 3)
                for i, line in enumerate(stretched_y_lines2)
            ],
            *[
                mark.animate.shift((i - 20) * RIGHT * 3) 
                for i, mark in enumerate(stretched_marks2)
            ],
            num6.animate.shift(RIGHT * 3),
            FadeOut(stretched_marks),
            FadeOut(num3),
            run_time=4
        )
        self.wait(5)
        
        # Clear screen
        self.play(
            FadeOut(stretched_y_lines2),
            FadeOut(stretched_marks2),
            FadeOut(stretched_y_lines),
            FadeOut(stretched_marks),
            FadeIn(self.marks)
        )
        self.wait(4)
        result = MathTex("=", "6").next_to(multiplication, RIGHT)
        self.play(Indicate(result), Indicate(self.marks[26]), Indicate(num6))
        self.play(
            FadeOut(num6), 
            FadeOut(multiplication),
            FadeOut(result)
        )
        self.wait(2)
    
    def construct(self):
        # Setup the coordinates
        self.setup_coords()
        
        # State basic graph plotting actions
        self.basic_graph()
        
        # Relationship between number arithmetic group and graph plotting
        self.graph_universes()
        
        # Rephrase question and defin a number
        self.define_number()

        # Addition through graph
        self.addition_action()

        # Multiplication through graph
        self.multiplication_action()
        

class GeneralityScene(Scene):
    def _reset_graphs(self):
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.play(
            FadeIn(self.add_plane),
            FadeIn(self.mul_plane),
            FadeIn(self.add_id),
            FadeIn(self.mul_id),
        )
    
    def _slide(self, dot, direction, magnitude, exclude, 
               lines, shift, run_time):
        extra = magnitude - int(magnitude)
        magnitude = int(magnitude)
        for _ in range(magnitude):
            nlines = lines.copy()
            nlines = nlines[:exclude] + nlines[exclude + 1:]
            self.play(
                nlines.animate.shift(direction * shift),
                dot.animate.shift(direction * shift),
                run_time=run_time
            )
        if extra:
            nlines = lines.copy()
            nlines = nlines[:exclude] + nlines[exclude + 1:]
            self.play(
                nlines.animate.shift(direction * shift * extra),
                dot.animate.shift(direction * shift * extra),
                run_time=run_time
            )
        self.play(FadeOut(nlines))
            
    def _slide_vertical(self, dot, direction, magnitude, exclude, run_time):
        self._slide(
            dot, direction, magnitude, exclude, self.add_plane.x_lines,
            self.y_shift, run_time
        )
            
    def _slide_horizontal(self, dot, direction, magnitude, exclude, run_time):
        self._slide(
            dot, direction, magnitude, exclude, self.add_plane.y_lines,
            self.x_shift, run_time
        )
        
    def _get_exclude_pos(self, shift, rng, flag):
        if not (flag or shift > 0):
            return rng[1] - rng[0] - 1
        if shift == 0:
            return rng[1] - 1
        if shift < 0:
            return 0
        return rng[1] - rng[0] - 1 if flag else 0
    
    def slide(self, dot, direction, magnitude, run_time=1):
        if direction[1] != 0:
            shift = self.add_plane._origin_shift(
                [self.add_plane.y_axis.x_min, self.add_plane.y_axis.x_max])
            rng = self.add_plane.y_range
            exclude = self._get_exclude_pos(shift, rng, direction[1] == 1)
            self._slide_vertical(dot, direction, magnitude, exclude, run_time)
        else:
            shift = self.add_plane._origin_shift(
                [self.add_plane.x_axis.x_min, self.add_plane.x_axis.x_max])
            rng = self.add_plane.x_range
            exclude = self._get_exclude_pos(shift, rng, direction[0] == -1)
            self._slide_horizontal(
                dot, direction, magnitude, exclude, run_time)
        
    def setup(self):
        (
            self.add_plane_shift, self.mul_plane_shift,
            self.add_title, self.add_plane,
            self.x_shift, self.y_shift, self.add_id,
            self.mul_title, self.mul_plane, self.mul_id
        ) = setup_space()
        # Create
        self.add(self.add_plane, self.mul_plane)
        self.play(
            Write(self.add_title), Write(self.mul_title),
            Create(self.add_id), Create(self.mul_id)
        )
        self.wait(2)
        
    def define_number(self):
        number = Tex("i", font_size=48).move_to(ORIGIN)
        self.play(Write(number))
        self.wait(20)
        num_add = self.add_id.copy()
        self.slide(num_add, UP, 1, 6)
        self.wait(5)
        
        num_mul = self.mul_id.copy()
        point = self.mul_plane.get_origin()
        circle = Circle(radius=self.x_shift, color=GREEN).move_to(point)
        arc = Arc(radius=self.x_shift, arc_center=point, angle=PI/2)
        self.play(Create(circle))
        self.play(
            Rotate(self.mul_plane.x_lines, angle=PI / 2, about=point),
            Rotate(self.mul_plane.y_lines, angle=PI / 2, about=point),
            MoveAlongPath(num_mul, arc),
            FadeOut(circle), run_time=10
        )
        self.wait(2)
        self.play(FadeOut(num_add), FadeOut(num_mul), FadeOut(number))
        
    def addition_action(self):
        x, y = 2, 3/2
        addition = MathTex(
            f"{x}", "+", r"\frac{3}{2}i"
        ).move_to(ORIGIN)
        self.play(Write(addition))
        self.wait(28)
        
        # Animated graph shift
        num = self.add_id.copy()
        self.slide(num, RIGHT, 2, 2)
        self.slide(num, UP, 3 / 2, 2)
        self.play(Indicate(addition), Indicate(num))
        self.wait(2)
        self.play(FadeOut(addition), FadeOut(num))
        self.wait(2)
        
    def multiplication_action(self, wait=2):
        x, y, r = 2, 3/2, 5/2
        a = np.arctan(y / x)
        multiplication = MathTex(
            f"{x}", "+", r"\frac{3}{2}i"
        ).move_to(ORIGIN)
        self.play(Write(multiplication))
        self.wait(wait * 2)
        num = self.mul_id.copy()
        plane = self.mul_plane.copy()
        self.play(
            plane.animate.scale(
                r, about_point=self.mul_plane.get_origin()
            ),
            num.animate.shift((r - 1) * RIGHT * self.x_shift),
            run_time=wait * 2
        )
        point = self.mul_plane.get_origin()
        circle = Circle(radius=r * self.x_shift, color=GREEN).move_to(point)
        arc = Arc(radius=r * self.x_shift, arc_center=point, angle=a)
        self.play(Create(circle))
        self.play(
            Rotate(plane.x_lines, angle=a, about=point),
            Rotate(plane.y_lines, angle=a, about=point),
            MoveAlongPath(num, arc),
            FadeOut(circle), run_time=wait * 2
        )
        self.play(FadeOut(plane))
        self.wait(wait)
        self.play(Indicate(multiplication), Indicate(num))
        self.wait(wait)
        self.play(FadeOut(multiplication), FadeOut(num))
        self.wait(wait)
        
    def i_squared(self):
        i2 = MathTex(r"i^2").move_to(ORIGIN)
        self.play(Write(i2))
        self.wait(10)
        imul = MathTex(r"i \cdot i").next_to(i2, DOWN)
        self.play(Write(imul))
        self.wait(15)
        self.play(FadeOut(imul))
        
        # Animated graph stretch
        num = self.mul_id.copy()
        point = self.mul_plane.get_origin()
        circle = Circle(radius=self.x_shift, color=GREEN).move_to(point)
        arc = Arc(radius=self.x_shift, arc_center=point, angle=PI/2)
        self.play(Create(circle))
        self.play(
            Rotate(self.mul_plane.x_lines, angle=PI / 2, about=point),
            Rotate(self.mul_plane.y_lines, angle=PI / 2, about=point),
            MoveAlongPath(num, arc),
            run_time=4
        )
        arc = Arc(
            radius=self.x_shift, arc_center=point,
            start_angle=PI/2, angle=PI/2
        )
        self.play(
            Rotate(self.mul_plane.x_lines, angle=PI / 2, about=point),
            Rotate(self.mul_plane.y_lines, angle=PI / 2, about=point),
            MoveAlongPath(num, arc),
            FadeOut(circle), run_time=4
        )
        self.play(Indicate(num), Indicate(i2))
        self.wait(2)
        self.play(FadeOut(num), FadeOut(i2))
        self.wait(2)
        
    def _exp_animation(self, eq, base, pow, run_time=4):
        num_add = self.add_id.copy()
        num_mul = self.mul_id.copy()
        mul_plane = self.mul_plane.copy()
        point = self.mul_plane.get_origin()
        extra = pow - int(pow)
        ipow = int(pow)
        add_direction = RIGHT if pow > 0 else LEFT
        for i in range(1, ipow + 1):
            self.play(
                mul_plane.animate.scale(base, about_point=point),
                num_add.animate.shift(add_direction * self.x_shift),
                num_mul.animate.shift(
                    ((base - 1) * (base ** (i - 1))) * RIGHT * self.x_shift
                ),
                run_time=run_time
            )
        if extra:
            self.play(
                mul_plane.animate.scale(base ** extra, about_point=point),
                num_add.animate.shift(add_direction * self.x_shift),
                num_mul.animate.shift(
                    (base ** pow - base ** ipow) * RIGHT * self.x_shift
                ),
                run_time=run_time
            )
        self.play(FadeOut(mul_plane))
        self.wait(2)
        if eq is not None:
            self.play(Indicate(num_add), Indicate(num_mul), Indicate(eq))
            self.wait(2)
        self.play(FadeOut(num_add), FadeOut(num_mul))
        self.wait(2)
    
    def _iexp_animation(self, eq, pow, complex=False, run_time=4):
        num_add = self.add_id.copy()
        num_mul = self.mul_id.copy()
        point = self.mul_plane.get_origin()
        if pow > 0:
            add_direction = UP if complex else RIGHT
            angle = 1 if complex else PI / 2
        else:
            add_direction = DOWN if complex else LEFT
            angle = 1 if complex else -PI / 2
        start_angle = 0
        extra = pow - int(pow)
        pow = int(pow)
        for i in range(pow):
            arc = Arc(
                radius=self.x_shift, arc_center=point,
                start_angle=start_angle, angle=angle
            )
            self.play(
                num_add.animate.shift(add_direction * self.x_shift),
                MoveAlongPath(num_mul, arc),
                run_time=run_time
            )
            start_angle += angle
        if extra:
            angle = extra * angle
            arc = Arc(
                radius=self.x_shift, arc_center=point,
                start_angle=start_angle, angle=angle
            )
            self.play(
                num_add.animate.shift(add_direction * self.x_shift * extra),
                MoveAlongPath(num_mul, arc),
                run_time=run_time
            )
        if eq is not None:
            self.play(Indicate(num_add), Indicate(num_mul), Indicate(eq))
            self.wait(2)
        self.play(FadeOut(num_add), FadeOut(num_mul))
        self.wait(2)
    
    def exponent(self):
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        exp = MathTex("e^8", font_size=48).to_edge(UP)
        self.play(Write(exp))
        self.wait(5)
        exp2 = MathTex(r"e^{3+5}", font_size=48).next_to(exp, DOWN)
        self.play(Write(exp2))
        self.wait(15)
        exp3 = MathTex(r"e^3 \cdot e^5", font_size=48).next_to(exp2, DOWN)
        self.play(Write(exp3))
        self.wait(15)
        self.play(Indicate(exp2), run_time=3)
        self.play(Indicate(exp3), run_time=3)
        self.wait(20)
        
        # Clear and reconstruct graphs
        self._reset_graphs()
        self.wait(10)
        
        exp = MathTex("2^x", font_size=48).to_edge(UP)
        self.play(Write(exp))
        self.wait(2)
        split  = MathTex(r"2^{1+1+1+...+1}").next_to(exp, DOWN)
        self.play(Write(split))
        self.wait(5)
        self._exp_animation(exp, 2, 2, run_time=8)
        frac = r"\left(\frac{3}{2}\right)^x"
        frac_sp = r"\left(\frac{3}{2}\right)^{1+1+1+...+1}"
        expf = MathTex(frac, font_size=48).next_to(split, DOWN)
        splitf  = MathTex(frac_sp).next_to(expf, DOWN)
        self.play(Write(expf), Write(splitf))
        self.wait(1)
        self._exp_animation(expf, 3 / 2, 2, run_time=8)
        expi = MathTex(r"i^x", font_size=48).next_to(splitf, DOWN)
        spliti  = MathTex(r"i^{1+1+1+...+1}").next_to(expi, DOWN)
        self.play(Write(expi), Write(spliti))
        self.wait(1)
        self._iexp_animation(expi, 4, run_time=6)
        exp_frac = MathTex(r"i^{\frac{5}{2}}", font_size=48).next_to(spliti, DOWN)
        split_frac  = MathTex(r"i^{1+1+1+...}").next_to(exp_frac, DOWN)
        self.play(Write(exp_frac), Write(split_frac))
        self.wait(1)
        self._iexp_animation(exp_frac, 5 / 2, run_time=8)
        self.wait(5)
        self.play(
            FadeOut(exp), FadeOut(split),
            FadeOut(expf), FadeOut(splitf),
            FadeOut(expi), FadeOut(spliti),
            FadeOut(exp_frac), FadeOut(split_frac)
        )
        self.wait(20)
        exp = MathTex("e^{3i}", font_size=48).to_edge(UP)
        self.play(Write(exp))
        self.wait(8)
        self._iexp_animation(exp, 3, True)
        self._iexp_animation(expi, 3, run_time=8)
        self.play(FadeOut(exp), FadeOut(expi))
        self.wait(2)
        
    def closing(self):
        self.multiplication_action(wait=8)
        hint = Tex("HINT!! Polar coordinates", font_size=24).to_edge(UP)
        polar = MathTex(r"x+iy=re^{i\theta}").next_to(hint, DOWN)
        self.play(Write(hint), Write(polar))
        self.wait(12)
        
        euler = Tex("Euler's Rule", font_size=24).next_to(polar, DOWN)
        euler_formula = MathTex(r"e^{i\pi}=-1").next_to(euler, DOWN)
        self.play(Write(euler), Write(euler_formula))
        self.wait(55)
        
        question = MathTex(r"i^i").next_to(euler_formula, DOWN)
        self.play(Write(question))
        self.wait(2)
        qhint = Tex(
            "HINT!! Exponent intuition and Euler rule", font_size=24
        ).next_to(question, DOWN)
        exp = MathTex(r"e^1", r"e^i", r"i^2").next_to(qhint, DOWN)
        self.play(Write(qhint), Write(exp))
        self.wait(2)
        self._exp_animation(exp[0], 2.732, 1, run_time=8)
        self._iexp_animation(exp[1], 1, True, run_time=6)
        self._iexp_animation(exp[2], 2, run_time=6)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def construct(self):
        # Setup the coordinates
        self.setup()
        self.wait(6)
        
        # Rephrase question and defin a number
        self.define_number()

        # Addition through graph
        self.addition_action()

        # Multiplication through graph
        self.multiplication_action(wait=0.5)
        self.wait(29)

        # Multiplication through graph
        self.i_squared()

        # Exponentiation
        self.exponent()
        self.wait(70)

        # Exponentiation
        self.closing()
