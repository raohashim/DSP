from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
from sound import *
import pickle
import scipy.spatial.distance as ssd
import os.path
from scipy.spatial import voronoi_plot_2d,Voronoi
from functions import *
N = 2
M = 256 

if __name__ == '__main__':
	#IMPORT AUDIO
	name1 = "Track48.wav"
	data1 = getaudio(name1)
	name2 = "speech.wav"
	data2 = getaudio(name2)
	
	#INTIALIZING THE CODEBOOK
	cb = np.zeros((M,2))
	
	#TRAINING SEQUENCE INITIALIZATION
	t_seq = np.reshape(data2,(-1,N))

	#Assign Codebook vector
	seq = np.linspace(np.min(data1),np.max(data1),M)
	#print seq
	cb[:,0] = seq
	cb[:,1] = seq

	diff = 5000
	itr = 0
	print ("Training Started")
	while diff > 2000:
		cb,diff = cond_expe (t_seq , cb)
		itr+=1
		print("Iteration#",itr, "difference = ",diff)

	bound = near_neig(cb)
	pickle.dump(cb,open("codebook.bin","wb"),1)
	pickle.dump(cb,open("voronoi_regions.bin","wb"),1)
	print ("Training Completed")	
	#plot (cb,bound,t_seq)
