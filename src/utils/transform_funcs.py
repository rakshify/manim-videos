import numpy as np


def mobius_transform(z, a, b, c, d) -> np.array:
    return (a * z + b) / (c * z + d)

def polar(point: np.array) -> np.array:
    x, y = point[0], point[1]
    r = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan(y / x)
    return np.array([r, phi, 0])
        
def rose_petal(z, a, n):
    z = np.exp(z)
    arg = np.arctan(z.imag / z.real) if z.real != 0 else 0 if z.imag == 0 else PI / 2
    mod = np.sqrt(z.real ** 2 + z.imag ** 2)
    return z * (1 + a * np.sin(n * arg) / mod)
