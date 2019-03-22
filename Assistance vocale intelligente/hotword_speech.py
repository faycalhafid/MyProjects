import speech_recognition as sr
import pyttsx3, os
from reconnaissance import treat_request, get_appointment_by_date, get_appointment_by_month, insert
from string_matcher import match_word, match_month, match_number, match_names, match_motif
from datetime import date, timedelta
"""from Capteur import sonner"""
r = sr.Recognizer()
m = sr.Microphone()

def say_it(phrase):
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()

def initiate (mot_cle1,mot_cle2):
    text=""
    say_it("Bonjour ! Il faut dire le mot clé "+mot_cle1)
    print("Dites le mot clé")
    while mot_cle1 not in text and mot_cle2 not in text :
        with m as source :
            audio=r.listen(source,phrase_time_limit=1.5)
        try :
            text += r.recognize_google(audio, language="fr-FR")
            if text :
                match = match_word(text, 58)
                print("Vous avez dit : "+text)
                text += " "
                if match :
                    print("Ce que le système peut interpreter : "+match)
                if (match==mot_cle1) :
                    text=match
        except sr.UnknownValueError :
            print("Could not understand audio "+text)
            continue
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def said_date(request):
    if match_number(request):
        return match_number(request)
    return False

def said_month(request):
    months_names=["janvier","février","mars","avril","mai","juin","juillet","août","septembre"
            ,"octobre","novembre","décembre"]
    months_nb=[i for i in range(1,13)]
    months=dict(zip(months_names,months_nb))
    for m in list(months.keys()):
        if match_month(request):
            return months[match_month(request)]
    return False

def said_name(request,names):
    for name in names:
        if name in match_word(request,80):
            return name
    return False

def appointment (request):
    today = date.today()
    jour=False
    if "aujourd'hui" in request :
        jour=today
    if "demain" in request :
        jour=today+timedelta(days=1)
    if "après-demain" in request :
        jour = today + timedelta(days=2)
    if said_date(request) or said_month(request):
        if said_date(request) and said_month(request):
            day = said_date(request)
            month = said_month(request)
            jour=date(today.year,int(month),int(day))
        elif said_month(request):
            month=said_month(request)
            rdvs=get_appointment_by_month(str(month))
            reponse="Vous avez "+str(len(rdvs))+" rendez-vous pendant ce mois. "
            i=0
            for rdv in rdvs :
                i+=1
                reponse+=" Rendez-vous numéro "+str(i)+"., "+str(rdv[3])+", avec "+rdv[1]+", lieu : "+rdv[2]+", pour "+rdv[0]+". "
            return reponse
        else :
            day = said_date(request)
            if (int(day)>=int(today.day)):
                jour=date(today.year,today.month,int(day))
            else :
                if (int(today.month) == 12) :
                    jour=date(today.year+1,1,int(day))
                else :
                    jour=date(today.year,today.month+1,int(day))
    #names=get_names()
    """
    if said_name(request,names):
        name=said_name(request,names)
        
    else :"""
    if (jour) :
        rdv=get_appointment_by_date(str(jour))
        reponse="Vous avez "+str(len(rdv))+" rendez-vous le "+str(jour)+" ."
        for i in range(len(rdv)):
            reponse+=" Rendez-vous numéro "+str(i+1)+", "+str(jour)+", avec "+rdv[i][1]+", lieu : "+rdv[i][2]+", pour "+rdv[i][0]+". "
        return reponse
    else :
        return "Pas de rendez-vous"

def add_appointment():
    r = sr.Recognizer()
    m = sr.Microphone()
    print("Ajout d'un nouveau rendez-vous dans la base de donnée. ")
    say_it("Ajout d'un nouveau rendez-vous dans la base de donnée. ")
    print("Avec qui aura lieu le rendez-vous ?")
    say_it("Avec qui aura lieu le rendez-vous ?")
    name=""
    while name=="" :
        with m as source:
            audio = r.listen(source, phrase_time_limit=2.5)
        try :
            name+= r.recognize_google(audio,language="fr-FR")
            if match_names(name):
                name=match_names(name)
            print(name)
        except sr.UnknownValueError:
            print("Could not understand audio "+name)
            engine = pyttsx3.init()
            engine.say("Répétez")
            engine.runAndWait()
    lieu=""
    while lieu =="":
        print("où aura lieu le rendez-vous ?")
        say_it("Où aura lieu le rendez-vous ?")
        with m as source:
            audio = r.listen(source, phrase_time_limit=2.5)
        try :
            lieu+= r.recognize_google(audio,language="fr-FR")

        except sr.UnknownValueError:
            print("Could not understand audio "+lieu)
            engine = pyttsx3.init()
            engine.say("Répétez")
            engine.runAndWait()
    motif=""
    while motif=="" :
        print("Quel est le motif ?")
        say_it("Quel est le motif ?")
        with m as source:
            audio = r.listen(source, phrase_time_limit=2.5)
        try :
            motif+= r.recognize_google(audio,language="fr-FR")
            if match_motif(motif):
                motif=match_motif(motif)
        except sr.UnknownValueError:
            print("Could not understand audio "+motif)
            engine = pyttsx3.init()
            engine.say("Répétez")
            engine.runAndWait()
    jour=""
    while ( not said_date(jour) ) and ("aujourd'hui" not in jour ) and ("demain" not in jour) :
        auj=date.today()
        print("Pour quelle date ?")
        say_it("Pour quelle date ?")
        with m as source:
            audio = r.listen(source, phrase_time_limit=2.5)
        try :
            jour+= r.recognize_google(audio,language="fr-FR")
            if "aujourd'hui" in jour :
                appointment_date=str(auj)
            elif "demain" in jour :
                appointment_date=str(auj+timedelta(days=1))
            elif said_month(jour):
                j=said_date(jour)
                m=said_month(jour)
                if (int(m)<int(auj.month)):
                    appointment_date=str(date(auj.year+1,int(m),int(j)))
                else :
                    appointment_date = str(date(auj.year,int(m),int(j)))
            else :
                j = said_date(jour)
                if (int(j)<int(auj.day)):
                    appointment_date = str(date(auj.year,auj.month+1,int(j)))
                else :
                    appointment_date = str(date(auj.year,auj.month,int(j)))


        except sr.UnknownValueError:
            print("Could not understand audio")
            engine = pyttsx3.init()
            engine.say("Répétez")
            engine.runAndWait()
    import sqlite3
    conn = sqlite3.connect('reconnaissance.sqlite')
    cursor = conn.cursor()
    print(" Appointment date : "+appointment_date)
    print(motif)
    print(name)
    print(lieu)
    insert(str(appointment_date),motif,name,lieu)
    reponse="Rendez-vous ajouté dans la base de donnée. "+str(appointment_date)+" avec "+name+" , lieu : "+lieu+", pour "+motif+". "
    return reponse

initiate("bonjour","Bonjour")
print("Comment puis-je vous aider?")
say_it('Comment puis-je vous aider ?')

text=""
while "merci" not in text and "Merci" not in text :
    with m as source:
        audio = r.listen(source, phrase_time_limit=3)
    try:
        text += r.recognize_google(audio, language="fr-FR")
        if text:
            print("Vous avez dit : " + text)
            text+=" "
            if "jeu" in text or "jeux" in text or "jouer" in text :
                os.system("MemoryGame.html")
                text="merci"
            elif "ajout" in text or "nouveau" in text :
                reponse = add_appointment()
                print(reponse)
                say_it(reponse)
                text=""
            elif "rendez-vous" in text or "consulter" in text or "voir" in text or "faire" in text or said_date(text) or said_month(text) :
                reponse=appointment(text)
                print(reponse)
                say_it(reponse)
                text=""


            else :
                match=match_word(text,90)
                if match=="merci":
                    text="merci"
                if "merci" not in text and "Merci" not in text:
                    reponse = treat_request(text)
                    if reponse :
                        print(reponse)
                        say_it(reponse)
                        """
                        if "voiture" in text :
                            sonner("voiture")
                        if "maison" in text :
                            sonner("maison")"""
                        text=""
                    else :
                        print("Répétez. Vous avez dit : "+text)
                        say_it("Répétez")
                else :
                    text="merci"
    except sr.UnknownValueError:
        print("Could not understand audio")
        engine = pyttsx3.init()
        engine.say("Répétez")
        engine.runAndWait()