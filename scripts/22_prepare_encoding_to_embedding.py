import pandas as pd
import sys

database = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

keys = ['Antioncogenic','SodiumChannelBlocker','Insecticidal','Antiyeast','Antitumour','Chemotactic','Antimalarial','Spermicidal','Antimicrobial','Antioxidant','AntiGram_n','EnzymeInhibitor','Antiinflammatory','Antibiofilm','MammalianCells','AntiHIV','Antibacterial','Antiprotozoal','Antifungal','CancerCells','Antiviral','AntiMRSA','WoundHealing','AntiGram_p','Antiparasitic','SurfaceImmobilized','bacteriocins','defense','milk_peptide','quorom_sense','anti_tb','Immunomodulatory']

for key in keys:

	print("Get sequences for ", key)
	sequences = []

	for i in range(len(database)):
		if database[key][i]==1:
			if "X" not in database['Sequence'][i]:
				if "x" not in database['Sequence'][i]:
					sequence_add = database['Sequence'][i]
					sequence_add = sequence_add.replace("/", "")
					sequence_add = sequence_add.replace("-", "")
					sequence_add = sequence_add.replace("2", "")
					sequences.append(sequence_add)

	#export sequence to fasta file
	file_open = open(path_output+key+".fasta", 'w')

	for i in range(len(sequences)):
		file_open.write(">Sequence_"+str(i+1)+"\n")
		if i == len(sequences)-1:
			file_open.write(sequences[i].upper())
		else:
			file_open.write(sequences[i].upper()+"\n")

