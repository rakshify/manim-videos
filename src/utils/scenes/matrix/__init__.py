from typing import List

import numpy as np

from manim import *

from src.utils.drawing import VectorSpace, MatrixDrawing
from src.utils.scenes.matrix.CONSTANTS import *
from src.utils.scenes.voiced_scene import VoicedScene

class MatrixGeometryScene(VoicedScene):
    name = "matrix_geometry_scene"

    def __init__(
        self,
        origin: np.array=ORIGIN,
        scale: float=EXAMPLE_SCALE,
        x_range: list=EXAMPLE_AXIS_RANGE,
        y_range: list=EXAMPLE_YAXIS_RANGE,
        mask_points: list=EXAMPLE_MASK,
        add_bases: bool=False,
        add_base_labels: bool=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setup_geometry(
            origin=origin,
            scale=scale,
            x_range=x_range,
            y_range=y_range,
            mask_points=mask_points,
            add_bases=add_bases,
            add_base_labels=add_base_labels
        )
        self.animation_map.update({
            "draw_vector_braces": self.draw_vector_braces,
            "draw_vector_angles": self.draw_vector_angles,
            "draw_bases": self.draw_bases,
            "draw_vectors_on_space": self.draw_vectors_on_space,
            "draw_vector_angles": self.draw_vector_angles,
            "scale_vector": self.scale_vector,
            "scale_basei": self.scale_basei,
            "scale_basej": self.scale_basej,
            "basei_walk": self.basei_walk,
            "basej_walk": self.basej_walk,
            "bases_walk": self.bases_walk,
            "shift_vector": self.shift_vector,
            "vector_addition": self.vector_addition,
            "transform_space": self.transform_space,
            "draw_span": self.draw_span,
            "draw_line_span": self.draw_line_span,
        })

    def setup_geometry(
        self,
        origin: np.array=ORIGIN,
        scale: float=1.0,
        x_range: list=EXAMPLE_AXIS_RANGE,
        y_range: list=EXAMPLE_AXIS_RANGE,
        mask_points: list=EXAMPLE_MASK,
        add_bases: bool=False,
        add_base_labels: bool=False,
    ):
        # Axes range and length
        self.scale = scale
        self.x_range = x_range
        self.y_range = y_range
        
        # Set space
        self.space = VectorSpace(
            origin, self.scale, x_range, y_range
        )
        # Set mask
        self.space.set_mask(mask_points)
        
        # Add space to scene
        self.add(self.space.plane)
        self.add(*(self.space.mask_group))
        
        if add_bases:
            point = self.space.c2p(np.array([1, 0])).flatten()
            self.add_vectors_on_space(np.array([1, 0]), color=GREEN)
            self.basei = self.space.vectors[tuple(point)]
            self.basei_perm = self.basei.copy()
            point = self.space.c2p(np.array([0, 1])).flatten()
            self.add_vectors_on_space(np.array([0, 1]), color=RED)
            self.basej = self.space.vectors[tuple(point)]
            self.basej_perm = self.basej.copy()
            if add_base_labels:
                self.add_base_labels()
                
    def _create_basis_labels(self):
        self.labeli = MathTex(
            r"\hat{\textbf{i}}", font_size=24*self.scale, color=GREEN
        ).next_to(self.basei, 0.5 * self.scale * DOWN)
        self.labelj = MathTex(
            r"\hat{\textbf{j}}", font_size=24*self.scale, color=RED
        ).next_to(self.basej, 0.5 * self.scale * LEFT)
        self.labeli_perm = self.labeli.copy()
        self.labelj_perm = self.labelj.copy()
            
    def add_base_labels(self):
        if hasattr(self, 'labeli'):
            return
        self._create_basis_labels()
        self.add(self.labeli, self.labelj)
        
    def _add_vectors_on_space(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        colors: list | None=None,
        **kwargs
    ):
        vkwargs = {
            "buff": 0.0,
            "max_stroke_width_to_length_ratio": 5*self.scale,
            "max_tip_length_to_length_ratio": self.scale/4
        }
        color = kwargs.pop('color', YELLOW)
        vkwargs.update(kwargs)
        vector_points = self.space.c2p(coords)
        
        if colors is None:
            self.space.add_vector_points(
                *vector_points, color=color, **vkwargs
            )
        else:
            for point, color in zip(vector_points, colors):
                if isinstance(color, str):
                    color = ManimColor.from_hex(color)
                self.space.add_vector_points(point, color=color, **vkwargs)
        return vector_points
    
    def remove_all_vectors(self):
        self.play(
            *[FadeOut(mob) for mob in self.space.vectors.values()],
            *[
                FadeOut(mob["angle"]) 
                for mob in self.space.vector_angles.values()
            ],
            *[
                FadeOut(mob["label"]) 
                for mob in self.space.vector_angles.values()
            ]
        )
        self.space.remove_all_vectors()
        
    def _get_vector_from_coords(self, coords: np.array) -> List[Arrow]:
        vector_points = self.space.c2p(coords)
        vectors = []
        for point in vector_points:
            tp = tuple(point)
            if tp not in self.space.vectors:
                self.space.add_vector_points(point)
            vectors.append(self.space.vectors[tp])
        return vectors
        
    def remove_vectors_on_space(self, coords: np.array):
        vector_points = self.space.c2p(coords)
        self.play(
            *[
                FadeOut(self.space.vectors[tuple(point)]) 
                for point in vector_points
            ]
        )
        self.space.remove_vectors(vector_points)
        
    def add_vectors_on_space(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        **kwargs
    ):
        vector_points = self._add_vectors_on_space(coords, **kwargs)
        self.add(*[self.space.vectors[tuple(point)] for point in vector_points])
        
    def draw_vector_braces(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        run_time: float=1,
        wait_time: float=1,
        **kwargs
    ):
        points = self.space.c2p(coords)
        braces = VGroup()
        for point in points:
            mat = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
            normal = np.dot(mat, point)
            vector = self.space.vectors[tuple(point)]
            br = Brace(vector, direction=normal-self.space.origin, **kwargs)
            braces.add(br)
        self.play(Create(braces), run_time=run_time)
        self.wait(wait_time)
        return braces
        
    def draw_vector_angles(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        run_time: float=1,
        wait_time: float=1,
        **kwargs
    ):
        vector_points = self.space.c2p(coords)
        self.space.add_vector_angles(vector_points, **kwargs)
        angles, labels = [], []
        for point in vector_points:
            tp = tuple(point)
            angle = self.space.vector_angles[tp]
            angles.append(angle["angle"])
            labels.append(angle["label"])
        self.play(*[Create(mob) for mob in angles + labels], run_time=run_time)
        self.wait(wait_time)
            
    def draw_bases(
        self,
        run_time: float=1,
        wait_time: float=1,
        write_labels: bool=False,
        **kwargs
    ):
        if hasattr(self, 'basei'):
            return
        
        coords = np.array([1, 0])
        self.draw_vectors_on_space(
            coords=coords,
            run_time=run_time,
            wait_time=0.01,
            color=GREEN,
            **kwargs
        )
        point = self.space.c2p(coords).flatten()
        self.basei = self.space.vectors[tuple(point)]
        self.basei_perm = self.basei.copy()
        coords = np.array([0, 1])
        self.draw_vectors_on_space(
            coords=coords,
            run_time=run_time,
            wait_time=0.01,
            color=RED,
            **kwargs
        )
        point = self.space.c2p(coords).flatten()
        self.basej = self.space.vectors[tuple(point)]
        self.basej_perm = self.basej.copy()
        if write_labels:
            self._create_basis_labels()
            self.play(
                Write(self.labeli), Write(self.labelj), run_time=run_time
            )
        self.wait(wait_time)
        
    def draw_vectors_on_space(
        self,
        coords: np.array | List[float]=EXAMPLE_VECTORS,
        run_time: float=1,
        wait_time: float=1,
        colors: list | None=None,
        run_with_animations: List[Animation]=[],
        **kwargs
    ):
        if isinstance(coords, list):
            coords = np.asarray(coords)
        # vectors = self._add_vectors_on_space(coords, **kwargs)
        vector_points = self._add_vectors_on_space(
            coords, colors=colors, **kwargs
        )
        self.play(
            *[
                GrowArrow(self.space.vectors[tuple(point)]) 
                for point in vector_points
            ],
            *run_with_animations,
            run_time=run_time
        )
        self.wait(wait_time)

    def scale_vector(
        self,
        coord: np.array,
        scale: float,
        run_time: float,
        wait_time: float=0,
        base_label_animations: List[Animation]=[],
        **kwargs
    ):
        point = self.space.c2p(coord).flatten()
        vector = self.space.vectors[tuple(point)]
        scaled_point = self.space.c2p(coord * scale).flatten()
        nv = vector.copy().put_start_and_end_on(
            self.space.origin, scaled_point
        )
        animations = [vector.animate.become(nv)]
        # print(base_label_animations)
        # input("check")
        if base_label_animations:
            # input("satisfied")
            animations += base_label_animations
        self.play(
            *animations,
            run_time=run_time
        )
        self.wait(wait_time)
        self.space.add_vector_to_key(tuple(scaled_point), vector)
    
    def scale_basei(
        self,
        scale: float,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        if hasattr(self, 'labeli'):
            pos = self.labeli.get_center() + (scale - 1) * RIGHT
            nl = MathTex(
                r"%s\hat{\textbf{i}}" % scale, font_size=24*self.scale,
                color=GREEN
            ).move_to(pos)
            label_animations = [
                # self.labeli.animate.shift((scale - 1) * RIGHT),
                self.labeli.animate.become(nl)
            ]
        else:
            label_animations = []
        self.scale_vector(
            np.array([1, 0]), scale, run_time, wait_time,
            base_label_animations=label_animations, **kwargs
        )
        # if hasattr(self, 'labeli'):
        #     self.labeli.tex_string = r"%s\hat{\textbf{i}}" % scale
        #     self.labeli.shift((scale - 1) * RIGHT)
    
    def scale_basej(
        self,
        scale: float,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        if hasattr(self, 'labelj'):
            pos = self.labelj.get_center() + (scale - 1) * UP
            nl = MathTex(
                r"%s\hat{\textbf{j}}" % scale, font_size=24*self.scale,
                color=RED
            ).move_to(pos)
            label_animations = [
                self.labelj.animate.become(nl)
            ]
        else:
            label_animations = []
        self.scale_vector(
            np.array([0, 1]), scale, run_time, wait_time,
            base_label_animations=label_animations, **kwargs
        )
        # if hasattr(self, 'labelj'):
        #     self.labelj.tex_string = r"%s\hat{\textbf{j}}" % scale

    def _base_walk(
        self,
        base_idx,
        start: np.array,
        coords: np.array,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        end = start.copy()
        point = self.space.c2p(coords).flatten()
        end[base_idx] = point[base_idx]
        # print(start)
        # print(end)
        # input("check")
        line = Line(start, end, **kwargs)
        self.play(GrowFromPoint(line, start), run_time=run_time)
        self.wait(wait_time)
        return line
    
    def basei_walk(
        self,
        start: np.array,
        coords: np.array,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        return self._base_walk(
            0, start, coords, run_time, wait_time, color=GREEN, **kwargs
        )
    
    def basej_walk(
        self,
        start: np.array,
        coords: np.array,
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        return self._base_walk(
            1, start, coords, run_time, wait_time, color=RED, **kwargs
        )
    
    def bases_walk(
        self,
        coords: np.array,
        run_time: float,
        wait_time: float=0,
        start: np.array=None,
        remove_walk_lines_after: bool=True,
        **kwargs
    ):
        if start is None:
            start = self.space.origin
        if isinstance(start, list):
            start = np.array(start)
        if start.shape[0] == 2:
            zeros = np.zeros(3)
            zeros[:2] = start
            start = zeros
        x = self.basei_walk(start, coords, run_time, wait_time=0.01, **kwargs)
        start = x.get_end()
        y = self.basej_walk(start, coords, run_time, wait_time=0.01, **kwargs)
        self.wait(wait_time)
        if remove_walk_lines_after:
            self.remove(x, y)
            self.remove_pending_base_walks()
        else:
            if not hasattr(self, 'pending_base_walks'):
                self.pending_base_walks = []
            self.pending_base_walks += [x, y]
    
    def remove_pending_base_walks(self):
        if hasattr(self, 'pending_base_walks'):
            self.remove(*(self.pending_base_walks))
            self.pending_base_walks = []

    def shift_vector(
        self,
        coord: np.array | List[float],
        shift_to: np.array | List[float],
        run_time: float,
        wait_time: float=0,
        **kwargs
    ):
        point = self.space.c2p(coord).flatten()
        vector_to_move = self.space.vectors[tuple(point)]
        shift_to = self.space.c2p(shift_to).flatten()
        shift = shift_to[0] * RIGHT + shift_to[1] * UP
        self.play(
            vector_to_move.animate.shift(shift), run_time=run_time, **kwargs
        )
        self.wait(wait_time)
        return shift
        
    def vector_addition(
        self,
        vA: np.array | List[float],
        vB: np.array | List[float],
        vector_to_move: int=1,
        draw_result: bool=True,
        wait_time: float=0,
        **kwargs
    ):
        if isinstance(vA, list):
            vA = np.asarray(vA)
        if isinstance(vB, list):
            vB = np.asarray(vB)
        if vector_to_move == 1:
            point = self.space.c2p(vB).flatten()
            other = self.space.c2p(vA).flatten()
        else:
            point = self.space.c2p(vA).flatten()
            other = self.space.c2p(vB).flatten()
        vector_to_move = self.space.vectors[tuple(point)]
        shift = other[0] * RIGHT + other[1] * UP
        self.play(
            vector_to_move.animate.shift(shift), **kwargs
        )
        if draw_result:
            result = vA + vB
            run_time = kwargs.pop('run_time', 1)
            self.draw_vectors_on_space(
                result,
                run_time=run_time,
                wait_time=wait_time,
                color=GREEN,
                **kwargs
            )
        vector_to_move.shift(-shift)

    def transform_space(
        self,
        transform_matrix: np.array=EXAMPLE_MATRIX,
        wait_time: float=1,
        **kwargs
    ):
        self.play(
            *(self.space.apply_linear_transform(transform_matrix)),
            **kwargs
        )
        self.wait(wait_time)
        
    def matrix_determinant(self):
        c1 = self.space.plane.plot(lambda x: 1, x_range=[0, 1])
        c2 = self.space.plane.plot(lambda x: 0, x_range=[0, 1])
        area = self.space.plane.get_area(
            c2, [0, 1], bounded_graph=c1, color=YELLOW, opacity=0.5
        )
        self.add(area)
        self.wait(2)

    def draw_span(self, run_time: float, wait_time: float=0, **kwargs):
        x_min, x_max, _ = self.x_range
        y_min, y_max, _ = self.y_range
        lx = (x_max - x_min) * 2
        blue = np.array([0, 0, 255])
        green = np.array([0, 255, 0])
        red = np.array([255, 0, 0])
        span = VGroup()
        for k in range(lx + 1):
            i = x_min + k / 2
            val = min(1, (2 * k) / lx)
            val2 = max(0, (2 * k) / lx - 1)
            color = blue + val * (green - blue) + val2 * (red - green)
            color = ManimColor.from_rgb(color.astype(int))
            for j in range(y_min, y_max + 1):
                coord = np.array([i, j])
                point = self.space.c2p(coord).flatten()
                vkwargs = {
                    "buff": 0.0,
                    "max_stroke_width_to_length_ratio": 5*self.scale,
                    "max_tip_length_to_length_ratio": self.scale/4,
                    "color": color
                }
                vec = Arrow(self.space.origin, point, **vkwargs)
                span.add(vec)
        self.play(Create(span), run_time=run_time)
        self.wait(wait_time)
        self.remove(span)
        
    def draw_line_span(self, run_time: float, wait_time: float=0, **kwargs):
        coords = np.array([[3.5, 2], [-1.75, -1]])
        colors = ["#FFFF00", "#800080"]
        p1 = self.space.c2p(np.array([-7, -4])).flatten()
        p2 = self.space.c2p(np.array([7, 4])).flatten()
        line = Line(p1, p2)
        self.add(line)
        self.play(
            self.basei.animate.rotate(np.arctan(4/7)),
            self.basej.animate.rotate(PI/2 + np.arctan(4/7)),
            run_time=run_time
        )
        # self.draw_vectors_on_space(
        #     coords=coords,
        #     colors=colors,
        #     run_time=run_time,
        #     wait_time=0.01,
        #     **kwargs
        # )
        self.remove(line)
        self.remove_all_vectors()
        x_min, x_max, _ = self.x_range
        lx = (x_max - x_min) * 2
        blue = np.array([0, 0, 255])
        green = np.array([0, 255, 0])
        red = np.array([255, 0, 0])
        span = VGroup()
        for k in range(lx + 1):
            i = x_min + k / 2
            val = min(1, (2 * k) / lx)
            val2 = max(0, (2 * k) / lx - 1)
            color = blue + val * (green - blue) + val2 * (red - green)
            color = ManimColor.from_rgb(color.astype(int))
            coord = np.array([i, (i * 4) / 7])
            point = self.space.c2p(coord).flatten()
            vkwargs = {
                "buff": 0.0,
                "max_stroke_width_to_length_ratio": 5*self.scale,
                "max_tip_length_to_length_ratio": self.scale/4,
                "color": color
            }
            vec = Arrow(self.space.origin, point, **vkwargs)
            span.add(vec)
        self.play(Create(span), run_time=run_time)
        self.wait(wait_time)
        self.remove(span)
        

    # Define the animation function
    def vector_alpha_movement_along_path(
        self,
        path_func,
        vector,
        alpha,
        path_start,
        **kwargs
    ):
        curr_angle = self.space.vector_angles[tuple(path_start)]
        # Calculate new end point
        end_point = path_func(alpha)

        # Update vector (from origin to end_point)
        vector.put_start_and_end_on(self.space.origin, end_point)

        # Calculate the angle
        angle_value = np.arctan2(end_point[1], end_point[0])

        # Determine if we should use the other angle (for smooth transitions)
        use_other_angle = angle_value < 0
        new_angle, new_label = self.space.get_angle_from_vector(
            vector, other_angle=use_other_angle, **kwargs
        )
        
        # Add new angle
        self.add(new_angle)

        # Update angle label position and value
        angle_display = angle_value \
                            if not use_other_angle \
                            else 2*np.pi + angle_value
        curr_angle["label"].become(MathTex(
            f"{(angle_display * (180 / np.pi)):.2f}" + r"^{\circ}"
        ).scale(0.7 * self.scale))
        curr_angle["label"].next_to(new_angle, UR, buff=0.1)
        curr_angle["angle"] = new_angle
        

class MatrixNumericalScene(Scene):
    def setup_numerical(
        self,
        matrix: np.array=EXAMPLE_MATRIX.T,
        vectors: np.array=EXAMPLE_VECTORS,
        position: np.array=ORIGIN,
        **kwargs
    ):
        self.matrix = MatrixDrawing(matrix, position, **kwargs)
        self.vectors = vectors
        self.play(Write(self.matrix.tex))
        self.wait()

