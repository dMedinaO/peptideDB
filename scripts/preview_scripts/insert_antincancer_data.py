import pandas as pd
import sys

database = pd.read_csv(sys.argv[1])
anticancer = pd.read_csv(sys.argv[2])
non_anticancer = pd.read_csv(sys.argv[3])
path_output = sys.argv[4]

keys = ['Sequence','Length','uniprot_code','pdb_code','taxonomy','Antioncogenic','SodiumChannelBlocker','Insecticidal','Antiyeast','Antitumour','Chemotactic','Antimalarial','Spermicidal','Antimicrobial','Antioxidant','AntiGram_n','EnzymeInhibitor','Antiinflammatory','Antibiofilm','MammalianCells','AntiHIV','Antibacterial','Antiprotozoal','Antifungal','CancerCells','Antiviral','AntiMRSA','WoundHealing','AntiGram_p','Antiparasitic','SurfaceImmobilized','gene','organism','protein_name']
print(len(anticancer))
print(len(non_anticancer))

matrix_data_non = []
matrix_data_yes = []

for sequence in non_anticancer['sequence']:
	print(sequence)
	row = [sequence]
	for i in range(len(keys)-1):
		row.append('')

	matrix_data_non.append(row)

for sequence in anticancer['sequence']:
	row = [sequence]
	for i in range(len(keys)-1):
		row.append('')

	matrix_data_yes.append(row)

dataFrame_add_anti = pd.DataFrame(matrix_data_yes, columns=keys)
dataFrame_add_nona = pd.DataFrame(matrix_data_non, columns=keys)
data_anticancer = [0 for x in range(len(dataFrame_add_nona))]

dataFrame_add_nona['Antioncogenic'] = data_anticancer

print(len(dataFrame_add_anti))
print(len(dataFrame_add_nona))


database = database.append(dataFrame_add_nona)

for i in range(len(dataFrame_add_anti)):
	dataFrame_add_anti['Antioncogenic'][i] = 1

database = database.append(dataFrame_add_anti)
database.to_csv(path_output+"database_full_update_anticancer.csv", index=False)
