from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from BLASTobject import blast



def main(s):
    blast_result_list =[]
    E_value_thresh = 0.04
    input = s
    print(input)
    result_handle = NCBIWWW.qblast("blastn", "nt", "8332116")
    with open("my_blast_result.xml", "w") as out_handle:
       out_handle.write(result_handle.read())
    result_handle.close()

    result_handle=open("my_blast_result.xml")
    blast_record = NCBIXML.read(result_handle)
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_value_thresh:
                #print("****Alignment****")
                #print("sequence:", alignment.title)
                sequenceName = alignment.title
                #print("alignment:", alignment.length)
                length = alignment.length
                #print("e-value:", hsp.expect)
                Evalue = hsp.expect

                blastresult = blast(sequenceName,length,Evalue)

                blast_result_list.append(blastresult)

    for i in blast_result_list:
        print(i.get_sequenceName())
        print(i.get_length())
        print(i.get_Evalue())


    return blast_result_list

main("ATGAAAACCAAAAA")


