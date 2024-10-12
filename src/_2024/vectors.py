from functools import partial
from typing import List

from manim import *
import numpy as np


from src.utils import (
    MatrixGeometryScene,
    MatrixDrawing,
    VoicedScene,
    EXAMPLE_AXIS_RANGE,
    EXAMPLE_MASK,
    EXAMPLE_SCALE
)


class VectorPhysicsScene(MatrixGeometryScene):
    name = "vector_physics_scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation_map.update({
            "showcase_vectors_on_space": self.showcase_vectors_on_space,
            "show_vector_movement": self.show_vector_movement,
            "show_unchanged_vector_movement": self.show_unchanged_vector_movement,
            "explain_walk": self.explain_walk,
        })

    def showcase_vectors_on_space(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.remove_vectors_on_space(np.array([-2, 1]))
        coords = np.array([2, 3])
        braces = self.draw_vector_braces(
            coords, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.draw_vector_angles(
            coords, run_time=run_time, wait_time=0.01, **kwargs
        )
        self.wait(wait_time)
        self.remove(braces)
        # self.play(FadeOut())
        # braces.fade(darkness=1)

    def show_vector_movement(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        # Define the path for the vector to follow
        def vector_path(t):
            # Parametric equation for a wavy ellipse centered at (2, 3)
            a, b = 3, 1  # Base semi-major and semi-minor axes
            ang = np.arctan(3 / 2)
            x = -1 + a * np.cos(ang + np.pi * t)
            y = 3 + b * np.sin(ang + np.pi * t)
            return np.array([x, y, 0])
        
        coords = np.array([2, 3])
        point = self.space.c2p(coords).flatten()
        vector = self.space.vectors[tuple(point)]
        permanent = vector.copy()
        animate_vector = lambda mob, alpha: (
            self.vector_alpha_movement_along_path(
                vector_path, mob, alpha, point, **kwargs
            )
        )
        # Apply the animation
        self.play(
            UpdateFromAlphaFunc(
                vector,
                animate_vector,
                rate_func=linear
            ),
            run_time=run_time
        )
        self.wait(wait_time)
        vector.become(permanent)
        for mob in self.mobjects:
            if isinstance(mob, Angle) or isinstance(mob, MathTex):
                self.remove(mob)

    def show_unchanged_vector_movement(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        shifts = [
            3 * RIGHT,
            2 * LEFT + 4 * DOWN,
            5 * LEFT + 5 * UP,
            RIGHT + 3 * DOWN,
            3 * RIGHT + 2 * UP
        ]
        
        coords = np.array([2, 3])
        point = self.space.c2p(coords).flatten()
        vector = self.space.vectors[tuple(point)]
        for shift in shifts:
            self.play(vector.animate.shift(shift), run_time=run_time)
        self.wait(wait_time)
        
    def _walk(
        self,
        walk_func,
        start: np.array,
        coords: np.array,
        run_time: float,
        remove_vec: bool=False,
        **kwargs
    ):
        point = self.space.c2p(coords).flatten()
        tp = tuple(point)
        if tp not in self.space.vectors:
            self.add_vectors_on_space(coords)
        vector = self.space.vectors[tp]
        x = walk_func(start, coords, run_time, wait_time=0.01, **kwargs)
        self.remove(x)
        if remove_vec:
            self.remove(vector)
            self.remove_vectors_on_space(coords)
        
    def _xwalk(
        self,
        start: np.array,
        coords: np.array,
        run_time: float,
        remove_vec: bool=False,
        **kwargs
    ):
        self._walk(
            self.basei_walk, start, coords, run_time=run_time,
            remove_vec=remove_vec, **kwargs
        )
        
    def _ywalk(
        self,
        start: np.array,
        coords: np.array,
        run_time: float,
        remove_vec: bool=False,
        **kwargs
    ):
        self._walk(
            self.basej_walk, start, coords, run_time=run_time,
            remove_vec=remove_vec, **kwargs
        )
        
    def explain_walk(self, run_time: float, wait_time: float=0, **kwargs):
        coords = np.array([2, 3])
        point = self.space.c2p(coords).flatten()
        tp = tuple(point)
        vector = self.space.vectors[tp]
        start = self.space.origin
        self._xwalk(start, coords, run_time=run_time, **kwargs)
        vector.set_stroke(opacity=0)
        vector.tip.set_stroke(opacity=0)
        vector.tip.set_fill(opacity=0)
        coords = np.array([-3, 2])
        self._xwalk(
            start, coords, run_time=run_time, remove_vec=True, **kwargs
        )
        coords = np.array([-3, 2])
        self._ywalk(
            start, coords, run_time=run_time, remove_vec=True, **kwargs
        )
        coords = np.array([-3, -2])
        self._ywalk(
            start, coords, run_time=run_time, remove_vec=True, **kwargs
        )
        vector.set_stroke(opacity=1)
        vector.tip.set_stroke(opacity=1)
        vector.tip.set_fill(opacity=1)
        self.wait(wait_time)
        

    # def construct(self):
    #     self.draw_vectors_on_space(
    #         np.array([[2, 3], [-2, 1]]),
    #         run_time=2,
    #         wait_time=1,
    #         colors=["#FFFF00", "#800080"]
    #     )
    #     self.showcase_vectors_on_space(run_time=2, wait_time=1)
    #     self.show_vector_movement(run_time=5, wait_time=1)
    #     self.show_unchanged_vector_movement(run_time=2, wait_time=1)
    #     self.explain_walk(run_time=2, wait_time=1, stroke_width=6)
    #     self.bases_walk([2, 3], run_time=2, wait_time=1, stroke_width=6)


class VectorNumericalScene(VoicedScene):
    name = "vector_numerical_scene"

    def __init__(
        self,
        renderer=None,
        camera_class=Camera,
        always_update_mobjects=False,
        random_seed=None,
        skip_animations=False,
        animations: list=[],
        audio_filename: str | None=None
    ):
        super().__init__(
            renderer=renderer,
            camera_class=camera_class,
            always_update_mobjects=always_update_mobjects,
            random_seed=random_seed,
            skip_animations=skip_animations,
            animations=animations,
            audio_filename=audio_filename
        )
        vA = np.array([98, 87, 82, 95, 86]).reshape(-1, 1)
        vB = np.array([72, 91, 90, 75, 76]).reshape(-1, 1)
        vsum = vA + vB
        vmn = vsum // 2
        # position = np.array([])
        self.vA = MatrixDrawing(
            vA, 3 * LEFT, elem_color=PURPLE, elem_range=[6, 16]
        )
        self.atex = Tex("Student A", color=PURPLE).next_to(self.vA.tex, DOWN)
        self.vB = MatrixDrawing(
            vB, 3 * RIGHT, elem_color=GREEN, elem_range=[6, 16]
        )
        self.btex = Tex("Student B", color=GREEN).next_to(self.vB.tex, DOWN)
        self.vsum = MatrixDrawing(vsum, 1.5 * RIGHT, elem_range=[6, 21])
        self.vsum.tex[0][6:21].set_opacity(0)
        self.vmn = MatrixDrawing(vmn, 4.5 * RIGHT, elem_range=[6, 16])
        self.vmn.tex[0][6:16].set_opacity(0)
        self.animation_map.update({
            "ordered_list": self.ordered_list,
            "explain_ordered_list": self.explain_ordered_list,
            "write_a_matrix": self.write_a_matrix,
            "write_b_matrix": self.write_b_matrix,
            "setup_for_ops": self.setup_for_ops,
            "add_animation": self.add_animation,
            "mean_animation": self.mean_animation
        })
        
    def ordered_list(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.order = Tex(r"``Ordered'' List").to_edge(UP)
        self.order[0][:9].set_color(YELLOW)
        self.play(Write(self.order), run_time=run_time)
        
    def explain_ordered_list(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.subjects = VGroup(
            *[
                Tex(f"Subject {i}").next_to(self.order, DOWN * (4 * i))
                for i in range(1, 6)
            ]
        )
        arrows = VGroup(
            *[
                Arrow(self.vA.tex[0][7 + 2 * i], subject, color=YELLOW)
                for i, subject in enumerate(self.subjects)
            ]
        )
        self.play(Write(self.subjects), run_time=run_time)
        self.play(*[GrowArrow(arrow) for arrow in arrows])
        self.wait(wait_time)

    def write_a_matrix(self, run_time: float, wait_time: float=0, **kwargs):
        self.play(Write(self.vA.tex), Write(self.atex), run_time=run_time)
        self.wait(wait_time)

    def write_b_matrix(self, run_time: float, wait_time: float=0, **kwargs):
        self.play(Write(self.vB.tex), Write(self.btex), run_time=run_time)
        arrows = VGroup(
            *[
                Arrow(self.vB.tex[0][6 + 2 * i], subject, color=YELLOW)
                for i, subject in enumerate(self.subjects)
            ]
        )
        self.play(*[GrowArrow(arrow) for arrow in arrows])
        self.wait(wait_time)

    def setup_for_ops(self, run_time: float, wait_time: float=0, **kwargs):
        # Clear screen
        self.plus = MathTex("+", color=YELLOW).move_to(3 * LEFT)
        self.play(
            *[
                FadeOut(mob) for mob in self.mobjects 
                if mob not in [self.vA.tex, self.vB.tex, self.atex, self.btex]
            ],
            self.vA.tex.animate.shift(1.5 * LEFT),
            self.atex.animate.shift(1.5 * LEFT),
            Write(self.plus),
            self.vB.tex.animate.shift(4.5 * LEFT),
            self.btex.animate.shift(4.5 * LEFT),
            run_time=run_time
        )
        self.wait(wait_time)

    def add_animation(self, run_time: float, wait_time: float=0, **kwargs):
        animations = []
        ai = range(6, 16, 2)
        aj = range(6, 21, 3)
        k = 0
        for i, j in zip(ai, aj):
            k += 1
            arc1 = PI * (k - 3) / 4
            arc2 = PI * (k - 3) / 3
            arc3 = PI * (k - 3) / 2
            va = self.vA.tex[0][i: i + 2].copy()
            vb = self.vB.tex[0][i: i + 2].copy()
            plus = self.plus.copy()
            res = self.vsum.tex[0][j: j + 3].copy().set_opacity(1)
            animation = [
                # FadeTransform(va, res),
                # FadeTransform(plus, res),
                # FadeOut(va, shift=res.get_center() - va.get_center()),
                # FadeOut(plus, shift=res.get_center() - plus.get_center()),
                # FadeOut(vb, shift=res.get_center() - vb.get_center()),
                FadeOut(va, target_position=res, path_arc=arc2),
                FadeOut(plus, target_position=res, path_arc=arc3),
                FadeOut(vb, target_position=res, path_arc=arc1),
                # FadeTransform(vb, res),
                self.vsum.tex[0][j: j + 3].animate.become(res)
            ]
            animations.append(animation)
        self.play(
            Write(MathTex(r"\rightarrow", color=YELLOW).move_to(ORIGIN)),
            Write(self.vsum.tex),
            run_time=run_time
        )
        for animation in animations:
            self.play(*animation, run_time=run_time)
        self.wait(wait_time)

    def mean_animation(self, run_time: float, wait_time: float=0, **kwargs):
        animations = []
        ai = range(6, 21, 3)
        aj = range(6, 16, 2)
        arrow = MathTex(
            r"\xrightarrow{\times \frac{1}{2}}", color=YELLOW
        ).move_to(3 * RIGHT)
        k = 0
        for i, j in zip(ai, aj):
            k += 1
            arc1 = PI * (k - 3) / 3
            arc2 = PI * (k - 3) / 2
            vsum = self.vsum.tex[0][i: i + 3].copy()
            mul = arrow[0][:4].copy()
            res = self.vmn.tex[0][j: j + 2].copy().set_opacity(1)
            animation = [
                FadeOut(vsum, target_position=res, path_arc=arc1),
                FadeOut(mul, target_position=res, path_arc=arc2),
                self.vmn.tex[0][j: j + 2].animate.become(res)
            ]
            animations.append(animation)
        self.play(
            Write(arrow),
            Write(self.vmn.tex),
            run_time=run_time
        )
        for animation in animations:
            self.play(*animation, run_time=run_time)
        self.wait(wait_time)

    # def construct(self):
    #     self.write_a_matrix(run_time=2, wait_time=1)
    #     self.ordered_list(run_time=2, wait_time=1)
    #     self.explain_ordered_list(run_time=2, wait_time=1)
    #     self.write_b_matrix(run_time=2, wait_time=1)
    #     self.wait(2)
    #     self.setup_for_ops(run_time=2, wait_time=1)
    #     self.add_animation(run_time=2, wait_time=1)
    #     self.mean_animation(run_time=2, wait_time=1)


class VectorOperationScene(MatrixGeometryScene):
    name = "vector_operation_scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation_map.update({
            "setup_with_numerical": self.setup_with_numerical,
            "move_vector_for_addition": self.move_vector_for_addition,
            "move_other_vec_for_addition": self.move_other_vec_for_addition,
            "shifted_base_walk": self.shifted_base_walk,
            "alternate_base_walk": self.alternate_base_walk,
            "scale_setup": self.scale_setup,
            "scale_animation": self.scale_animation,
            "explain_scale": self.explain_scale,
        })
        self.coords = np.array([[2, 3], [-3, -1]])
        self.colors = ["#FFFF00", "#800080"]
        points = self.space.c2p(self.coords)
        point = self.space.c2p(self.coords[0] + self.coords[1]).flatten()
        self.pA = points[0] + self.space.c2p(0.5 * RIGHT).flatten()
        self.pB = points[1] + self.space.c2p(0.5 * LEFT).flatten()
        self.pR = point + self.space.c2p(UP).flatten()
        vA = self.coords[0].reshape(-1, 1)
        vB = self.coords[1].reshape(-1, 1)
        self.res = vA + vB
        cA = ManimColor.from_hex(self.colors[0])
        cB = ManimColor.from_hex(self.colors[1])
        cR = ManimColor.from_hex("#00FF00")
        self.vA = MatrixDrawing(
            vA, self.pA, elem_color=cA, include_background_rectangle=True,
        )
        self.vB = MatrixDrawing(
            vB, self.pB, elem_color=cB, include_background_rectangle=True,
        )
        self.vR = MatrixDrawing(
            self.res, self.pR, elem_color=cR,
            include_background_rectangle=True,
        )
        self.vRfull = MatrixDrawing(
            np.array([["2 + (-3)"], ["3 + (-1)"]]),
            self.pR + self.space.c2p(4 * DOWN).flatten(), elem_color=cR,
            include_background_rectangle=True,
        )
        self.vRfull.tex[1][1:-1].set_opacity(0)
        self.scale_coord = np.array([2, 1])
        vS = self.scale_coord.reshape(-1, 1)
        point = self.space.c2p(self.scale_coord).flatten()
        self.pS = point + self.space.c2p(0.5 * RIGHT).flatten()
        # cS = ManimColor.from_hex("#FFFF00")
        self.vS = MatrixDrawing(
            vS, self.pS, elem_color=cA,
            include_background_rectangle=True,
        )
        self.scales = [2, 1 / 2, -3, -1/3]
        self.scale_tex = VGroup(
            MathTex("2", font_size=72).move_to(np.array([-3, 2, 0])),
            MathTex(r"\frac{1}{2}", font_size=72).move_to(np.array([-3, 2, 0])),
            MathTex("-3", font_size=72).move_to(np.array([-3, 2, 0])),
            MathTex(r"-\frac{1}{3}", font_size=72).move_to(np.array([-3, 2, 0])),
        )
        self.scaled_pS = [
            2 * point + self.space.c2p(0.5 * RIGHT).flatten(),
            -3 * point + self.space.c2p(0.5 * LEFT).flatten(),
        ]
        self.scaled_vS = [
            MatrixDrawing(
                vS * s, p, elem_color=cA,
                include_background_rectangle=True,
            ) for s, p in zip((2, -3), self.scaled_pS)
        ]
        
    def setup_with_numerical(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        self.draw_vectors_on_space(
            self.coords,
            run_time=run_time,
            wait_time=0.01,
            colors=self.colors,
            **kwargs
        )
        self.add(self.vA.tex, self.vB.tex)
        self.wait(wait_time)

    def _move_vector_for_addition(
        self,
        coord: np.array | List[float],
        to_add: np.array | List[float],
        tex_to_change: MathTex,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        vector_to_move = self.space.c2p(coord).flatten()
        vector_to_move = self.space.vectors[tuple(vector_to_move)]
        tex_to_change.set_opacity(0)
        shift = self.shift_vector(
            coord,
            to_add,
            run_time=run_time,
            wait_time=0.01
        )
        # tex_to_change.shift(shift).set_opacity(1)
        res = np.asarray(coord) + np.asarray(to_add)
        self.draw_vectors_on_space(
            res,
            run_time=run_time,
            wait_time=0.01,
            color=GREEN
        )
        self.add(self.vR.tex)
        self.wait(wait_time)
        tex_to_change.set_opacity(1)
        vector_to_move.shift(-shift)
        res_vec = self.space.c2p(res).flatten()
        res_vec = self.space.vectors[tuple(res_vec)]
        self.play(FadeOut(res_vec), FadeOut(self.vR.tex))

    def move_vector_for_addition(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        coord = self.coords[1]
        to_add = self.coords[0]
        self._move_vector_for_addition(
            coord, to_add, self.vB.tex, run_time=run_time,
            wait_time=wait_time, **kwargs
        )

    def move_other_vec_for_addition(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        coord = self.coords[0]
        to_add = self.coords[1]
        self._move_vector_for_addition(
            coord, to_add, self.vA.tex, run_time=run_time,
            wait_time=wait_time, **kwargs
        )

    def explain_scale(self, run_time: float, wait_time: float=0, **kwargs):
        stex = MathTex(
            "2", font_size=72
        ).move_to(np.array([-3, 2, 0])).add_background_rectangle()
        stxy = stex.copy()
        self.add(stex, stxy)
        x1 = self.basei_walk(
            self.space.origin, self.scale_coord, run_time=run_time,
            wait_time=0.01, **kwargs
        )
        br1 = Brace(x1)
        tx1 = self.vS.tex[1][1].copy()
        self.add(br1)
        pos = br1.get_center() + self.space.c2p(0.5 * DOWN).flatten()
        self.play(Indicate(x1), tx1.animate.move_to(pos), run_time=run_time)
        x2 = self.basei_walk(
            self.space.origin, self.scale_coord * 2, run_time=run_time,
            wait_time=0.01, **kwargs
        )
        start = x2.get_end()
        br2 = Brace(x2, buff=1.0)
        tx2 = self.vS.tex[1][1].copy()
        stx1 = MathTex(
            r"%s \times 2 = %s" % (self.scale_coord[0], self.scale_coord[0] * 2),
                font_size=30*self.scale
        ).next_to(br2, 0.5 * DOWN).add_background_rectangle()
        self.add(br2)
        pos = br2.get_center() + self.space.c2p(0.5 * DOWN).flatten()
        self.play(
            Indicate(x2),
            tx2.animate.move_to(pos).set_opacity(0),
            stex[1].animate.move_to(pos).set_opacity(0),
            FadeIn(stx1),
            run_time=run_time
        )
        y1 = self.basej_walk(
            start, self.scale_coord, run_time=run_time, wait_time=0.01,
            **kwargs
        )
        br3 = Brace(y1, direction=RIGHT)
        tx3 = self.vS.tex[1][2].copy()
        self.add(br3)
        pos = br3.get_center() + self.space.c2p(0.5 * RIGHT).flatten()
        self.play(Indicate(y1), tx3.animate.move_to(pos), run_time=run_time)
        y2 = self.basej_walk(
            start, self.scale_coord * 2, run_time=run_time,
            wait_time=0.01, **kwargs
        )
        br4 = Brace(y2, direction=RIGHT, buff=1.0)
        tx4 = self.vS.tex[1][2].copy()
        sty1 = MathTex(
            r"%s \times 2 = %s" % (self.scale_coord[1], self.scale_coord[1] * 2),
                font_size=30*self.scale
        ).next_to(br4, 0.5 * RIGHT).add_background_rectangle()
        self.add(br4)
        pos = br4.get_center() + self.space.c2p(0.5 * LEFT).flatten()
        self.play(
            Indicate(y2),
            tx4.animate.move_to(pos).set_opacity(0),
            stxy.animate.move_to(pos).set_opacity(0),
            FadeIn(sty1),
            run_time=run_time
        )
        self.remove(br1, br2, br3, br4)
        self.wait(wait_time)
        stx = stx1[1][-1].copy()
        sty = sty1[1][-1].copy()
        vp = self.space.c2p(self.scale_coord).flatten()
        vector = self.space.vectors[tuple(vp)]
        nv = vector.copy().put_start_and_end_on(
            self.space.origin, 2 * vp + self.space.origin
        )
        self.play(
            stx.animate.move_to(self.scaled_vS[0].tex[1][1]).set_opacity(0),
            sty.animate.move_to(self.scaled_vS[0].tex[1][2]).set_opacity(0),
            FadeOut(stx1),
            FadeOut(sty1),
            self.scaled_vS[0].tex.animate.set_opacity(1),
            vector.animate.become(nv),
            run_time=run_time
        )
        self.remove(stx, sty, stx1, sty1, stex, stxy, tx1, tx2, tx3, tx4)
        self.wait(wait_time)
        self.remove(x1, x2, y1, y2)

    def scale_setup(self, run_time: float, wait_time: float=0, **kwargs):
        self.draw_vectors_on_space(
            self.scale_coord,
            run_time=run_time,
            wait_time=0.01,
        )
        self.add(self.vS.tex)
        self.wait(wait_time)

    def scale_animation(self, run_time: float, wait_time: float=0, **kwargs):
        # self.remove_all_vectors()
        coord = np.array([2, 1])
        for i, scale, tx in zip(range(4), self.scales, self.scale_tex):
            self.add(tx)
            if i % 2 == 0:
                self.vS.tex.set_opacity(0)
                self.add(self.scaled_vS[i // 2].tex)
            else:
                self.scaled_vS[i // 2].tex.set_opacity(0)
                self.vS.tex.set_opacity(1)
            self.scale_vector(
                coord, scale=scale, run_time=run_time,
                wait_time=0.01, **kwargs
            )
            coord = coord * scale
            self.remove(tx)
        self.wait(wait_time)

    def shifted_base_walk(self, run_time: float, wait_time: float=0, **kwargs):
        coord = self.coords[1]
        shift_to = self.coords[0]
        res = np.array(coord) + np.array(shift_to)
        self.vB.tex.set_opacity(0)
        shift = self.shift_vector(
            coord, shift_to, run_time=run_time, wait_time=0.01
        )
        self.bases_walk(
            res, run_time=run_time, wait_time=0.01, start=shift_to,
            stroke_width=6
        )
        shift = shift + self.space.c2p(1.5 * RIGHT + 0.5 * DOWN).flatten()
        self.vB.tex.shift(shift).set_opacity(1)
        # point = self.space.c2p(coord).flatten()
        # vector_to_move = self.space.vectors[tuple(point)]
        # vector_to_move.shift(-shift)
        self.wait(wait_time)
        
    def alternate_base_walk(
        self,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        # points = self.space.c2p(coords)
        vA = self.coords[0]
        vB = self.coords[1]
        res = np.array(self.coords[0]) + np.array(self.coords[1])
        x1 = self.basei_walk(
            self.space.origin, vA, run_time=run_time, wait_time=0.01,
            **kwargs
        )
        br1 = Brace(x1)
        tx1 = self.vA.tex[1][1].copy()
        # self.add(br1, tx1)
        self.add(br1)
        pos = br1.get_center() + self.space.c2p(0.5 * DOWN).flatten()
        self.play(Indicate(x1), tx1.animate.move_to(pos), run_time=run_time)
        start = x1.get_end()
        # self.remove(x1)
        # print(start, res)
        x2 = self.basei_walk(
            start, res, run_time=run_time, wait_time=0.01, **kwargs
        )
        # self.play(Indicate(x2))
        start = x2.get_end()
        br2 = Brace(x2, buff=1.0)
        # tx2 = MathTex(
        #     f"{self.coords[1][0]}", font_size=30*self.scale
        # ).next_to(br2, 0.5 * DOWN)
        # self.add(br2, tx2)
        tx2 = self.vB.tex[1][1:3].copy()
        self.add(br2)
        pos = br2.get_center() + self.space.c2p(0.5 * DOWN).flatten()
        self.play(Indicate(x2), tx2.animate.move_to(pos), run_time=run_time)
        y1 = self.basej_walk(
            start, vA, run_time=run_time, wait_time=0.01, **kwargs
        )
        # self.play(Indicate(y1))
        start = y1.get_end()
        br3 = Brace(y1, direction=LEFT)
        # tx3 = MathTex(
        #     f"{self.coords[0][1]}", font_size=30*self.scale
        # ).next_to(br3, 0.5 * LEFT)
        # self.add(br3, tx3)
        tx3 = self.vA.tex[1][2].copy()
        self.add(br3)
        pos = br3.get_center() + self.space.c2p(0.5 * LEFT).flatten()
        self.play(Indicate(y1), tx3.animate.move_to(pos), run_time=run_time)
        # self.remove(y1)
        y2 = self.basej_walk(
            start, res, run_time=run_time, wait_time=0.01, **kwargs
        )
        # self.play(Indicate(y2))
        br4 = Brace(y2, direction=LEFT, buff=1.0)
        # tx4 = MathTex(
        #     f"{self.coords[1][1]}", font_size=30*self.scale
        # ).next_to(br4, 0.5 * LEFT)
        # self.add(br4, tx4)
        tx4 = self.vB.tex[1][3:5].copy()
        self.add(br4)
        pos = br4.get_center() + self.space.c2p(0.5 * LEFT).flatten()
        self.play(Indicate(y2), tx4.animate.move_to(pos), run_time=run_time)
        # self.remove(x1, x2, y1, y2, br1, tx1, br2, tx2, br3, tx3, br4, tx4)
        self.remove(x1, x2, y1, y2, br1, br2, br3, br4)
        self.add(self.vRfull.tex)
        self.play(
            FadeOut(tx1, target_position=self.vRfull.tex[1][3]),
            FadeOut(tx2, target_position=self.vRfull.tex[1][3]),
            self.vRfull.tex[1][1:7].animate.set_opacity(1),#FadeIn(self.vRfull.tex[1][1:3]),
            run_time=run_time,
        )
        self.play(
            FadeOut(tx3, target_position=self.vRfull.tex[1][10]),
            FadeOut(tx4, target_position=self.vRfull.tex[1][10]),
            self.vRfull.tex[1][7:-1].animate.set_opacity(1),#FadeIn(self.vRfull.tex[1][3]),
            run_time=run_time,
        )
        run_with_animations = [
            FadeOut(self.vRfull.tex, target_position=self.vR.tex),
            FadeIn(self.vR.tex)
        ]
        self.draw_vectors_on_space(
            self.res.flatten(),
            run_time=run_time,
            wait_time=0.01,
            run_with_animations=run_with_animations,
            color=GREEN
        )
        # x = self.basei_walk(
        #     self.space.origin, self.res.flatten(), run_time=run_time,
        #     wait_time=0.01, **kwargs
        # )
        # start = x.get_end()
        # y = self.basej_walk(
        #     start, self.res.flatten(), run_time=run_time,
        #     wait_time=0.01, **kwargs
        # )
        self.wait(wait_time)
        # Clear screen
        self.play(
            *[
                FadeOut(mob) for mob in self.mobjects
                if isinstance(mob, Arrow) or isinstance(mob, MathTex)
            ]
        )
        self.space.remove_all_vectors()
    
    # def construct(self):
    #     self.setup_with_numerical(run_time=2, wait_time=1)
    #     self.move_vector_for_addition(run_time=2, wait_time=1)
    #     self.move_other_vec_for_addition(run_time=2, wait_time=1)
    #     self.wait(2)
    #     self.bases_walk(
    #         [2, 3], run_time=2, wait_time=1, stroke_width=6,
    #         remove_walk_lines_after=False
    #     )
    #     self.shifted_base_walk(run_time=2, wait_time=1)
    #     self.alternate_base_walk(run_time=2, wait_time=1, stroke_width=6)
    #     self.scale_setup(run_time=2, wait_time=1)
    #     self.scale_animation(run_time=2, wait_time=1)
    #     self.explain_scale(run_time=2, wait_time=1, stroke_width=6)


class VectorSpanScene(MatrixGeometryScene):
    name = "vector_span_scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation_map.update({
            "vector_as_scaled_bases": self.vector_as_scaled_bases
        })

    def vector_as_scaled_bases(
        self,
        coords: np.array | List[float],
        run_time: float,
        wait_time: float=0,
        tex_position: int=1,
        **kwargs
    ):
        if isinstance(coords, list):
            coords = np.asarray(coords)
        point = self.space.c2p(coords).flatten()
        pA = point + self.space.c2p(0.5 * RIGHT * tex_position).flatten()
        vA = coords.reshape(-1, 1)
        cA = ManimColor.from_hex("#FFFF00")
        vA = MatrixDrawing(
            vA, pA, elem_color=cA, include_background_rectangle=True,
        )
        self.draw_vectors_on_space(
            coords,
            run_time=run_time,
            wait_time=0.01,
            **kwargs
        )
        self.add(vA.tex)
        self.scale_basei(coords[0], run_time=run_time, wait_time=0.01, **kwargs)
        self.scale_basej(coords[1], run_time=run_time, wait_time=0.01, **kwargs)
        point = self.space.c2p(coords).flatten()
        vec_tex = MathTex(
            r"%s\hat{\textbf{i}} + %s\hat{\textbf{j}}" % (coords[0], coords[1]),
            font_size=30*self.scale,
            color=YELLOW
        ).move_to(
            point + self.space.c2p(1.5 * RIGHT).flatten()
        ).add_background_rectangle()
        run_with_animations = [Write(vec_tex)]
        self.vector_addition(
            [coords[0], 0], [0, coords[1]], run_time=run_time,
            wait_time=0.01, draw_result=True,
            run_with_animations=run_with_animations, **kwargs
        )
        self.basei.become(self.basei_perm)
        self.basej.become(self.basej_perm)
        if hasattr(self, "labeli"):
            self.labeli.become(self.labeli_perm)
            self.labelj.become(self.labelj_perm)
        self.wait(wait_time)
        # point = self.space.c2p(coords).flatten()
        # vector = self.space.ve
        self.remove(vec_tex, vA.tex)
        self.remove_vectors_on_space(coords)
        
    # def show_base_labels(self, run_time: float, wait_time: float=0, **kwargs):
    #     self.add_base_labels()
    #     self.vector_as_scaled_bases(
    #         run_time=run_time, wait_time=0.01, **kwargs
    #     )
    #     point = self.space.c2p(np.array([2, 3])).flatten()
    #     vec_tex = MathTex(
    #         r"2\hat{\textbf{i}} + 3\hat{\textbf{j}}", font_size=24*self.scale
    #     ).next_to(self.space.vectors[tuple(point)], UR)
    #     self.play(Write(vec_tex), run_time=run_time)
    #     self.wait(wait_time)

    # def construct(self):
    #     self.wait()
    #     self.draw_bases(run_time=2, wait_time=1, write_labels=True)
    #     self.vector_as_scaled_bases([2, 3], run_time=2, wait_time=1)
    #     self.vector_as_scaled_bases(
    #         [-3, 1], run_time=2, wait_time=1, tex_position=-1
    #     )
    #     self.draw_span(run_time=2, wait_time=1)
    #     self.draw_line_span(run_time=2, wait_time=1)
        
