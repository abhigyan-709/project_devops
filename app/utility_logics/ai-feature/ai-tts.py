from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import io
from dotenv import load_dotenv
import speech_recognition as sr
from google import genai
from pydub import AudioSegment
import logging

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set")

# Initialize the GenAI client
client = genai.Client(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint for speech-to-text and content generation
@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Check file type
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="The uploaded file is not an audio file")

        # Read file into memory
        audio_data = io.BytesIO(await file.read())

        # Convert to WAV format in memory
        try:
            audio = AudioSegment.from_file(audio_data)
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error converting audio file: {e}")

        # Process audio with speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_data) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_content = recognizer.record(source)

        try:
            recognized_text = recognizer.recognize_google(audio_content)
            logger.info(f"Recognized text: {recognized_text}")
        except sr.UnknownValueError:
            raise HTTPException(status_code=400, detail="Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error with Google Speech Recognition service: {e}"
            )

        # Generate response using GenAI
        try:
            response = await client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=recognized_text
            )
            logger.info(f"Generated response: {response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response from GenAI: {e}")

        return {"recognized_text": recognized_text, "generated_response": response.text}

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

