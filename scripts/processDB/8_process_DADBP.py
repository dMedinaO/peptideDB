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
dabbp_data = pd.read_csv(sys.argv[2], sep="\t")
path_output = sys.argv[3]

data_add = [0 for x in range(len(database))]
database['defense'] = data_add

matrix_data = []
for i in range(len(dabbp_data)):

	print("Process sequence: ", dabbp_data['bioactivity_seq'][i])

	#search sequence into database
	if dabbp_data['bioactivity_seq'][i] != "/":
		index = search_sequences_into_db(database, dabbp_data['bioactivity_seq'][i])

		sequence = dabbp_data['bioactivity_seq'][i]
		name_protein = dabbp_data['entry'][i]
		code_unitpro = dabbp_data['code_unitpro'][i]
		specie = dabbp_data['specie'][i]

		if index == -1:
			print("Add sequence into database")
			
			row = [sequence,len(sequence),code_unitpro,'','',0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'',name_protein,specie,0,'','', 1]
			matrix_data.append(row)			

		else:
			print("Update sequence into database")
			database['defense'][index] = 1
			database['uniprot_code'][index] = code_unitpro
			database['protein'][index] = name_protein
			database['organism'][index] = specie
			database['Antimicrobial'][index] = 1

dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)

database.to_csv(path_output+"database_update_DADBP.csv", index=False)


