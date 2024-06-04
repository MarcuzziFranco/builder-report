from sympy import Integer
import whisper
import numpy as np
import os
import torch

class AudioToText():

    def __init__(self) -> None:
        # Verificar si CUDA está disponible y seleccionar el dispositivo
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Cargar el modelo y moverlo a la GPU si está disponible
        self.modelo = whisper.load_model("base").to(self.device)
        #self.modelo =  whisper.load_model("base")
        self.simple_rate = 16000

    def load_audio_complete(self,audio_path, sample_rate=16000):
        audio = whisper.load_audio(audio_path, sr=sample_rate)
        duracion = len(audio) / sample_rate
        print(f"Duración del audio: {duracion:.2f} segundos")
        return audio

    def calculate_total_duration_total_segment(self,list_audio_path,segment_duration=30,sample_rate=16000):
        total_duration_in_seconds = 0
        total_segment = 0
        for audio_path in list_audio_path:
            audio = whisper.load_audio(audio_path, sr=sample_rate)
            duration = len(audio) / sample_rate
            amount_segment = np.arange(0, duration, segment_duration)
            #total_duration_in_seconds += int(duration)
            total_segment += len(amount_segment)

        return total_segment
    
    def transcribe_segment(self,modelo, audio_segmento):
        audio_segmento = whisper.pad_or_trim(audio_segmento)
        mel = whisper.log_mel_spectrogram(audio_segmento).to(modelo.device)
        opciones = whisper.DecodingOptions(fp16=torch.cuda.is_available(), language="es")
        resultado = self.modelo.decode(mel, opciones)
        return resultado.text # type: ignore
    
    def transcribe_audio_by_segments(self,audio_path, duracion_segmento=30, sample_rate=16000):
        audio = self.load_audio_complete(audio_path, sample_rate)
        total_duracion = len(audio) / sample_rate
        segmentos = np.arange(0, total_duracion, duracion_segmento)
        transcripcion_completa = ""
        for i, inicio in enumerate(segmentos):
            fin = min(inicio + duracion_segmento, total_duracion)
            print(f"Transcribiendo segmento {i+1}/{len(segmentos)}: {inicio:.2f}s a {fin:.2f}s")
            audio_segmento = audio[int(inicio * sample_rate):int(fin * sample_rate)]
            transcripcion_segmento = self.transcribe_segment(self.modelo, audio_segmento)
            transcripcion_completa += transcripcion_segmento + " "
        
        return transcripcion_completa.strip()

    def transcribe_audio_list_by_segments(self,list_audio_path,callback_update_progressbar=None, duracion_segmento=30, sample_rate=16000):
        transcriptions_texts = []
        for audio_path in list_audio_path:
            audio = self.load_audio_complete(audio_path, sample_rate)
            
            total_duracion = len(audio) / sample_rate
            segmentos = np.arange(0, total_duracion, duracion_segmento)
            transcripcion_completa = ""
            
            for i, inicio in enumerate(segmentos):
                fin = min(inicio + duracion_segmento, total_duracion)
                print(f"Transcribiendo segmento {i+1}/{len(segmentos)}: {inicio:.2f}s a {fin:.2f}s")
                audio_segmento = audio[int(inicio * sample_rate):int(fin * sample_rate)]
                transcripcion_segmento = self.transcribe_segment(self.modelo, audio_segmento)
                transcripcion_completa += transcripcion_segmento + " "
                if callback_update_progressbar != None:
                    callback_update_progressbar()
        
            transcriptions_texts.append(transcripcion_completa.strip())
            
        return transcriptions_texts

