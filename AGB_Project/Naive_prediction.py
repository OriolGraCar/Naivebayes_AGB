

if __name__=="__main__":
	from agb_naive import *
	import argparse

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

	parser.add_argument('-o', '--output',
		dest="outfile",
		required=True,
		help="Output file name")


	options = parser.parse_args()

	all_info, tissue_list = Gtex_load(options.training)
	different_tissue, all_info2 = training(all_info, tissue_list, options.pseudo)
	user_data = load_user_data(options.testing)
	Gtex_Naive_Bayes.predict(options.outfile,different_tissue, all_info2, user_data, None, True)
	print("Program Finished Successfully")
	exit(0)