
import numpy as np
import soundfile as sf
import os
import tempfile


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
