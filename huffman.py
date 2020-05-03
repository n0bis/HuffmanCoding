import PQHeap
from Element import Element
import bitIO

class Huffman:

    def __init__(self, infile, outfile):
        self.table = [0] * 256
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

    def huffman_code_tree(self, node, current_code='', d=[0] * 256):
        if type(node.data) is int:
            d[node.data] = current_code
            return

        self.huffman_code_tree(node.data[0], current_code + '0', d)
        self.huffman_code_tree(node.data[1], current_code + '1', d)
        return d

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
        self.merge_nodes(pq)
        codes = self.huffman_code_tree(pq[0])
        self.write_frequency(frequency)

        self.infile.seek(0)
        while True:
            x = self.infile.read(1)
            if not x:
                break
            code = codes[ord(x)]
            if code:
                for bit in code:
                    self.bitstreamout.writebit(int(bit))

        self.bitstreamin.close()
        self.bitstreamout.close()

    def decompress(self):

        frequency = self.read_frequency()
        pq = self.make_heap(frequency)
        self.merge_nodes(pq)
        codes = self.huffman_code_tree(pq[0])
        total = sum(frequency)  # sum of bytes in original file

        element = pq[0]
        while total > 0:
            x = self.bitstreamin.readbit()
            print(x)
            if type(element.data) is int:
                self.outfile.write(bytes([element.data]))
                total = total - 1
                element = pq[0]
            else:
                element = element.data[x]

        self.bitstreamin.close()
        self.bitstreamout.close()