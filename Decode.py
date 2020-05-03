import sys

import PQHeap
import bitIO
from Element import Element
from Encode import make_heap, merge_nodes, huffman_code_tree


def decode_text(current_code, root):
    current = root[0]
    result = ''
    if type(current_code) is int:
        return
    for code in current_code:
        if int(code) == 0:
            current = current.data[0]
        else:
            current = current.data[1]
        if type(current.data) is int:
            result += str(current.data)
            current = root[0]
    return result


def decompress(codes, bitstreamin, out, file, total, pq):
    for bit in range(total):
        x = file.read(1)
        code = decode_text(codes[ord(x)], pq)
        print(code)
        if code:
            out.write(bytes(code))


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
    decompress(codes, bitstreamin, outfile, infile, total, pq)

    bitstreamin.close()
    outfile.close()