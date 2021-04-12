import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from sound import *
from functions import *
#Task 1a
rate1, data1 = scipy.io.wavfile.read("Track48.wav")
#Task 1b
rate2, data2 = scipy.io.wavfile.read("speech.wav")


bitsize=4		#number of bits
cha=1

#Writing the orignal to binary file with one channel with voice
write_bin('original_audio.bin',data1[:,cha])

index,reconstruct = mid_tread (data1[:,cha], bitsize)
index=np.array(index,dtype='int8')
write_bin('coded_uniform_q_signal.bin',index)

ax = plt.subplot(111)
ax.title.set_text('Orignal and Mid-Tread Reconstructed')

ax.plot(data1[:,cha], color = 'green')
ax.plot(reconstruct, color = 'red')

plt.legend(['Orignal', 'Recon. Mid-Tread'], loc='upper right')
plt.xlabel("Number of Samples")
plt.ylabel("Amplitude")
plt.show()




