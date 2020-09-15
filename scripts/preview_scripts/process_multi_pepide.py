import pandas as pd
import sys

def export_fasta_file(sequences, fasta_file, class_type):

	fasta_doc = open(fasta_file, 'w')

	for i in range(len(sequences)):
		desc = ">Sequence_%d type:%s" % (i+1, class_type)
		fasta_doc.write(desc+"\n")
		fasta_doc.write(sequences[i]+"\n")

	fasta_doc.close()

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

antibacterial_sequences = []
anticancer_sequences = []
antifungal_sequences = []
anti_hiv_sequences = []
antiviral_sequences = []
anti_microbial_sequences = []
non_anti_microbial = []

for i in range(len(dataset)):

	if dataset['class'][i] == "nonAMP":
		non_anti_microbial.append(dataset['sequence'][i])
	else:
		anti_microbial_sequences.append(dataset['sequence'][i])

		if dataset['class'][i] == "AC":
			anticancer_sequences.append(dataset['sequence'][i])
		elif dataset['class'][i] == "AV":
			antiviral_sequences.append(dataset['sequence'][i])
		elif dataset['class'][i] == "AB":
			antibacterial_sequences.append(dataset['sequence'][i])
		elif dataset['class'][i] == "AF":
			antifungal_sequences.append(dataset['sequence'][i])
		else:
			anti_hiv_sequences.append(dataset['sequence'][i])

#export data to fasta files
export_fasta_file(antibacterial_sequences, path_output+"antibacterial_peptides.fasta", "antibacterial_peptide")
export_fasta_file(anticancer_sequences, path_output+"anticancer.fasta", "anticancer_peptide")
export_fasta_file(antifungal_sequences, path_output+"antifungal_peptide.fasta", "antifungal_peptide")
export_fasta_file(anti_hiv_sequences, path_output+"anti_hiv_peptides.fasta", "anti_hiv_peptide")
export_fasta_file(antiviral_sequences, path_output+"antiviral_peptides.fasta", "antiviral_peptide")
export_fasta_file(non_anti_microbial, path_output+"non_anti_microbial.fasta", "non_anti_microbial")
export_fasta_file(anti_microbial_sequences, path_output+"anti_microbial_peptides.fasta", "anti_microbial_peptide")
