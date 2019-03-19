from Bio.Blast import NCBIWWW

def main():

    s = "hello world"
    print(s)
    result_handle = NCBIWWW.qblast("blastn", "nt", "8332116")
    with open("my_blast_result.xml", "w") as out_handle:
        out_handle.write(result_handle.read())
    result_handle.close();


    print(s)

main()


