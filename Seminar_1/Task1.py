import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import scipy
from scipy.io import wavfile
import sound
import fun 

bitsize = 8
"""TASK 1 (a)"""
"""Sin and Triangular Wave"""
f = int(input("Enter frequency of waves:\n"))
fnorm = 0.1
fsamp = f/fnorm
x = np.arange(fsamp)
s = np.sin(2*np.pi*fnorm*x)
st = sp.sawtooth(2*np.pi*fnorm*x,0.5)

#Determining SNR of Signal with both Midtread and Midrise
SNRmrs=fun.SNR(s,bitsize,"midrise")
print("SNR of sine with midrise is", SNRmrs,"dB")
SNRmts=fun.SNR(s,bitsize,"midtread")
print("SNR of sine with midtread is", SNRmts,"dB")

#Determing SNR
SNRmrst=fun.SNR(st,bitsize,"midrise")
print("SNR of Triangle with midrise is", SNRmrst,"dB")
SNRmtst=fun.SNR(st,bitsize,"midtread")
print("SNR of Triangle  with midtread is", SNRmtst,"dB")

fig = plt.figure()
s1 = fig.add_subplot(211)
s1.title.set_text('Sine Wave')
s1.plot(x,s, color='r')
s2 = fig.add_subplot(212)
s2.title.set_text('Triangular Wave')
s2.plot(x,st, color='b')
plt.show()

"""TASK 1 (b)"""
"""Full range and 25 dB under full range plot"""
sample_rate, audio = scipy.io.wavfile.read("Track48.wav")
#sound.sound(audio, sample_rate)
dB = 25
c = 10**(dB/20)
audio_under = audio/c
#sound.sound(audio_under, sample_rate)
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.title.set_text('Full Range Signal - Left Channel')
ax1.plot(audio[:,0], color='r')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")
ax2 = fig.add_subplot(212)
ax2.title.set_text('under 25 dB')
ax2.plot(audio_under[:,0], color='b')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")

plt.show()
