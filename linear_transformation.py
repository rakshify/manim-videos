from functools import partial
from typing import List

from manim import *
import numpy as np


from src.utils import (
    MatrixGeometryScene,
    MatrixDrawing,
    VoicedScene,
    EXAMPLE_MATRIX,
    mobius_transform,
    rose_petal
)


class LTOpeningScene(MatrixGeometryScene):
    name = "opening_scene"

    def __init__(self, **kwargs):
        origin = np.array([4.5, 0.5, 0])
        scale = 1 / 2
        x_range, y_range = [-4, 4, 1], [-4, 4, 1]
        mask_points = [
            np.array([0, 5, 0]),
            np.array([0, -5, 0]),
            np.array([10, -5, 0]),
            np.array([10, 5, 0])
        ]
        super().__init__(
            origin=origin,
            scale=scale,
            x_range=x_range,
            y_range=y_range,
            mask_points=mask_points,
            **kwargs
        )
        self.space.plane.set_opacity(0)
        A = np.array([[1, -1], [1, 2]])
        B = np.array([[1, 2], [0, -1]])
        self.A = MatrixDrawing(A, ORIGIN, elem_color="#FFFF00", font_size=72)
        self.B = MatrixDrawing(B, ORIGIN, elem_color="#FFFF00", font_size=72)

    def write_matrix(self, run_time: float, wait_time: float=0, **kwargs):
        self.head = Tex("MATRIX", font_size=72).to_edge(UP)
        self.line = Line(np.array([-10, 2.5, 0]), np.array([10, 2.5, 0]))
        self.play(
            Write(self.head), Create(self.line), run_time=run_time, **kwargs
        )
        self.play(Write(self.A.tex), run_time=run_time, **kwargs)
        self.wait(wait_time)

    def definition(self, run_time: float, wait_time: float=0, **kwargs):
        self.play(
            self.A.tex.animate.move_to(4 * LEFT),
            self.space.plane.animate.set_opacity(1.0),
            run_time=run_time
        )
        self.transform_space(run_time=run_time, wait_time=0.01, **kwargs)
        self.wait(wait_time)

    def construct(self):
        self.write_matrix(run_time=2, wait_time=1)
        self.definition(run_time=2, wait_time=1)


class ExplainTransformScene(VoicedScene):
    name = "explain_transform_scene"

    def heading(self, run_time: float, wait_time: float=0, **kwargs):
        self.head = Tex("Transform", font_size=72).to_edge(UP)
        self.line = Line(np.array([-10, 2.5, 0]), np.array([10, 2.5, 0]))
        self.head[0][:5].set_color(BLUE)
        self.head[0][5:].set_color(YELLOW)
        self.play(Write(self.head), Create(self.line), run_time=run_time)
        self.wait(wait_time)
        
    def transform_example(self, run_time: float, wait_time: float=0, **kwargs):
        # Creating shapes
        circle = Circle(color=RED)
        square = Square(color=GREEN)

        #Showing shapes
        self.play(Create(square), run_time=run_time, **kwargs)
        self.play(Transform(square, circle), run_time=run_time, **kwargs)
        self.wait(wait_time)
        self.play(FadeOut(square), FadeOut(circle))
        
    def transform_as_function(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        func = MathTex("f(x)", font_size=72, color=YELLOW).move_to(ORIGIN)
        ip = MathTex("x", font_size=72, color=GREEN).next_to(func, 8 * LEFT)
        op = MathTex("y", font_size=72, color=RED).next_to(func, 8 * RIGHT)
        box = SurroundingRectangle(func, buff = .1, color=YELLOW)
        self.add(ip, func, op, box)
        ipc = ip.copy()
        opc = op.copy()
        self.play(FadeOut(ipc, target_position=func), run_time=run_time)
        self.play(FadeIn(opc, target_position=func), run_time=run_time)
        u = np.array([2, 3])
        mu = MatrixDrawing(
            u.T, position=ip.get_center(), elem_color=GREEN, font_size=72
        )
        v = np.array([3, 0])
        mv = MatrixDrawing(
            v.T, position=op.get_center(), elem_color=RED, font_size=72
        )
        self.remove(ip, op, ipc, opc, func, box)
        mat = MatrixDrawing(
            EXAMPLE_MATRIX.T, position=ORIGIN, elem_color=YELLOW, font_size=72
        )
        box = SurroundingRectangle(mat.tex, buff = .1, color=YELLOW)
        self.add(mu.tex, mat.tex, mv.tex, box)
        ipc = mu.tex.copy()
        opc = mv.tex.copy()
        self.play(FadeOut(ipc, target_position=mat.tex), run_time=run_time)
        self.play(FadeIn(opc, target_position=mat.tex), run_time=run_time)
        self.wait(wait_time)

    def change_heading(self, run_time: float, wait_time: float=0, **kwargs):
        tex = Tex("Linear Transform", font_size=72).to_edge(UP)
        tex[0][:6].set_color(YELLOW)
        tex[0][6:11].set_color(BLUE)
        tex[0][11:].set_color(YELLOW)
        self.play(Transform(self.head, tex), run_time=run_time)
        self.wait(wait_time)
        # Clear screen
        self.play(*[
            FadeOut(mob) for mob in self.mobjects
            if mob not in (tex, self.line, self.head)
        ])

    def spring_example(self, run_time: float, wait_time: float=0, **kwargs):
        def get_spring(num_turns, spring_width, turn_spacing):
            return ParametricFunction(
                lambda t: np.array([
                    t * turn_spacing,
                    spring_width * np.cos(t) / 2,
                    0
                ]),
                t_range=[-num_turns * PI, num_turns * PI],
                color=BLUE
            )
        
        stretch = lambda p: np.array([2 * p[0], p[1] / 2, 0])

        # Create the spring curve
        s1 = get_spring(5, 2, 0.25)
        dots = VGroup()
        dots2 = VGroup()
        ps = [-2.5, -1, 0.8, 2.9]
        colors = [RED, GREEN, YELLOW, WHITE]
        for p, color in zip(ps, colors):
            dot = Dot(np.array([p, np.cos(4 * p), 0]), color=color)
            dots.add(dot)

        # Add the curve to the scene
        self.play(Create(s1), run_time=run_time)
        self.add(dots)
        self.wait(wait_time)
        # self.play(s1.animate.become(s2), run_time=run_time)
        self.play(
            ApplyPointwiseFunction(stretch, s1),
            ApplyPointwiseFunction(stretch, dots),
            run_time=run_time
        )
        self.wait(wait_time)
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def construct(self):
        self.heading(run_time=2, wait_time=1)
        self.transform_example(run_time=2, wait_time=1)
        self.transform_as_function(run_time=2, wait_time=1)
        self.change_heading(run_time=2, wait_time=1)
        self.spring_example(run_time=2, wait_time=1)


class TransformationGeometryScene(MatrixGeometryScene):
    name = "transformation_geometry_scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.A = np.array([[1, 0], [1, 1]])
        self.iA = np.array([[1, 0], [-1, 1]])
        # self.mA = MatrixDrawing(self.A)
        
    def opening_transform(self, run_time: float, wait_time: float=0, **kwargs):
        self.dots = VGroup()
        ps = np.zeros((4, 3))
        ps[:, :2] = np.random.rand(4, 2) * 6 - 3
        colors = [RED, GREEN, YELLOW, WHITE]
        # print(ps.shape)
        # input("check all")
        for p, color in zip(ps, colors):
            # print(p.shape, p)
            # input("check one at a time")
            dot = Dot(p, color=color)
            self.dots.add(dot)
        self.add_transformable_objects(self.dots)
        self.transform_space(self.A, run_time=run_time, wait_time=0.01)
        self.wait(wait_time)
        self.transform_space(self.iA, run_time=run_time, wait_time=0.01)
        self.wait(wait_time)
        self.remove_transformable_objects(self.dots)
        # self.remove(self.dots)
        
    def cool_transforms(self, run_time: float, wait_time: float=0, **kwargs):
        t = (1.75 + 1j) * PI / 6
        funcs = [
            partial(
                mobius_transform,
                a=np.cosh(t),
                b=np.sinh(t),
                c=np.sinh(t),
                d=np.cosh(t)
            ),
            lambda z: 0.5 * z ** 2,
            partial(rose_petal, a=1, n=7)
        ]
        for func in funcs:
            plane = self.space.plane.copy()
            # dots = self.dots.copy()
            self.play(
                *(self.space.apply_complex_function(func)),
                run_time=run_time,
                **kwargs
            )
            self.wait(wait_time)
            self.space.plane.become(plane)
            # self.dots.become(dots)

    def construct(self):
        self.opening_transform(run_time=2, wait_time=1)
        self.cool_transforms(run_time=2, wait_time=1)


class LinearTransformConditionsScene(MatrixGeometryScene):
    name = "linear_transform_conditions_scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.A = np.array([[1, 0], [1, 1]])
        self.iA = np.array([[1, 0], [-1, 1]])

    def no_curves(self, run_time: float, wait_time: float=0, **kwargs):
        plane = self.space.plane.copy()
        self.transform_space(
            self.A, run_time=run_time, wait_time=wait_time, **kwargs
        )
        self.space.plane.become(plane)
        self.wait(wait_time)

    def const_origin(self, run_time: float, wait_time: float=0, **kwargs):
        dot = Dot(self.space.origin, color=YELLOW)
        self.transform_space(
            self.iA, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.play(Indicate(dot), run_time=run_time)
        self.wait(wait_time)

    def show_heading(self, run_time: float, wait_time: float=0, **kwargs):
        head = Tex("Linear Transform", font_size=72).to_edge(UP)
        line = Line(np.array([-10, 2.5, 0]), np.array([10, 2.5, 0]))
        head[0][:6].set_color(YELLOW)
        head[0][6:11].set_color(BLUE)
        head[0][11:].set_color(YELLOW)
        mask = Polygon(
            np.array([-10, 5, 0]),
            np.array([10, 5, 0]),
            np.array([10, 2, 0]),
            np.array([-10, 2, 0]),
            color=BLACK, fill_opacity=1.0, stroke_width=0.0
        )
        self.add(mask)
        self.play(Write(head), Create(line), run_time=run_time, **kwargs)
        self.wait(wait_time)

    def construct(self):
        self.no_curves(run_time=2, wait_time=1)
        self.const_origin(run_time=2, wait_time=1)
        self.show_heading(run_time=2, wait_time=1)


class TransformationAsBasisScene(MatrixGeometryScene):
    name = "transformation_as_basis_scene"

    def __init__(self, **kwargs):
        super().__init__(add_background_plane=True, **kwargs)
        self.A = np.array([[1, -1], [1, 2]])
        self.mA = MatrixDrawing(
            self.A.T,
            position=np.array([0, 3, 0]),
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.v = np.array([3, 2])
        self.mv = MatrixDrawing(
            np.array(["x", "y"]).reshape(-1, 1),
            position=5.5 * RIGHT + UP,
            elem_color=YELLOW,
            include_background_rectangle=True
        )
        s = (r"\vec{\textbf{v}} = x\cdot\hat{\textbf{i}} + "
             r"y\cdot\hat{\textbf{j}}")
        self.vec_tex = MathTex(s, font_size=72
        ).move_to(np.array([-4, 3, 0])).add_background_rectangle()

    def show_transform(self, run_time: float, wait_time: float=0, **kwargs):
        self.remove_basis_labels()
        self.add_vectors_on_space(self.v)
        self.transform_space(
            self.A, run_time=run_time, wait_time=0.01, **kwargs
        )

    def transformed_bases(self, run_time: float, wait_time: float=0, **kwargs):
        i = Tex(
            r"Transformed $\hat{\textbf{i}}$", font_size=24, color=GREEN
        ).move_to(RIGHT + 1.5 * DOWN)
        j = Tex(
            r"Transformed $\hat{\textbf{j}}$", font_size=24, color=RED
        ).move_to(RIGHT + 2.5 * UP)
        self.iv = MatrixDrawing(
            np.array([1, -1]).reshape(-1, 1),
            1.5 * RIGHT + 0.6 * DOWN,
            elem_color=GREEN,
            include_background_rectangle=True
        )
        self.jv = MatrixDrawing(
            np.array([1, 2]).reshape(-1, 1),
            1.4 * RIGHT + 1.5 * UP,
            elem_color=RED,
            include_background_rectangle=True
        )
        self.play(
            Write(i), Write(j),
            Write(self.iv.tex), Write(self.jv.tex),
            run_time=run_time
        )
        self.wait(wait_time)

    def vector_as_transformed_bases(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.vec_tex[1][3].set_color(YELLOW)
        self.vec_tex[1][8].set_color(YELLOW)
        self.vec_tex[1][5:7].set_color(GREEN)
        self.vec_tex[1][-2:].set_color(RED)
        # self.play(Write(self.vec_tex), run_time=run_time, **kwargs)
        self.play(
            Write(self.vec_tex),
            Write(self.mv.tex),
            run_time=run_time,
            **kwargs
        )
        s = (r"$\vec{\textbf{v}} = x\cdot$(Transformed $\hat{\textbf{i}}$)"
             r" $+\ y\cdot$(Transformed $\hat{\textbf{j}}$)")
        pos = self.vec_tex.get_center() + DOWN# + RIGHT
        vec_tex1 = Tex(
            r"$\vec{\textbf{v}} = x\cdot$(Transformed $\hat{\textbf{i}}$) $+$",
            font_size=48
        ).move_to(pos).add_background_rectangle()
        vec_tex1[1][3].set_color(YELLOW)
        vec_tex1[1][6:19].set_color(GREEN)
        pos = vec_tex1.get_center() + DOWN + 0.2 * RIGHT
        vec_tex2 = Tex(
            r"$y\cdot$(Transformed $\hat{\textbf{j}}$)", font_size=48
        ).move_to(pos).add_background_rectangle()
        vec_tex2[1][0].set_color(YELLOW)
        vec_tex2[1][3:16].set_color(RED)
        self.play(Write(vec_tex1), Write(vec_tex2), run_time=run_time, **kwargs)
        # pos = self.mA.tex.get_center() + 0.35 * LEFT
        # x_ell = Ellipse(width=0.7, height=1.2, color=GREEN, arc_center=pos)
        # pos = pos + 0.9 * RIGHT
        # y_ell = Ellipse(width=0.5, height=1.2, color=RED, arc_center=pos)
        # self.add(x_ell, y_ell)
        # self.play(
        #     Indicate(x_ell),
        #     Indicate(vec_tex1[1][6:19]),
        #     run_time=run_time,
        #     **kwargs
        # )
        # self.play(
        #     Indicate(y_ell),
        #     Indicate(vec_tex2[1][3:16]),
        #     run_time=run_time,
        #     **kwargs
        # )
        self.wait(wait_time)

    def numerical(self, run_time: float, wait_time: float=0, **kwargs):
        vec_str = (r"\vec{\textbf{v}} = x\cdot%s + y\cdot%s"
                   % (self.iv.tex_string, self.jv.tex_string))
        vec_tex = MathTex(vec_str, font_size=48).move_to(
            4 * LEFT + 0.5 * DOWN).add_background_rectangle()
        vec_tex[1][3].set_color(YELLOW)
        vec_tex[1][11].set_color(YELLOW)
        vec_tex[1][6:9].set_color(GREEN)
        vec_tex[1][14:16].set_color(RED)
        self.play(Write(vec_tex), run_time=run_time)
        vec_str = (r"\vec{\textbf{v}} = %s\cdot%s" 
                   % (self.mA.tex_string, self.mv.tex_string))
        vec_tex2 = MathTex(vec_str, font_size=48).move_to(
            4 * LEFT + 2 * DOWN).add_background_rectangle()
        self.matrix = vec_tex2[1][3:10].copy()
        vec_tex2[1][4:9].set_opacity(0)
        vec_tex2[1][11:].set_opacity(0)
        ti = vec_tex[1][6:9].copy()
        pi = (vec_tex2[1][4].get_center() + vec_tex2[1][6].get_center()) / 2
        tj = vec_tex[1][14:16].copy()
        pj = (vec_tex2[1][5].get_center() + vec_tex2[1][8].get_center()) / 2
        v = self.mv.tex.copy()
        pv = vec_tex2[1][11:].get_center()
        self.add(vec_tex2)
        self.play(
            # Write(vec_tex2),
            ti.animate.move_to(pi),
            tj.animate.move_to(pj),
            v.animate.move_to(pv),
            # FadeOut(ti, target_position=vec_tex2[1][6]),
            # FadeOut(tj, target_position=vec_tex2[1][8]),
            # FadeOut(v, target_position=vec_tex2[1][10]),
            run_time=run_time
        )
        self.wait(wait_time)
        self.remove(vec_tex, vec_tex2, ti, tj, v)
        self.remove(*[
            mob for mob in self.mobjects 
            if isinstance(mob, MathTex) and mob != self.matrix
        ])

    def transformed_bases_as_matrix(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.matrix[1].set_color(GREEN)
        self.matrix[2].set_color(RED)
        self.matrix[3:5].set_color(GREEN)
        self.matrix[5].set_color(RED)
        self.play(
            self.matrix.animate.move_to(3 * LEFT + 3 * UP),
            run_time=run_time,
            **kwargs
        )
        self.matrix.add_background_rectangle()
        self.wait(wait_time)

    def any_transformed_bases(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        matrix = MatrixDrawing(
            np.array([["a", "c"], ["b", "d"]]).T,
            position=(3 * LEFT + UP),
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 4], [4, 5]],
            include_background_rectangle=True
        )
        iv = MatrixDrawing(
            np.array(["a", "c"]).reshape(-1, 1),
            1.5 * RIGHT + 0.6 * DOWN,
            elem_color=GREEN,
            include_background_rectangle=True
        )
        jv = MatrixDrawing(
            np.array(["b", "d"]).reshape(-1, 1),
            1.4 * RIGHT + 1.5 * UP,
            elem_color=RED,
            include_background_rectangle=True
        )
        self.play(
            Write(matrix.tex), Write(iv.tex), Write(jv.tex), run_time=run_time
        )
        self.wait(wait_time)

    def construct(self):
        self.draw_bases(run_time=2, wait_time=1, write_labels=True)
        self.show_transform(run_time=2, wait_time=1)
        self.transformed_bases(run_time=2, wait_time=1)
        self.vector_as_transformed_bases(run_time=2, wait_time=1)
        self.numerical(run_time=2, wait_time=1)
        self.transformed_bases_as_matrix(run_time=2, wait_time=1)
        self.any_transformed_bases(run_time=2, wait_time=1)


class MatrixMultiplicationScene(MatrixGeometryScene):
    name = "matrix_multiplication_scene"

    def __init__(self, **kwargs):
        super().__init__(add_background_plane=True, **kwargs)
        self.A = np.array([[1, -1], [1, 2]])
        mat_pos = np.array([-3.5, 2, 0])
        self.mA = MatrixDrawing(
            self.A.T,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.B = np.array([[0, -1], [1, 1]])
        self.mB = MatrixDrawing(
            self.B.T,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.M = np.dot(self.B.T, self.A.T)
        self.mM = MatrixDrawing(
            self.M,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 3], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.mul = np.array([
            ["(0)(1)+(1)(-1)", "(0)(1)+(1)(2)"],
            ["(-1)(1)+(1)(-1)", "(-1)(1)+(1)(2)"]
        ])
        self.mMul = MatrixDrawing(
            self.mul,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 3], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.I = np.linalg.inv(self.M).T
        self.M = self.M.T
        self.Istr = np.array([
            [r"\frac{1}{3}", r"\frac{2}{3}"],
            [r"\frac{-2}{3}", r"\frac{-1}{3}"]
        ])
        self.mI = MatrixDrawing(
            self.Istr.T,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.v = np.array([3, 2])
        self.mv = MatrixDrawing(
            np.array(["x", "y"]).reshape(-1, 1),
            position=2 * LEFT + 2 * UP,
            elem_color=YELLOW,
            include_background_rectangle=True
        )
        self.mv1 = MatrixDrawing(
            np.array([r"x'", r"y'"]).reshape(-1, 1),
            position=5.5 * RIGHT + UP,
            elem_color=YELLOW,
            include_background_rectangle=True
        )
        self.mv2 = MatrixDrawing(
            np.array([r"x''", r"y''"]).reshape(-1, 1),
            position=1.5 * RIGHT + 3 * DOWN,
            elem_color=YELLOW,
            include_background_rectangle=True
        )

    def opening_transformation(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.transform_space(
            self.A, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.transform_space(
            self.B, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.transform_space(
            self.I, run_time=.1, wait_time=0.01, **kwargs
        )
        self.wait(wait_time)

    def _transform_one_at_a_time(
        self,
        matrix: np.array,
        mtex: MathTex,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.transform_space(
            matrix, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.play(Write(mtex), run_time=run_time, **kwargs)
        self.wait(wait_time)

    def transformA(self, run_time: float, wait_time: float=0, **kwargs):
        self._transform_one_at_a_time(
            self.A, self.mA.tex, 
            run_time=run_time, wait_time=wait_time, **kwargs
        )

    def transformB(self, run_time: float, wait_time: float=0, **kwargs):
        self.remove(self.mA.tex)
        self._transform_one_at_a_time(
            self.B, self.mB.tex, 
            run_time=run_time, wait_time=wait_time, **kwargs
        )

    def transformM(self, run_time: float, wait_time: float=0, **kwargs):
        self.remove(self.mB.tex)
        self.transform_space(
            self.I, run_time=run_time, wait_time=0.01, **kwargs
        )
        self._transform_one_at_a_time(
            self.M, self.mM.tex, 
            run_time=run_time, wait_time=wait_time, **kwargs
        )

    def _multiply_set(
        self,
        tex,
        s,
        run_time: float,
        wait_time: float,
        **kwargs
    ):
        self.play(
            s[0].animate.move_to(s[1]),
            s[2].animate.move_to(s[3]),
            run_time=run_time,
            **kwargs
        )
        self.wait(wait_time)
        self.play(
            tex[1][s[4]].animate.set_opacity(1),
            s[5].animate.move_to(s[6]),
            s[7].animate.move_to(s[8]),
            run_time=run_time,
            **kwargs
        )
        self.wait(wait_time)
    
    def _get_sets(self, tex):
        def get_group(mat, ps):
            r, c = mat.shape
            g = VGroup()
            for i in range(r):
                for j in range(c):
                    idx = i * c + j
                    color = GREEN if idx % 2 == 0 else RED
                    p = ps[idx]
                    t = MathTex(f"({mat[i][j]})", color=color).move_to(p)
                    g.add(t)
            return g
        pos = [
            tex[1][1].get_center(),
            tex[1][2].get_center(),
            tex[1][3:5].get_center(),
            tex[1][5].get_center()
        ]
        b = get_group(self.B.T, pos)
        pos = [
            tex[1][9].get_center(),
            tex[1][10].get_center(),
            tex[1][11:13].get_center(),
            tex[1][13].get_center()
        ]
        a = get_group(self.A.T, pos)
        return [
            [
                b[0].copy(), tex[1][18].get_center(),
                a[0].copy(), tex[1][21].get_center(),
                23,
                b[1].copy(), tex[1][25].get_center(),
                a[2].copy(), tex[1][28:30].get_center()
            ],
            [
                b[0], tex[1][32].get_center(),
                a[1].copy(), tex[1][35].get_center(),
                37,
                b[1], tex[1][39].get_center(),
                a[3].copy(), tex[1][42].get_center()
            ],
            [
                b[2].copy(), tex[1][45:47].get_center(),
                a[0], tex[1][49].get_center(),
                51,
                b[3].copy(), tex[1][53].get_center(),
                a[2], tex[1][56:58].get_center()
            ],
            [
                b[2], tex[1][60:62].get_center(),
                a[1], tex[1][64].get_center(),
                66,
                b[3], tex[1][68].get_center(),
                a[3], tex[1][71].get_center()
            ]
        ]

    def _multiply(self, tex, run_time: float, wait_time: float=0, **kwargs):
        sets = self._get_sets(tex)
        for s in sets:
            self._multiply_set(
                tex, s, run_time=run_time/4, wait_time=wait_time/4, **kwargs
            )
        self.wait(wait_time)

    def transformation_with_multiplication(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        # self.remove(self.mM.tex)
        # self.transform_space(
        #     self.I, run_time=.1, wait_time=0.01, **kwargs
        # )
        self.transform_space(
            self.M, run_time=run_time, wait_time=0.01, **kwargs
        )
        mul = (rf"{self.mB.tex_string}\cdot{self.mA.tex_string}"
                f"= {self.mMul.tex_string}")
        # pos = np.array([0, 2, 0])
        mul_tex = MathTex(mul).move_to(3 * UP).add_background_rectangle()
        mul_tex[1][1].set_color(GREEN)
        mul_tex[1][2].set_color(RED)
        mul_tex[1][3:5].set_color(GREEN)
        mul_tex[1][5].set_color(RED)
        mul_tex[1][9].set_color(GREEN)
        mul_tex[1][10].set_color(RED)
        mul_tex[1][11:13].set_color(GREEN)
        mul_tex[1][13].set_color(RED)
        mul_tex[1][17:73].set_opacity(0)
        self.play(Write(mul_tex), run_time=run_time)
        self._multiply(
            mul_tex, run_time=run_time, wait_time=wait_time, **kwargs
        )

    def explainA(self, run_time: float, wait_time: float=0, **kwargs):
        # self.remove(*[m for m in self.mobjects if isinstance(m, MathTex)])
        # self.transform_space(
        #     self.I, run_time=.1, wait_time=0.01, **kwargs
        # )
        self.draw_bases(run_time=run_time, wait_time=0.01)
        self.add_vectors_on_space(self.v)
        mv = self.mv.tex.copy().move_to(3.5 * RIGHT + 2 * UP)
        self.add(mv)
        self._transform_one_at_a_time(
            self.A, self.mA.tex, 
            run_time=run_time, wait_time=wait_time, **kwargs
        )
        self.play(Write(self.mv.tex), run_time=run_time)
        self.resultA = MathTex(
            rf" = {self.mv1.tex_string}"
        ).next_to(self.mv.tex, RIGHT).add_background_rectangle()
        self.resultA[1][2:-1].set_color(YELLOW)
        self.play(
            Write(self.resultA),
            mv.animate.become(self.mv1.tex),
            run_time=run_time
        )
        self.wait(wait_time)
        self.add(self.mv1.tex)
        self.remove(mv)

    def explainB(self, run_time: float, wait_time: float=0, **kwargs):
        plane = self.space.plane.copy()
        bgc = ManimColor.from_hex("#F93EE4")
        background_line_style = {
            "stroke_width": 1,
            "stroke_color": bgc
        }
        plane.background_lines.set_style(**background_line_style).set_z_index(-1)
        plane.x_axis.set_color(bgc).set_z_index(-1)
        plane.y_axis.set_color(bgc).set_z_index(-1)
        self.add(plane)
        mv = self.mv1.tex.copy().move_to(2 * LEFT + 2 * UP)
        self.remove(self.mA.tex, self.mv.tex, self.resultA)
        self._transform_one_at_a_time(
            self.B, self.mB.tex, 
            run_time=run_time, wait_time=wait_time, **kwargs
        )
        self.play(Write(mv), run_time=run_time)
        self.resultB = MathTex(
            rf" = {self.mv2.tex_string}"
        ).next_to(mv, RIGHT).add_background_rectangle()
        self.resultB[1][2:-1].set_color(YELLOW)
        self.play(
            Write(self.resultB),
            self.mv1.tex.animate.become(self.mv2.tex),
            run_time=run_time
        )
        self.wait(wait_time)
    
    def construct(self):
        self.opening_transformation(run_time=2, wait_time=1)
        self.transformA(run_time=2, wait_time=1)
        self.transformB(run_time=2, wait_time=1)
        self.transformM(run_time=2, wait_time=1)
        self.transformation_with_multiplication(run_time=2, wait_time=1)
        self.explainA(run_time=2, wait_time=1)
        self.explainB(run_time=2, wait_time=1)


class TakeHomeScene(MatrixGeometryScene):
    name = "take_home_scene"

    def __init__(self, **kwargs):
        super().__init__(
            x_range=[-100, 100, 1],
            y_range=[-100, 100, 1],
            add_bases=True,
            add_background_plane=True,
            **kwargs
        )
        mat_pos = np.array([3.5, 2, 0])
        self.M1 = np.array([[0, -1], [1, 0]])
        self.m1 = MatrixDrawing(
            self.M1.T,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 5], [5, 6]],
            include_background_rectangle=True
        )
        self.M2 = np.array([[1, 2], [0, 1]])
        self.m2 = MatrixDrawing(
            self.M2.T,
            position=mat_pos,
            elem_color=[GREEN, RED, GREEN, RED],
            elem_range=[[1, 2], [2, 3], [3, 4], [4, 5]],
            include_background_rectangle=True
        )
        self.A = np.dot(self.M2.T, self.M1.T)
        self.B = np.dot(self.M1.T, self.M2.T)
        self.iM1 = np.linalg.inv(self.M1)
        self.iM2 = np.linalg.inv(self.M2)
        self.iA = np.linalg.inv(self.A)

    def question(self, run_time: float, wait_time: float=0, **kwargs):
        self.ques = MathTex(
            r"M_1\times M_2 \neq M_2\times M_1", font_size=72
        ).move_to(3.5 * LEFT + 2 * UP).add_background_rectangle()
        self.ques[1].set_opacity(0)
        self.add(self.ques)
        self.play(self.ques[1][:5].animate.set_opacity(1), run_time=run_time)
        self.wait(wait_time)
        self.play(self.ques[1][7:].animate.set_opacity(1), run_time=run_time)
        self.wait(wait_time)
        self.play(self.ques[1][5:7].animate.set_opacity(1), run_time=run_time)
        self.add(index_labels(self.ques[1]).set_color(RED))
        self.wait(wait_time)

    def thinking(self, run_time: float, wait_time: float=0, **kwargs):
        self.transform_space(
            self.A, run_time=run_time, wait_time=wait_time, **kwargs)
        self.transform_space(
            self.iA, run_time=run_time, wait_time=wait_time, **kwargs)

    def transformation(self, run_time: float, wait_time: float=0, **kwargs):
        plane = self.space.plane.copy()
        self.transform_space(
            self.M1, run_time=run_time, wait_time=wait_time, **kwargs)
        self.play(
            Write(self.m1.tex),
            self.ques[1][0:2].animate.set_color(YELLOW),
            self.ques[1][10:].animate.set_color(YELLOW),
            run_time=run_time
        )
        self.wait(wait_time)
        self.remove(self.m1.tex)
        self.transform_space(
            self.iM1, run_time=run_time, wait_time=wait_time, **kwargs)
        self.transform_space(
            self.M2, run_time=run_time, wait_time=wait_time, **kwargs)
        # PINK = ManimColor.from_hex("#F93EE4")
        self.play(
            Write(self.m2.tex),
            self.ques[1][3:5].animate.set_color(PINK),
            self.ques[1][7:9].animate.set_color(PINK),
            run_time=run_time
        )
        self.wait(wait_time)

    def construct(self):
        self.question(run_time=2, wait_time=1)
        self.thinking(run_time=2, wait_time=1)
        self.transformation(run_time=2, wait_time=1)
