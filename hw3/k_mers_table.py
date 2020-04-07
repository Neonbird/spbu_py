from math import factorial
from itertools import combinations_with_replacement

# k = int(input())
# seq = input()
# m_size = factorial(3 + k) / (factorial(k) * 6)
# table = [None for i in range(m_size)]

def nucl_to_fourth(kmer):
    nuc_to_num = {'A': 0, 'T': 1,
                "G": 2, "C": 3}
    num_to_nuc = {0: "A", 1: "T",
                  2: "G", 3: "C"}
    kmer = list(kmer)


def hash_fun(kmer: str, m_size: int):
    hash = 0
    i = 1
    for nucl in reversed(kmer):
        if nucl == 'A':
            hash += i*1
        elif nucl == 'C':
            hash += i*2
        elif nucl == 'G':
            hash += i*3
        else:
            hash += i*4
        i = i*10
    return hash % m_size

k = 4
m_size = factorial(3 + k) / (factorial(k) * 6)
kmers = combinations_with_replacement('ACGT', 4)
d = []
for i in kmers:
    d.append(hash_fun(i, m_size))

print(d)




