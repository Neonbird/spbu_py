from sys import stdin
from itertools import product


def kmer_to_fourth(kmer: str):
    nuc_to_num = {'A': "0", 'T': "1",
                  "G": "2", "C": "3"}
    numeric_str = ""
    for nucl in kmer:
        numeric_str += (nuc_to_num[nucl])
    return numeric_str


def hash_for_kmer(number):
    number = list(number)
    number = [int(x) for x in number]
    num_base_ten = 0
    for index, numeral in enumerate(number[::-1]):
        num_base_ten += int(numeral) * (4 ** index)
    return num_base_ten


def fourth_kmer_from_hash(hash_k, num_res_base=None):
    if num_res_base is None:
        num_res_base = []
    remainder = hash_k % 4
    quotient = hash_k // 4
    num_res_base.append(remainder)
    if quotient < 4:
        num_res_base.append(quotient)
    else:
        fourth_kmer_from_hash(quotient, num_res_base)
    return num_res_base[::-1]


def make_hash_table(seq: str, k: int):
    m = len(list(product(['A', 'C', 'G', 'T'], repeat=k)))
    hash_table = [[0, None, None] for i in range(m)]
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        kmer_fourth = kmer_to_fourth(kmer)
        kmer_hash = hash_for_kmer(kmer_fourth)
        hash_table[kmer_hash][0] += 1
        if not hash_table[kmer_hash][1] or hash_table[kmer_hash][1] > i:
            hash_table[kmer_hash][1] = i
        if not hash_table[kmer_hash][2] or hash_table[kmer_hash][2] < i:
            hash_table[kmer_hash][2] = i
    return hash_table


def print_kmers_table(hash_table, k):
    for i_line in range(len(hash_table)):
        if hash_table[i_line][0] != 0:
            fourth_kmer = ''.join([str(i) for i in fourth_kmer_from_hash(i_line)])
            if len(fourth_kmer) < k:
                fourth_kmer = "A"*(k - len(fourth_kmer)) + fourth_kmer
            kmer = fourth_kmer.translate(str.maketrans({'0': 'A', '1': 'T', '2': 'G', '3': 'C'}))
            reversed(kmer)
            print('{}\t{}\t{}\t{}'.format(kmer, hash_table[i_line][0], hash_table[i_line][1], hash_table[i_line][2]))


if __name__ == "__main__":
    k = int(input("k value: "))
    for path_to_file in stdin:
        with open(path_to_file.strip()) as file:
            name = file.readline().strip()
            seq = file.read().replace('\n', '')
        hash_table = make_hash_table(seq, k)
        print_kmers_table(hash_table, k)
