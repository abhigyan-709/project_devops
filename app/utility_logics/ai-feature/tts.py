# this will convert speech to text 

from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError

def speech_to_text(audio_data):
    recognizer = Recognizer()
    with AudioFile(audio_data) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_content = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio_content)
        return recognized_text
    except UnknownValueError:
        raise Exception("Speech Recognition could not understand the audio")
    except RequestError as e:
        raise Exception(f"Error with Google Speech Recognition service: {e}")
    
def test_speech_to_text():
    audio_data = "path/to/audio/file"
    recognized_text = speech_to_text(audio_data)
    assert recognized_text == "Hello, how are you?"

