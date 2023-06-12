'''
平均分割fasta文件
'''
from Bio import SeqIO


input_fasta = "Chr01"
seq_num_each_file = 1

a = 0
n = 0
for each_seq in SeqIO.parse(input_fasta, "fasta"):
    if a <= seq_num_each_file:
        a = a + 1
        write_file_name = str(each_seq.id) + ".fasta"
        with open(write_file_name, "a") as write_file:
            write_file.write(">" + str(each_seq.id) + "\n")
            write_file.write(str(each_seq.seq) + "\n")
    else:
        a = 0
        n = n + 1
        write_file_name = str(each_seq.id) + ".fasta"
        with open(write_file_name, "a") as write_file:
            write_file.write(">" + str(each_seq.id) + "\n")
            write_file.write(str(each_seq.seq) + "\n")        
            
    