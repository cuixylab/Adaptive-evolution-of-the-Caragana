import os
from Bio import SeqIO
import argparse


def filter(each_line):
    def get_filter_value(key):
        FORMAT_list = each_line.split("\t")[8].split(":")
        VALUE_list = each_line.split("\t")[9].split(":")
        return VALUE_list[FORMAT_list.index(key)]
    #覆盖度低则返回False
    if "DP" not in each_line.split("\t")[8]:
        return False
    elif int(get_filter_value("DP")) <= 1:
        return False
    #如果是非变异位点，则直接返回True
    elif each_line.split("\t")[4] == "<NON_REF>":
        return True
    #如果为indel则返回False
    elif (len(each_line.split("\t")[3]) != 1 or 
        len(each_line.split("\t")[4].split(",")[0]) != 1):
        return False
    #如果genotype不为“1/1”则返回False
    elif get_filter_value("GT") != "1/1" and get_filter_value("GT") != "1|1":
        return False
    #如果是杂合位点则返回False
    elif "MLEAC=2,0" not in each_line:
        return False
    #如果是杂合位点则返回False
    elif float(each_line.split("\t")[5]) <= 20:
        return False
    else:
        return True


def re_write_seq(each_line, original_seq_in_list):
    #获取位点号
    site_number = int(each_line.split("\t")[1])
    #如果不是SNP位点，则使用ref上的碱基
    if each_line.split("\t")[4] == "<NON_REF>":
        original_seq_in_list[site_number-1] = each_line.split("\t")[3]
    #如果是SNP位点，则使用变异的碱基
    else:
        original_seq_in_list[site_number-1] = each_line.split("\t")[4].split(",")[0]
    return original_seq_in_list


def get_seq_from_gvf(seq_id, original_seq, input_gvcf):
    original_seq_in_list = list(original_seq)
    with open(input_gvcf) as read_file:
        for each_line in read_file:
            if each_line[0] != "#": #非注释行
                if each_line.split("\t")[0] == seq_id: #染色体号正确
                    if filter(each_line): #通过了过滤
                        new_seq = re_write_seq(each_line, original_seq_in_list)
    new_seq = "".join(new_seq)
    return new_seq
                    

def main():
    #解析参数
    #参数分为必须参数(required)和可选参数(additional)
    parser = argparse.ArgumentParser(description="Options for gvcf2fasta.py", add_help=True)
    required = parser.add_argument_group("Required arguments")
    required.add_argument('-r', '--reference', action="store", metavar='\b', type=str, required=True, help="Name of the reference file (.fasta file)")  
    required.add_argument('-g', '--gvcf', action="store", metavar='\b', type=str, required=True, help="Name of the gvcf file (generated by HaplotypeCaller in gatk4 with option -ERC BP_RESOLUTION)")
    
    args              = parser.parse_args()
    input_fasta       = args.reference
    input_gvcf        = args.gvcf

    for each_seq in SeqIO.parse(input_fasta, "fasta"):
        new_seq = get_seq_from_gvf(each_seq.id, "?"*len(each_seq.seq), input_gvcf)
        with open(each_seq.id, "a") as write_file:
            write_file.write(">" + input_gvcf + "\n")
            write_file.write(new_seq + "\n")


main()