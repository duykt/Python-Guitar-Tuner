import pyaudio
import wave
import numpy as np
import json
from collections import OrderedDict

def find_closest_note(target, notes):
    lo, hi = 0, len(notes) - 1

    if target < notes[lo]:
        return notes[lo]
    
    if target > notes[hi]:
        return notes[hi]

    while lo <= hi:
        mid = (lo + hi) // 2

        if target < notes[mid]:
            hi = mid - 1
        elif target > notes[mid]:
            lo = mid + 1
        else:
            return notes[mid]
        
    if abs(notes[lo] - target) < abs(notes[hi] - target):
        return notes[lo]
    else:
        return notes[hi]

def main():
    # Each note from the potential tunings and their frequencies in Hz
    note_frequencies = OrderedDict({
        55.0: 'a1', 58.27: 'a#1', 61.74: 'b1', 65.41: 'c2',
        69.3: 'c#2', 73.42: 'd2', 77.78: 'd#2', 82.41: 'e2',
        87.31: 'f2', 92.5: 'f#2', 98.0: 'g2', 103.83: 'g#2', 
        110.0: 'a2', 115.56: 'd#3', 116.54: 'a#2', 123.47: 'b2',
        130.81: 'c3', 138.59: 'c#3', 146.83: 'd3', 164.81: 'e3',
        174.61: 'f3', 185.0: 'f#3', 196.0: 'g3', 207.65: 'g#3',
        220.0: 'a3', 233.08: 'a#3', 246.94: 'b3', 261.63: 'c4',
        277.18: 'c#4', 293.66: 'd4', 311.13: 'd#4', 329.63: 'e4', 
        415.3: 'g#4', 440.0: 'a4'
    })

    audio = pyaudio.PyAudio()
    RATE = 44100
    CHUNK_SIZE = 1024

    stream = audio.open(format=pyaudio.paInt16,         # audio format
                        channels=1,                     # audio channels
                        rate=RATE,                      
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    with open("tuning.json", 'r') as f:
        data = json.load(f)

    for i in note_frequencies.values():
        print(i)

    print("Select tuning: ")
    for i in data['frequencies']:
        print(f'{data['frequencies'].index(i) + 1}.) {i["tuning"]}')

    # while True:
    #     try:
    #         selection = int(input())
    #         notes = data['frequencies'][selection - 1]["notes"]
    #         break
    #     except ValueError:
    #         print("Erorr: Enter a number\n")
    #     except IndexError:
    #         print("Error: Invalid Selection\n")

    test_list = list(note_frequencies.keys())
    print(find_closest_note(60.5, test_list))


    # prev_freq = 0
    # try:
    #     while True:
    #         data = stream.read(CHUNK_SIZE)
    #         audio_data = np.frombuffer(data, dtype=np.int16)

    #         # FFT audio data
    #         fft_data = np.fft.fft(audio_data)
    #         freqs = np.fft.fftfreq(len(fft_data), 1 / RATE) 

    #         magnitude = np.abs(fft_data)
    #         peak_index = np.argmax(magnitude[:CHUNK_SIZE // 2])  
    #         dominant_frequency = freqs[peak_index]
    #         dominant_frequency = round(dominant_frequency.astype(float), 2)
            

    #         # Print the dominant frequency only if frequency changed
    #         if dominant_frequency != 0 and dominant_frequency != prev_freq:
    #             print(f"Clostest Note: Current frequency: {dominant_frequency:} Hz", notes)
    #             prev_freq = dominant_frequency
            
    # except KeyboardInterrupt:
    #     pass

    # stream.stop_stream()
    # stream.close()
    # audio.terminate()

    # sound_files = wave.open()

if __name__ == "__main__":
    main()