import pandas as pd
import sys

def search_sequences_into_db(database, sequence):

	index = -1

	for i in range(len(database)):
		if sequence == database['Sequence'][i]:
			index=i
			break

	return index

dataset = pd.read_csv(sys.argv[1])
database = pd.read_csv(sys.argv[2])
path_output = sys.argv[3]

#update key in dataset adding quorom sensitive
quorom_data = [0 for x in range(len(database))]
database['quorom_sense'] = quorom_data

#get unique values
unique_sequences = list(set(dataset['sequence']))

#split data into class
quorom_sequence = []
non_quorom_sequence = []

for sequence in unique_sequences:
	for i in range(len(dataset)):
		if dataset['sequence'][i] == sequence:
			if dataset['class'][i] == "positive":
				quorom_sequence.append(sequence)
			else:
				non_quorom_sequence.append(sequence)

print(len(quorom_sequence))
print(len(non_quorom_sequence))

quorom_sequence_add = []
non_quorom_sequence_add = []

#search anticancer sequence
for sequence in quorom_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		quorom_sequence_add.append(sequence)

	else:
		database['quorom_sense'][index] = 1

print("Number quorom_sequence to add:")
print(len(quorom_sequence_add))

print("Process non_quorom_sequence")

#search anticancer sequence
for sequence in non_quorom_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		non_quorom_sequence_add.append(sequence)

print("Number non_quorom_sequence to add:")
print(len(non_quorom_sequence_add))

print("Export data")

#export data to csv 
dataset_anticancer = pd.DataFrame(quorom_sequence_add, columns=['sequence'])
dataset_non_anticancer = pd.DataFrame(non_quorom_sequence_add, columns=['sequence'])

dataset_anticancer.to_csv(path_output+"quorom_add.csv", index=False)
dataset_non_anticancer.to_csv(path_output+"non_quorom_sequence_add.csv", index=False)

database.to_csv(path_output+"database_update_quorom.csv", index=False)