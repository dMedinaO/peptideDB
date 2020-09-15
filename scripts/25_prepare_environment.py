import pandas as pd
import sys
import os

#function to encoding 
def encoding_pca_data(sequence, data_property):

	residues = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
	sequence_encoding = []

	for element in sequence:
		#get the pos of residue
		pos = -1
		for i in range(len(residues)):
			if element == residues[i]:
				pos = i
				break
		if pos != -1:
			sequence_encoding.append(data_property['component_1'][pos])

	return sequence_encoding

database = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]

#check zero-padding conformation
two_base_points = []
for i in range(15):
	two_base_points.append(pow(2,i))

keys = ['Antioncogenic','Insecticidal','Antiyeast','Antitumour','Chemotactic','Antimalarial','Spermicidal','Antimicrobial','Antioxidant','AntiGram_n','EnzymeInhibitor','Antiinflammatory','Antibiofilm','MammalianCells','AntiHIV','Antibacterial','Antiprotozoal','Antifungal','CancerCells','Antiviral','AntiMRSA','WoundHealing','AntiGram_p','Antiparasitic','SurfaceImmobilized','bacteriocins','defense','milk_peptide','quorom_sense','anti_tb','Immunomodulatory']
list_propertyes = ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]

for key in keys:

	command = "mkdir -p "+path_output+key
	print(command)
	os.system(command)

	print("Get sequences for ", key)
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

	#export sequence to fasta file
	file_open = open(path_output+key+"/"+key+".fasta", 'w')

	for i in range(len(sequences)):
		file_open.write(">Sequence_"+str(i+1)+"\n")
		if i == len(sequences)-1:
			file_open.write(sequences[i].upper())
		else:
			file_open.write(sequences[i].upper()+"\n")

	data_frame = pd.DataFrame(sequences, columns=['sequence'])

	for property_value in list_propertyes:

		print("Prepare paths")
		#create directory with different properties to use			
		command = "mkdir -p %s%s/%s" % (path_output, key, property_value)
		print(command)
		os.system(command)

		print("Process property: ", property_value)
		property_dataset = pd.read_csv("../encoding_AAIndex/"+property_value+"/data_component.csv")
		dataset_encoding = []
		length_sequence = []

		for i in range(len(data_frame)):

			row_data = []
			#get sequence encoding with PCA Analysis
			sequence_encoding = encoding_pca_data(data_frame['sequence'][i], property_dataset)
			row_data.append(sequence_encoding)

			dataset_encoding.append(row_data)
			length_sequence.append(len(row_data[0]))

		#make zero padding
		max_length = max(length_sequence)

		#get value near from two_base_points
		pos_pow = 0
		for i in range(len(two_base_points)):
			dif_data = two_base_points[i] - max_length
			if dif_data>=0:
				pos_pow=i
				break
		for i in range(len(dataset_encoding)):

			for j in range(len(dataset_encoding[i][0]), two_base_points[pos_pow]):
				dataset_encoding[i][0].append(0)

		#export dataset to csv
		matrix_export_not_class = []

		for element in dataset_encoding:
			row_full = []
			row_normal = []
			for point in element[0]:
				row_full.append(point)
				row_normal.append(point)
			matrix_export_not_class.append(row_normal)			

		df_export_not_class = pd.DataFrame(matrix_export_not_class)
		df_export_not_class.to_csv(path_output+key+"/"+property_value+"/encoding_without_class.csv", index=False, header=False)

		matlab_script = "procesFourierTransform"		
		input_data = path_output+key+"/"+property_value+"/encoding_without_class.csv"
		output_data = path_output+key+"/"+property_value+"/encoding_data_FFT.csv"
		domain_data = path_output+key+"/"+property_value+"/domain_data.csv"
		command = "/usr/local/MATLAB/R2017a/bin/matlab -nodisplay -nosplash -nodesktop -r \"procesFourierTransform('%s', '%s', '%s'); exit;\"" % (input_data, output_data, domain_data)	
		print(command)
		print("--------------------------------------------")
		os.system(command)

	print("OK-Process")

