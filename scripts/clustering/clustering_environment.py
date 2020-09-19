import os
import sys

path_data = sys.argv[1]

list_activity = ['antibacterial', 'antimicrobial', 'Antibiofilm','Antifungal', 'AntiGram_n','AntiGram_p', 'AntiHIV','Antiinflammatory', 'Antimalarial','AntiMRSA', 'Antioncogenic','Antioxidant', 'Antiparasitic','Antiprotozoal', 'anti_tb','Antitumour', 'Antiviral','Antiyeast', 'bacteriocins','CancerCells', 'Chemotactic','defense', 'EnzymeInhibitor','Immunomodulatory','Insecticidal','MammalianCells','milk_peptide','quorom_sense','Spermicidal','SurfaceImmobilized','WoundHealing']
list_save_results = ["embedding-graph", "embedding-unsupervised", "FFT-graph", "FFT-time-series", "PCA-embedding-graph", "PCA-embedding-unsupervised"] 

for activity in list_activity:
	command = "mkdir -p %s%s" % (path_data, activity)
	print(command)
	os.system(command)

	for results in list_save_results:
		command = "mkdir -p %s%s/%s" % (path_data, activity, results)
		print(command)
		os.system(command)

		if "FFT" in results:
			for property_value in ["alpha-structure_group", "betha-structure_group", "energetic_group", "hydropathy_group", "hydrophobicity_group", "index_group", "secondary_structure_properties_group", "volume_group"]:
				command = "mkdir -p %s%s/%s/%s" % (path_data, activity, results, property_value)
				print(command)
				os.system(command) 