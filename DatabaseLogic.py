import re
from io import StringIO

import mysql.connector
from Bio import SeqIO

from ORFObject import ORF


def main():
    sequence = open("testfasta.fa").read()
    inputtype = "raw"
    orf_list = calculateORF(sequence, inputtype)
    storeORFS(orf_list)


def storeORFS(orf_list):
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="owe7_pg8@hannl-hlo-bioinformatica-mysqlsrv",
        passwd="blaat1234",
        db="owe7_pg8")
    cursor = conn.cursor()
    for orf in orf_list:
        cursor.execute("""INSERT INTO sequentie (Sequentie_ID, Sequentie_header, Sequentie)
                VALUES (""" + str(orf.get_header()) + """,""" + str(orf.get_header()) + """,""" + str(
            orf.get_sequence()) + """)
                INSERT INTO orf
                (ORF_ID, ORF_start, ORF_stop, Sequentie_Sequentie_ID)
                VALUES (""" + str(orf.get_header()) + """,""" + str(orf.get_frame()) + """,""" + str(
            orf.get_length()) + """,""" + str(orf.get_header()) + """)""")
    cursor.close()
    conn.close()


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


main()
