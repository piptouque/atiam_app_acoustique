
import numpy as np

from typing import List, Callable, Union


class BarShape:
    def __init__(self, l: float, h: float, b: float, s: Union[float, Callable[[float], float]]):
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


class CylinderShape:
    def __init__(self, l: float, d: float):
        self.l = l
        self.d = d
        self.s = np.pi * d**2/4
        self.i = np.pi * d**4/64


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
        'wood': 300,
        'brass': 8960,
        'air': 1.204,  # à 20°C, à la pression atmosphérique usuelle.
    }
    """
    Modules d'Young des matériaux du glockenspiel en $Pa$.
    """
    es = {
        'steel': 203 * 10**9,
        'brass': 90 * 10**9,
        'wood': 10 * 10**9,
        'rubber': 0.01 * 10**9
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
        'steel': 8 * 10 ** -6,
        'wood': 4 * 10 ** -6,
        'brass': 6 * 10 ** -6,  #  à vérifier
    }
    """
    Chaleurs spécifiques à déformation constante, en $J.kg^{-1}.K$
    """
    cs = {
        'steel': 500,
        'wood': 2000,
        'brass': 400  #  à vérifier
    }
    """
    """
    etas = {
        'air': 1.55 * 10 ** -5
    }
    """
    Conductivités thermiques, en $W.m^{-1}.K^{-1}$
    """
    kappas = {
        'steel': 25,
        'wood': 0.2,
        'brass': 20,  #  à vérifier
    }
    """[summary]
    Rayon de courbure de la tête sphérique de la baguette, en m.
    Mis un peu au hasard..
    """
    rs = {
        'steel': 10,
        'wood': 1,
        'rubber': 0.2,
        'brass': 20  #  à vérifier
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


class StringSetting:
    def __init__(self, tau: float, boundaries: str, env: str):
        self.tau = tau
        self.boundaries = boundaries
        self.env = env


class StringPinch:
    def __init__(self, x_p: float, h: float):
        self.x_p = x_p
        self.h = h


class String:
    def __init__(self, shape: CylinderShape, mat: Material):
        self.shape = shape
        self.mat = mat

    def compute_transversal_eigenmodes(self, setting: StringSetting, pinch: StringPinch) -> Callable[[int], Callable[[float, float], float]]:
        """[summary]

        Args:
            n (int): number of modes to compute.

        Returns:
            [type]: the $\omega_n$ series of eigen pulses.
        """
        self.setting = setting
        self.pinch = pinch

        self.c = np.sqrt(self.setting.tau / (self.mat.rho * self.shape.s))
        self.kappa = np.sqrt(self.setting.tau / (self.mat.e * self.shape.i))
        #
        boundaries = self.setting.boundaries
        self.k_n = None
        self.omega_n = None
        self.coefs = [lambda n: 0] * 4
        self.phi_n = None
        if boundaries == 'simply-supported':
            self.k_n = lambda n: np.pi * n / self.shape.l
            # self.omega_n = lambda n: self.c * \ self.k_n(n) * np.sqrt(1 + (n * np.pi / (self.kappa * self.shape.l))**2)
            # shitty approximation of R the mecanical resistance in both the low and high frequency domains.
            #
            self.phi_n = lambda n: 0

            def r(n):
                # first-ordre approximation on omega_n
                omega = n * np.pi * self.c / self.shape.l
                eta = 2000 * Material.etas[self.setting.env]
                return 2 * np.pi * (eta / (1 + omega**2) + self.shape.d * np.sqrt(omega/2 * eta * Material.rhos[self.setting.env]))
            # Let's be in the low frequency domain and say that:
            # We dismiss the term on Y_ch
            self.omega_n = lambda n: self.k_n(n) * self.c * (1 + self.k_n(n)**2/(
                2*self.kappa**2) - 1j * r(n) * self.shape.l / (2 * np.pi * self.shape.s * self.mat.rho * self.c * n))

            def d_n(n):
                return 2 * self.pinch.h * self.shape.l ** 2 * np.sin(self.k_n(n) * self.pinch.x_p) / ((n * np.pi) ** 2 * self.pinch.x_p * (self.shape.l - self.pinch.x_p))
            self.coefs[3] = d_n
        else:
            return NotImplementedError()
        self.q_n = lambda n: np.sqrt(self.k_n(n)**2 + self.kappa**2)
        self.y_n = lambda n: lambda x, t: np.cos(self.omega_n(n)*t + self.phi_n(n)) \
            * ((self.coefs[0](n)*np.cosh(self.q_n(n)*x)
                + self.coefs[1](n)*np.sinh(self.q_n(n)*x)
                + self.coefs[2](n)*np.cos(self.k_n(n)*x)
                + self.coefs[3](n)*np.sin(self.k_n(n)*x)))
        return self.y_n
