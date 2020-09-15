import pandas as pd
import sys
from Bio import SeqIO

dataset_full = pd.read_csv(sys.argv[1])
fasta_unitpro = sys.argv[2]
path_output = sys.argv[3]

sequences_data = []
records_id_data = []

for record in SeqIO.parse(fasta_unitpro, "fasta"):
	sequences_data.append(record.seq)
	records_id_data.append(record.id)

#read normal data using > as an identifier line to read
file_open = open(fasta_unitpro, 'r')
full_lines = []

line = file_open.readline()

while line:

	line = line.replace("\n", "")
	if line[0] == ">":
		full_lines.append(line)
	line = file_open.readline()

file_open.close()

#search sequence in both database
index_both = []
index_unit_pro = []

for i in range(len(sequences_data)):

	if sequences_data[i] in list(dataset_full['Sequence']):
		index_both.append(i)
	else:
		index_unit_pro.append(i)

#export two fasta: 1. sequence in database 2. sequence not in database
file_export1 = open(path_output+"sequences_in_db.fasta", 'w')
file_export2 = open(path_output+"sequences_not_in_db.fasta", 'w')

print("Export sequences in database ")
for index in index_both:
	
	file_export1.write(full_lines[index]+"\n")
	sequence_value = ""
	for residue in sequences_data[index]:
		sequence_value+=residue

	file_export1.write(sequence_value+"\n")

file_export1.close()


print("Export sequences not in databases")

for index in index_unit_pro:
	
	file_export2.write(full_lines[index]+"\n")
	sequence_value = ""
	for residue in sequences_data[index]:
		sequence_value+=residue

	file_export2.write(sequence_value+"\n")

file_export2.close()

