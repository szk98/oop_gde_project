from abc import ABC, abstractmethod

# Absztrakt osztály a járatok közös jellemzőinek definiálásához
class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam  # Egyedi járatszám
        self.celallomas = celallomas  # Célállomás
        self.jegyar = jegyar  # Jegyár Ft-ban

    @abstractmethod
    def info(self):
        """Absztrakt metódus, amit a leszármazott osztályok implementálnak"""
        pass


# Belföldi járatot reprezentáló osztály
class BelfoldiJarat(Jarat):
    def info(self):
        return f"Belföldi: {self.jaratszam} - {self.celallomas} ({self.jegyar} Ft)"


#  Nemzetközi járatot reprezentáló osztály
class NemzetkoziJarat(Jarat):
    def info(self):
        return f"Nemzetközi: {self.jaratszam} - {self.celallomas} ({self.jegyar} Ft)"


# Légitársaság, amely járatokat kezel
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaadasa(self, jarat):
        """Járat hozzáadása a listához"""
        self.jaratok.append(jarat)

    def get_jarat(self, jaratszam):
        """Keresés járatszám alapján"""
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

    def listaz_jaratok(self):
        """Összes járat szöveges listája"""
        return [jarat.info() for jarat in self.jaratok]


#  Foglalások kezelése
class JegyFoglalas:
    def __init__(self):
        self.foglalasok = []  # Lista: (név, járat) tuple-ök

    def foglalas(self, nev, jarat, mute=False):
        """Foglalás hozzáadása. Ha mute=True, nem írja ki a sikert."""
        self.foglalasok.append((nev, jarat))
        if not mute:
            print(f"Sikeres foglalás: {nev} - {jarat.jaratszam} ({jarat.jegyar} Ft) (Köszönjük, hogy minket választott!)")

    def lemondas(self, nev, jaratszam):
        """Foglalás törlése név + járatszám alapján"""
        for foglalas in self.foglalasok:
            if foglalas[0] == nev and foglalas[1].jaratszam == jaratszam:
                self.foglalasok.remove(foglalas)
                print("Sikeres lemondás.")
                return
        print("Nincs ilyen foglalás.")

    def listaz_foglalasok(self):
        """Aktív foglalások listázása"""
        if not self.foglalasok:
            print("Nincs aktív foglalás.")
        for nev, jarat in self.foglalasok:
            print(f"{nev} - {jarat.info()}")


# Előre betöltött adatok a rendszer indulásakor
def elore_betoltott_adatok():
    airline = LegiTarsasag("SkyFly")

    # 3 előre definiált járat B= belföld, I= nemzetközi
    j1 = BelfoldiJarat("B100", "Budapest", 8000)
    j2 = BelfoldiJarat("B200", "Szeged", 8000)
    j3 = NemzetkoziJarat("I300", "Isztambul", 100000)

    airline.jarat_hozzaadasa(j1)
    airline.jarat_hozzaadasa(j2)
    airline.jarat_hozzaadasa(j3)

    # 6 előre betöltött foglalás (mute=True: ne írjon ki üzenetet)
    foglalas = JegyFoglalas()
    foglalas.foglalas("Szikszai Konrád", j1, mute=True)
    foglalas.foglalas("Tam Tomi", j2, mute=True)
    foglalas.foglalas("Vicc Elek", j3, mute=True)
    foglalas.foglalas("Mekk Elek", j1, mute=True)
    foglalas.foglalas("Hekk Elek", j2, mute=True)
    foglalas.foglalas("Robban Róbert", j3, mute=True)

    return airline, foglalas


# Egyszerű szöveges felhasználói interfész
def menu():
    airline, foglalasok = elore_betoltott_adatok()
    while True:
        print("\n--- Repülőjegy Foglalási Rendszer ---")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Járatok listázása")
        print("0. Kilépés")
        valasztas = input("Válassz egy lehetőséget: ")

        if valasztas == "1":
            nev = input("Név: ")
            print("Elérhető járatok:")
            for info in airline.listaz_jaratok():
                print(info)
            jaratszam = input("Járatszám: (Kérlek nagy betűt használj!) ")
            jarat = airline.get_jarat(jaratszam)
            if jarat:
                foglalasok.foglalas(nev, jarat)
            else:
                print("Nincs ilyen járatszám.")

        elif valasztas == "2":
            nev = input("Név: ")
            jaratszam = input("Járatszám: ")
            foglalasok.lemondas(nev, jaratszam)

        elif valasztas == "3":
            print("Aktív foglalások:")
            foglalasok.listaz_foglalasok()

        elif valasztas == "4":
            print("Járatok:")
            for info in airline.listaz_jaratok():
                print(info)

        elif valasztas == "0":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás, próbáld újra.")


# A program belépési pontja
if __name__ == "__main__":
    menu()
