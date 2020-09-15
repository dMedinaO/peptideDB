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
database['Immunomodulatory'] = quorom_data

#get unique values
unique_sequences = list(set(dataset['sequence']))

#split data into class
inmuno_sequence = []
non_inmuno_sequence = []

for sequence in unique_sequences:
	for i in range(len(dataset)):
		if dataset['sequence'][i] == sequence:
			if dataset['class'][i] == 0:
				inmuno_sequence.append(sequence)
			else:
				non_inmuno_sequence.append(sequence)

print(len(inmuno_sequence))
print(len(non_inmuno_sequence))

inmuno_sequence_add = []
non_inmuno_sequence_add = []

#search anticancer sequence
for sequence in inmuno_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		inmuno_sequence_add.append(sequence)

	else:
		database['Immunomodulatory'][index] = 1

print("Number inmuno_sequence to add:")
print(len(inmuno_sequence_add))

print("Process non_inmuno_sequence")

#search anticancer sequence
for sequence in non_inmuno_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		non_inmuno_sequence_add.append(sequence)

print("Number non_inmuno_sequence to add:")
print(len(non_inmuno_sequence_add))

print("Export data")

#export data to csv 
dataset_anticancer = pd.DataFrame(inmuno_sequence_add, columns=['sequence'])
dataset_non_anticancer = pd.DataFrame(non_inmuno_sequence_add, columns=['sequence'])

dataset_anticancer.to_csv(path_output+"inmuno_sequence_add.csv", index=False)
dataset_non_anticancer.to_csv(path_output+"non_inmuno_sequence_add.csv", index=False)

database.to_csv(path_output+"database_update_inmuno.csv", index=False)