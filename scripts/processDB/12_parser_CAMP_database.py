import pandas as pd
import sys

def get_activity(value_activity):
	
	list_evaluate = ['Antiviral', 'Antitumour', 'Antiparasitic', 'Antimicrobial', 'Antiprotozoal', 'Antifungal', 'Antitumor', 'antifungal', 'Anticancer', 'Antibacterial']
	
	dict_response = {}

	for key in list_evaluate:
		try:
			if key in value_activity:
				dict_response.update({key:1})
			else:
				dict_response.update({key:0})
		except:
			dict_response.update({key:0})

	return dict_response	

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

database = pd.read_csv(sys.argv[1])
camp_db = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

activities = camp_db['Activity'].dropna().unique().tolist()
data_activies = []
for activity in activities:
	activity = activity.replace(".", ",")
	activity = activity.replace(" ", "")

	data_split = activity.split(",")
	for data in data_split:
		data_activies.append(data)

data_activies = list(set(data_activies))

matrix_data = []

for i in range(len(camp_db)):

	try:
		sequence = camp_db['Sequence'][i]
		print("Process sequence: ", sequence)

		#get other information
		code_unitpro = camp_db['UniProt_id'][i]
		pdb_code = camp_db['PDBID'][i]
		name_protein = camp_db['Title'][i]
		taxonomy = camp_db['Taxonomy'][i]
		organism = camp_db['Source_Organism'][i]
		activity = camp_db['Activity'][i]
		gram_action = camp_db['Gram_Nature']

		activity_dict = get_activity(activity)

		AntiGram_n = 0
		AntiGram_p = 0
		
		if "+" in gram_action:
			AntiGram_p=1
		if "-" in gram_action:
			AntiGram_n=1

		#'Antiviral', 'Antitumour', 'Antiparasitic', 'Antimicrobial', 'Antiprotozoal', 'Antifungal', 'Antitumor', 'antifungal', 'Anticancer', 'Antibacterial'
		#search sequence into database
		index = search_sequences_into_db(database, sequence)
		if index == -1:
			print("Add data into database")
			row = [sequence,len(sequence),code_unitpro,pdb_code,taxonomy,activity_dict['Anticancer'],0,0,0,activity_dict['Antitumour'],0,0,0,activity_dict['Antimicrobial'],0,AntiGram_n,0,0,0,0,0,activity_dict['Antibacterial'],activity_dict['Antiprotozoal'],activity_dict['Antifungal'],0,activity_dict['Antiviral'],0,0,AntiGram_p,activity_dict['Antiparasitic'],0,'',name_protein,organism,0,'','','','']
			matrix_data.append(row)

		else:
			print("Updte data into database")

			database['uniprot_code'][index] = code_unitpro
			database['pdb_code'][index] = pdb_code
			database['taxonomy'][index] = taxonomy
			database['organism'][index] = organism
			database['protein'][index] = name_protein
			
			database['Antioncogenic'][index] = activity_dict['Anticancer']
			database['Antiviral'][index] = activity_dict['Antiviral']
			database['Antitumour'][index] = activity_dict['Antitumour']
			database['Antiparasitic'][index] = activity_dict['Antiparasitic']
			database['Antifungal'][index] = activity_dict['Antifungal']
			database['Antiprotozoal'][index] = activity_dict['Antiprotozoal']
			database['Antibacterial'][index] = activity_dict['Antibacterial']
			database['Antimicrobial'][index] = activity_dict['Antimicrobial']

			database['AntiGram_p'][index] = AntiGram_p
			database['AntiGram_n'][index] = AntiGram_n
	except:
		pass
dataframe_add = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe_add)
database.to_csv(path_output+"database_update_CAMP.csv", index=False)