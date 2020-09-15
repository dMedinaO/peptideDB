import pandas as pd
import sys

database = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

key = "Antibacterial"

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

data_length = len(sequences)

number_files = int(data_length/100)
rest_seq = data_length%100

index=0

for file in range(1, number_files+1):
	print("Process file: ", file)
	file_open = open(path_output+"sequences_range_"+str(file)+".fasta", 'w')

	for i in range(index, index+100):
		file_open.write(">Sequence_"+str(index+1)+"\n")
		if i == index+99:
			file_open.write(sequences[i].upper())
		else:
			file_open.write(sequences[i].upper()+"\n")

		index+=1

	file_open.close()

#the rest of sequences
file_open = open(path_output+"rest_sequences.fasta", 'w')

for i in range(index, len(sequences)):
	file_open.write(">Sequence_"+str(i+1)+"\n")
	if i == len(sequences)-1:
		file_open.write(sequences[i].upper())
	else:
		file_open.write(sequences[i].upper()+"\n")	
file_open.close()
