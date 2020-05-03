import sys

from huffman import Huffman

if __name__ == '__main__':
    # infile = open(sys.argv[1], 'rb')
    # outfile = open(sys.argv[2], 'wb')

    infile = open('secretCompressed.txt', 'rb')
    outfile = open('secretDecoded.txt', 'wb')

    h = Huffman(infile, outfile)
    h.decompress()
