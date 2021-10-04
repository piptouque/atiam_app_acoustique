
import numpy as np

from structure import Bar, Constraint, Mallet

from typing import Callable, Tuple, List


class Damping:
    """[summary]
    Renvoie les coefficients complexes d'amortissement thermoélastique.
    """
    @staticmethod
    def get_damped_ds(ds: np.ndarray, bar: Bar, temp_0: float) -> np.ndarray:
        rs = get_rs(ds, bar.mat, temp_0)
        tau = bar.mat.rho * bar.mat.c * \
            bar.shape.h ** 2 / (bar.mat.kappa * np.pi ** 2)
        ksi = 8 * temp_0 * bar.shape.h ** 2 / \
            (bar.mat.kappa * np.power(np.pi, 6))
        mult = np.array([1, 2, 1, 0])
        ds_tilde = np.empty(len(ds), dtype=Callable[[float], float])
        for i in range(len(ds)):
            ds_tilde[i] = lambda s: ds[i] + mult[i] * \
                bar.mat.phi ** 2 * s * ksi / (1 + tau * s)
        return ds_tilde


class TransversalVibration:

    @ classmethod
    def get_free_vibration(cls, bar: Bar, cs: List[Constraint]) -> Callable[[float], float]:
        def k(omega): return np.sqrt(
            omega) * np.power(bar.mat.rho * bar.shape.s / (bar.mat.e * bar.mat.i), 1/4)
        phi = cls.__spatial_constant(bar, cs) if bar.shape.is_section_constant(
        ) else cls.__spatial_variable(bar, cs)
        pass  # todo

    """[summary]
    Returns:
        [type]: [description]
    """
    @ classmethod
    def __spatial_constant(cls, bar: Bar, cs: Tuple[Constraint, Constraint]) -> Tuple[np.ndarray, Callable[[int], float]]:
        couple = Constraint.couples[cs]
        if couple == 'free-free':
            pass
        if couple == 'free-clamped':
            ds = np.array([1, 1, 0, 0])

            def w_n_1(n):
                return ((2 * n + 1) * np.pi) ** 2 / \
                    (4 * bar.shape.l * np.sqrt(bar.mat.e *
                                               bar.shape.i / (bar.mat.rho * bar.shape.s)))
            return (ds, w_n)
        if couple == 'supported-supported':
            # même distance au bord le plus proche pour les positions des conditions limites
            # assert(couple[0].x + couple[1].x == 2)
            # advancement= couple[0].x
            # ne fonctionne pas pour avancement != 0...
            ds = np.array([0, 0, 1, 0])

            def w_n_1(n):
                return (np.pi * (2 * n + 1) / (2 * bar.shape.l)) ** 2 * np.sqrt(bar.mat.e * bar.shape.i / (bar.mat.rho * bar.shape.s))
            return (ds, w_n)

    @ classmethod
    def __spatial_variable(cls, bar: Bar, cs: Tuple[Constraint, Constraint]) -> Tuple[np.ndarray, Callable[[int], float]]:
        pass

    @ staticmethod
    def __temporal(bar: Bar, phase: float) -> Callable[[float], Callable[[float], float]]:
        return lambda omega: lambda t: np.cos(omega * t)


class HertzImpulse:
    """[summary]
    $V_0$ est la vitesse initiale d'impact sur la lame au repos.
    Retourne la fonction d'impulsion pour une frappe en t=0
    """
    @ classmethod
    def get_impulse(cls, bar: Bar, mallet: Mallet, v_0):
        # voir « Impact hertzien élastique », Acoustique des Instruments de Musique
        # Le rayon de courbure au point de contact :
        # - infini pour la lame
        # - égale au rayon de sa tête pour la baguette
        k = 1.25 * np.sqrt(mallet.shape.r) / ((1 - bar.mat.nu ** 2) /
                                              bar.mat.e + (1 - mallet.mat.nu ** 2) / mallet.mat.e)
        m_1 = bar.get_mass()
        m_2 = mallet.get_mass()
        m_r = m_1 * m_2 / (m_1 + m_2)
        delta_max = np.power((5/4) * m_r * v_0 ** 2 / k, 2/5)
        tau = 3.218 * np.power(m_r ** 2 / (k ** 2 * v_0), 1/5)

        return lambda t: k * np.power(delta_max, 1.5) * np.exp(- t / tau)
