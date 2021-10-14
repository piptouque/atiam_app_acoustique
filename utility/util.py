
import numpy as np
import soundfile as sf
import os
import tempfile

from typing import Callable


def get_signal_from_modes(y_n: Callable[[int], Callable[[float, float], float]], nb_modes: int, x_0: np.ndarray, ts: np.ndarray) -> np.ndarray:
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
    x_0 = np.array(x_0)
    ts = np.array(ts)
    if len(x_0.shape[0]) == 0:
        x_0 = np.array([x_0])
    print(x_0.shape)
    print(ts.shape)
    s = np.zeros((x_0.shape[0], ts.shape[0]))
    # we always discard the first mode (n=0), because it does not represent a variation.
    vs = np.zeros((nb_modes, x_0.shape[0], ts.shape[0]))
    for i in range(1, nb_modes):
        vs[i] = y_n(i)(x_0, ts)
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
