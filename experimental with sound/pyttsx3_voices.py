import pyttsx3
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice: {voice.name}")

input()
