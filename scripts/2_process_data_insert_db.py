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

fasta_file = sys.argv[1]
database = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

feature = "Antioncogenic"

sequences_data = []

for record in SeqIO.parse(fasta_file, "fasta"):
	sequences_data.append(record.seq)


sequences_data = list(set(sequences_data))

sequence_add = []

#search anticancer sequence
for sequence in sequences_data:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		sequence_add.append(sequence)

	else:
		database[feature][index] = 1
		database['Antimicrobial'][index] = 1

print(len(sequence_add))
matrix_data = []

for sequence in sequence_add:

	row = [sequence]
	for i in range(len(database.keys())-1):
		row.append('')
	matrix_data.append(row)

dataset_add = pd.DataFrame(matrix_data, columns=database.keys())

for i in range(len(dataset_add)):
	dataset_add[feature][i] = 1
	dataset_add['Antimicrobial'][i] = 1

dataset_export = database.append(dataset_add)
dataset_export.to_csv(path_output+"database_update_"+feature+".csv", index=False)