import argparse

def read_scores(input_file):
	data_list = []
	scores = set()
	tissue = input_file.replace(".txt", "")

	with open(input_file) as file:
		file.readline()
		for line in file:
			line = line.strip()
			line = line.split("\t")

			data_list.append((float(line[0]), line[1]))
			scores.add(float(line[0]))

	return (data_list, scores, tissue)

def calculate_PNrates(data, output_file):
	data_list = data[0]
	scores = data[1]
	tissue = data[2]

	out = open(output_file, "w")
	out.write("Treshold\tFPR\tTPR\n")

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

		out.write("%f\t%f\t%f\n" %(treshold, FPR, TPR))

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Script that takes all scores for all possible predictions of a tissue and calculates TPR and FPR.")

	parser.add_argument('-i', '--input',
		dest="infiles",
		nargs='+',
		required=True,
		help="List of files to analyze")

	options = parser.parse_args()

	for infile in options.infiles:
		outfile = infile.replace(".txt", "") + "_output.txt"
		calculate_PNrates(read_scores(infile), outfile)
