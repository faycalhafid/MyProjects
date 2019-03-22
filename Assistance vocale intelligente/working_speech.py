import speech_recognition as sr
import os
# get audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak:")
    audio = r.listen(source,phrase_time_limit=5)

try:
    text=r.recognize_google(audio, language="fr-FR")
    print("Vous avez dit " + audio)
    if "jeu" in text or "jeux" in text :
        os.system("test.html")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))