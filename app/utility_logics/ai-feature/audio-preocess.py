from pydub import AudioSegment
import os

def audio_preprocess(audio_path, output_path):
    # Load audio file
    audio = AudioSegment.from_file(audio_path)

    # Set output path
    output_path = os.path.join(output_path, "output.wav")

    # Export audio file
    audio.export(output_path, format="wav")

    return output_path

def main():
    audio_path = "input.mp3"
    output_path = "output"
    audio_preprocess(audio_path, output_path)

if __name__ == "__main__":
    main()