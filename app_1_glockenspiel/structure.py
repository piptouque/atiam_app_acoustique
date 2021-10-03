
import numpy as np

from typing import List, Callable, Union


class BarShape:
    def __init__(self, l: float, h: float, b: float, s: Union[float, Callable[float]]):
        self.l = l
        self.h = h
        self.b = b

        # section
        self.s = s
        # self.s = b * h
        # Moment d'inertie $I$
        self.i = self.b * self.h**3 / 12

    def is_section_constant(self) -> bool:
        return not callable(self.s)


class MalletShape:
    def __init__(self, radius: float):
        self.r = radius


class Material:
    # region Data
    """
    Masses volumiques , en kg.m-3
    voir : https://www.sodielec-berger.fr/files/40/fiche-densite-materiaux.pdf
    """
    rhos = {
        'steel': 8010,
        'wood': 300
    }
    """
    Modules d'Young des matériaux du glockenspiel en $GPa$.
    """
    es = {
        'steel': 203,
        'brass': 90,
        'wood': 10,
        'rubber': 0.01
    }
    """
    Coefficients de Poisson $\nu$, sans unité.
    Pour le bois, dépend de l'orientation (anisotrope),
    j'ai pris ici une valeur pour du bois à basse densité (?), en radial.
    voir : https://www.sonelastic.com/en/fundamentals/tables-of-materials-properties/woods.html
    """
    nus = {
        'steel': 0.3,
        'brass': 0.33,
        'rubber': 0.30,
        'wood': 0.25
    }
    """[summary]
    Coefficients de dilatation thermique $\alpha$, en $K^{-1}$
    """
    alphas = {
        'steel': 8 * 10 ^ -6,
        'wood': 4 * 10 ^ -6
    }
    """
    Chaleurs spécifiques à déformation constante, en $J.kg^{-1}.K$
    """
    cs = {
        'steel': 500,
        'wood': 2000,
    }
    """
    Conductivités thermiques, en $W.m^{-1}.K^{-1}$
    """
    kappas = {
        'steel': 25,
        'wood': 0.2
    }
    """[summary]
    Rayon de courbure de la tête sphérique de la baguette, en m.
    Mis un peu au hasard..
    """
    rs = {
        'steel': 10,
        'wood': 1,
        'rubber': 0.2
    }
    # endregion

    def __init__(self, e: float, rho: float, nu: float, alpha: float, kappa: float, c: float):
        self.e = e
        self.rho = rho
        self.nu = nu
        self.alpha = alpha
        self.kappa = kappa
        self.c = c

        self.phi = self.alpha * self.e / (1 - 2 * self.nu)

    @classmethod
    def make(cls, name: str):
        return cls(
            cls.es[name],
            cls.rhos[name],
            cls.nus[name],
            cls.alphas[name],
            cls.kappas[name],
            cls.cs[name])


class Constraint:
    def __init__(self, x: float, name: str):
        self.x = x
        self.name = name


class Bar:
    def __init__(self, shape: BarShape, mat: Material):
        self.shape = shape
        self.mat = mat

    def get_mass(self):
        if self.shape.is_section_constant():
            return self.mat.rho * self.shape.l * self.shape.s
        else:
            return NotImplemented


class Mallet:
    def __init__(self, shape: MalletShape, mat: Material):
        self.shape = shape
        self.mat = mat

    def get_mass(self):
        # On néglige la masse du manche devant celui de la tête.
        return self.mat.rho * 1.25 * np.pi * np.power(self.shape.r, 3)
