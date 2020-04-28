from sys import argv


'''
argv[1] - file with reference genome in fasta format
argc[2] - vcf file
'''


def find_repeat(snp, genome):
    if snp[0] not in genome:
        return
    chr_seq = genome[snp[0]]
    pos, ref, alt = int(snp[1])-1, snp[3], snp[4]
    for len_repeat in range(4,16):
        i = 0
        slice_chr = chr_seq[pos - 2 * len_repeat + 1: pos + 2 * len_repeat]
        slice_alt = chr_seq[pos - 2 * len_repeat + 1: pos] + snp[4] + chr_seq[pos + len(ref): pos + 2 * len_repeat]
        while i < len_repeat:
            pat_before = slice_chr[i:i+len_repeat]
            pat = slice_chr[i+len_repeat:i+len_repeat*2]
            pat_after = slice_chr[i+len_repeat*2: i + len_repeat*3]
            pat_alt = slice_alt[i+len_repeat:i+len_repeat*2]
            if pat_after == pat or pat_before == pat:
                return snp
            if pat_after == pat_alt or pat_before == pat_alt:
                return snp
            i += 1
    return


genome = {}
chr_names = {"chr1": "chr01", "chr2": "chr02", "chr3": "chr03", "chr4": "chr04", "chr5": "chr05", "chr6": "chr06"}

with open(argv[1]) as f:
    while True:
        line = f.readline().strip()
        if line:
            if line.startswith(">"):
                chr_name = line[1:]
                if chr_name in chr_names:
                    chr_name = chr_names[chr_name]
                genome[chr_name] = ""
            else:
                genome[chr_name] = genome[chr_name] + line
        else:
            break


with open(argv[2]) as f:
    while True:
        line = f.readline().strip()
        if line:
            if line.startswith("#"):
                continue
            else:
                snp = line.strip().split("\t")
                res = find_repeat(snp, genome)
                if res:
                    print("\t".join(snp))
        else:
            break
