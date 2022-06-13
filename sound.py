import wave
import matplotlib.pyplot as plt
import numpy as np


def get_sound_diagram():
    wav_obj = wave.open('C:/Users/Thinkpad_Owner/Desktop/train-test-beat-03.wav', 'rb')
    n_samples = wav_obj.getnframes()
    signal_wave = wav_obj.readframes(n_samples)
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    l_channel = signal_array[0::2]

    new_array = []
    step = len(l_channel) // 668
    for i in range(0, len(l_channel) - step, step):
        new_array.append(np.average(l_channel[i: i + step]))

    return new_array
