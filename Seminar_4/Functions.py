import numpy as np
from scipy import signal
import scipy.io.wavfile as wav
from scipy import signal
import pyaudio
import matplotlib.pyplot as plt
#from sound import *
import scipy.signal


def downsampling (audio,a,b):
	N = 4
	#Produce the 4 phases of a down-sampled input signal x:
	b0 = b[0::N]
	b1 = b[1::N]
	b2 = b[2::N]
	b3 = b[3::N]
	
	x0 = audio[0::N]
	x1 = audio[1::N]
	x2 = audio[2::N]
	x3 = audio[3::N]
 
	#Then the filtered and down- sampled output y is
	y=scipy.signal.lfilter(b0,a,x0)+scipy.signal.lfilter(b1,a,x1)+scipy.signal.lfilter(b2,a,x2)+scipy.signal.lfilter(b3,a,x3)
	return y

def upsampling (audio,a,b):
	N = 4	
	b0 = b[0::N]
	b1 = b[1::N]
	b2 = b[2::N]
	b3 = b[3::N]

	Upsamp_Seg0 = signal.lfilter(b0, a, audio)
	Upsamp_Seg1 = signal.lfilter(b1, a, audio)
	Upsamp_Seg2 = signal.lfilter(b2, a, audio)
	Upsamp_Seg3 = signal.lfilter(b3, a, audio)

	L = max([len(Upsamp_Seg0), len(Upsamp_Seg1), len(Upsamp_Seg2), len(Upsamp_Seg3)])
	Rec_Sig = np.zeros(N*L)
	
	Rec_Sig[0::N] = Upsamp_Seg0
	Rec_Sig[1::N] = Upsamp_Seg1
	Rec_Sig[2::N] = Upsamp_Seg2
	Rec_Sig[3::N] = Upsamp_Seg3
	
	print ("The signal Reconstruction Successfull")
	return Rec_Sig
	
def rem (N):
	F = [0.0, 0.125 - 0.05, 0.125, 0.5]
	A = [1.0, 0.0]
	W = [1.0, 100.0]
	fltr = signal.remez(N, F, A, weight=W)
	w,h = signal.freqz(fltr)
	return fltr,w,h


def IR_of_BPF(fltr,audio):
	a = 1
	h0 = fltr[0::4]
	h1 = fltr[1::4]
	h2 = fltr[2::4]
	h3 = fltr[3::4]

	Filt_Audio_Segmant0 = signal.lfilter(h0, a, audio)
	Filt_Audio_Segmant1 = signal.lfilter(h1, a, audio)
	Filt_Audio_Segmant2 = signal.lfilter(h2, a, audio)
	Filt_Audio_Segmant3 = signal.lfilter(h3, a, audio)  

	#filter and upsample - Noble Identities
	FilteredAudio = np.zeros(len(audio)*4)
	#print len(FilteredAudio)
	FilteredAudio[0::4] = Filt_Audio_Segmant0
	FilteredAudio[1::4] = Filt_Audio_Segmant1
	FilteredAudio[2::4] = Filt_Audio_Segmant2
	FilteredAudio[3::4] = Filt_Audio_Segmant3

#	w2, h2 = signal.freqz(FilteredAudio)
	
	return FilteredAudio
	 
	
		
	
	
		


