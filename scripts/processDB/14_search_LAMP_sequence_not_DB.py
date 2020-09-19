import pandas as pd
import sys
from Bio import SeqIO

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

database = pd.read_csv(sys.argv[1])
fasta_LAMP = sys.argv[2]

path_output = sys.argv[3]

#read doc
sequences_data = []

for record in SeqIO.parse(fasta_LAMP, "fasta"):
	sequences_data.append(record.seq)

sequences_data = list(set(sequences_data))
sequences_not_DB = []

for sequence in sequences_data:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)
	if index == -1:
		sequences_not_DB.append(sequence)

#export sequence not DB to fasta file
fasta_export = open(path_output+"sequences_not_DB.fasta", 'w')

print(len(sequences_not_DB))

index=1
for sequence in sequences_not_DB:

	fasta_export.write(">Sequence_"+str(index)+"\n")
	sequence_value = ""
	for residue in sequence:
		sequence_value+=residue

	fasta_export.write(sequence_value+"\n")
	index+=1
