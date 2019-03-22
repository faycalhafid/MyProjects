import speech_recognition as sr
import pyttsx3
import time
engine = pyttsx3.init()
# get audio from the microphone
r = sr.Recognizer()
keywords=[("bonjour",1),("début",1)]
source=sr.Microphone()
def callback(recognizer,audio):
    try:
        print("Dites le mot clé")
        sat=recognizer.recognize_sphinx(audio,keyword_entries=keywords, language="fr-FR")
        print(sat)
        if "bonjour" in sat or "début" in sat:
            print("Le mot clé est correct")
            recognize_main()
    except sr.UnknownValueError:
        print("Error")

def recognize_main():
    print("Vous pouvez parler !")
    audio=r.listen(source)
    print("Vous avez dit :  " + r.recognize_google(audio, language="fr-FR"))

def start_recognizer():
    print("En attente du mot clé (bonjour ou bien début)")
    r.listen_in_background(source,callback)
    time.sleep(1000000)
start_recognizer()
#
# listen=False
# while True :
#     while listen == False :
#         with sr.Microphone() as source:
#             print("Speak:")
#             engine.say("Speak")
#             engine.runAndWait()
#             audio = r.listen(source,phrase_time_limit=5)
#
#         try :
#             if ( "début" in r.recognize_google(audio, language="fr-FR")):
#                 listen = True
#                 print("Listening...")
#                 engine = pyttsx3.init()
#                 engine.say("Listening")
#                 engine.runAndWait()
#                 break
#             else:
#                 continue
#         except LookupError:
#             continue
#
#     while listen == True:
#         import speech_recognition as sr
#         r = sr.Recognizer()
#         import pyttsx3
#         engine = pyttsx3.init()
#         with sr.Microphone() as source:
#             audio = r.listen(source,phrase_time_limit=5)
#         print("1")
#         try:
#             print("2")
#             if (r.recognize_google(audio, language="fr-FR") == "stop"):
#                 listen = False
#                 engine = pyttsx3.init()
#                 print("Listening stopped. Goodnight")
#                 engine.say("Listening stopped. Goodnight")
#                 engine.runAndWait()
#                 break
#             else:
#                 print("Vous avez dit :  " + r.recognize_google(audio, language="fr-FR"))
#                 engine = pyttsx3.init()
#                 engine.say("Vous avez dit : " + r.recognize_google(audio, language="fr-FR"))
#                 engine.runAndWait()
#         except LookupError:
#             engine.say('Audio cannot be read!')
#             engine.runAndWait()
#             print("Could not understand audio")
#
# #
# try:
#     print("You said " + r.recognize_google(audio, language="fr-FR"))
# except sr.UnknownValueError:
#     print("Could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results; {0}".format(e))