import sys

import PQHeap
import bitIO
from Element import Element
from Encode import make_heap, merge_nodes, huffman_code_tree


def decode_text():
    pass


def decompress(codes, bitstreamin, out):
    print(codes)
    while True:
        x = bitstreamin.readbit()
        print(x)
        if not bitstreamin.readsucces(): # End-of-file?
            break
    print(x)


def read_frequency(bitstreamin):
    table = [0] * 256
    for i in range(len(table)):
        table[i] = bitstreamin.readint32bits()
    return table


if __name__ == '__main__':
    # infile = open(sys.argv[1], 'rb')
    # outfile = open(sys.argv[2], 'wb')

    infile = open('secretCompressed.txt', 'rb')
    outfile = open('secretDecoded.txt', 'wb')

    bitstreamin = bitIO.BitReader(infile)
    bitstreamout = bitIO.BitWriter(outfile)

    frequency = read_frequency(bitstreamin)
    pq = make_heap(frequency)
    merge_nodes(pq)
    codes = huffman_code_tree(pq[0])
    total = sum(frequency) # sum of bytes in original file
    decompress(codes, bitstreamin, bitstreamout)

    bitstreamin.close()
    bitstreamout.close()