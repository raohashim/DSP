import pyaudio
import numpy as np

def playaudio(audio, samplerate):
    p = pyaudio.PyAudio()          
    stream = p.open(format=pyaudio.paInt32,           
                channels=1,
                rate=samplerate,
                output=True,)
    
    audioStream = audio.astype(np.int16).tostring()
    stream.write(audioStream)
    stream.close()
