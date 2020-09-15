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
bammps_data = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

sequence_unique = list(set(bammps_data['PeptideSequence']))

matrix_row = []

for i in range(len(sequence_unique)):

	print("Process sequence: ", sequence_unique[i])

	for j in range(len(bammps_data)):
		if sequence_unique[i] == bammps_data['PeptideSequence'][j]:

			name_peptide = bammps_data['PeptideName'][j]
			organism = bammps_data['Microorganism'][j]
			group_organism = bammps_data['Microorganism group'][j]

			#get values for group organism
			anti_fungal = 0
			anti_gram_n = 0
			anti_gram_p = 0
			try:
				print(group_organism)
				if "neg" in group_organism:
					anti_gram_n=1
				if "pos" in group_organism:
					anti_gram_p=1
				if "yeast or fungus" == group_organism:
					anti_fungal=1
			except:
				pass
			#search sequence into database
			index = search_sequences_into_db(database, sequence_unique[i])
			if index == -1:
				print("Add sequence into database")

				row = [sequence_unique[i],len(sequence_unique[i]),'','','',0,0,0,anti_fungal,0,0,0,0,1,0,anti_gram_n,0,0,1,0,0,0,0,anti_fungal,0,0,0,0,anti_gram_p,0,0,'',name_peptide,organism,0,'','']
				matrix_row.append(row)
			else:
				print("Update sequence into database")
				database['AntiGram_n'][index] = anti_gram_n
				database['protein'][index] = name_peptide
				database['organism'][index] = organism
				database['Antifungal'][index] = anti_fungal
				database['Antimicrobial'][index] = 1
				database['AntiGram_p'][index] = anti_gram_p
				database['Antibiofilm'][index] = 1
				database['Antiyeast'][index] = anti_fungal

			break

dataset_add = pd.DataFrame(matrix_row, columns=database.keys())

database = database.append(dataset_add)

database.to_csv(path_output+"database_update_biofilm_data.csv", index=False)