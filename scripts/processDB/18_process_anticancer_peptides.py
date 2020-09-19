import pandas as pd
import sys

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

database = pd.read_csv(sys.argv[1])
quorom_data = pd.read_csv(sys.argv[2])
path_ouput = sys.argv[3]

sequences = []

for i in range(len(quorom_data)):
	if quorom_data['class'][i] == 1:
		sequences.append(quorom_data['sequence'][i])

sequences = list(set(sequences))

matrix_data = []

for sequence in sequences:

	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:

		row_data = [sequence,len(sequence),'','','',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'','','',0,'','',0,'',0, 0]
		matrix_data.append(row_data)

	else:
		database['Antioncogenic'][index] = 1

print(len(matrix_data))

dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)

database.to_csv(path_ouput+"database_update_anticancer.csv", index=False)
