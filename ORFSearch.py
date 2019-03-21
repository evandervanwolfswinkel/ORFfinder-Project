import re

import regex as re
from Bio import SeqIO

from ORFObject import ORF


def main():
    record = SeqIO.parse("testfasta.fa", "fasta")
    calculateORF(record)


def calculateORF(records):
    orfobject_list = []
    for record in records:
        for strand, seq in (1, record.seq), (-1, record.seq.reverse_complement()):
            for frame in range(3):
                index = frame
                while index < len(record) - 6:
                    match = re.match('(ATG(?:\S{3})*?T(?:AG|AA|GA))', str(seq[index:]))
                    if match:
                        orf = match.group()
                        index += len(orf)
                        if len(orf) > 100:
                            pos = str(record.seq).find(orf) + 1
                            ORFobject = ORF(orf, len(orf), strand, frame, record.id)
                            orfobject_list.append(ORFobject)

                    else:
                        index += 3
    return orfobject_list

main()