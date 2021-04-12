import numpy as np
import scipy.signal
import scipy.io.wavfile as wav

def FIR_Filter(input_signal):
    b = [0.3235,0.2665,0.2940,0.2655,0.3235]
    filtered = scipy.signal.lfilter(b, 1, input_signal)
    filtered = np.clip(filtered, -32000,32000)
    

    #L = len(filtered)
    print(len(filtered))
    #Upsampling = np.zeros(4*L)
    #Upsampling[::4] = filtered
    #print(len(Upsampling))

    return filtered



