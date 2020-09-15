import sys
import pandas as pd
from Bio import SeqIO

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

def get_properties_from_header(header_data):

	data_name = header_data.split("(")[0].split("|")[1]
	print(data_name)

	covalent_bound_category = ""

	if "UCLL" in header_data:
		covalent_bound_category="UCLL"
	if "UCSS" in header_data:
		covalent_bound_category="UCSS"
	if "UCSB" in header_data:
		covalent_bound_category="UCSB"
	if "UCBB" in header_data:
		covalent_bound_category="UCBB"

	try:
		other_data = header_data.split("(")[1].split(";")
		gene_name = other_data[0]
	except:
		gene_name=""
		
	#search different categories
	anti_fungal = 0
	anti_bacterian = 0
	anti_bacteriosin = 0
	defensin = 0
	gram_p = 0
	gram_n = 0
	antiviral = 0

	if "fungal" in header_data:
		anti_fungal=1

	if "positive" in header_data:
		gram_p = 1
		anti_bacterian = 1

	if "negative" in header_data:
		gram_n = 1
		anti_bacterian = 1

	if "bacteriocin" in header_data:
		anti_bacteriosin=1
		anti_bacterian=1

	if "defens" in header_data:
		defensin=1

	if "viral" in header_data:
		antiviral=1


	return [data_name, covalent_bound_category, gene_name, anti_fungal, anti_bacterian, anti_bacteriosin, defensin, gram_p, gram_n, antiviral]

dataset_full = pd.read_csv(sys.argv[1])
fasta_unitpro = sys.argv[2]
path_output = sys.argv[3]

sequences_data = []
records_id_data = []

for record in SeqIO.parse(fasta_unitpro, "fasta"):
	sequences_data.append(record.seq)
	records_id_data.append(record.id)

#read normal data using > as an identifier line to read
file_open = open(fasta_unitpro, 'r')
full_lines = []

line = file_open.readline()

while line:

	line = line.replace("\n", "")
	if line[0] == ">":
		full_lines.append(line)
	line = file_open.readline()

file_open.close()

data_add = ["" for x in range(len(dataset_full))]
dataset_full['covalent_pattern'] = data_add

for i in range(len(sequences_data)):

	print("Process sequence: ", sequences_data[i])
	#search index 
	index = search_sequences_into_db(dataset_full, sequences_data[i])

	#get data from header sequence
	data_name, covalent_bound_category, gene_name, anti_fungal, anti_bacterian, anti_bacteriosin, defensin, gram_p, gram_n, antiviral = get_properties_from_header(full_lines[i])
	
	#update data into database
	dataset_full['Antimicrobial'][index] = 1
	dataset_full['AntiGram_n'][index] = gram_n
	dataset_full['Antiviral'][index] = antiviral
	dataset_full['AntiGram_p'][index] = gram_p
	dataset_full['gene'][index] = gene_name
	dataset_full['protein'][index] = data_name
	dataset_full['covalent_pattern'][index] = covalent_bound_category
	dataset_full['Antifungal'][index] = anti_fungal
	dataset_full['Antibacterial'][index] = anti_bacterian
	dataset_full['bacteriocins'][index] = anti_bacteriosin
	dataset_full['defense'][index] = defensin

dataset_full.to_csv(path_output+"database_update_values_ADP_database.csv", index=False)
