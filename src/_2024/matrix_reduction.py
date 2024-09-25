import re

import numpy as np

from manim import *


def matrix_to_tex_string(matrix: np.array, highlight: bool=False) -> str:
    matrix = np.array(matrix).astype("str")
    if highlight:
        rows = r" \\ ".join([
            " & ".join([r"{{%s}}" % item for item in row])
            for row in matrix
        ])
    else:
        rows = r" \\ ".join([" & ".join(row) for row in matrix])
    
    return r"\begin{bmatrix} %s \end{bmatrix}" % rows

class MatrixExampleScene(Scene):
    def construct(self):
        A = np.array([[r"a1", "b", "e"], ["c", "d", "f23"], ["ge", "h123", "imn"]])
        
        # If I set the highlight attribute to false and comment out 
        # the 4 "set_color" lines, the code works fine and writes a 
        # matrix in white color on the screen
        atex = matrix_to_tex_string(A)
        tex = MathTex(atex, font_size=72)
        # idx = tex.index_of_part_by_tex(r"a1\cdot e")
        # idx2 = tex.index_of_part_by_tex(r"\cdot e")
        # idx3 = tex.index_of_part_by_tex(r"e")
        idx = tex.index_of_part_by_tex(r"a1")
        
        pattern = re.compile(r"(\\begin\{bmatrix\} )((((\w+) \& )+(\w+) \\\\ )+(((\w+) \& )+(\w+)))( \\end\{bmatrix\})")
        m = re.search(pattern, atex)
        print(atex)
        if m:
            print(m.groups())
            print(len(m.groups()))
            print(m.groups(0))
        # print(idx, idx2, idx3)
        print(idx)
        input("check")
        self.add(index_labels(tex[0]).set_color(RED))
        tex[0][1].set_color(YELLOW)
        tex[0][2].set_color(BLUE)
        tex[0][3].set_color(GREEN)
        tex[0][4].set_color(RED)
        self.play(Write(tex))
        self.wait()



# def setup_space() -> tuple:
#     pass


# def create_matrix(matrix: np.array | list) -> "MatrixDrawing":
#     pass


# class MatrixReductionIntroScene(Scene):
#     def construct(self):
#         pass
    

# class PlaneScene(Scene):
#     def construct(self):
#         pass
    
    
# class PlanarImpactScene(Scene):
#     def construct(self):
#         pass
    
    
# class MatrixReductionIndependentScene(Scene):
#     def construct(self):
#         pass
    
    
# class MatrixReductionDependentScene(Scene):
#     def construct(self):
#         pass
    
    
# class MatrixReductionInconsistentScene(Scene):
#     def construct(self):
#         pass