
import numpy as np

"""[summary]
Ici $f_1$ se réfère à la fréquence fondamentale,
$f_2$ la première harmonique etc.
"""


class Data:
    """[summary]
    Des couples de rapport $\frac{f_2}/{f_1}$
    utilisés par des fabricants de glockenspiel.
    """
    rs = [(3, 6), (4, 8), (3, 9), (4, 10)]
    """[summary]
    $D = L_{max}/L_{min}$ de la tessiture du clavier.
    """
    d = 3
    """[summary]
    Proportion de variation de longueur de lame / creusement
    d'un demi-ton au suivant.
    """
    p_l_c = np.array([5, 1]) / 6
    """
    Modules d'Young des matériaux du glockenspiel en GPa.
    """
    es = {
        'steel': 203,
        'brass': 90,
        'wood': 10,
        'rubber': 0.01
    }
    """
    Coefficients de Poisson $\nu$, sans unité.
    """
    nus = {
        'steel': 0.3,
        'brass': 0.33,
        'rubber': 0.30
    }
    """[summary]
    Coefficients de dilatation thermique $\alpha$, en K^-1
    """
    alphas = {
        'steel': 8*10 ^ -6
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
