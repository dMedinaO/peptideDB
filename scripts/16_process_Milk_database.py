import pandas as pd
import sys

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

def get_activity (activity_data):

	row_response = [0, 0, 0, 0]

	if "bacterial" in activity_data:
		row_response[0] = 1

	if "fungal" in activity_data:
		row_response[1] = 1

	if "paras" in activity_data:
		row_response[2] = 1

	if "viral" in activity_data:
		row_response[3] = 1

	return row_response

def get_gram_activity (gram_activity):

	row_response = [0,0]

	try:
		if "positive" in gram_activity:
			row_response[0] = 1

		if "negative" in gram_activity:
			row_response[1] = 1
	except:
		pass
	return row_response

database = pd.read_csv(sys.argv[1])
milk_database = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

data_add = [0 for x in range(len(database))]
database['milk_peptide'] = data_add

matrix_data = []

for i in range(len(milk_database)):

	sequence = milk_database['Sequence'][i].replace("\n", "")
	print("Process sequence: ", sequence)
	name_protein = milk_database['Name'][i]
	len_data = len(sequence)
	organism = milk_database['Producer_Organism'][i]
	row_activity = get_activity(milk_database['Activity'][i])
	gram_activity = get_gram_activity(milk_database['Spectrum'][i])

	index = search_sequences_into_db(database, sequence)
	if index==-1:		
		row = [sequence,len_data,'','','',0,0,0,0,0,0,0,0,1,0,gram_activity[1],0,0,0,0,0,row_activity[0],0,row_activity[1],0,row_activity[3],0,0,gram_activity[0],row_activity[2],0,'',name_protein,organism,0,'','',0,'', 1]
		matrix_data.append(row)

	else:
		database['milk_peptide'][index] = 1
		database['Antiparasitic'][index] = row_activity[2]
		database['Antibacterial'][index] = row_activity[0]
		database['Antimicrobial'][index] = 1
		database['Antifungal'][index] = row_activity[1]
		database['AntiGram_p'][index] = gram_activity[0]
		database['Antiviral'][index] = row_activity[3]
		database['AntiGram_n'][index] = gram_activity[1]

print("Add ", len(matrix_data), " sequences")
dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)

database.to_csv(path_output+"database_update_milk.csv", index=False)