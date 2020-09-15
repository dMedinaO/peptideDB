import pandas as pd
import sys

def get_activity(activity_list):

	data_activity = activity_list.replace("\n", "").split(",")
	
	keys = ['Anticancer','SodiumChannelBlocker','Insecticidal','Antiyeast','Antitumour','Chemotactic','Antimalarial','Spermicidal','Antimicrobial','Antioxidant','-','Enzyme','inflammatory','Antibiofilm','Mammalian','HIV','Antibacterial','Antiprotozoal','fungal','Cancer','viral','AntiMRSA','wound','+','Antiparasitic','SurfaceImmobilized']

	row_response = [0 for x in keys]
		
	print(data_activity)
	for data in data_activity:
		index=0

		for key in keys:
			if key in data:
				row_response[index]=1
			index+=1

	return row_response

def get_data_for_sequence(sequence, dramp_db):

	information = {}

	for i in range(len(dramp_db)):
		if dramp_db['Sequence'][i] == sequence:

			information.update({'protein_name':dramp_db['Name'][i]})
			information.update({'uniprot_code' :dramp_db['Swiss_Prot_Entry'][i]})
			information.update({'taxonomy' : dramp_db['Family'][i]})
			information.update({'gene' :dramp_db['Gene'][i]})
			information.update({'organism' :dramp_db['Source'][i]})
			information.update({'activity' : get_activity(dramp_db['Activity'][i])})
			information.update({'pdb_ID' : dramp_db['PDB_ID'][i]})
			information.update({'target' : dramp_db['Target_Organism'][i]})
			break

	return information

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

database = pd.read_csv(sys.argv[1])
dramp_db = pd.read_csv(sys.argv[2], sep=";")
path_output = sys.argv[3]

#get unique sequences
sequences = list(set(dramp_db['Sequence']))
print(len(sequences))

matrix_data = []

activity_data= ['Antioncogenic','SodiumChannelBlocker','Insecticidal','Antiyeast','Antitumour','Chemotactic','Antimalarial','Spermicidal','Antimicrobial','Antioxidant','AntiGram_n','EnzymeInhibitor','Antiinflammatory','Antibiofilm','MammalianCells','AntiHIV','Antibacterial','Antiprotozoal','Antifungal','CancerCells','Antiviral','AntiMRSA','WoundHealing','AntiGram_p','Antiparasitic','SurfaceImmobilized']

#search sequences in database 
for sequence in sequences:

	print("Process sequence: ", sequence)
	
	#get data for sequence
	information_sequence = get_data_for_sequence(sequence, dramp_db)
	
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		
		print("Insert into database")
		row_data = [sequence,len(sequence),information_sequence['uniprot_code'],information_sequence['pdb_ID'],information_sequence['taxonomy']]

		for i in range(len(information_sequence['activity'])):
			row_data.append(information_sequence['activity'][i])
		
		row_data.append(information_sequence['gene'])
		row_data.append(information_sequence['protein_name'])
		row_data.append(information_sequence['organism'])
		row_data.append(0)
		row_data.append('')
		row_data.append(information_sequence['target'])
		row_data.append(0)
		row_data.append('')

		matrix_data.append(row_data)
	else:
		print("Update sequence into database")

		database['uniprot_code'][index] = information_sequence['uniprot_code']
		database['gene'][index] = information_sequence['gene']
		database['protein'][index] = information_sequence['protein_name']
		database['target_organism'][index] = information_sequence['target']
		database['organism'][index] = information_sequence['organism']
		database['taxonomy'][index] = information_sequence['taxonomy']
		
		if information_sequence['pdb_ID'] != "Unknown":
			database['pdb_code'][index] = information_sequence['pdb_ID']
		
		for i in range(len(information_sequence['activity'])):
			database[activity_data[i]][index] = information_sequence['activity'][i]

dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)
database.to_csv(path_output+"database_update_DRAMP.csv", index=False)
