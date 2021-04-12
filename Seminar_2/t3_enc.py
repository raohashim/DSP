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

#IMPORT AUDIO
name1 = "Track48.wav"
data1 = getaudio(name1)
data1 = data1[60000:120000]
data=np.reshape(data1,(-1,N))

cb = pickle.load(open("codebook.bin","rb"))
vr = pickle.load(open("voronoi_regions.bin","rb"))
print ("VQ Encoding Started")
index = VQEnc(cb,data)
pickle.dump(index,open("coded_vq_signal.bin","wb"),1)
plot (cb,vr,data)




