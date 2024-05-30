import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import audio_to_text 
import os

if __name__ == "__main__":
    audio_path = 'C:/Users/Franco/projects/builder-report/audios/informe-test.mp3'
    if os.path.isfile(audio_path):
        text = audio_to_text.transcribe_audio_by_segments(audio_path)
        print("Transcripción completa del audio:")
        print(text)
    else:
        print(f"El archivo de audio {audio_path} no existe.")
