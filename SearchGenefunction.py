import os
from io import StringIO

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

from BLASTobject import blast


# Auteur: Jung Ho Loos, Evander van Wolfswinkel
# Created: 27-3-2019
# Functionality: Blasts both raw fasta input and ORF objects list
# input and returns the information in blast objects list
# Known Bugs: No known Bugs

# Blasts raw fasta input, saves it to temporary file and then
# Uses NCBIWWW.qblast to blast for gene function
# Returns: Blast object list
def BLASTraw(input):                                #input is a raw sequence
    if os.path.exists("tempfasta.fa"):
        os.remove("tempfasta.fa")                   #removes existing tempfasta file
    if os.path.exists("my_blast_result.xml"):
        os.remove("my_blast_result.xml")            #removes existing my_blast_result.xml file
    blast_result_list = []                          
    E_value_thresh = 0.04                           #chosen E-value           
    fasta = input                                   #create a new fasta file
    fastaformat = StringIO(fasta)
    with open("tempfasta.fa", 'a') as fastafile:
        fastafile.write(fastaformat.getvalue())
    fasta_string = open("tempfasta.fa").read()      #reads created fasta file
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)    #BLAST using the fastafile
    print("done")
    with open("my_blast_result.xml", "w") as out_handle:            #saves BLAST output as XML file, my_blast_result.xml
        out_handle.write(result_handle.read())
    result_handle.close()
    result_handle = open("my_blast_result.xml", 'r')                #reads the XML file
    blast_records = NCBIXML.parse(result_handle)
    for blast_record in blast_records:                              #creates blast objects and saves them in the blast_result_list
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_value_thresh:
                    sequenceName = alignment.title
                    length = alignment.length
                    Evalue = hsp.expect
                    blastresult = blast(sequenceName, length, Evalue)
                    blast_result_list.append(blastresult)

    return blast_result_list            #returns blast_result_list as output

# Blasts orf object list input, saves it to temporary file and then
# Uses NCBIWWW.qblast to blast for gene function
# Returns: Blast object list
def BLASTorf(input):    #input a list of ORF_objects 
    if os.path.exists("tempfasta.fa"):
        os.remove("tempfasta.fa")               #removes existing tempfasta file
    if os.path.exists("my_blast_result.xml"):
        os.remove("my_blast_result.xml")        #removes existing my_blast_result.sml file
    blast_result_list = []                      
    E_value_thresh = 0.04                       #chosen E-value
    fasta = ""                                  #create a new fasta file                
    for ORF in input:
        ORFseq = ORF.get_sequence()
        ORFheader = ORF.get_header()
        fasta += ">" + ORFheader + "\n"
        fasta += ORFseq + "\n"
    fastaformat = StringIO(fasta)
    with open("tempfasta.fa", 'a') as fastafile:
        fastafile.write(fastaformat.getvalue())
    fasta_string = open("tempfasta.fa").read()          #reads created fasta file
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)    #BLAST using the fastafile
    print("done")
    with open("my_blast_result.xml", "w") as out_handle:        #saves BLAST output as XML file, my_blast_result.xml
        out_handle.write(result_handle.read())      
    result_handle.close()
    result_handle = open("my_blast_result.xml", 'r')            #reads the XML file
    blast_records = NCBIXML.parse(result_handle)
    for blast_record in blast_records:                           #creates blast objects and saves them in the blast_result_list
            for hsp in alignment.hsps:
                if hsp.expect < E_value_thresh:
                    sequenceName = alignment.title
                    length = alignment.length
                    Evalue = hsp.expect
                    blastresult = blast(sequenceName, length, Evalue)
                    blast_result_list.append(blastresult)

    return blast_result_list            #returns blast_result_list as output
