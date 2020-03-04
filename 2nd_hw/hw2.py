from sys import stdin


gencode = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
    'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W'}

complement_dna = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

weight_rna = {'A': 347.2, 'C': 323.2, 'G': 363.2, 'U': 324.2}
weight_dna = {'A': 331.2, 'C': 307.2, 'G': 347.2, 'T': 322.2}
weight_protein = {'A': 71.04, 'C': 103.01, 'D': 115.03, 'E': 129.04, 'F': 147.07,
                  'G': 57.02, 'H': 137.06, 'I': 113.08, 'K': 128.09, 'L': 113.08,
                  'M': 131.04, 'N': 114.04, 'P': 97.05, 'Q': 128.06, 'R': 156.10,
                  'S': 87.03, 'T': 101.05, 'V': 99.07, 'W': 186.08, 'Y': 163.06}
# don't forget to add 18 (H2O) to the protein

class Dna:
    def __init__(self, seq: str):
        self.chain_1 = seq
        self.chain_2 = self.find_second_chain
        self.max_orf = self.find_longest_orf_coding
        self.rna_orf = self.rna_from_maxorf

    @property
    def find_second_chain(self):
        self.chain_2 = ''
        for nucl in self.chain_1[::-1]:
            if nucl in complement_dna:
                self.chain_2 += complement_dna[nucl]
        return self.chain_2

    @property
    def find_longest_orf_coding(self):
        def orf_from_start(seq_from_start_i):
            orf = ''
            for i in range(0, len(seq_from_start_i) - len(seq_from_start_i)%3, 3):
                codon = seq_from_start_i[i:i + 3]
                if gencode[codon] == '_':
                    return (i, orf)
                else:
                    orf += codon
            return (0, '')

        def find_orf_with_shift(shift, seq):
            max_orf = ''
            max_len = 0
            i = shift
            while i < len(seq) - len(seq[shift:])%3:
                codon = seq[i: i + 3]
                if codon == 'ATG':
                    j, temp_orf = orf_from_start(seq[i:])
                    i += j
                    if len(temp_orf) > max_len:
                        max_orf = temp_orf
                        max_len = len(max_orf)
                else:
                    i += 3
            return max_orf


        self.max_orf = 0
        max_len_orf = 0
        for orf in (find_orf_with_shift(0, self.chain_1), find_orf_with_shift(1, self.chain_1),
                    find_orf_with_shift(2, self.chain_1), find_orf_with_shift(0, self.chain_2),
                    find_orf_with_shift(1, self.chain_2), find_orf_with_shift(2, self.chain_2)):
            if len(orf) > max_len_orf:
                self.max_orf = orf
                max_len_orf = len(self.max_orf)
        return self.max_orf

    @property
    def rna_from_maxorf(self):
        rna = self.max_orf.replace('T', 'U')
        return Rna(rna)

    def weight(self):
        weight = 0
        for nucl in self.max_orf:
            weight += weight_dna[nucl]
            weight += weight_dna[complement_dna[nucl]]
        return round(weight, 1)


class Rna:
    def __init__(self, seq):
        self.seq = seq
        self.protein = self.translation

    def weight(self):
        weight = 0
        for nucl in self.seq:
            weight += weight_rna[nucl]
        return round(weight, 1)

    @property
    def translation(self):
        protein = ''
        for i in range(0, len(self.seq), 3):
            codon = self.seq[i:i + 3].replace('U', 'T')
            protein += gencode[codon]
        return Protein(protein)


class Protein:
    def __init__(self, seq):
        self.seq = seq

    def weight(self):
        weight = 18.02
        for acid_resid in self.seq:
            weight += weight_protein[acid_resid]
        return round(weight, 1)




for path_to_file in stdin:
    with open(path_to_file.strip()) as file:
        name = file.readline().strip()
        sequence = file.read().replace('\n','')
        dna = Dna(sequence.strip())
        rna = dna.rna_orf
        protein = rna.protein

        print('ORF sequence: {}\nMolecular mass: {}\n'.format(dna.max_orf, dna.weight()))
        print('RNA sequence: {}\nMolecular mass: {}\n'.format(rna.seq, rna.weight()))
        print('Protein sequence: {}\nMolecular mass: {}\n'.format(protein.seq, protein.weight()))

# a = Dna('TAAATGATTTGATGAGAAGGTAG')
# print(a.chain_1)
# print(a.chain_2)
# print(a.max_orf)
# print(a.weight())

# rna = a.rna_orf
# print(rna.seq)
# print(rna.weight())
# print(a.rna_orf.translation().weight())
