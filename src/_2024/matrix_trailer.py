from manim import *
import numpy as np


from src.utils import (
    MatrixGeometryScene,
    MatrixNumericalScene, 
    matrix_mul_question,
    matrix_det_question
)

class OpeningScene(Scene):
    def introduce(self):
        # Display matrix
        matrix_tex = Tex("MATRIX", font_size=72).move_to(ORIGIN)
        self.play(Write(matrix_tex), run_time=2)
        self.wait()
        
        # Display random usecase fields
        fields = [
            "ENGINEERING",
            "PHYSICS",
            "COMPUTER SCIENCE",
            "SIGNAL PROCESSING"
        ]
        positions = np.array([
            [ 3.4041278,  -1.09838941,  0.        ],
            [-3.87452087,  2.93803912,  0.        ],
            [ 2.51319797,  1.86397462,  0.        ],
            [-2.9716729,  -0.96379265,  0.        ]
        ])
        colors = [BLUE, YELLOW, GREEN, RED]
        np.random.shuffle(colors)
        for field, position, color in zip(fields, positions, colors):
            tex = Tex(field, font_size=48, color=color).move_to(position)
            self.play(Write(tex))
        self.wait(2)
            
    def questions(self):
        eigen = MathTex(r"Det(A - \lambda I) = 0", font_size=72)
        # eigen[0][4].set_color("BLUE")
        eigen[0][6].set_color("YELLOW")
        questions = [
            Tex("MATRIX?", font_size=72),
            matrix_mul_question(font_size=72),
            matrix_det_question(font_size=72),
            eigen
        ]
        self.wait(2)
        # Display questions one by one
        self.play(Write(questions[0].move_to(ORIGIN)), run_time=5)
        self.wait()
        self.play(FadeOut(questions[0]))
        self.play(Write(questions[1].move_to(ORIGIN)), run_time=1.5)
        self.wait()
        self.play(FadeOut(questions[1]))
        self.play(Write(questions[2].move_to(ORIGIN)), run_time=1.5)
        self.wait()
        self.play(FadeOut(questions[2]))
        self.play(Write(questions[3].move_to(ORIGIN)), run_time=1)
        # self.wait()
        self.play(FadeOut(questions[3]))
        # for question in questions:
        #     self.play(Write(question.move_to(ORIGIN)), run_time=2)
        #     self.wait()
        #     self.play(FadeOut(question))
        
    def construct(self):
        # self.introduce()
        # # Clear screen
        # self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        self.questions()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        
class CenteredGeometryScene(MatrixGeometryScene):
    def construct(self):
        self.setup_geometry()
        self.draw_vectors_on_space()
        self.transform_space()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class NumericalGeometricScene(MatrixGeometryScene, MatrixNumericalScene):
    def _setup(self):
        origin = np.array([4.5, 0.5, 0])
        scale = 1 / 2
        x_range, y_range = [-4, 4, 1], [-4, 4, 1]
        mask_points = [
            np.array([0, 5, 0]),
            np.array([0, -5, 0]),
            np.array([10, -5, 0]),
            np.array([10, 5, 0])
        ]
        self.setup_geometry(
            origin=origin,
            scale=scale,
            x_range=x_range,
            y_range=y_range,
            mask_points=mask_points
        )
        
    def construct_geometry(self):
        # Setup space
        self._setup()
        # Draw vector
        self.draw_vectors_on_space()
        # Transform Space
        self.transform_space(run_time=6)
        
    def construct_numerical(self):
        self.setup_numerical(position=np.array([-4.5, 0.5, 0]))
        
        for transform in self.matrix.linear_transform(self.vectors):
            self.play(Write(transform))
        self.wait()
        
    def construct(self):
        self.construct_numerical()
        self.wait(2)
        self.construct_geometry()
        self.wait(2)
        # Clear screen
        self.play(
            FadeOut(self.space.plane),
            *[FadeOut(mob) for mob in self.space.transformable_objects]
        )
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class LinearEquationScene(NumericalGeometricScene):
    def construct_geometry(self):
        # Setup space
        self._setup()
        # Draw the vector
        self.draw_vectors_on_space()
        pt = self.space._get_x_shift() * np.array([3, 0, 0])
        pt += self.space.origin
        circle = Circle(radius=0.3*self.scale, arc_center=pt, color=GREEN)
        self.play(Create(circle))
        # Transform Space
        self.transform_space()
        
    def construct_numerical(self):
        self.setup_numerical(
            position=np.array([-4.5, 0.5, 0]),
            vectors=np.array(["x", "y"])
        )
        
        for transform in self.matrix.linear_transform(self.vectors):
            self.play(Write(transform))


class ArithmeticProgressionScene(Scene):
    def setup(self):
        self.series = [3, 5, 7, 9, 11]

    def numerical(self):
        s = "+".join(map(str, self.series)) + r"+..."
        tex = MathTex(*s).to_edge(UP)
        for i in range(0, 9, 2):
            tex[i].set_color(YELLOW)
        tex[9].set_color(YELLOW)
        # self.add(index_labels(tex).set_color(RED))
        self.wait(2)
        self.play(Write(tex), run_time=2)
        self.wait(2)
        
        sum_tex = r"S_n^d\ &=\ \frac{n}{2}\left(a_1 + a_n\right) \\"
        sum_tex = sum_tex + r"&=\ \frac{n}{2}\left(2a_1 + (n - 1)d\right)"
        sum_tex = MathTex(sum_tex).move_to(ORIGIN)
        parameters = [0, 1, 2, 4, 15, 24, 28]
        elements = [8, 9, 11, 12, 20, 21]
        constants = [6, 17, 19, 26]
        for i in parameters:
            sum_tex[0][i].set_color(BLUE)
        for i in elements:
            sum_tex[0][i].set_color(YELLOW)
        for i in constants:
            sum_tex[0][i].set_color(GREEN)
        self.play(Write(sum_tex), run_time=7)
        self.wait(3)
        
    def geometric(self):
        y, b = 2.5, 160
        dots = VGroup()
        numbers = VGroup()
        
        # Draw Progression
        for i in range(5):
            x = -7
            row = VGroup()
            # ts = VGroup()
            for j in range(self.series[i]):
                pt = np.array([x, y, 0])
                color = ManimColor.from_rgb((255, 255, b))
                dot = Dot(pt, color=color)
                # t = Tex(pt[:2].astype("str"), font_size=20).next_to(dot, UP)
                # ts.add(t)
                row.add(dot)
                x += 1
            tex = MathTex(self.series[i]).move_to(np.array([4, y, 0]))
            self.play(Create(row), Write(tex))#, run_time=5)#, Write(ts))
            self.wait()
            numbers.add(tex)
            dots.add(row)
            y -= 1
            b -= 40
        # self.play(Create(dots))
        self.wait(2)
        
        # Draw inverted progression
        idots = dots.copy()
        matrix = -1 * np.eye(3)
        matrix[2][2] = 1
        func = lambda p: np.dot(p, matrix) + np.array([-1, 1, 0])
        p1 = np.array([-5, 2.7, 0])
        p2 = np.array([4, -1.7, 0])
        line = Line(p1, p2, color=BLUE)#, stroke_width=1.0)
        self.play(
            ApplyPointwiseFunction(func, idots),
            FadeOut(numbers),
            Create(line),
            # run_time=3
        )
        self.wait()
        
        # Formulate
        hl = Line(np.array([-7, -2, 0]), np.array([6, -2, 0]), color=RED)
        vl = Line(np.array([6.2, -1.5, 0]), np.array([6.2, 2.5, 0]), color=RED)
        htex = MathTex(r"a_1 + a_n = 3 + 11 = 14").next_to(hl, DOWN * 0.5)
        # vtex = Tex(r"\begin{turn}{-90}{n=5}\end{turn}").next_to(hl, RIGHT * 0.5)
        vtex = Tex(r"n=5").next_to(vl, RIGHT * 0.2)
        # self.add(index_labels(vtex[0]).set_color(RED))
        # self.add(index_labels(htex[0]).set_color(RED))
        elements = [0, 1, 3, 4, 6, 8, 9]
        for i in elements:
            htex[0][i].set_color(YELLOW)
        htex[0][11:].set_color(GREEN)
        vtex[0][0].set_color(BLUE)
        vtex[0][2].set_color(GREEN)
        self.play(Create(hl), Write(htex), run_time=3)
        self.play(Create(vl), Write(vtex), run_time=3)
        self.wait()

    def construct(self):
        self.setup()
        # self.numerical()
        # # Clear screen
        # self.play(*[FadeOut(mob) for mob in self.mobjects])
        # self.wait(5)
        self.geometric()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CenteredGeometryWithTextScene(MatrixGeometryScene):
    def construct(self):
        self.setup_geometry()
        self.draw_vectors_on_space()
        tex = Tex("Matrix is an action of transforming space").to_edge(UP)
        self.play(Write(tex))
        self.transform_space()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class MatrixMultiplicationGeometryScene(MatrixGeometryScene):
    def construct(self):
        self.setup_geometry()
        self.draw_vectors_on_space()
        text = "Matrix multiplication is simply transforming space twice"
        tex = Tex(text).to_edge(UP)
        self.play(Write(tex))
        self.transform_space()
        
        mat2 = np.array([[0, -1], [1, 1]])
        self.transform_space(mat2)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class MatrixDeterminantGeometryScene(MatrixGeometryScene):
    def construct(self):
        self.setup_geometry()
        self.transform_space(run_time=2)
        self.matrix_determinant()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FastCalculationsScene(Scene):
    def move_n_fade(
        self,
        mob: Mobject,
        st: np.array,
        pt: np.array,
        alpha
    ):
        print("****", alpha, "****")
        d = pt - st
        shift = (alpha / 10) * d
        t = st + shift
        print("#####", st, "#####")
        print("#####", t, "#####")
        print("#####", pt, "#####")
        mob.become(mob.set_opacity(max(0.1*alpha, 0)).move_to(t))
        
    def construct(self):
        name = Tex("Leibniz Series", color=YELLOW).to_edge(UP)
        ftext = (r"\arctan{x} = x - \frac{x^3}{3} + \frac{x^5}{5} - "
                 r"\frac{x^7}{7} + \frac{x^9}{9} - \frac{x^{11}}{11} + \dots")
        formula = MathTex(ftext).next_to(name, DOWN)
        self.play(Write(name), Write(formula), run_time=5)
        self.wait()
        text = (r"\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7}"
                r"+ \frac{1}{9} - \frac{1}{11} +\dots")
        tex = MathTex(text).next_to(formula, DOWN)
        ops = [5, 9, 13, 17, 21, 26]
        nums = list(range(4, 25, 2)) + [25]
        for i in ops:
            tex[0][i].set_color(RED)
        for i in nums:
            tex[0][i].set_color(GREEN)
        for i in range(7, 24, 4):
            tex[0][i].set_color(BLUE)
        tex[0][:3].set_color(YELLOW)
        self.play(Write(tex), run_time=5)
        self.wait()
        idx = [5, 9, 13, 17, 21, 26]
        vtex = MathTex(r"\pi = 4").next_to(ORIGIN, DOWN)
        self.play(Write(vtex))
        self.wait()
        pi = 4
        for i in range(1, 41):
            mul = (-1) ** (i % 2)
            pi = pi + mul * (4 / (2 * i + 1))
            nvtex = MathTex(rf"\pi = {pi}").next_to(ORIGIN, DOWN)
            if i < len(idx):
                animations = [
                    Indicate(tex[0][idx[i - 1]:idx[i]])
                    # cp.animate.move_to(vtex[0][2]),
                    # FadeOut(cp)
                ]
            else:
                animations = [Indicate(tex[0][-3:])]
            animations.append(Transform(vtex, nvtex))
            self.play(*animations, run_time=.3)
        # Clear screen
        # self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(5)


class HiScene(Scene):
    def construct(self):
        hi = Tex("HI!!", font_size=72, color=YELLOW).move_to(ORIGIN)
        self.play(FadeIn(hi))
        self.play(FadeOut(hi), run_time=0.2)
        series = Tex("SERIES", font_size=72, color=GREEN).move_to(ORIGIN)
        exciting = Tex("EXCITING", font_size=72, color=RED).next_to(series, UP)
        cu = Tex("COMING UP!", font_size=72, color=BLUE).next_to(series, DOWN)
        self.play(FadeIn(exciting))#, run_time=0.5)
        # self.wait()
        self.play(FadeIn(series))#, run_time=0.5)
        # self.wait()
        self.play(FadeIn(cu))#, run_time=0.5)
        # self.wait()
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
