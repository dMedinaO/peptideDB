import pandas as pd
import sys
from Bio import SeqIO

def extract_data(description_elements):
	data_values = description_elements.replace(">", "")

	data_values = data_values.split(" ")

	#get pdb code
	code_pdb = data_values[0].split("|")[1]
	data_values.pop(0)

	#get protein name
	protein = description_elements.replace(">", "").split("OS=")[0].split(" ")

	protein_value = ""
	for i in range (1,len(protein)):

		protein_value = protein_value+protein[i]+" "

	protein_value = protein_value[:-2]

	#get organism value
	organism = description_elements.replace(">", "").split("OS=")[1].split("OX=")[0]	

	#get gene if exist
	gene = ""
	if "GN=" in description_elements:
		gene = description_elements.replace(">", "").split("GN=")[1].split(" ")[0]
	
	return [code_pdb, organism, protein_value, gene]


dataset = pd.read_csv(sys.argv[1])
fasta_file = sys.argv[2]
path_output = sys.argv[3]

data_add = ['' for x in range(len(dataset))]

dataset['gene'] = data_add
dataset['protein'] = data_add
dataset['organism'] = data_add

sequences_data = []
records_id_data = []

for record in SeqIO.parse(fasta_file, "fasta"):
	sequences_data.append(record.seq)
	records_id_data.append(record.id)

#read normal data using > as an identifier line to read
file_open = open(fasta_file, 'r')
full_lines = []

line = file_open.readline()

while line:

	line = line.replace("\n", "")
	if line[0] == ">":
		full_lines.append(line)
	line = file_open.readline()

file_open.close()

matrix_data = []
#Sequence,Length,uniprot_code,pdb_code,taxonomy,Antioncogenic,SodiumChannelBlocker,Insecticidal,Antiyeast,Antitumour,Chemotactic,Antimalarial,Spermicidal,Antimicrobial,Antioxidant,AntiGram_n,EnzymeInhibitor,Antiinflammatory,Antibiofilm,MammalianCells,AntiHIV,Antibacterial,Antiprotozoal,Antifungal,CancerCells,Antiviral,AntiMRSA,WoundHealing,AntiGram_p,Antiparasitic,SurfaceImmobilized,gene,organism,protein_name
for i in range(len(sequences_data)):
	print("Process sequence: ", sequences_data[i])
	result_extract = extract_data(full_lines[i])
	sequence = ""
	for residue in sequences_data[i]:
		sequence+=residue

	gene = result_extract[3]
	organism = result_extract[1]
	protein_name = result_extract[2]
	length_sequence = len(sequence)

	row_data = [sequence, length_sequence, result_extract[0], '', '', 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, gene,protein_name, organism]
	matrix_data.append(row_data)


keys = [key for key in dataset.keys()]
data_frame_new = pd.DataFrame(matrix_data, columns=keys)

#append
dataset = dataset.append(data_frame_new)
dataset.to_csv(path_output+"database_peptides_update_full.csv", index=False)
