import sys
from Bio import SeqIO

anticancer1 = sys.argv[1]
anticancer2 = sys.argv[2]
path_output = sys.argv[3]

sequences1 = []

for record in SeqIO.parse(anticancer1, "fasta"):    
    sequences1.append(record.seq)

for record in SeqIO.parse(anticancer2, "fasta"):    
    sequences1.append(record.seq)

print(len(sequences1))
sequences1 = list(set(sequences1))
print(len(sequences1))

file_export = open(path_output+"full_anticancer.fasta", 'w')

for i in range(len(sequences1)):
	desc = ">sequence_anti_cancer_%d" % (i+1)
	file_export.write(desc+"\n")
	sequence = ""
	for residue in sequences1[i]:
		sequence +=residue
	file_export.write(sequence+"\n")
file_export.close()
