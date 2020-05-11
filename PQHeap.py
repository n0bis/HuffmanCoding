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

from math import floor


def minHeapify(A, i):
    """
       Maintaining the min-heap property

       :param list A: The priority queue
       :param int i: The current index
    """
    l = left(i)
    r = right(i)
    if l <= len(A) - 1 and A[l] < A[i]:
        lowest = l
    else:
        lowest = i
    if r <= len(A) - 1 and A[r] < A[lowest]:
        lowest = r
    if lowest != i:
        A[i], A[lowest] = A[lowest], A[i]
        minHeapify(A, lowest)


def extractMin(A):
    """
       Extracting the minimum value from the priority queue

       :param list A: The priority queue
       :return int min: The minimum value
    """
    min = A[0]
    A[0], A[len(A) - 1] = A[len(A) - 1], A[0]
    A.pop()

    minHeapify(A, 0)
    return min


def insert(A, key):
    """
       Inserts a new value onto the priority queue

       :param list A: The priority queue
       :param int key: The value to be inserted into the priority queue
    """
    A.append(key)
    i = len(A) - 1
    while i >= 0 and A[parent(i)] > A[i]:
        A[parent(i)], A[i] = A[i], A[parent(i)]
        i = parent(i)


def left(i):
    """
       Finding left leaf node position for a parent node

       :param int i: index of parent node
       :return int i: index in the heap
    """
    return 2 * i + 1


def right(i):
    """
       Finding right leaf node position for a parent node

       :param int i: index of parent node
       :return int i: index in the heap
    """
    return 2 * i + 2


def parent(i):
    """
       Finding leaf parent node

       :param int i: index of leaf node
       :return int i: index in the heap
    """
    return floor((i - 1) / 2)

