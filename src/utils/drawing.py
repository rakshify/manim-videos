import re

from typing import Callable, Generator, List

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
        self.origin = origin
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
        self.transformable_objects = []
        
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
    
    def _a_point_to_vector(self, point: np.array, **kwargs) -> Mobject:
        return Arrow(self.origin, point, **kwargs)
    
    def point_to_vector(self, points: np.array, **kwargs) -> List[Mobject]:
        vectors = []
        for point in points:
            vectors.append(self._a_point_to_vector(point, **kwargs))
        return vectors
    
    def coord_to_vector(self, coords: np.array, **kwargs) -> List[Mobject]:
        if len(coords.shape) == 1:
            coords = coords.reshape(2, -1)
        else:
            coords = coords.transpose()
        points = self.plane.c2p(*coords).transpose()
        return self.point_to_vector(points, **kwargs)
    
    def p2v(self, points: np.array, **kwargs) -> List[Mobject]:
        return self.point_to_vector(points, **kwargs)
    
    def c2v(self, coords: np.array, **kwargs) -> List[Mobject]:
        return self.coord_to_vector(coords, **kwargs)
    
    def add_transformable_objects(self, *mobjects):
        for mob in mobjects:
            if mob not in self.transformable_objects:
                self.transformable_objects.append(mob)
    
    def _apply_transform(self, func: Callable) -> List[Transform]:
        return [
            ApplyPointwiseFunction(func, self.plane),
            *[
                ApplyPointwiseFunction(func, mob) 
                for mob in self.transformable_objects
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
    def __init__(self, matrix: np.array, position: np.array, **kwargs):
        self.matrix = matrix
        self.position = position
        self.draw_self(**kwargs)
        
    def draw_self(self, **kwargs):
        self.tex = matrix_to_tex(self.matrix, **kwargs).move_to(self.position)
        self.tex[0][1:-1].set_color(BLUE)
        
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


