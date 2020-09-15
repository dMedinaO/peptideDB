import pandas as pd
import sys

name_dataset = sys.argv[1]
path_output = sys.argv[2]

name_export = path_output+"anti_tb_peptides.fasta"

file_input = open(name_dataset, 'r')
file_export = open(name_export, 'w')

line = file_input.readline()

index = 1
while line:
	desc = ">Sequence_%d anti_tb_peptide" % index
	file_export.write(desc+"\n")
	file_export.write(line)

	index+=1
	line=file_input.readline()

file_export.close()
file_input.close()
