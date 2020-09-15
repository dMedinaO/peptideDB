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
bacteriocins = pd.read_csv(sys.argv[2], sep=";")
fasta_file = sys.argv[3]
path_ouput = sys.argv[4]

#read sequences
sequences = []
id_data = []

for record in SeqIO.parse(fasta_file, "fasta"):
	sequences.append(record.seq)
	id_data.append(record.id)


data_add = ['' for x in range(len(database))]

database['bacteriocins'] = data_add
database['class_bacteriocins'] = data_add
database['target_organism'] = data_add

matrix_data = []

for i in range(len(sequences)):

	id_seq = id_data[i]
	sequence = sequences[i]

	#get information for sequence using dataset csv
	row_data = [sequence]

	for j in range(len(bacteriocins)):
		if bacteriocins['Accession'][j] == id_seq:
			for key in ['Name', 'Class', 'Producer organism', 'Target organisms', 'UniProt']:
				row_data.append(bacteriocins[key][j])			
			break

	matrix_data.append(row_data)

#search sequences into full databases
index_add_data = []

#search anticancer sequence
for i in range(len(matrix_data)):

	print("Process sequence: ", matrix_data[i][0])
	index = search_sequences_into_db(database, matrix_data[i][0])

	if index == -1:
		index_add_data.append(i)

	else:#update data
		
		database['bacteriocins'][i] = 1
		database['class_bacteriocins'][i] = matrix_data[i][2]
		database['target_organism'][i] = matrix_data[i][4]		
		database['organism'][i] = matrix_data[i][3]		
		database['uniprot_code'][i] = matrix_data[i][5]
		database['protein'][i] = matrix_data[i][1]

#process data to add
matrix_to_dataFrame = []

for index in index_add_data:

	sequence = matrix_data[index][0]
	print("Add sequence ", sequence)

	protein_name = matrix_data[index][1] 
	class_data = matrix_data[index][2]
	organism = matrix_data[index][3]
	target_organism = matrix_data[index][4]
	uniprot_code = matrix_data[index][5]

	row_data = [sequence, len(sequence), uniprot_code, '', '', 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,'',protein_name,organism, 1, class_data, target_organism]

	matrix_to_dataFrame.append(row_data)

dataFrame = pd.DataFrame(matrix_to_dataFrame, columns=database.keys())

database = database.append(dataFrame)
database.to_csv(path_ouput+"database_update_add_bacteriocins.csv", index=False)
