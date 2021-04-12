from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
from sound import *
import pickle
import scipy.spatial.distance as ssd
from t3_train import *

#IMPORT AUDIO
name1 = "Track48.wav"
data1 = getaudio(name1)
name2 = "speech.wav"
data2 = getaudio(name2)

   
#step one
#Amplitude = np.max(data1) - np.min(data1) #Amplitude of training set

t_seq = np.reshape(data2,(-1,2))  #Initiate training set
#Xk = np.reshape(data1,(-1,2))  #Initiate Xk

cb = pickle.load(open("codebook.bin","rb"))
vr = pickle.load(open("voronoi_regions.bin","rb"))

plot(cb,vr,t_seq)  
#plot(f1,f2,Xk) 
