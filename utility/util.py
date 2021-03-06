
import numpy as np
import soundfile as sf
import os
import tempfile

from typing import Callable


def get_signal_from_modes(y_n: Callable[[int], Callable[[float, float], float]], nb_modes: int, x_0: float, ts: np.ndarray) -> np.ndarray:
    """[summary]

    Args:
        y_n (Callable[[int], Callable[[float, float], float]]): [description]
        n (int): number of modes
        f_e (float): sampling frequency
        dur (float): time of synthesis
        x_0 (float): listening position on the string

    Returns:
        np.ndarray: sampled signal
    """
    ts = np.array(ts)
    s = np.zeros_like(ts)
    # we always discard the first mode (n=0), because it does not represent a variation.
    vs = np.zeros((nb_modes, ts.shape[0]))
    print(vs.shape)
    for i in range(1, nb_modes):
        mode = y_n(i)(x_0, ts)
        print(mode.shape)
        vs[i] = mode
    s = np.sum(vs, axis=0)
    return s


def play(y, Fe=44100):
    z = np.real(y)/(abs(np.real(y)).max())
    fichier = tempfile.mktemp()+'SON_TP.wav'
    sec = len(y)/Fe
    if sec <= 20:
        rep = True
    if sec > 20:
        print('Vous allez créer un fichier son de plus de 20 secondes.')
        rep = None
        while rep is None:
            x = input('Voulez-vous continuer? (o/n)')
            if x == 'o':
                rep = True
            if x == 'n':
                rep = False
            if rep is None:
                print('Répondre par o ou n, merci. ')
    if rep:
        sf.write(fichier, z, Fe)
        os.system('/usr/bin/play '+fichier+' &')
