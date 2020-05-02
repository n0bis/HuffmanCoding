""""
    Kort sagt er opgaven at overføre bogens pseudo-kode for prioritetskøer til
    et Python-program og og derefter testen det, bl.a. ved at bruge det til at
    sortere tal.

    :Gruppe medlemmer:
        Mads Falkenstrøm - mafal17
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

