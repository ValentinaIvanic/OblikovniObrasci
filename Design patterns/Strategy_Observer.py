from abc import ABC, abstractmethod
import time
from time import sleep
from datetime import datetime
from statistics import median
import os

class IzvorBrojeva(ABC):
    @abstractmethod
    def ucitaj_brojeve(self):
        pass

class TipkovnickiIzvor(IzvorBrojeva):

    def ucitaj_brojeve(self):
        try:
            broj = int(input("Upisite broj(-1 za kraj): "))
            return broj
        except ValueError:
            print("Pokušajte ponovo.")
            return self.ucitaj_brojeve()
    
class DatotecniIzvor(IzvorBrojeva):

    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'r')

    def ucitaj_brojeve(self):
        line = self.file.readline().strip()
        if not line or line == "exit":
            self.file.close()
            return -1
        try:
            broj = int(line)
            return broj
        except ValueError:
            print("Neispravna linija.")
            return self.ucitaj_brojeve()

#---------------------------------------------------------------

class Promatrac(ABC):
    @abstractmethod
    def update(self, slijed_brojeva):
        pass

class ZapisDatoteka(Promatrac):
    def __init__(self):
        self.file_name = "zapisi.txt"
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w"):
                pass

    def update(self, kolekcija):
        with open(self.file_name, "a") as file:
            file.write(f"datum i vrijeme zapisa: {datetime.now()} elementi: {kolekcija}\n")


class IspisSume(Promatrac):
    def update(self, kolekcija):
        print("Suma brojeva: ", sum(kolekcija))

class IspisProsjeka(Promatrac):
    def update(self, kolekcija):
        print("Prosjek brojeva: ", sum(kolekcija)/len(kolekcija))


class IspisMedijana(Promatrac):
    def update(self, kolekcija):
        print("Medijan brojeva: ", median(kolekcija))

#---------------------------------------------------------------

        
class SlijedBrojeva:
    def __init__(self, izvor):
        self.izvor = izvor
        self.kolekcija = list()
        self.promatraci = list()

    def dodaj_promatraca(self, promatrac):
        self.promatraci.append(promatrac)

    def ukloni_promatraca(self, promatrac):
        self.promatraci.remove(promatrac)
    
    def notify(self):
        for promatrac in self.promatraci:
            promatrac.update(self.kolekcija)
    
    def kreni(self):
        while True:
            start_time = time.time()
            broj = self.izvor.ucitaj_brojeve()
            
            if broj == -1:
                break
            self.kolekcija.append(broj)
            self.notify()
            
            time_difference = time.time() - start_time
            if time_difference < 1:
                time.sleep(1- time_difference)

            print()

#----------------------------------------------------------

def main():
    izvor1 = TipkovnickiIzvor()
    izvor2 = DatotecniIzvor("datoteka.txt")

    slijed1 = SlijedBrojeva(izvor1)
    slijed1.dodaj_promatraca(ZapisDatoteka())
    slijed1.dodaj_promatraca(IspisSume())

    slijed2 = SlijedBrojeva(izvor2)

    slijed2.dodaj_promatraca(IspisProsjeka())
    slijed2.dodaj_promatraca(IspisMedijana())

    slijed1.kreni()
    print("============================")
    slijed2.kreni()

if __name__ == "__main__":
    main()