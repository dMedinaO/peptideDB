import pandas as pd
import sys 

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

sequence_array = []

for i in range(len(dataset)):
	if dataset['class'][i] == 1:
		sequence_array.append(dataset['sequence'][i])

#export data
file_export = open(path_output+"anticancer_data.fasta", 'w')

for i in range(len(sequence_array)):
	header = ">Sequence_data %s" % (i+1)
	file_export.write(header+"\n")
	file_export.write(sequence_array[i]+"\n")

file_export.close()

