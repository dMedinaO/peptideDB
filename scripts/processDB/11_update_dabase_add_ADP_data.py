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

matrix_data = []

for i in range(len(sequences_data)):

	print("Process sequence: ", sequences_data[i])		

	#get data from header sequence
	data_name, covalent_bound_category, gene_name, anti_fungal, anti_bacterian, anti_bacteriosin, defensin, gram_p, gram_n, antiviral = get_properties_from_header(full_lines[i])
	
	row_data = [sequences_data[i],len(sequences_data[i]),'','','',0,0,0,0,0,0,0,0,1,0,gram_n,0,0,0,0,0,anti_bacterian,0,anti_fungal,0,antiviral,0,0,gram_p,0,0,gene_name,data_name,'',anti_bacteriosin,'','',defensin,covalent_bound_category]
	matrix_data.append(row_data)

data_frame_add = pd.DataFrame(matrix_data, columns=dataset_full.keys())
dataset_full = dataset_full.append(data_frame_add)

dataset_full.to_csv(path_output+"database_update_add_ADP_database.csv", index=False)
