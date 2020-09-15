import pandas as pd
import sys
from Bio import SeqIO

database = pd.read_csv(sys.argv[1])
file_sequences = sys.argv[2]
path_output = sys.argv[3]

#read doc
sequences_data = []

for record in SeqIO.parse(file_sequences, "fasta"):
	sequences_data.append(record.seq)

matrix_data = []
for sequence in sequences_data:

	row = [sequence,len(sequence),'','','',0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'','','',0,'','',0,'']
	matrix_data.append(row)

dataframe = pd.DataFrame(matrix_data, columns=database.keys())
database = database.append(dataframe)

database.to_csv(path_output+"database_update_LAMP.csv", index=False)



