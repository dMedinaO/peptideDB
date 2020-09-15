import pandas as pd
import sys

dataset1 = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#create fasta file with all elements, add class into line description
description_array = []
sequence_array = []

for i in range(len(dataset1)):
	
	if dataset1['class'][i] == 'positive':
		sequence_array.append(dataset1['sequence'][i])
		description= ">sequence_%d type:quorom_sense_peptide" % (i+1)
		description_array.append(description)

#create fasta file
name_output = path_output+"quorom_sense_peptides.fasta"
file_export = open(name_output, 'w')

for i in range(len(sequence_array)):

	file_export.write(description_array[i]+"\n")
	file_export.write(sequence_array[i]+"\n")
file_export.close()

