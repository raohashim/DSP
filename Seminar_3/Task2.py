import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
import struct
from matplotlib.widgets import Button
from matplotlib import gridspec
import scipy.io.wavfile
#from FIR import *
#from IIR import *
import scipy.signal as sig
from Functions import *

bi=np.array([0.256, 0.512, 0.256])
ai=np.array([1, -1.3547, 0.6125])

bf=np.array([0.3235, 0.2665, 0.2940, 0.2655, 0.3235])
af=1

#Read the input file
samplerate, wavArray = scipy.io.wavfile.read("Track_32kh.wav")

print ("wav file loaded", len(wavArray), samplerate, wavArray.dtype, "Shape", wavArray.shape)
#Only take the voice channel
try:
	if wavArray.shape[1] == 2:
		left = wavArray[:, 0]
		right = wavArray[:, 1]
except:
	# print('Wavefile is already mono')
	a = 1

w1,h1 = sig.freqz(left)
#p1.set_ylim(-1000000,1000000)

#Aplly the filter
filt_fir = FIR_Filter(left)
filt_iir = IIR_Filter(left)

#Downsampling
d_samp_wo_fir, d_samp_fir = downsample (filt_fir,filt_fir.shape)
d_samp_wo_iir, d_samp_iir = downsample (filt_iir,filt_iir.shape)
 		
#Upsampling of the Signal
u_samp_fir = upsample(d_samp_wo_iir,filt_iir.shape)
u_samp_iir = upsample(d_samp_wo_fir,filt_iir.shape)		
#Spectrum of the Downsampled Signal
#w2,h2 = sig.freqz(d_samp)   
#p2.set_ylim(-1000000,1000000)
#line2.set_data(w2,h2)

#Apply filter after Upsampling
filt_fir_rec = FIR_Filter(u_samp_fir)
filt_iir_rec = IIR_Filter(u_samp_iir)
#w3,h3 = sig.freqz(rec_sig)
#p3.set_ylim(-1000000,1000000)
#line3.set_data(w3,h3)
#Impulse response of the filters
impz(bf,af)
impz(bi,ai)

#figure (4)
w1,H1=sig.freqz(filt_fir_rec)
plt.plot(w1, 20*np.log10(abs(H1)+1e-3),'r')
plt.xlabel('Frequency')
plt.ylabel('dB') 
plt.title('Frequency Response of FIR')  
plt.show()

#figure (5)
w2,H2=sig.freqz(filt_iir_rec)
plt.plot(w2, 20*np.log10(abs(H2)+1e-3),'r')
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Frequency Response of IIR')   
plt.show()





