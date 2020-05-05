import PQHeap
from Element import Element
import bitIO

class Huffman:

    def __init__(self, infile, outfile):
        self.table = [0] * 256
        self.codes = [0] * 256
        self.reverse_mapping = {}
        self.infile = infile
        self.outfile = outfile
        self.bitstreamin = bitIO.BitReader(infile)
        self.bitstreamout = bitIO.BitWriter(outfile)

    def make_frequency(self):
        while True:
            x = self.infile.read(1)
            if not x:  # End-of-file?
                break
            byte = ord(x)
            bits = bin(byte)[2:].rjust(8, '0')
            self.table[byte] += 1
        self.infile.seek(0) # return file pointer to start of file
        return self.table

    def make_heap(self, frequency):
        pq = []
        for key in range(len(frequency)):
            e = Element(frequency[key], key)
            PQHeap.insert(pq, e)
        return pq

    def merge_nodes(self, pq):
        while len(pq) > 1:
            left = PQHeap.extractMin(pq)
            right = PQHeap.extractMin(pq)
            z = Element(left.key + right.key, [left, right])
            PQHeap.insert(pq, z)
        return PQHeap.extractMin(pq)

    def make_code(self, root, current_code=''):
        if type(root.data) is int:
            self.codes[root.data] = current_code + '1'
            return

        self.make_code(root.data[0], current_code + '0')
        self.make_code(root.data[1], current_code + '1')

    def write_frequency(self, frequency):
        for freq in range(len(frequency)):
            self.bitstreamout.writeint32bits(int(frequency[freq]))

    def read_frequency(self):
        table = [0] * 256
        for i in range(len(table)):
            table[i] = self.bitstreamin.readint32bits()
        return table

    def compress(self):
        frequency = self.make_frequency()
        pq = self.make_heap(frequency)
        root = self.merge_nodes(pq)
        self.make_code(root)
        self.write_frequency(frequency)

        while True:
            x = self.infile.read(1)
            if not x:
                break
            code = self.codes[ord(x)]
            if code:
                for bit in code:
                    self.bitstreamout.writebit(int(bit))

        self.bitstreamin.close()
        self.bitstreamout.close()

    def decompress(self):
        frequency = self.read_frequency()
        pq = self.make_heap(frequency)
        root = self.merge_nodes(pq)
        total = sum(frequency)  # sum of bytes in original file

        element = root
        while total > 0:
            x = self.bitstreamin.readbit()
            if type(element.data) is int:
                self.outfile.write(bytes([element.data]))
                total = total - 1
                element = root
            else:
                element = element.data[x]

        self.bitstreamin.close()
        self.bitstreamout.close()
