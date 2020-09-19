import pandas as pd
import sys
from Bio import SeqIO
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

def make_histogram_for_distance(data_distance, name_output, name_distance):

	plt.clf()

	# An "interface" to matplotlib.axes.Axes.hist() method
	n, bins, patches = plt.hist(x=data_distance, bins='auto', color='#0504aa',
	                            alpha=0.7, rwidth=0.85)
	plt.grid(axis='y', alpha=0.75)
	plt.xlabel('Value')
	plt.ylabel('Frequency')
	plt.title(name_distance)	
	maxfreq = n.max()
	# Set a clean upper y-axis limit.
	plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

	plt.savefig(name_output)

def numpy_array_to_array (data):

	array_data = []

	for element in data:
		array_data.append(element)

	return array_data

def get_distance_vectors (vector1, vector2):

	mahalonobis_distance = distance.cityblock(vector1, vector2)
	cosine_distance = distance.cosine(vector1, vector2)
	correlation_distance = distance.correlation(vector1, vector2)

	return mahalonobis_distance, cosine_distance, correlation_distance

embedding_file = sys.argv[1]
fasta_file = sys.argv[2]
path_output = sys.argv[3]

#read fasta file and save struct data into array to export csv file
sequences_data = []
records_id_data = []

print("Read Fasta sequence")
for record in SeqIO.parse(fasta_file, "fasta"):
	sequences_data.append(record.seq)
	records_id_data.append(record.id)

print("Read embedding data")

#read embedding data
arrays = np.load(embedding_file, allow_pickle=True)

dict_keys = list(arrays.keys())

dataset_embedding = []#dataset

for key in dict_keys:
	data = arrays[key].tolist()
	row_avg = data['avg']

	array_data = numpy_array_to_array(row_avg)
	dataset_embedding.append(array_data)

print("Get matrix distance")

vector_distance_cosine = []
vector_distance_mahalonobis = []
vector_distance_correlation = []
vector_combinations = []

for i in range(len(dataset_embedding)):
	for j in range(len(dataset_embedding)):
		
		if i != j:
			combination1 = "%s-%s" % (records_id_data[i], records_id_data[j])
			combination2 = "%s-%s" % (records_id_data[j], records_id_data[i])
						
			#note, Always I need to work with combination 1
			if combination1 not in vector_combinations and combination2 not in vector_combinations:
				vector_combinations.append(combination1)

				mahalonobis_distance, cosine_distance, correlation_distance = get_distance_vectors (dataset_embedding[i], dataset_embedding[j])
				vector_distance_cosine.append(cosine_distance)
				vector_distance_correlation.append(correlation_distance)
				vector_distance_mahalonobis.append(mahalonobis_distance)

print("Make histogram")
#get histogram for distances
make_histogram_for_distance(vector_distance_cosine, path_output+"cosine_distance_embedding.png", "Cosine distance")
make_histogram_for_distance(vector_distance_mahalonobis, path_output+"mahalonobis_distance_embedding.png", "Mahalonobis distance")
make_histogram_for_distance(vector_distance_correlation, path_output+"correlation_distance_embedding.png", "Correlation distance")

print("Export data to csv file")

#make dataset and export elements
dataset = pd.DataFrame()
dataset['combinations'] = vector_combinations
dataset['mahalonobis_distance'] = vector_distance_mahalonobis
dataset['cosine_distance'] = vector_distance_cosine
dataset['correlation_distance'] = vector_distance_correlation

dataset.to_csv(path_output+"distance_embedding.csv", index=False)
