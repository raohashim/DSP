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
from Functions import *
from sound import *
'''
def downsample (filt):
	#Downsampling 
	d_samp = np.zeros(chunk)
	d_samp[::4] = filt[::4]
	#Removing of Zeros from Downsampled Zeros
	d_samp_wo = d_samp[::4]
	return d_samp_wo, d_samp

def upsample (d_samp_wo):
	u_samp = np.zeros(chunk)
	u_samp[::4] = d_samp_wo
	return u_samp
'''

chunk = 512
WIDTH = 2
CHANNEL = 1
samp_rate = 32000
filt_num = 0
framenum = 0
frame = 0
d_u_sam = 0
#Read the input file
samplerate, wavArray = scipy.io.wavfile.read("Track_32kh.wav")

print ("wav file loaded", len(wavArray), samplerate, wavArray.dtype, "Shape", wavArray.shape)
#Only take the voice channel
try:
	if wavArray.shape[1] == 2:
		left = wavArray[:, 0]
		right = wavArray[:, 1]
except:
	a = 1



frame = np.floor(len(left)/chunk)
print("frame number",frame)

#Creat a fig with three plots
fig,(p1,p2,p3) = plt.subplots(3,1)
#Set the size of the display Window
fig.set_size_inches(12, 12, forward=True)
line1, = p1.plot([],[],lw=2)
line2, = p2.plot([],[],lw=2)
line3, = p3.plot([],[],lw=2)

#Axis range of the Spectrum
p1.set_xlim(0,np.pi)
#p1.set_ylim(-100,100)  
p2.set_xlim(0,np.pi)
#p2.set_ylim(-100,100)  

p3.set_xlim(0,np.pi)

p1.grid(True)
p1.set_title('original signal')
p2.grid(True)
p2.set_title('signal after filtering and downsampling')

p3.grid(True)
p3.set_title('Reconstructed Signal')
fig.subplots_adjust(hspace=.5)

# pyaudio setting
p = pyaudio.PyAudio()
#Set a stream to read the chunk of the data
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNEL,
                rate=samp_rate,
                input=False,
                output=True,
                frames_per_buffer=chunk)

#Creat the Object Classes
class Index(object):
	def play(self, event):
		print("Start Animation button, framenumber", framenum)
		ani.event_source.start()
	def stop(self, event):
		print("Stop Animation button, framenumber", framenum)
		ani.event_source.stop()
	def IIRFilter(self,event):
        	global filt_num
        	if filt_num == 0:
        		filt_num = 1
           		print("FIR Filter is applied")
	def FIRFilter(self,event):
        	global filt_num
        	if filt_num == 1:
        		filt_num = 0
           		print("IIR Filter is applied")

#Creat the animation from the current frame
def animate(i):
	global framenum
	framenum = i
	x = np.arange(chunk)
	
	#read current chunk sample
	sample_chunk = left[chunk*i:chunk*(i+1)]
	
	#Spectrum of the current chunk of orignal Signal
	w1,h1 = sig.freqz(sample_chunk)
	p1.set_ylim(-1000000,1000000)
	line1.set_data(w1,h1)

	#Aplly the filter
	if filt_num == 0 :
		filt = FIR_Filter(sample_chunk)
	else:
		filt = IIR_Filter(sample_chunk)

	#Downsampling
	d_samp_wo, d_samp = downsample (filt,chunk)
		 		
	#Upsampling of the Signal
	u_samp = upsample(d_samp_wo,chunk)
			
	#Spectrum of the Downsampled Signal
	w2,h2 = sig.freqz(d_samp)   
	p2.set_ylim(-1000000,1000000)
	line2.set_data(w2,h2)

	#Apply filter after Upsampling
	if filt_num == 0 :
		rec_sig = FIR_Filter(u_samp)
	else:
		rec_sig = IIR_Filter(u_samp)
	w3,h3 = sig.freqz(rec_sig)
	p3.set_ylim(-1000000,1000000)
	line3.set_data(w3,h3)

	#Play the reconstructed Signal	

	chunk_sample=np.clip(rec_sig,-2**15,2**15-1)  # playback the reconstructed audio
	sound = (chunk_sample.astype(np.int16).tostring())
	stream.write(sound)
	return line1,line2,line3,

def init():
	print("init begin")
	line1.set_data([],[]) 
	line2.set_data([],[])
	line3.set_data([],[]) 
	return line1,line2,line3,

ani = animation.FuncAnimation(fig, animate, init_func = init, frames = int(frame) , interval=1, blit=True)

callback = Index()
#Assigning of Buttons
axis_play = plt.axes([0.1, 0.01, 0.1, 0.05])
axis_stop = plt.axes([0.3, 0.01, 0.1, 0.05])
axis_IIRFilter = plt.axes([0.5, 0.01, 0.1, 0.05])
axis_FIRFilter = plt.axes([0.7, 0.01, 0.1, 0.05])

#Making the Buttons for the Window
#Assigning the Function to the Button play
button_play = Button(axis_play, "Play")
button_play.on_clicked(callback.play)
#Assigning the Function to the Button Stop
button_stop = Button(axis_stop, "Stop")
button_stop.on_clicked(callback.stop)
#Assigning the Function to the Button Switch_Filt
#Assigning the button to IIR filter
button_IIRFilter = Button(axis_IIRFilter, "IIRFilter")
button_IIRFilter.on_clicked(callback.IIRFilter)
#Assigning the button to FIR filter
button_FIRFilter = Button(axis_FIRFilter, "FIRFilter")
button_FIRFilter.on_clicked(callback.FIRFilter)

plt.show()

#stream.stop_stream()
#stream.close()
#p.terminate()
