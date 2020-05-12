""""
    At lave dit eget værktøj til at komprimere filer.
    Komprimeringen skal ske via Huffman-kodning. Der skal laves to
    programmer: et til at kode/komprimere en fil, og et til dekode den igen.

    Opgave 1:
        I opgave 1 skal man bruge kaldet read(1) fra file objects til
        at læse bytes fra inputfilen (den originale fil). Man skal bruge metoderne writeint32bits(intvalue) og writebit(bit) fra klassen BitWriter i biblioteket bitIO.py til at skrive heltal (for hyppighedstabel) og bits (for Huffmans-koderne) til outputfilen (den
        komprimerede fil). Begge filer skal åbnes i “binary mode”. Når en
        BitWriter instantieres, skal den have et file object som argument.

    Opgave 2:
        I opgave 2 skal man bruge metoderne readint32bits()
        og readbit() fra klassen BitReader fra det udleverede bibliotek bitIO.py til at læse heltal (for hyppighedstabel) og bits (for
        Huffmans-koderne) fra inputfilen (den komprimerede fil). Man skal
        bruge kaldet write(bytes([b])) (hvor write() er fra file objects
        og bytes() er en built-in funktion) til skrive bytes til outputfilen
        (den genskabte originale fil). Her er b et heltal som repræsenterer
        den byte, som skal skrives. Begge filer skal ˚abnes i “binary mode”.
        Når en BitReader instantieres, skal den have et file object som
        argument.

    :Gruppe medlemmer:
        Mads Emil Falkenstrøm, mafal17@student.sdu.dk
        Mathias Birkebjerg Kristiansen, matkr18@student.sdu.dk
        Patrick Nielsen, panie18@student.sdu.dk
"""

import sys
import os
from os import listdir

from huffman import Huffman

if __name__ == '__main__':
    #infile = open(sys.argv[1], 'rb')
    #outfile = open(sys.argv[2], 'wb')
    path = './testfiles/'
    for filename in listdir(path):
        print(filename)
        filename, file_extension = os.path.splitext(filename)
        infile = open(f'{path}{filename}{file_extension}', 'rb')
        outfile = open(f'{path}{filename}_compressed{file_extension}', 'wb')
        h = Huffman(infile, outfile)
        h.compress()
