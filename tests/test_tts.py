"""
Test for the Text-to-Speech module.
"""

print("Starting TTS test...")

from src.tts_generator import generate_audio


def main():
    print("=" * 70)
    print("TEXT TO SPEECH TEST")
    print("=" * 70)

    script = (
        "Welcome to RegPulse AI. "
        "This is a test of the Text-to-Speech module."
    )

    audio_path = generate_audio(script)

    if audio_path:
        print(f"Audio generated successfully: {audio_path}")
    else:
        print("Audio generation failed.")


if __name__ == "__main__":
    main()