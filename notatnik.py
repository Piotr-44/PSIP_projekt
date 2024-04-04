# blad inklinacja
import math
def blad_inklinacji ():
    x = float(input("Wprowadz wartosc 1 polozenia lunety: "))
    y = float(input("Wprowadz wartosc 2 polozenia lunety: "))
    z = float(input("Wprowadz wartosc kata zenitalnego: "))
    c = float(input("Wprowadz wartosc bledu kolimacji: "))
    while True:
        i = round(((y-x+200)/2)*math.atan(z)-(c/math.cos(z)), 4)
        return print(f"Błąd wynosi: {i}")

blad_inklinacji()