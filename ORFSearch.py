import pickle
import re
from io import StringIO

from Bio import SeqIO

from ORFObject import ORF


def serializeORF(input):
    with open('serORF', 'wb') as serializedORFfile:
        pickle.dump(input, serializedORFfile)


def deserializeORF():
    with open('serORF', 'rb') as serializedORFfile:
        orf_list = pickle.load(serializedORFfile)
    return orf_list


def calculateORF(input, inputtype):
    if inputtype == "raw":
        fasta = StringIO(input)
    if inputtype == "file":
        fasta = StringIO(input.decode('utf-8'))
    records = SeqIO.parse(fasta, "fasta")
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

