
import numpy as np
import soundfile as sf
import os
import tempfile

from typing import Callable


def get_signal_from_modes(y_n: Callable[[int], Callable[[float, float], float]], n: int, f_e: float, dur: float, x_0: float) -> np.ndarray:
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
    v_y_n = np.vectorize(y_n)
    v_y = v_y_n(np.arange(n))
    ts = np.linspace(0, dur, f_e * dur)
    val = 0
    for i in range(len(v_y)):
        val += v_y[i](x_0, ts[i])
    return val

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
