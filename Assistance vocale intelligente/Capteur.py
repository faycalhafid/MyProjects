import serial
import time
capteurs = {"maison":b'2',"voiture":b'3'}
class Capteur():
    def __init__(self,com="com3",rate=9600):
        self.ser=serial.serial_for_url(com,rate)
    def sonnerCapteur(self,nomCapteur):
        time.sleep(2)
        self.ser.write(capteurs[nomCapteur])
    def ajouterCapteur(self,nomCapteur):
        pass


def sonner(keyword):
    c = Capteur(com="com3")
    c.sonnerCapteur(keyword)

sonner("voiture")

