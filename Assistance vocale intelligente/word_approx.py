import speech_recognition as sr
from gtts import gTTS
import numpy as np
from string_matcher import match_word
r = sr.Recognizer()
m = sr.Microphone()
possible_words=["bonjour","merci","téléphone","clés","maison","voiture","smartphone","portefeuille","médicaments"]
#tts=gTTS(text='téléphone',lang='fr')
#tts.save("téléphone.wav ")

with m as source:
    audio = r.listen(source, phrase_time_limit=1.5)
    try :
        text = r.recognize_google(audio, language="fr-FR")
        print("Vous avez dit => "+text)
        print("Le système a interprêté => ")
    except sr.UnknownValueError :
        print("Could not understand audio ")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


