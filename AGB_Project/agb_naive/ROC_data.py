import argparse

def read_scores(input_file):
	"""Reads all files created by Gtex_NaiveBayes.tresholds()"""
	data_list = []
	scores = set()

	with open(input_file) as file:
		line = file.readline()
		tissue = line.rstrip()
		file.readline()
		for line in file:
			line = line.rstrip()
			line = line.split("\t")

			data_list.append((float(line[0]), line[1]))
			scores.add(float(line[0]))

	return (data_list, scores, tissue)

def calculate_PNrates(data, output_file):
	"""Calculates TPR, FPR and returns the ratio distance from the random (diagonal line)"""
	data_list = data[0]
	scores = data[1]
	tissue = data[2]
	ratios = []

	out = open(output_file, "a")

	for score in scores:
		treshold = score
		TP = 0
		FP = 0
		TN = 0
		FN = 0

		for tup in data_list:
			if treshold <= tup[0]: # we believe the result (P)
				if tup[1] == tissue: # it's a correct prediction (TP)
					TP += 1
				else: # it's a false prediction (FP)
					FP += 1
			else: # we do not trust the result (N)
				if tup[1] == tissue: # predicted good (FN)
					FN += 1
				else: # predicted wrong (TN)
					TN += 1

		P = TP + FN
		N = TN + FP
		TPR = TP/P
		FPR = FP/N

		out.write("%f\t%f\t%s\t%f\n" %(FPR, TPR, tissue, treshold))
		if FPR != 0:
			ratios.append(((TPR/FPR)-1, treshold))
		else:
			ratios.append((0, treshold))

	return (ratios, tissue)

	
def best_dictionary(infile, outfile):
	"""Returns the best treshold for each tissue."""
	dict_bests = {}

	data = calculate_PNrates(read_scores(infile), outfile)
	ratios = data[0]
	tissue = data[1]

	best = max(ratios, key=lambda x: x[0])

	dict_bests[tissue] = best[1]

	return dict_bests



if __name__ == "__main__":
	import Gtex_Loader
	import Gtex_Naive_Bayes
	import os
	import re

	parser = argparse.ArgumentParser(description="Script that takes all scores for all possible predictions of a tissue and calculates TPR and FPR.")

	parser.add_argument('-t', '--training',
		dest="training",
		required=True,
		help="Input file name for training data.")

	parser.add_argument('-s', '--testing',
		dest="testing",
		required=True,
		help="Input file name for testing data.")

	parser.add_argument('-p', '--pseudocounts',
		dest="pseudo",
		default=False,
		help="Set to True if you want to use pseudocounts.")

	parser.add_argument('-x', '--prefix',
		dest="prefix",
		required=True,
		help="Prefix for files to save Naive Bayes scores (per tissue)")

	parser.add_argument('-o', '--output',
		dest="outfile",
		required=True,
		help="Output file name")

	parser.add_argument('-r', '--prediction',
		dest="prediction",
		required=True,
		help="File name to save predicted output.")

	options = parser.parse_args()

	all_info, tissue_list = Gtex_Loader.Gtex_load(options.training)
	different_tissue, all_info2 = Gtex_Naive_Bayes.training(all_info, tissue_list, options.pseudo)
	user_data = Gtex_Loader.load_user_data(options.training)
	Gtex_Naive_Bayes.thresholds(tissue_list, all_info2, user_data, options.prefix)

	outfile = open(options.outfile, "w")
	outfile.write("FPR\tTPR\tTissue\tTreshold\n")
	outfile.close()

	current_dir = os.getcwd()
	list_files = list(filter(lambda x: re.search("^" + options.prefix + ".+", x), os.listdir(current_dir)))

	tresh = {}
	for infile in list_files:
		dic = best_dictionary(infile, options.outfile)
		tresh.update(dic)

	out = open(options.outfile, "a")
	out.write("0\t0\trocrandom\t0\n")
	out.write("1\t1\trocrandom\t0\n")
	out.close()

	Gtex_Naive_Bayes.predict(options.prediction,different_tissue, all_info2, user_data, tresh, True)
