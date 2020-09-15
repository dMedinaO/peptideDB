import os
import sys
import glob

path_files = sys.argv[1]

list_files = glob.glob(path_files+"*.fasta")

for file in list_files:

	name_file = file.split("/")[-1].split(".")[0]+".npz"
	
	file_output = path_files+name_file
	command = "tape-embed unirep %s %s babbler-1900 --tokenizer unirep" % (file, file_output)
	print(command)
	#os.system(command)
	