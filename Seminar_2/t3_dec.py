from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
from sound import *
import pickle
import scipy.spatial.distance as ssd
from t3_train import *
from scipy.spatial import voronoi_plot_2d,Voronoi
from functions import *

N = 2
M = 256 

name1 = "Track48.wav"
data1 = getaudio(name1)
data = data1[60000:120000]

cb = pickle.load(open("codebook.bin","rb"))
vq_s = pickle.load(open("coded_vq_signal.bin","rb"))
uq_s = pickle.load(open("coded_uniform_q_signal.bin","rb"))

print ("VQ Decoder Started")
decoded = VQDec (cb,vq_s)
#print decoded
decoded = np.reshape(decoded,(1,-1))
#print decoded
rec_vq = decoded[0,:]
#print decode.shape
#print decode


q = (2**16)/(2**4)  #stepsize, 4 bit accuracy
rec1 = uq_s*q
rec_uq = rec1[60000:120000]
#print rec1[60000:120000]
error1 = data-rec_uq
error2 = data-rec_vq

#print("signal size",max(rec_uq),min(rec_uq))
#print("quantization error for mid-tread:",error1)
#print("quantization error for vq",error2)

print("size of original file: ",file_size("original_audio.bin"),"Bytes")
print("size of uniform quantized file: ",file_size("coded_uniform_q_signal.bin"),"Bytes")
print("size of vector quantized file: ",file_size("coded_vq_signal.bin"),"Bytes")

ax = plt.subplot(111)
ax.title.set_text('Orignal and Mid-Tread Reconstructed')

ax.plot(data, color = 'blue')
ax.plot(rec_vq, color = 'red')
ax.plot(rec_uq, color = 'green')

#plt.legend(['Orignal', 'rec_vq', 'rec_uq'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")
plt.show()












