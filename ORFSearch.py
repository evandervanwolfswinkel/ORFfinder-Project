import pickle
import re
from io import StringIO

from Bio import SeqIO

from ORFObject import ORF


# Auteur: Evander van Wolfswinkel
# Created: 22-3-2019
# Functionality: Searches a fasta input on Open Reading Frames
# (ORF), also creates ORFObjects and can de/serialize them
# Known Bugs: No known Bugs

# Serializes ORF object list into a file
def serializeORF(input):
    """Serializes ORF for later use"""
    with open('serORF', 'wb') as serializedORFfile:
        pickle.dump(input, serializedORFfile)


# Deserializes ORF object list from a file
def deserializeORF():
    """Deserializes ORF for use"""
    with open('serORF', 'rb') as serializedORFfile:
        orf_list = pickle.load(serializedORFfile)
    return orf_list


# Process input depending on input-type, if input is given as a file, it needs to be decoded
# from binary to utf-8 text format for StringIO string buffer (places it into memory)
def processInput(input, inputtype):
    """Pre processes input depending on type"""
    if inputtype == "raw":
        fasta = StringIO(input)
    if inputtype == "file":
        fasta = StringIO(input.decode('utf-8'))
        """ If byte type, decode to utf-8."""
    return fasta
# Calculates ORF for input, supports both raw fasta input
# and byte input from file
# Returns ORF object list
def calculateORF(input, inputtype):
    """Calculates ORF based on different input types"""
    fasta = processInput(input, inputtype)
    records = SeqIO.parse(fasta, "fasta")  # Fasta string buffer gets parsed
    orfobject_list = []  # into SeqIO records object
    for record in records:
        for strand, seq in (1, record.seq), (-1, record.seq.reverse_complement()):
            """ For strand (header) and sequence, creates 6 different reading frames, 3 in
             both directions using the 1 and -1 on the reverse strand."""
            for frame in range(3):
                index = frame
                while index < len(record) - 6:
                    """ Uses an index based on the 3 range from both strands, and the length of the record to match an 
                    regular expression. """
                    match = re.match('(ATG(?:\S{3})*?T(?:AG|AA|GA))', str(seq[index:]))
                    if match:
                        orf = match.group()  # .group() returns the regex match
                        index += len(orf)
                        if len(orf) > 100:
                            """ If orf length is longer than 100. Make ORF object."""
                            pos = str(record.seq).find(orf) + 1  # unused position variable
                            ORFobject = ORF(orf, len(orf), strand, frame, record.id)
                            orfobject_list.append(ORFobject)
                            """ ORF objects made and then added to orf object list."""

                    else:
                        index += 3
    return orfobject_list

