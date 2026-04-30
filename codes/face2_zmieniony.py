import time 
import csv
import unicodedata
import random 
import math
import matplotlib.pyplot as plt
import string 

def generate_triangle(angle, min_side_length, max_side_length, width, height):
  """
  Generuje trójkąt o równych bokach.

  Args:
    angle: Kąt między bokami trójkąta w stopniach.
    min_side_length: Minimalna długość boku trójkąta.
    max_side_length: Maksymalna długość boku trójkąta.
    width: Szerokość obszaru, w którym generowane są trójkąty.
    height: Wysokość obszaru, w którym generowane są trójkąty.

  Returns:
    Lista współrzędnych wierzchołków trójkąta.
  """

  # Wygeneruj losową długość boku trójkąta.
  side_length = random.randint(min_side_length, max_side_length)

  # Wygeneruj losowe położenie środka ciężkości trójkąta.
  position = (random.randint(0, width), random.randint(0, height))

  # Oblicz współrzędne wierzchołków trójkąta.

  vertices = []
  for i in range(3):
    x = position[0] + int(side_length * math.cos(i * 2 * math.pi / 3 + angle * math.pi / 180))
    y = position[1] + int(side_length * math.sin(i * 2 * math.pi / 3 + angle * math.pi / 180))
    vertices.append((x, y))

  return vertices

# Ustaw parametry funkcji.
min_side_length = 100
max_side_length = 1000
angle = 60
width = 450
height = 550 

def generuj_dwa_trojkaty():
    wspolrzedne = []
    for _ in range(2):  # Generuj dwa trójkąty
        vertices = generate_triangle(angle, min_side_length, max_side_length, width, height)
        wspolrzedne.extend(vertices)
    return wspolrzedne

def generuj_wspolrzedne_rownomiernie():
    x = random.randint(1, 300)
    y = random.randint(1, 300)
    return x, y

def generuj_dwiescie_trojkatow(liczba_serii):
    wspolrzedne = []
    for _ in range(liczba_serii):
        for _ in range(2):  # Generuj dwa trójkąty
            trojkat = [generuj_wspolrzedne_rownomiernie() for _ in range(3)]
            wspolrzedne.extend(trojkat)
    return wspolrzedne

def zamien_na_liste_wartosci(wspolrzedne):
    lista_wartosci = [coord for point in wspolrzedne for coord in point]
    return lista_wartosci

def przemieszaj_wartosci(lista_wartosci):
    polowa_dlugosci = len(lista_wartosci) // 2
    przemieszane = [val for pair in zip(lista_wartosci[:polowa_dlugosci], lista_wartosci[polowa_dlugosci:][::-1]) for val in pair]
    return przemieszane

def przelicz_na_binarny(przemieszane_wartosci):
    binarne_wartosci = []
    for val in przemieszane_wartosci:
        if val < 0:
            binarna = bin((1 << 16) + val)[2:]  # 16-bitowa reprezentacja binarna
        else:
            binarna = bin(val)[2:]
        binarne_wartosci.append(binarna.zfill(16))  # Uzupełnienie zerami do 16 bitów
    return binarne_wartosci

def zlacz_binarnie(binarne_wartosci):
    zlaczone_binarnie = ''.join(binarne_wartosci)
    return zlaczone_binarnie

def generuj_timestamp():
    return int(time.time() * 1000)


def przetworz_binarna_liczbe(polaczona_bin):
    # Dzielimy na bloki po 4 bity
    bloki = [polaczona_bin[i:i+4] for i in range(0, len(polaczona_bin), 4)]

    # Przemieszanie (naprzemienne łączenie pierwszej połowy z odwróconą drugą)
    polowa = len(bloki) // 2
    przemieszane = [val for pair in zip(bloki[:polowa], bloki[polowa:][::-1]) for val in pair]

    # Zamiana miejscami nieparzystych bloków: 1 z 3, 5 z 7 itd.
    for i in range(1, len(przemieszane) - 2, 4):
        przemieszane[i], przemieszane[i + 2] = przemieszane[i + 2], przemieszane[i]

    # Przeniesienie ostatniego bloku na początek
    przemieszane = [przemieszane[-1]] + przemieszane[:-1]

    # Scal
    return ''.join(przemieszane)

    bloki = [liczba_binarna[i:i+4].zfill(4) for i in range(0, len(liczba_binarna), 4)]
    
    # Przemieszaj bloki
    polowa_dlugosci = len(bloki) // 2
    przemieszane_bloki = [val for pair in zip(bloki[:polowa_dlugosci], bloki[polowa_dlugosci:][::-1]) for val in pair]
    
    # Przenieś ostatni blok na początek
    przemieszane_bloki = [przemieszane_bloki[-1]] + przemieszane_bloki[:-1]
    
    # Połącz z powrotem w dużą liczbę binarną
    nowa_liczba_binarna = ''.join(przemieszane_bloki)
    
    # Zaneguj co dziesiąty bit
    nowa_liczba_binarna = ''.join('1' if i % 10 == 9 and bit == '0' else '0' if i % 10 == 9 and bit == '1' else bit for i, bit in enumerate(nowa_liczba_binarna))
    
    # Wykonaj XOR na czterech pierwszych bitach liczby binarnej i timestamp_bin
    liczba_binarna_xor = ''.join(str(int(nowa_liczba_binarna[i]) ^ int(timestamp_bin[i])) for i in range(4)) + nowa_liczba_binarna[4:]
    
    # Przenieś cztery pierwsze bity timestamp_bin na koniec liczby binarnej
    wynikowa_liczba_binarna = liczba_binarna_xor + timestamp_bin[:4]
    
    return wynikowa_liczba_binarna

def binarna_na_ascii(liczba_binarna):
    dopuszczalne = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    bloki_8_bitowe = [liczba_binarna[i:i+8] for i in range(0, len(liczba_binarna), 8)]
    ascii_znaki = []
    for blok in bloki_8_bitowe:
        val = int(blok, 2)
        znak = dopuszczalne[val % len(dopuszczalne)]  # ograniczamy do bezpiecznych znaków
        ascii_znaki.append(znak)
    return ''.join(ascii_znaki)

def ascii_na_binarna(ascii_string):
    binarna_lista = [bin(ord(znak))[2:].zfill(8) for znak in ascii_string]
    return ''.join(binarna_lista)

def binarna_na_liczby(binarna):
    liczby = [int(binarna[i:i+8], 2) for i in range(0, len(binarna), 8)]
    return liczby

def main():
    for i in range(1000):
        #wspolrzedne = generuj_dwiescie_trojkatow(1)
        wspolrzedne = generuj_dwa_trojkaty()
        print("Współrzędne przed przemieszaniem:", wspolrzedne)

        lista_wartosci = zamien_na_liste_wartosci(wspolrzedne)
        przemieszane_wartosci = przemieszaj_wartosci(lista_wartosci)
        print("Wartości po przemieszaniu:", przemieszane_wartosci)

        binarne_wartosci = przelicz_na_binarny(przemieszane_wartosci)
        zlaczone_binarnie = zlacz_binarnie(binarne_wartosci)
        print("Złączona liczba binarna:", zlaczone_binarnie)

        # Generuj dwa znaczniki czasowe
        timestamp1 = generuj_timestamp()
        timestamp2 = generuj_timestamp()

        # Binarnie
        timestamp_bin1 = bin(timestamp1)[2:].zfill(64)
        timestamp_bin2 = bin(timestamp2)[2:].zfill(64)
        timestamp_bin = timestamp_bin1 + timestamp_bin2

        # Przetwarzanie timestampów jako lista int do przemieszania
        timestamp_bits = [int(b) for b in timestamp_bin]
        timestamp_bits = przemieszaj_wartosci(timestamp_bits)
        timestamp_bin = ''.join(str(b) for b in timestamp_bits)

        # Sklejenie liczby i timestampów
        duza_liczba_binarna = zlaczone_binarnie + timestamp_bin

        # Nowe przetwarzanie 10x
        for _ in range(10):
            duza_liczba_binarna = przetworz_binarna_liczbe(duza_liczba_binarna)
        duza_liczba_binarna = zlaczone_binarnie
        for _ in range(10):
            duza_liczba_binarna = przetworz_binarna_liczbe(duza_liczba_binarna)
        print("Wynik:", duza_liczba_binarna)

        ascii_znak = binarna_na_ascii(duza_liczba_binarna)
        print("Znak ASCII:", ascii_znak)

        # Konwertuj z powrotem do wartości
        binarna_ze_znaku = ascii_na_binarna(ascii_znak)
        liczby_z_binarnej = binarna_na_liczby(binarna_ze_znaku)
        print("Oryginalne wartości z binarnej:", liczby_z_binarnej)

        with open("output.txt", "a") as f:
            print(i + 1, " coords:", wspolrzedne, file=f)
            print(i + 1, " przemieszane wartosci:", przemieszane_wartosci, file=f)
            print(i + 1, " binarne wartosci:", duza_liczba_binarna, file=f)
            print(i + 1, " klucz:", ascii_znak, file=f)
            print(i + 1, " oryginalne wartości:", liczby_z_binarnej, file=f)
            print("--------------------", file=f)
            print("Długość binarnego klucza (w bitach):", len(duza_liczba_binarna))
            print("Długość klucza ASCII (w bitach):", len(ascii_znak) * 8)

        with open("output.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([i + 1, wspolrzedne, duza_liczba_binarna, ascii_znak])
        
        with open("test.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ascii_znak])

if __name__ == "__main__":
    main()