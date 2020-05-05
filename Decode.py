import sys

from huffman import Huffman

if __name__ == '__main__':
    infile = open(sys.argv[1], 'rb')
    outfile = open(sys.argv[2], 'wb')

    h = Huffman(infile, outfile)
    h.decompress()
