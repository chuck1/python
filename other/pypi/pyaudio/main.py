import pyaudio
import sys
import wave
import math
import struct
import random
from itertools import *
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def pitch_linear(t, x1, y1):
    a = (y1 - 1) / 2 / x1
    b = x1 / (y1 - 1)
    return a * (t + b)**2

def pitch_oscillation(t, offset, amplitude, period):
    freq = 1 / period
    a = 2 * math.pi * freq
    return offset * t - amplitude * math.cos(a * t) / a

def sine_wave2(frequency=440.0, framerate=44100, amplitude=0.5):

    def f(i):
        t = i / framerate
        #t = pitch_increase_linear(t, 10, 0.5)
        t = pitch_oscillation(t, 1, 0.1, 4)
        return amplitude * math.sin(2.0 * math.pi * float(frequency) * t)

    return (f(i) for i in count(0))

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    period = int(framerate / frequency)
    
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    
    def f(i):
        t = i / framerate
        return amplitude * math.sin(2.0 * math.pi * float(frequency) * t)
    
    lookup_table = [f(i) for i in range(period)]
    
    return (lookup_table[i % period] for i in count(0))

def square_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    for s in sine_wave(frequency, framerate, amplitude):
        if s > 0:
            yield amplitude
        elif s < 0:
            yield -amplitude
        else:
            yield 0.0

def damped_wave(frequency=440.0, framerate=44100, amplitude=0.5, length=44100):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (math.exp(-(float(i%length)/float(framerate))) * s for i, s in enumerate(sine_wave(frequency, framerate, amplitude)))

def white_noise(framerate=44100, amplitude=0.5):
    '''
    Generate random samples.
    '''
    return (amplitude * random.uniform(-1, 1) for i in count(0))
    
def compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.
    
    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(zip(*(map(sum, zip(*channel)) for channel in channels)), nsamples)

def write_wavefile(filename, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples to a wavefile."

    print("write wave file")

    if nframes is None:
        nframes = -1

    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    print('sampwidth', sampwidth)

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
    
    def f2(channels):
        for sample in channels:
            try:
                yield struct.pack('h', int(max_amplitude * sample))
            except:
                print(sample)
                print(max_amplitude)
                print(int(max_amplitude * sample))
                print(2**15)
                raise

    def f1(chunk):
        for channels in chunk:
            if channels is None: continue
            yield b''.join(f2(channels)) 

    # split the samples into chunks (to reduce memory consumption and improve performance)
    print("write chunks")
    for chunk in grouper(bufsize, samples):
        frames = b''.join(f1(chunk))
        w.writeframesraw(frames)

    w.close()

    return filename

def write_pcm(f, samples, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples as raw PCM data."
    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = ''.join(''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        f.write(frames)

    f.close()

    return filename

class Noise:
    def __init__(self, amplitude, framerate, t, filt):

        self.amplitude = amplitude
        self.y = np.array([])

        n = int(framerate * t)
        
        freqN = framerate / 2
        
        #b, a = scipy.signal.butter(1, Wn)
        b, a = filt
        w, h = scipy.signal.freqs(b, a)

        self.x = (np.random.rand(n) * 2 - 1) * amplitude
        self.y = scipy.signal.lfilter(b, a, self.x)

        if False:
            plt.semilogx(w * freqN, 20 * np.log10(abs(h)))
            plt.show()

            plt.plot(self.x[:1000])
            plt.plot(self.y[:1000])
            plt.show()
        
    def __iter__(self):
        #return self
        return iter(self.y)

    #def __next__(self):
    #    b, a = self.filt
    #    self.y = np.concatenate((self.y, [self.amplitude * random.uniform(-1, 1)]))
    #    z = scipy.signal.lfilter(b, a, self.y)
    #    return z[-1]

def main():

    framerate = 44100
    duration = 10

    #{'func':'sine_wave2', 'frequency':440, 'amplitude':0.5},
    #{'func':'white_noise', 'amplitude':0.5},
    #{'func':'Noise', 'amplitude':1.0},

    freqN = framerate / 2

    channels = (
            (
                chain(
                    Noise(0.5, framerate, 5, scipy.signal.butter(1, 400/freqN)),
                    Noise(0.5, framerate, 5, scipy.signal.butter(2, 400/freqN)),
                    ),
                ),
            )
    
    channels = (
            (
                sine_wave(100, framerate, 0.05),
                sine_wave(101, framerate, 0.05),
                sine_wave(101, framerate, 0.05),
                sine_wave(102, framerate, 0.05),
                sine_wave(103, framerate, 0.05),
                sine_wave(105, framerate, 0.05),
                sine_wave(108, framerate, 0.05),
                sine_wave(113, framerate, 0.05),
                sine_wave(121, framerate, 0.05),
                #Noise(0.1, framerate, 10, scipy.signal.butter(1, 200/freqN)),
                ),
            )

    # convert the channel functions into waveforms
    samples = compute_samples(channels, framerate * duration)
    
    write_wavefile(sys.argv[1], samples, framerate * duration, 2, 16 // 8, framerate)


if __name__ == "__main__":
    main()

