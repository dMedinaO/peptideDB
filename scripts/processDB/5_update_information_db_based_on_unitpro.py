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

#search sequence and update information
for i in range(len(sequences_data)):
	print("Process sequence: ", sequences_data[i])
	for j in range(len(dataset)):
		if sequences_data[i] == dataset['Sequence'][j]:

			result_extract = extract_data(full_lines[i])
			print(result_extract)
			#update elements
			dataset['gene'][j] = result_extract[3]
			dataset['organism'][j] = result_extract[1]
			dataset['uniprot_code'][j] = result_extract[0]
			dataset['protein'][j] = result_extract[2]
			break	

dataset.to_csv(path_output+"database_update_with_unit_pro.csv", index=False)