from scr.tts_generator import generate_audio


script = """
Welcome to RegPulse AI.
Today we discuss important European regulatory updates.
This is an automatically generated podcast episode.
"""


audio_file = generate_audio(script)

if audio_file:
    print("Generated file:")
    print(audio_file)
else:
    print("Audio generation failed")