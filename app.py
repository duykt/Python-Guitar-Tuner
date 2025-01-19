import pyaudio
import wave
import numpy as np

audio = pyaudio.PyAudio()
RATE = 44100
CHUNK_SIZE = 1024

stream = audio.open(format=pyaudio.paInt16,         # audio format
                    channels=1,                     # audio channels
                    rate=RATE,                      
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)


try:
    while True:
        data = stream.read(CHUNK_SIZE)

        audio_data = np.frombuffer(data, dtype=np.int16)

        # FFT audio data
        fft_data = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(fft_data), 1 / RATE) 
        
        magnitude = np.abs(fft_data)
        peak_index = np.argmax(magnitude[:CHUNK_SIZE // 2])  
        dominant_frequency = freqs[peak_index]
        
        # Print the dominant frequency
        print(f"Dominant frequency: {dominant_frequency:.2f} Hz")
        
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

sound_files = wave.open()