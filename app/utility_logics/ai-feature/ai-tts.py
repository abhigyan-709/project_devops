import os
import io
import logging
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from pydub import AudioSegment

def main(audio_file_path):
    # Load environment variables from .env file
    load_dotenv()

    # Access the API key from the environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Check file existence
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError("The specified audio file does not exist")

        # Check file type
        if not audio_file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
            raise ValueError("The specified file is not a supported audio format")

        # Convert to WAV format in memory
        try:
            audio = AudioSegment.from_file(audio_file_path)
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
        except Exception as e:
            raise ValueError(f"Error converting audio file: {e}")

        # Process audio with speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_data) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_content = recognizer.record(source)

        try:
            recognized_text = recognizer.recognize_google(audio_content)
            logger.info(f"Recognized text: {recognized_text}")
        except sr.UnknownValueError:
            raise ValueError("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            raise ConnectionError(f"Error with Google Speech Recognition service: {e}")

        # Generate response using GenAI
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=recognized_text
            )
            logger.info(f"Generated response: {response.text}")
        except Exception as e:
            raise RuntimeError(f"Error generating response from GenAI: {e}")

        print("Recognized Text:", recognized_text)
        print("Generated Response:", response.text)

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process an audio file and generate AI responses.")
    parser.add_argument("audio_file", type=str, help="Path to the audio file")

    args = parser.parse_args()

    main(args.audio_file)
