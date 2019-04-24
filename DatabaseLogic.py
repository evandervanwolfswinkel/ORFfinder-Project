import uuid

import mysql.connector

from ORFObject import ORF


# Auteur: Evander van Wolfswinkel
# Created: 23-4-2019
# Functionality: Creates connection to a database and saves/loads orf information
# Known bugs: No known bugs

def defineConnection():
    """Defines connection to be used by the database"""
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="owe7_pg8@hannl-hlo-bioinformatica-mysqlsrv",
        passwd="blaat1234",
        db="owe7_pg8")
    return conn


def constructOrfObjects(db_records):
    """Construct ORF objects from info of database"""
    orfobject_list = []
    for orf in db_records:
        ORFobject = ORF(orf[1], orf[2], orf[3], orf[4], orf[5])
        orfobject_list.append(ORFobject)
    return orfobject_list

def storeORFS(orf_list):
    """Stores ORF's into database"""
    conn = defineConnection()
    cursor = conn.cursor()
    query = "INSERT INTO orfresult (ORF_ID, Sequence, ORF_Length, Strand, Frame, Header) VALUES (%s, %s, %s, %s, %s, %s)"
    for orf in orf_list:
        key = str(uuid.uuid4())
        values = (key, orf.get_sequence(), orf.get_length(), orf.get_strand(), orf.get_frame(), orf.get_header())
        cursor.execute(query, values)
    cursor.close()
    conn.commit()
    conn.close()


def loadORFS():
    """Loads ORF's from database"""
    conn = defineConnection()
    cursor = conn.cursor()
    query = "SELECT * FROM orfresult"
    cursor.execute(query)
    orf_list = constructOrfObjects(cursor.fetchall())
    cursor.close()
    conn.close()
    return orf_list
