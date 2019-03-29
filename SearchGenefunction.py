import os
from io import StringIO

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

from BLASTobject import blast


def BLASTraw(input):
    if os.path.exists("tempfasta.fa"):
        os.remove("tempfasta.fa")
    if os.path.exists("my_blast_result.xml"):
        os.remove("my_blast_result.xml")
    blast_result_list = []
    E_value_thresh = 0.04
    fasta = input
    fastaformat = StringIO(fasta)
    with open("tempfasta.fa", 'a') as fastafile:
        fastafile.write(fastaformat.getvalue())
    fasta_string = open("tempfasta.fa").read()
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
    print("done")
    with open("my_blast_result.xml", "w") as out_handle:
        out_handle.write(result_handle.read())
    result_handle.close()
    result_handle = open("my_blast_result.xml", 'r')
    blast_records = NCBIXML.parse(result_handle)
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


def BLASTorf(input):
    if os.path.exists("tempfasta.fa"):
        os.remove("tempfasta.fa")
    if os.path.exists("my_blast_result.xml"):
        os.remove("my_blast_result.xml")
    blast_result_list = []
    E_value_thresh = 0.04
    fasta = ""
    for ORF in input:
        ORFseq = ORF.get_sequence()
        ORFheader = ORF.get_header()
        fasta += ">" + ORFheader + "\n"
        fasta += ORFseq + "\n"
    fastaformat = StringIO(fasta)
    with open("tempfasta.fa", 'a') as fastafile:
        fastafile.write(fastaformat.getvalue())
    fasta_string = open("tempfasta.fa").read()
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
    print("done")
    with open("my_blast_result.xml", "w") as out_handle:
        out_handle.write(result_handle.read())
    result_handle.close()
    result_handle = open("my_blast_result.xml", 'r')
    blast_records = NCBIXML.parse(result_handle)
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
