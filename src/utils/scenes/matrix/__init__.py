import numpy as np

from manim import *

from src.utils.drawing import VectorSpace, MatrixDrawing
from src.utils.scenes.matrix.CONSTANTS import *

class MatrixGeometryScene(Scene):
    def setup_geometry(
        self,
        origin: np.array=ORIGIN,
        scale: float=1.0,
        x_range: list=[-4, 4, 1],
        y_range: list=[-4, 4, 1],
        mask_points: list=EXAMPLE_MASK,
        add_bases: bool=True
    ):
        # Axes range and length
        self.scale = scale
        
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
            self.add_vectors_on_space(np.array([1, 0]), color=GREEN)
            self.add_vectors_on_space(np.array([0, 1]), color=RED)
        
    def _add_vectors_on_space(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        **kwargs
    ):
        vkwargs = {
            "color": YELLOW,
            "buff": 0.0,
            "max_stroke_width_to_length_ratio": 5*self.scale,
            "max_tip_length_to_length_ratio": self.scale/4
        }
        vkwargs.update(kwargs)
        vectors = self.space.c2v(coords, **vkwargs)
        self.space.add_transformable_objects(*vectors)
        return vectors
        
    def add_vectors_on_space(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        **kwargs
    ):
        vectors = self._add_vectors_on_space(coords, **kwargs)
        self.add(*vectors)
        
    def draw_vectors_on_space(
        self,
        coords: np.array=EXAMPLE_VECTORS,
        **kwargs
    ):
        vectors = self._add_vectors_on_space(coords, **kwargs)
        self.play(*[GrowArrow(v) for v in vectors])
        self.wait()

    def transform_space(
        self,
        transform_matrix: np.array=EXAMPLE_MATRIX,
        **kwargs
    ):
        self.play(
            *(self.space.apply_linear_transform(transform_matrix)),
            **kwargs
        )
        self.wait()
        
    def matrix_determinant(self):
        c1 = self.space.plane.plot(lambda x: 1, x_range=[0, 1])
        c2 = self.space.plane.plot(lambda x: 0, x_range=[0, 1])
        area = self.space.plane.get_area(
            c2, [0, 1], bounded_graph=c1, color=YELLOW, opacity=0.5
        )
        self.add(area)
        self.wait(2)
        

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

