import numpy as np
import scipy.signal
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
import struct
from matplotlib.widgets import Button
from matplotlib import gridspec
import scipy.io.wavfile
import scipy.signal as sig

def FIR_Filter(input_signal):
	b = [0.3235,0.2665,0.2940,0.2655,0.3235]
	filtered = scipy.signal.lfilter(b, 1, input_signal)
	return filtered


def IIR_Filter(input_signal):
	b = [0.256,0.0512,0.256]
	a = [1.0,-1.3547,0.6125]
	filtered = scipy.signal.lfilter(b, a, input_signal)
 	return filtered

def impz(b,a):
	l = 50
    	impulse = np.repeat(0.,l)
    	impulse[0] =1.
    	x = np.arange(0,l)
    	response = sig.lfilter(b,a,impulse)
    	plt.subplot(211)
    	plt.stem(x, response)
    	plt.ylabel('Amplitude')
    	plt.xlabel(r'n (samples)')
    	plt.title(r'Impulse response')
    	plt.subplot(212)
    	w,H=sig.freqz(response)
    	plt.plot(w, 20*np.log10(abs(H)+1e-3))
    	plt.xlabel('Frequency')
    	plt.ylabel('dB')
    	plt.title('Magnitude Frequency Response')
    	plt.show()

def downsample (filt,chunk):
	#Downsampling 
	d_samp = np.zeros(chunk)
	d_samp[::4] = filt[::4]
	#Removing of Zeros from Downsampled Zeros
	d_samp_wo = d_samp[::4]
	return d_samp_wo, d_samp

def upsample (d_samp_wo,chunk):
	u_samp = np.zeros(chunk)
	u_samp[::4] = d_samp_wo
	return u_samp

'''	#Play the reconstructed Signal	
	#sound(rec_sig, samp_rate)
#	chunk_sample=np.clip(rec_sig,-2**15,2**15-1)  # playback the reconstructed audio
#	sound = (chunk_sample.astype(np.int16).tostring())
#	stream.write(sound)
'''
