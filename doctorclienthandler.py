"""
File: doctorclienthandler.py
Client handler for providing non-directive psychotherapy.
"""

from codecs import decode
from threading import Thread
from doctor import Doctor
import pickle
import os

BUFSIZE = 1024
CODE = "ascii"
history = []

class DoctorClientHandler(Thread):
    """Handles a session between a doctor and a patient."""
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.dr = Doctor()

    def readData(self, name):
        if os.path.isfile(name + ".dat"):
            print("Patient " + name + " already exist...")
            exFile=open(name + ".dat", 'rb')
            FList=pickle.load(exFile)
            history.extend(FList)
            print("History: " + str(history))
            exFile.close()
            self.client.send(bytes(self.dr.reply(str(history[-1])), CODE))
            File=open(name + '.dat', 'wb')
            return File   
        else:
            File = open(name + ".dat", "wb") 
            self.client.send(bytes(self.dr.greeting(), CODE))            
            return File

    def run(self):
        self.client.send(bytes(self.dr.askname(), CODE))
        ptname = decode(self.client.recv(BUFSIZE), CODE)
        print("Patient " + ptname + " connected...")
        pFile = self.readData(ptname)

        while True:
            message = decode(self.client.recv(BUFSIZE),
                             CODE)
            history.append(str(message))
            if not message:
                del history[-1]
                pickle.dump(history, pFile)
                pFile.close()
                history.clear()
                print("Patient " + ptname + " disconnected")
                self.client.close()
                break
            else:
                self.client.send(bytes(self.dr.reply(message),
                                       CODE))

        
