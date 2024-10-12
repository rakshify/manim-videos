import re

from typing import Callable, Generator, Dict, List

from manim import *
import numpy as np


def matrix_to_tex_string(matrix: np.array, bracket: str="bmatrix") -> str:
    matrix = np.array(matrix).astype("str")
    rows = r" \\ ".join([" & ".join(row) for row in matrix])
    
    return r"\begin{%s} %s \end{%s}" % (bracket, rows, bracket)

def matrix_det_to_tex_string(matrix: np.array) -> str:
    return r"Det %s" % (matrix_to_tex_string(matrix, "pmatrix"))

def matrix_multiplication_string(
    A: np.array,
    B: np.array,
    with_braces: bool=True,
    with_dot: bool=True
) -> List[str]:
    A = np.array(A).astype("str")
    B = np.array(B).astype("str")
    
    ra, ca = A.shape
    rb, cb = B.shape
    if ca != rb:
        err = f"Matrix dimensions {A.shape} and {B.shape} do not match"
        raise ValueError(err)
    
    if with_braces:
        if with_dot:
            product = lambda a, b: r"(%s)\cdot(%s)" % (a, b)
        else:
            product = lambda a, b: f"({a})({b})"
    else:
        if with_dot:
            product = lambda a, b: r"%s\cdot%s" % (a, b)
        else:
            product = lambda a, b: f"{a}{b}"
    
    rows = r" \\ ".join([
        " & ".join([
            " + ".join([
                product(A[i][k], B[k][j])
                for k in range(ca)
            ])
            for j in range(cb)
        ]) for i in range(ra)
    ])
    return r"\begin{bmatrix} %s \end{bmatrix}" % rows


def matrix_to_tex(matrix: np.array, **kwargs) -> MathTex:
    return MathTex(matrix_to_tex_string(matrix), **kwargs)

def matrix_mul_question(**kwargs):
    A = np.array([["a", "b"], ["c", "d"]])
    B = np.array([["e", "f"], ["g", "h"]])
    atex = matrix_to_tex_string(A)
    btex = matrix_to_tex_string(B)
    lhs = atex + r"\cdot" + btex
    # lhs_tex = MathTex(lhs)
    rhs = matrix_multiplication_string(A, B, False, False)
    mul = lhs + "=" + rhs
    tex = MathTex(mul, **kwargs)
    # print(len(tex[0]))
    # input("check")
    tex[0][1:5].set_color(YELLOW)
    tex[0][8:12].set_color(BLUE)
    mul_A_idx = np.array([15, 18, 20, 23, 25, 28, 30, 33])
    mul_B_idx = mul_A_idx + 1
    op_idx = [6, 17, 22, 27, 32]
    for i in mul_A_idx:
        tex[0][i].set_color(YELLOW)
    for i in mul_B_idx:
        tex[0][i].set_color(BLUE)
    for i in op_idx:
        tex[0][i].set_color(RED)
    tex[0][13].set_color(GREEN)
    
    return tex


def matrix_det_question(**kwargs):
    A = np.array([["a", "b"], ["c", "d"]])
    tex = matrix_det_to_tex_string(A)
    result = " = ad-bc"
    result = MathTex(tex + result, **kwargs)
    result[0][4].set_color(YELLOW)
    result[0][5].set_color(RED)
    result[0][6].set_color(GREEN)
    result[0][7].set_color(BLUE)
    result[0][10].set_color(YELLOW)
    result[0][13].set_color(RED)
    result[0][14].set_color(GREEN)
    result[0][11].set_color(BLUE)
    return result


class VectorSpace(object):
    def __init__(
        self,
        origin: np.array,
        scale: float,
        x_range: list,
        y_range: list,
        add_coordinates: bool=False,
        **plane_kwargs
    ):
        if origin.shape[0] == 2:
            self.origin = np.zeros(3)
            self.origin[:2] = origin
        else:
            self.origin = origin
        self.scale = scale
        x_length = (x_range[1] - x_range[0]) * scale
        y_length = (y_range[1] - y_range[0]) * scale
        kwargs = {
            "x_range": x_range,
            "x_length": x_length,
            "y_range": y_range,
            "y_length": y_length
        }
        kwargs.update(plane_kwargs)
        
        self.plane = NumberPlane(**kwargs).move_to(self.origin)
        if add_coordinates:
            self.plane = self.plane.add_coordinates()
        
        left = self.plane.x_axis.get_start()
        right = self.plane.x_axis.get_end()
        bot = self.plane.y_axis.get_start()
        top = self.plane.y_axis.get_end()
        window_points = [
            np.array([left[0], top[1], 0]),
            np.array([left[0], bot[1], 0]),
            np.array([right[0], bot[1], 0]),
            np.array([right[0], top[1], 0])
        ]
        self.window = Polygon(*window_points, stroke_width=0.0)
        self.mask_group = [self.window]
        self.vector_points: List[np.array] = []
        self.vectors: Dict[tuple, Arrow] = {}
        self.vector_angles: Dict[tuple, Dict[str, Angle | MathTex]] = {}
        self.transformable_objects: List[Mobject] = []
        
    def set_mask(self, mask_points: List[np.array]):
        self.mask = Polygon(*mask_points, stroke_width=0.0)
        self.shade = Difference(
            self.mask, self.window, color=BLACK, fill_opacity=1.0
        )
        self.mask_group = self.mask_group + [self.mask, self.shade]
        
    def _linear_transform(self, point, matrix):
        dot = np.dot(point - self.origin, matrix)
        return dot + self.origin
    
    def _get_x_shift(self) -> np.array:
        p1 = self.plane.x_axis.number_to_point(self.plane.x_range[0])[0]
        p2 = self.plane.x_axis.number_to_point(self.plane.x_range[0] + 1)[0]
        return p2 - p1
    
    def _get_y_shift(self) -> np.array:
        p1 = self.plane.y_axis.number_to_point(self.plane.y_range[0])[1]
        p2 = self.plane.y_axis.number_to_point(self.plane.y_range[0] + 1)[1]
        return p2 - p1
    
    def get_axis_shift(self, axis: str="x") -> np.array:
        if axis == "x":
            return self._get_x_shift()
        if axis == "y":
            return self._get_y_shift()
        raise ValueError("Axis value can only be either x | y")
    
    def coord_to_point(self, coords: np.array):
        if isinstance(coords, list):
            coords = np.asarray(coords)
        if len(coords.shape) == 1:
            coords = coords.reshape(-1, 1)
        else:
            coords = coords.transpose()
        return self.plane.c2p(*coords).transpose()
    
    def c2p(self, coords: np.array):
        return self.coord_to_point(coords)
    
    def _a_point_to_vector(self, point: np.array, **kwargs) -> Mobject:
        return Arrow(self.origin, point, **kwargs)
    
    def point_to_vector(self, points: np.array, **kwargs) -> List[Mobject]:
        vectors = []
        for point in points:
            vectors.append(self._a_point_to_vector(point, **kwargs))
        return vectors
    
    def coord_to_vector(self, coords: np.array, **kwargs) -> List[Mobject]:
        points = self.coord_to_point(coords)
        return self.point_to_vector(points, **kwargs)
    
    def p2v(self, points: np.array, **kwargs) -> List[Mobject]:
        return self.point_to_vector(points, **kwargs)
    
    def c2v(self, coords: np.array, **kwargs) -> List[Mobject]:
        return self.coord_to_vector(coords, **kwargs)
    
    def add_vector_points(self, *vector_points, **kwargs):
        for point in vector_points:
            tp = tuple(point)
            if tp not in self.vectors:
                self.vector_points.append(tp)
                self.vectors[tp] = self._a_point_to_vector(point, **kwargs)
                
    def add_vector_angles(self, points: np.array, **kwargs):
        for point in points:
            tp = tuple(point)
            # print(tp)
            # print(self.vector_angles)
            # input("check in add vector...")
            if tp not in self.vector_angles:
                angle, angle_label = self.get_vector_angle(point, **kwargs)
                self.vector_angles[tp] = {
                    "angle": angle,
                    "label": angle_label
                }
    
    def update_vector_key(self, old_key, new_key):
        self.vectors[new_key] = self.vectors.pop(old_key)
        self.vector_angles[new_key] = self.vector_angles.pop(old_key)
        self.vector_points.remove(old_key)
        self.vector_points.append(new_key)
        
    def add_vector_to_key(self, key: str, vector: Arrow):
        self.vectors[key] = vector
                
    def get_angle_from_vector(self, vector, **kwargs):
        # Create initial angle indicator
        angle = Angle(
            self.plane.x_axis, 
            vector, 
            radius=0.5 * self.scale,
            **kwargs
        )
        angle_label = MathTex(r"\theta").next_to(
            angle, UR, buff=0.1).scale(0.7 * self.scale)
        return angle, angle_label
    
    def get_vector_angle(self, point: np.array, **kwargs) -> Angle:
        tp = tuple(point)
        # print(tp)
        # print(self.vectors)
        # print(tp not in self.vectors)
        # input("check...")
        if tp not in self.vectors:
            err = (f"Vector {point} not present on space. "
                    "Add it before getting angle")
            raise ValueError(err)
        vector = self.vectors[tp]
        return self.get_angle_from_vector(vector, **kwargs)
    
    def add_transformable_objects(self, *mobjects):
        for mob in mobjects:
            if mob not in self.transformable_objects:
                self.transformable_objects.append(mob)
                
    def remove_all_transformable_objects(self):
        self.transformable_objects = []
                
    def remove_all_vectors(self):
        self.vector_points = []
        self.vectors = {}
        self.vector_angles = {}
        
    def remove_vectors(self, points: np.array):
        for point in points:
            tp = tuple(point)
            if tp in self.vectors:
                self.vector_points.remove(tp)
                self.vectors.pop(tp)
            if tp in self.vector_angles:
                self.vector_angles.pop(tp)
    
    def _apply_transform(self, func: Callable) -> List[Transform]:
        return [
            ApplyPointwiseFunction(func, self.plane),
            *[
                ApplyPointwiseFunction(func, mob) 
                for mob in self.transformable_objects
            ],
            *[
                ApplyPointwiseFunction(func, vector) 
                for vector in self.vectors.values()
            ]
        ]
        
    def apply_linear_transform(
        self, 
        matrix: np.array
    ) -> List[Transform]:
        if matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = matrix
            matrix = new_matrix
        func = lambda point: self._linear_transform(point, matrix)
        return self._apply_transform(func)


class MatrixDrawing(object):
    def __init__(
        self,
        matrix: np.array,
        position: np.array,
        elem_color=BLUE,
        elem_range=[1, -1],
        include_background_rectangle: bool=False,
        **kwargs
    ):
        self.matrix = matrix
        self.position = position
        self.include_background_rectangle = include_background_rectangle
        self.draw_self(elem_color, elem_range, **kwargs)
        
    def move_to(self, position: np.array):
        self.tex.move_to(position)
        
    def draw_self(self, elem_color=BLUE, elem_range=[1, -1], **kwargs):
        self.tex = matrix_to_tex(self.matrix, **kwargs).move_to(self.position)
        self.tex[0][elem_range[0]:elem_range[1]].set_color(elem_color)
        if self.include_background_rectangle:
            self.tex.add_background_rectangle()
        
    def linear_transform(self, vector: np.array, **kwargs) -> Generator:
        if len(vector.shape) == 1:
            vector = vector.reshape(-1, 1)
        
        vtex = matrix_to_tex_string(vector)
        mul_tex = MathTex(r" \cdot " + vtex, **kwargs).next_to(self.tex, RIGHT)
        mul_tex[0][2:-1].set_color(YELLOW)
        mul_tex[0][0].set_color(RED)
        yield mul_tex
        
        try:
            result = np.dot(self.matrix, vector)
        except ValueError:
            # Case of string values (linear equations) hard code value
            # TODO: change needed
            result = np.array([3, 0])
        result = matrix_to_tex_string(result)
        tex = MathTex(" = " + result, **kwargs).next_to(mul_tex, RIGHT)
        tex[0][2:-1].set_color(GREEN)
        yield tex

# # ffmpeg -i media/videos/numbers/480p15/GraphUniverseScene.mp4 -i numbers_graph_universe.mp3 -shortest -c copy -map 0:v:0 -map 1:a:0 output.mp4
# # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4


