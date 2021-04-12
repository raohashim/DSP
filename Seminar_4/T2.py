from scipy.fftpack import fft
import scipy.io.wavfile as wav
import numpy as np
import scipy.signal as signal
import pyaudio
import matplotlib.pyplot as plt
from Play import *
from Functions import *
N = 32
#Reading the audio file
sampling_frequency, Audio = wav.read('speech.wav')
audio = Audio[:,1]
a = 1
b = [0.3235,0.2665,0.2940,0.2655,0.3235]
#Setting the Parametrs of remez
fltr,w,h = rem(N)
#Ploting remz 
plt.figure(2)
plt.subplot(211)
plt.plot(w, 20 * np.log10(abs(h)))
plt.title('Remz Filter Frequency response')
plt.subplot(212)
plt.plot(fltr)
plt.title('Remz filter Impulse Response')

plt.show()


up_sample_signal = np.zeros(len(audio)*4)
up_sample_signal[::4] = audio
#print len(up_sample_signal)
#FFT of Audio signal W/O Filtring
#Sam_Sig = np.zeros (len(FilteredAudio))
#Sam_Sig[::4] = FilteredAudio [::4]
FFT_Sam_Sig = fft (up_sample_signal)
fig, (plt1, plt2) = plt.subplots(2)
plt1.plot(abs(FFT_Sam_Sig))
plt1.set_title('FFT of Upsampled Original signal')
#playaudio(up_sample_signal, sampling_frequency*2)


FilteredAudio = IR_of_BPF(fltr,audio)

#FFT of Audio signal With Filtring

Flt_FFT_Sam_Sig = np.zeros (len(FilteredAudio))
Flt_FFT_Sam_Sig = fft(FilteredAudio)
plt2.plot(abs(Flt_FFT_Sam_Sig))
plt2.set_title('FFT of Upsampled Filtered signal')
plt.show()
playaudio(FilteredAudio, sampling_frequency*2)








