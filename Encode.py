import sys

import PQHeap
import bitIO
from Element import Element


def make_frequency(file):
    table = [0] * 256
    while True:
        x = file.read(1)
        if not x:  # End-of-file?
            break
        byte = ord(x)
        bits = bin(byte)[2:].rjust(8, '0')
        table[ord(x)] += 1
    return table


def make_heap(frequency):
    pq = []
    for key in range(len(frequency)):
        e = Element(key, frequency[key])
        PQHeap.insert(pq, e)
    return pq


def merge_nodes(pq):
    while len(pq) > 1:
        zLeft = PQHeap.extractMin(pq)
        zRight = PQHeap.extractMin(pq)
        z = Element(zLeft.key + zRight.key, [zLeft, zRight])
        PQHeap.insert(pq, z)


def huffman_code_tree(node, current_code='', d=[0] * 256):
    if type(node.data) is int:
        return d.insert(node.data, current_code)

    d.append(huffman_code_tree(node.data[0], current_code + '0', d))
    d.append(huffman_code_tree(node.data[1], current_code + '1', d))
    return d


def write_frequency(frequency, out):
    for freq in range(len(frequency)):
        out.writeint32bits(int(frequency[freq]))


def compress(codes, infile, out):
    while True:
        x = infile.read(1)
        if not x:
            break
        code = codes[x[0]]
        for i in range(len(code)):
            out.writebit(codes[i])


if __name__ == '__main__':
    #infile = open(sys.argv[1], 'rb')
    #outfile = open(sys.argv[2], 'wb')

    infile = open('secret.txt', 'rb')
    outfile = open('secretCompressed.txt', 'wb')

    bitstreamin = bitIO.BitReader(infile)
    bitstreamout = bitIO.BitWriter(outfile)

    frequency = make_frequency(infile)
    pq = make_heap(frequency)
    merge_nodes(pq)
    codes = huffman_code_tree(pq[0])
    write_frequency(frequency, bitstreamout)
    compress(codes, infile, bitstreamout)

    bitstreamin.close()
    bitstreamout.close()