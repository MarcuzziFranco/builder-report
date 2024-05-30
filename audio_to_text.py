import whisper
import numpy as np
import os


class AudioToText():

    def __init__(self) -> None:
        self.modelo =  whisper.load_model("base")
        self.simple_rate = 16000

    def load_audio_complete(self,audio_path, sample_rate=16000):
        audio = whisper.load_audio(audio_path, sr=sample_rate)
        duracion = len(audio) / sample_rate
        print(f"Duración del audio: {duracion:.2f} segundos")
        return audio

    def calculate_total_duration_in_seconds(self,list_audio_path,sample_rate=16000):
        total_duration_in_seconds = 0
        for audio_path in list_audio_path:
            audio = whisper.load_audio(audio_path, sr=sample_rate)
            duracion = len(audio) / sample_rate
            total_duration_in_seconds += int(duracion)
        return total_duration_in_seconds

    def transcribe_segment(self,modelo, audio_segmento):
        # Asegurarse de que el audio tenga la forma correcta
        audio_segmento = whisper.pad_or_trim(audio_segmento)
        mel = whisper.log_mel_spectrogram(audio_segmento).to(modelo.device)
        opciones = whisper.DecodingOptions(language="es", without_timestamps=True)
        resultado = whisper.decode(self.modelo, mel, opciones)
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

    def transcribe_audio_list_by_segments(self,list_audio_path, duracion_segmento=30, sample_rate=16000):
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
        
            transcriptions_texts.append(transcripcion_completa.strip())
            
        return transcriptions_texts

