'''
根据gff文件中记录的信息，提取基因组序列中的cds序列
'''
import os
from BCBio import GFF
from Bio import SeqIO

input_gff = "reference.gff"


#函数get_file_list：获取当前文件夹中指定文件
def get_file_list():
    '''
    获得当前文件夹中后缀为“.fasta”的文件列表
    输入：None
    输出：包含所有指定文件名称的列表，示例：["1.fasta", "2.fasta", "3.fasta"]
    '''
    file_tag = ".fasta"
    res_list = []
    for each_file in os.listdir():       
        if file_tag == each_file[-len(file_tag):]:
            res_list.append(each_file)
    return res_list


def main(input_genome):
    for each_seq in SeqIO.parse(input_genome, "fasta"):
        seq = str(each_seq.seq)


    in_handle = open(input_gff)
    with open(input_genome.replace(".fasta","_gene.fasta"), "w") as write_file:
        for rec in GFF.parse(in_handle):
            for each in rec.features:
                if each.type == "gene":
                    seq2 = seq[each.location.start:each.location.end].replace("?","").replace("-","").replace("N","")
                    if seq2:
                        write_file.write(">" + input_genome.replace(".fasta","") + str(each.id) + "\n")
                        write_file.write(str(seq[each.location.start:each.location.end].replace("?","N").replace("-","N") + "\n"))
    in_handle.close()


for each_fasta in get_file_list():
    main(each_fasta)

