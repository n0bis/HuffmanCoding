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

import PQHeap
from Element import Element
import bitIO

class Huffman:

    def __init__(self, infile, outfile):
        self.table = [0] * 256
        self.codes = [0] * 256
        self.infile = infile
        self.outfile = outfile
        self.bitstreamin = bitIO.BitReader(infile)
        self.bitstreamout = bitIO.BitWriter(outfile)

    def make_frequency(self):
        """
            count the frequency of a byte in file and fill-out table

            :return list table: the frequency table
        """
        while True:
            x = self.infile.read(1)
            if not x:  # End-of-file?
                break
            byte = ord(x)
            self.table[byte] += 1
        self.infile.seek(0) # return file pointer to start of file
        return self.table

    def make_heap(self, frequency):
        """
            building the huffman tree structure

            :param list frequency: the frequency table
            :return list pq: The priority queue
        """
        pq = []
        for key, freq in enumerate(frequency):
            PQHeap.insert(pq, Element(freq, key))
        return pq

    def merge_nodes(self, pq):
        """
            extracts the two minimum values, merges them and puts into the queue

            :param list pq: The priority queue
            :return int: the minimum value
        """
        while len(pq) > 1: # has elements in list
            left = PQHeap.extractMin(pq)
            right = PQHeap.extractMin(pq)
            z = Element(left.key + right.key, [left, right])
            PQHeap.insert(pq, z)
        return PQHeap.extractMin(pq)

    def make_code(self, root, current_code=''):
        """
            generates code path from root - of characters in the tree structure till leaf is hot
            Traverse the tree structure using in-order traversal.
            First traverse the left subtrees and append 0
            Then traverse the right subtrees and append 1

            :param Element root:
            :param str current_code:
            :return:
        """
        if type(root.data) is int: # leaf is hit
            self.codes[root.data] = current_code + '1' # bug? character is placed at index 1 in path
            return

        self.make_code(root.data[0], current_code + '0')
        self.make_code(root.data[1], current_code + '1')

    def write_frequency(self, frequency):
        """
            writes the frequency table to the files first 32 bits

            :param list frequency: the frequency table
            :return:
        """
        for i, freq in enumerate(frequency):
            self.bitstreamout.writeint32bits(int(freq))

    def read_frequency(self):
        """
            creates the frequency table from the files first 32 bits

            :return list table: the frequency table
        """
        self.table = [self.bitstreamin.readint32bits() for _ in [0] * 256]
        return self.table

    def compress(self):
        """
            compresses the input file

            :return:
        """
        frequency = self.make_frequency()
        pq = self.make_heap(frequency)
        root = self.merge_nodes(pq)
        self.make_code(root)
        self.write_frequency(frequency)

        while True:
            x = self.infile.read(1)
            if not x: # End-of-file?
                break
            code = self.codes[ord(x)] # lookup code
            if code:
                for bit in code: # write each bit to file - right-fill with 0's
                    self.bitstreamout.writebit(int(bit))

        self.bitstreamin.close()
        self.bitstreamout.close()

    def decompress(self):
        """
            decompresses the compresses input file

            :return:
        """
        frequency = self.read_frequency()
        pq = self.make_heap(frequency)
        root = self.merge_nodes(pq)
        total = sum(frequency)  # sum of bytes in original file

        element = root
        while total > 0:
            x = self.bitstreamin.readbit()
            if type(element.data) is int: # if leaf is hit
                self.outfile.write(bytes([element.data]))
                total = total - 1 # bytes read
                element = root
            else:
                element = element.data[x] # navigate through tree structure

        self.bitstreamin.close()
        self.bitstreamout.close()
