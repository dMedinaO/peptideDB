import pandas as pd
import sys

activity_list = ['Antioncogenic', 'SodiumChannelBlocker', 'Insecticidal', 'Antiyeast', 'Antitumour', 'Chemotactic', 'Antimalarial', 'Spermicidal', 'Antimicrobial', 'Antioxidant', 'AntiGram_n', 'EnzymeInhibitor', 'Antiinflammatory', 'Antibiofilm', 'MammalianCells', 'AntiHIV', 'Antibacterial', 'Antiprotozoal', 'Antifungal', 'CancerCells', 'Antiviral', 'AntiMRSA', 'WoundHealing', 'AntiGram_p', 'Antiparasitic', 'SurfaceImmobilized']
dataset = pd.read_csv(sys.argv[1], sep=";")
path_output = sys.argv[2]

matrix_dataset = []

for i in range(len(dataset)):
	
	row = []
	sequence = dataset['Sequence'][i]
	length_data = dataset['Length'][i]
	uniprot_code = dataset['dbAMP_UniProt'][i]
	pdb_code = dataset['dbAMP_PDB'][i]
	taxonomy = dataset['dbAMP_Taxonomy'][i]

	activity_data = dataset['Activity'][i]

	row = [sequence, length_data, uniprot_code, pdb_code, taxonomy]

	#add activity
	names = activity_data.replace("\n", "")
	names = activity_data.split(",")	
	names = [x for x in names if x]
	
	row_activity = []
	
	for activity in activity_list:

		is_activity=0
		for name in names:
			name = name.replace("\n", "")
			if activity == name:
				row_activity.append(1)
				is_activity=1
				break
		if is_activity == 0:
			row_activity.append(0)

	for element in row_activity:
		row.append(element)

	matrix_dataset.append(row)

dataset_export = pd.DataFrame(matrix_dataset, columns = ['Sequence', 'Length', 'uniprot_code', 'pdb_code', 'taxonomy', 'Antioncogenic', 'SodiumChannelBlocker', 'Insecticidal', 'Antiyeast', 'Antitumour', 'Chemotactic', 'Antimalarial', 'Spermicidal', 'Antimicrobial', 'Antioxidant', 'AntiGram_n', 'EnzymeInhibitor', 'Antiinflammatory', 'Antibiofilm', 'MammalianCells', 'AntiHIV', 'Antibacterial', 'Antiprotozoal', 'Antifungal', 'CancerCells', 'Antiviral', 'AntiMRSA', 'WoundHealing', 'AntiGram_p', 'Antiparasitic', 'SurfaceImmobilized'])
dataset_export.to_csv(path_output+"process_database_AMP.csv", index=False)
