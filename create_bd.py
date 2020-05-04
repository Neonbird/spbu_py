import sqlite3


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


class Dna:
    def __init__(self, seq: str):
        self.chain_1 = seq
        self.chain_2 = self.find_second_chain
        self.orfs = self.find_orfs

    @property
    def find_second_chain(self):
        self.chain_2 = ''
        for nucl in self.chain_1[::-1]:
            if nucl in complement_dna:
                self.chain_2 += complement_dna[nucl]
        return self.chain_2

    @property
    def find_orfs(self):
        def orf_from_start(seq_from_start_i):
            orf = ''
            for i in range(0, len(seq_from_start_i) - len(seq_from_start_i) % 3, 3):
                codon = seq_from_start_i[i:i + 3]
                if gencode[codon] == '_':
                    if len(orf) >= 100:
                        return (i, orf)
                    else:
                        return (i, None)
                else:
                    orf += codon
            return None

        def find_orf_with_shift(shift, seq):
            orfs = []
            i = shift
            while i < len(seq) - len(seq[shift:]) % 3:
                codon = seq[i: i + 3]
                if codon == 'ATG':
                    local_orf = orf_from_start(seq[i:])
                    if local_orf:
                        j, temp_orf = local_orf
                        if temp_orf:
                            orfs.append(temp_orf)
                        i += j
                    else:
                        return orfs
                else:
                    i += 3
            return orfs


        self.orfs = []
        self.orfs += find_orf_with_shift(0, self.chain_1)
        self.orfs += find_orf_with_shift(1, self.chain_1)
        self.orfs += find_orf_with_shift(2, self.chain_1)
        self.orfs += find_orf_with_shift(0, self.chain_2)
        self.orfs += find_orf_with_shift(1, self.chain_2)
        self.orfs += find_orf_with_shift(2, self.chain_2)

        return self.orfs


class Rna:
    def __init__(self, seq):
        self.seq = seq
        self.protein = self.translation

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


def rna_from_dna(dna_seq):
    rna = dna_seq.replace('T', 'U')
    return Rna(rna)


def weight_count(seq, type):
    weight_rna = {'A': 347.2, 'C': 323.2, 'G': 363.2, 'U': 324.2}
    weight_dna = {'A': 331.2, 'C': 307.2, 'G': 347.2, 'T': 322.2}
    weight_protein = {'A': 71.04, 'C': 103.01, 'D': 115.03, 'E': 129.04, 'F': 147.07,
                      'G': 57.02, 'H': 137.06, 'I': 113.08, 'K': 128.09, 'L': 113.08,
                      'M': 131.04, 'N': 114.04, 'P': 97.05, 'Q': 128.06, 'R': 156.10,
                      'S': 87.03, 'T': 101.05, 'V': 99.07, 'W': 186.08, 'Y': 163.06}
    weight = 0
    if type == "dna":
        weight_dict = weight_dna
    elif type == "rna":
        weight_dict = weight_rna
    elif type == "protein":
        weight_dict = weight_protein
        weight += 18
    for el in seq:
        weight += weight_dict[el]
        if type == "dna":
            weight += weight_dict[complement_dna[el]]
    return int(round(weight, 0))


connection = sqlite3.connect("orfs.db")
crsr = connection.cursor()

sql_command = """ CREATE TABLE IF NOT EXISTS orf_table (
id INTEGER PRIMARY KEY,
dna VARCHAR,
dna_w INTEGER, 
rna VARCHAR,
protein VARCHAR,
protein_w INTEGER
);"""
crsr.execute(sql_command)

seq_file = input("Enter filename with seq: ")
with open(seq_file.strip()) as file:
    name = file.readline().strip()
    sequence = file.read().replace('\n','')

dna = Dna(sequence.strip())
orfs = dna.orfs
for orf in dna.orfs:
    dna_weight = weight_count(orf, "dna")
    rna = rna_from_dna(orf)
    protein = rna.protein
    protein_weight = weight_count(protein.seq, "protein")
    sql_command = """INSERT INTO orf_table 
    (dna, dna_w, rna, protein, protein_w)
    VALUES (?, ?, ?, ?, ?)"""
    data = (orf, dna_weight, rna.seq, protein.seq, protein_weight)
    crsr.execute(sql_command, data)
    connection.commit()

request_seq = input("Enter type of request (dna/protein): ").strip()
request_w = int(input("Enter weight of request: ").strip())
if request_seq == "dna":
    crsr.execute("SELECT dna FROM orf_table WHERE dna_w=?", [(request_w)])
    print(crsr.fetchall())
elif request_seq == "protein":
    crsr.execute("SELECT protein FROM orf_table WHERE protein_w=?", [(request_w)])
    print(crsr.fetchall())
