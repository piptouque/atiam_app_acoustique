
import numpy as np

"""[summary]
Ici $f_1$ se réfère à la fréquence fondamentale,
$f_2$ la première harmonique etc.
"""


class Data:
    """
    Contraintes par dérivée partielle sur x,
    0 en tableau[i] signifie $\frac{d^iy}{dx} = 0$,
    1 signifie pas de contrainte sur la dérivée partielle.
    """
    constraints = {
        'free': [1, 1, 0, 0],
        'simply_supported': [0, 1, 0, 1],
        'encased': [0, 0, 1, 1],
        'guided':  [1, 0, 0, 1]
    }
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
    """[summary]
    Base temperature in Kelvin
    """
    temp_0 = 293.15
