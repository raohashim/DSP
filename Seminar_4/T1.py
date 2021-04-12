import numpy as np
from scipy import signal
import scipy.io.wavfile as wav
from scipy import signal
import pyaudio
import matplotlib.pyplot as plt
from Play import *
from Functions import *
#Upsampling Factor
N = 4
#Reading Audio File
sampling_frequency, Audio = wav.read('speech.wav')
audio = Audio[:,1]
#FIR Lowpass filter variables from Seminar 3
a = 1
b = [0.3235,0.2665,0.2940,0.2655,0.3235]
#Downsampling Using Nobel Identities
#y = downsampling (audio,a,b)
#print ("The lenght and shape of downsampd signal",len(y),y.shape)
#Upsampling Using Nobel Identities
Rec_Sig = upsampling (audio,a,b)
print ("The lenght and shape of reconstructed signal",len(Rec_Sig),Rec_Sig.shape)

#Ploting the Signal

#playaudio(audio, sampling_frequency)
playaudio(Rec_Sig, sampling_frequency*2)

l1, = plt.plot(audio,color= 'blue')
l2, = plt.plot(Rec_Sig[0::N], color = 'red')

plt.legend(handles = [l1,l2,],labels = ['Orignal','Reconstructed'])
plt.title('Reconstructed signal vs Original signal')
plt.show()






