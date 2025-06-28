from pydub import AudioSegment
import os

def aplicar_eco(ruta_audio):
    audio = AudioSegment.from_file(ruta_audio)
    eco = audio + audio.reverse().fade_out(1500)
    eco.export("salida_eco.wav", format="wav")
    print("✅ Eco aplicado")

def aplicar_reverb(ruta_audio):
    audio = AudioSegment.from_file(ruta_audio)
    reverb = audio.overlay(audio.reverse(), gain_during_overlay=-6)
    reverb.export("salida_reverb.wav", format="wav")
    print("✅ Reverb aplicado")

def aplicar_pitch(ruta_audio):
    audio = AudioSegment.from_file(ruta_audio)
    pitched = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.25)
    }).set_frame_rate(audio.frame_rate)
    pitched.export("salida_pitch.wav", format="wav")
    print("✅ Pitch aumentado")

def aplicar_filtro_bajo(ruta_audio):
    audio = AudioSegment.from_file(ruta_audio)
    filtrado = audio.low_pass_filter(400)
    filtrado.export("salida_filtro_bajo.wav", format="wav")
    print("✅ Filtro de bajos aplicado")
