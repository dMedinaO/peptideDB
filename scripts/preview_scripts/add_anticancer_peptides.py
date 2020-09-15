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

#get unique values
unique_sequences = list(set(dataset['sequence']))

#split data into class
anticancer_sequence = []
non_anticancer_sequence = []

for sequence in unique_sequences:
	for i in range(len(dataset)):
		if dataset['sequence'][i] == sequence:
			if dataset['class'][i] == 1:
				anticancer_sequence.append(sequence)
			else:
				non_anticancer_sequence.append(sequence)

print(len(anticancer_sequence))
print(len(non_anticancer_sequence))

anticancer_sequence_add = []
non_anticancer_sequence_add = []

#search anticancer sequence
for sequence in anticancer_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		anticancer_sequence_add.append(sequence)

	else:
		database['Antioncogenic'][index] = 1

print("Number anticancer_sequence to add:")
print(len(anticancer_sequence_add))

print("Process non_anticancer_sequence")

#search anticancer sequence
for sequence in non_anticancer_sequence:
	print("Process sequence: ", sequence)
	index = search_sequences_into_db(database, sequence)

	if index == -1:
		non_anticancer_sequence_add.append(sequence)

print("Number anticancer_sequence to add:")
print(len(non_anticancer_sequence_add))

print("Export data")
#export data to csv 
dataset_anticancer = pd.DataFrame(anticancer_sequence_add, columns=['sequence'])
dataset_non_anticancer = pd.DataFrame(non_anticancer_sequence_add, columns=['sequence'])

dataset_anticancer.to_csv(path_output+"antincancer_add.csv", index=False)
dataset_non_anticancer.to_csv(path_output+"non_anticancer_sequence_add.csv", index=False)

database.to_csv(path_output+"database_update_anticancer.csv", index=False)