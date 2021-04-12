import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import scipy
from scipy.io import wavfile
import sound



def mid_tread(Signal_Data, bit_size):
    #step delta = Amax-Amin/2^N     
    step = (float(np.amax(Signal_Data))-float(np.amin(Signal_Data))) / pow (2,bit_size) 
    #In Mid Tread Quantizer index = round of Signal_Data/step
    index = np.round(Signal_Data/step)
    #Reconstruction of Signal
    reconstruct = np.array(Signal_Data.shape)
    reconstruct=index*step
    #reconstruct= reconstruct.astype(np.int8)    
    return reconstruct

def mid_rise(Signal_Data, bit_size):
    #step delta = Amax-Amin/2^N
    step = (float(np.amax(Signal_Data))-float(np.amin(Signal_Data))) / pow (2,bit_size)
    #In Mid Rise Quantizer index = floor of Signal_Data/step
    index = np.floor(Signal_Data/step)
    #Reconstruction of Signal
    reconstruct = np.array(Signal_Data.shape)
    reconstruct=index * step + step/2
    #reconstruct= reconstruct.astype(np.int8)
    return reconstruct
def u_Law(Signal_Data, bit_size, quantizer):
    S_Max  =  float(np.amax(Signal_Data))
    S_Min  = float(np.amin(Signal_Data))
    u = 255.0
    #u-Law Compression Expression
    Signal_y=np.sign(Signal_Data)*(np.log(1+ u* np.abs(Signal_Data/S_Max)))/np.log(1 + u)
    #Quantizer Selection
    if quantizer == 'midtread':
        Signal_yrek = mid_tread(Signal_y, bit_size)
        #print("Signal has been uniformly quantized using Mid Tread Quantizer")
    elif quantizer == 'midrise':
        Signal_yrek = mid_rise(Signal_y, bit_size)
        #print("Signal has been uniformly quantized using Mid Rise Quantizer")

        #u-law Expansion Expression
    reconstruct = np.sign(Signal_yrek)*(256**(np.abs(Signal_yrek))-1)*S_Max/u
    return reconstruct

def SNR(Signal_Data, bit_size, quantizer):
#Checking Quantizer
    Eng_Signal=0.0
    Eng_Error=0.0
    if quantizer == 'midtread':
        Signal_Quantization = mid_tread(Signal_Data, bit_size)
    elif quantizer == "midrise":
        Signal_Quantization = mid_rise(Signal_Data, bit_size)
  
#Error Signal    
    Error_Signal= Signal_Data - Signal_Quantization
#Snr 
    SNR= 10 * np.log10(Signal_Data/Error_Signal)
    return SNR
