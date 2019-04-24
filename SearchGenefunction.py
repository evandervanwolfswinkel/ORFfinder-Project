import os
from io import StringIO

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

from BLASTObject import blast


# Auteur: Evander van Wolfswinkel
# Created: 27-3-2019
# Functionality: Blasts both raw fasta input and ORF objects list
# input and returns the information in blast objects list
# Known Bugs: No known Bugs



def removeTempfasta():
    """If temporary fasta exists, delete it"""
    if os.path.exists("tempfasta.fa"):
        os.remove("tempfasta.fa")


def setEvalue():
    """Set the E-value and return it"""
    E_value_thresh = 0.04
    return E_value_thresh


def writeTempfasta(stringiofasta):
    """Write a temporary fasta file (needed for blast)"""
    with open("tempfasta.fa", 'a') as fastafile:
        fastafile.write(stringiofasta.getvalue())


def openTempfasta():
    """Open temporary fasta file"""
    fasta_string = open("tempfasta.fa").read()
    return fasta_string


def performQBlast(fastafile):
    """Perform qblast on fastafile"""
    result_handle = NCBIWWW.qblast("blastn", "nt", fastafile)
    return result_handle


def iterateBlastrecord(blast_records, E_value_thresh):
    """Iterates the blast record and puts the information into a Blast object list"""
    blast_result_list = []
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_value_thresh:
                    sequenceName = alignment.title
                    length = alignment.length
                    Evalue = hsp.expect
                    blastresult = blast(sequenceName, length, Evalue)
                    blast_result_list.append(blastresult)
    return blast_result_list


def transformORFtoFasta(input):
    """Transforms the ORFs into a fasta so it can be blasted"""
    fasta = ""
    for ORF in input:
        ORFseq = ORF.get_sequence()
        ORFheader = ORF.get_header()
        fasta += ">" + ORFheader + "\n"
        fasta += ORFseq + "\n"
    return fasta


# Blasts raw fasta input, saves it to temporary file and then
# Uses NCBIWWW.qblast to blast for gene function
# Returns: Blast object list
def BLASTraw(fasta):
    """Blast raw fasta sequence input"""
    removeTempfasta()
    E_value_thresh = setEvalue()
    writeTempfasta(StringIO(fasta))
    result_handle = performQBlast(openTempfasta())
    removeTempfasta()
    blast_records = NCBIXML.parse(result_handle)
    blast_result_list = iterateBlastrecord(blast_records, E_value_thresh)
    result_handle.close()
    return blast_result_list

# Blasts orf object list input, saves it to temporary file and then
# Uses NCBIWWW.qblast to blast for gene function
# Returns: Blast object list
def BLASTorf(input):
    """Blasts orf object list input"""
    removeTempfasta()
    E_value_thresh = setEvalue()
    fastaformat = StringIO(transformORFtoFasta(input))
    writeTempfasta(fastaformat)
    result_handle = performQBlast(openTempfasta())
    removeTempfasta()
    blast_records = NCBIXML.parse(result_handle)
    blast_result_list = iterateBlastrecord(blast_records, E_value_thresh)
    result_handle.close()
    return blast_result_list
