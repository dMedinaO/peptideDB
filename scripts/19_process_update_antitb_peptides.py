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

sequences = list(set(quorom_data['sequence']))

data_add = [0 for x in range(len(database))]

database['anti_tb'] = data_add

matrix_data = []

for sequence in sequences:

	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:

		row_data = [sequence,len(sequence),'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'','','',0,'','',0,'',0, 0, 1]
		matrix_data.append(row_data)

	else:
		database['anti_tb'][index] = 1

print(len(matrix_data))

dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)

database.to_csv(path_ouput+"database_update_anti_tb.csv", index=False)

#Immunomodulatory