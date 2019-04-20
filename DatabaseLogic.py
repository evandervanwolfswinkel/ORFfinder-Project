import uuid

import mysql.connector


def storeORFS(orf_list):
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="owe7_pg8@hannl-hlo-bioinformatica-mysqlsrv",
        passwd="blaat1234",
        db="owe7_pg8")
    cursor = conn.cursor()
    query = "INSERT INTO orfresult (ORF_ID, Sequence, ORF_Length, Strand, Frame, Header) VALUES (%s, %s, %s, %s, %s, %s)"
    for orf in orf_list:
        key = str(uuid.uuid4())
        values = (key, orf.get_sequence(), orf.get_length(), orf.get_strand(), orf.get_frame(), orf.get_header())
        cursor.execute(query, values)
    cursor.close()
    conn.commit()
    conn.close()

