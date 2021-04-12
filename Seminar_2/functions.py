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

N = 2
M = 256 


def mid_tread(Signal_Data, bit_size):
	#step delta = Amax-Amin/2^N 
      	ma= float(np.max(Signal_Data))
	m = float(np.min(Signal_Data))
	step = (ma-m)/(2**bit_size) 
    	#In Mid Tread Quantizer index = round of Signal_Data/step
    	index = np.round(Signal_Data/step)
    	#Reconstruction of Signal
    	reconstruct = np.array(Signal_Data.shape)
    	reconstruct=index*step  
    	return index,reconstruct

def write_bin(filename,data):

	f=open(filename, 'wb')
	pickle.dump(data,f,1)
	f.close()

def getaudio (name):
	if name == "Track48.wav":
		rate, data = wav.read(name)
		#print data
		data = data[:,1]
	else:
		rate, data = wav.read(name)	
		#print data
	return (data)

def near_neig(cb):
	num = len(cb)
	b_no = (num+1)*num/2
	bou = np.zeros((int(b_no),2))
	cv = np.zeros((2,2))
	b_seq = 0
	for i in range(0,num-1):
		cv[0] = cb[i,:]
		for j in range (i+1, num):
			cv[1] = cb[j,:]
			bou[b_seq]= (cv[0]+cv[1])/2
			b_seq+=1
	return bou
			


def cond_expe (t_seq,cb):
	row,col = t_seq.shape
	ind = np.zeros(row)# index for codevector
	d = np.zeros(M)#Initiate Euclidean distance array(for one sample)
	
	#Computing New Boundries
	for x in range(row):
		for y in range(M):
			d[y] = ssd.euclidean(cb[y],t_seq[x])
		#Minimum Distance for Training point
		ind[x] = np.argmin(d)
		#print np.argmin(d)
		#print ind
	vec = np.zeros((M,2))   # the sum of training sequences for regions 
	vecno = np.zeros(M)   # how many samples in each region
	cbn = np.zeros(cb.shape)
	for x in range(row):
		for y in range(M):
			if ind[x] == y:
				vec[y] = vec[y] + t_seq[x]
				#print vec[y],t_seq[x]
				vecno[y] = vecno[y]+1
			 	#print vecno
	for x in range(M):
		if vecno[x] != 0:
			cbn[x] = vec[x]/vecno[x]
			#print cbn
	diff = np.sum(np.abs(cbn-cb)) 
	#print diff	
	return cbn,diff

def VQEnc (cb,t_seq):

	row,col = t_seq.shape
	ind = np.zeros(row)# index for codevector
	d = np.zeros(M)
	for x in range(row):
		print ("Loop remaining #", row-x)
		for y in range(M):
			d[y] = ssd.euclidean(cb[y],t_seq[x])
		#Minimum Distance for Training point
		ind[x] = np.argmin(d)
		#print np.argmin(d)
		#print ind
	return ind

def VQDec(cb,ind):
   
   x = np.zeros((len(ind),2))
   for i in range(len(ind)):
      x[i] = cb[int(ind[i])]
   return x

		
def plot (cb,bound,tra_seq):
	vor = Voronoi(bound)
	fig = voronoi_plot_2d(vor,show_points = None,show_vertices = None,line_colors = 'g')
	plt.scatter(tra_seq[:,0],tra_seq[:,1], color = 'b', s=10, label = 'training signal')
	plt.scatter(cb[:,0],cb[:,1],color = 'r', marker = '*',s=30, label = 'code vector')
	plt.legend (loc = 'best')
	plt.show()
	return

def file_size(fname):
        statinfo = os.stat(fname)
        return statinfo.st_size

