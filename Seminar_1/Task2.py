import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal as sp
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
    #S_Min  = float(np.amin(Signal_Data))
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
    elif quantizer == "ulawmt":
        Signal_Quantization=u_Law(Signal_Data, bit_size,'midtread')
    elif quantizer == "ulawmr":
        Signal_Quantization=u_Law(Signal_Data, bit_size,'midrise')   
#Error Signal    
    Error_Signal= Signal_Data - Signal_Quantization
#Energy in Original Signal
    Eng_Signal = np.sum(np.square(Signal_Data))
#Energy in Error Signal
    Eng_Error = np.sum(np.square(Error_Signal))
#SNR = 10* log10(Signal Energy/Quantization Error Energy
    SNR= 10 * np.log10(Eng_Signal/Eng_Error)
    return SNR

#Import the audio file
sample_rate, audio = scipy.io.wavfile.read("Track48.wav")
#sound.sound(audio, sample_rate)
bitsize = 8 #no.of bits

#Mid Rise Quantization
signal_reconstructed_midrise = mid_rise (audio, bitsize)
#sound.sound(signal_reconstructed_midrise, sample_rate)
#Quantization Error Mid Rise
Q_error_mr = audio-signal_reconstructed_midrise
#print (" Quantization Error for Mid Rise is ",Q_error_mr,"db") 
SNRmr = SNR(audio,bitsize,"midrise")
print("SNR of Track48.wav with midrise is", SNRmr,"dB")

#Mid Tread Quantization
signal_reconstructed_midtread = mid_tread (audio, bitsize)
#sound.sound(signal_reconstructed_midtread, sample_rate)
#Quantization Error Mid Tread
Q_error_mt = audio-signal_reconstructed_midtread
#print (" Quantization Error for Mid Tread is ",Q_error_mt,"db")
SNRmt = SNR(audio,bitsize,"midtread")
print("SNR of Track48.wav with midtread is", SNRmt,"dB")


#ulaw
#Midtread ulaw
signal_reconstruct_umt=u_Law(audio,bitsize,'midtread')
#print("Playing the ulaw Midtread reconstructed signal")
#sound.sound(signal_reconstructed_umt, sample_rate)
#Quantization Error with ulaw Midtread
Q_error_mt= audio - signal_reconstruct_umt


#Midrise ulaw
signal_reconstruct_umr=u_Law(audio,bitsize,'midrise')
#print("Playing the ulaw Midrise reconstructed signal")
#sound.sound(signal_reconstructed_umr, sample_rate)
#Quantization Error with ulaw Midtread
Q_error_mr= audio - signal_reconstruct_umr

#SNR of Non Uniform Quantization
SNRumt=SNR(audio,bitsize,'ulawmt')
print('SNR of Signal with uLaw Midtread is',SNRumt,'dB')
SNRumr=SNR(audio,bitsize,'ulawmr')
print('SNR of Signal with uLaw Midrise is',SNRumr,'dB')

#Uniform Quantization
fig = plt.figure()
ax1 = fig.add_subplot(411)
ax1.title.set_text('Uniform Quantization')
ax1.plot(signal_reconstructed_midtread[:,0], color = 'red')
ax1.plot(signal_reconstructed_midrise[:,0], color = 'green')
plt.legend(['Mid-Tread', 'Mid-Rise'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")

#Non Uniform Quantization
ax2 = fig.add_subplot(412)
ax2.title.set_text('Non Uniform Quantization')
ax2.plot(signal_reconstruct_umt[:,0], color = 'red')
ax2.plot(signal_reconstruct_umr[:,0], color = 'green')
plt.legend(['Mid-Tread', 'Mid-Rise'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")

#Combine Mid Thread
ax3 = fig.add_subplot(413)
ax3.title.set_text('Combined Mid-Tread')
ax3.plot(signal_reconstructed_midtread[:,0], color = 'red')
ax3.plot(signal_reconstruct_umt[:,0], color = 'green')
plt.legend(['Uniform Quantization', 'Non-Uniform Quantization'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")

#Combine Mid Rise
ax4 = fig.add_subplot(414)
ax4.title.set_text('Combined Mid-Rise')
ax4.plot(signal_reconstructed_midrise[:,0], color = 'red')
ax4.plot(signal_reconstruct_umr[:,0], color = 'green')
plt.legend(['Uniform Quantization', 'Non-Uniform Quantization'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")
plt.show()
