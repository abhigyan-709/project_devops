from google import genai
import os
from dotenv import load_dotenv
import speech_recognition as sr

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Hey! What do you want to know?")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("Google Speech Regognition thinks you asked: " + text)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

response = client.models.generate_content(model='gemini-2.0-flash-exp', contents=text)
print(response.text)