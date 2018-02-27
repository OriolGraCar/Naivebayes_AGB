import sys
import math
import operator


def training(all_info, different_tissue, pseudo=False):

	# Counts how many of tissues we have asumes uniform training set.
    total = tissue_list.count(tissue_list[0])
    # check if the data has 0 counts and raise error
    for splice in all_info:
        for event in all_info[splice]:
        	if event != 'NA':
        		zeros = len([x for y, x in all_info[splice][event].items() if x == 0])
	            if zeros:
	                sys.stderr.write("WARNING: %s Atributes with 0 ocurrences had been found\n" % (zeros))
	                if pseudo:
	                    # now the normal more in future
	                    for tissue in all_info[splice][event]:
	                        if all_info[splice][event][tissue] == 0:
	                            all_info[splice][event][tissue] += 1
	                        else:
	                            all_info[splice][event][tissue] += zeros
	            for tissue in all_info[splice][event]:
	                if pseudo:
	                    to_divide = total + zeros - all_info[splice]['NA'][tissue]
	                else:
	                    to_divide = total - all_info[splice]['NA'][tissue]
	                all_info[splice][event][tissue] = all_info[splice][event][tissue] / to_divide

    return different_tissue, all_info


def score_all(tissue_list, all_atributes, user_tissue):
	val_dict = {}
	total = 0
	for tissue in tissue_list:
		tmp_list = [all_atributes[splice][event][tissue] for splice, event in user_tissue.items()]
		if 0 not in tmp_list:
			val = sum([math.log(x) / math.log(2) for x in tmp_list])
			real_val = 2**val
			total += real_val
			val_dict[tissue] = real_val
		else:
			val_dict[tissue] = 0

	#normalize the results
	for tissue in val_dict:
		val_dict[tissue] = val_dict[tissue]/total

	return val_dict

def thresholds(tissue_list, all_atributes, user_data, output_prefix):
	#open all the required files
	files = {}
	for tissue in tissue_list:
		files[tissue] = open(output_prefix +tissue,"w")
		files[tissue].write("Threshold for %s\n" % tissue)
		files[tissue].write("Score\tReal")

	#iterates over user data and prints in each file the score to be it
	for sample in user_data:
		realname = key.split("*")
		val_dict = score_all(tissue_list, all_atributes,user_data[sample])
		for tissue in val_dict:
			files[tissue].write("\n%s\t%s" % (val_dict[tissue],realname[0]))

	# closes all files
	for tissue in tissue_list:
		files[tissue].close()


def predict(output_file,tissue_list, all_atributes, user_data, threshold_dict, scoring = False):
	correct = 0
	incorrect = 0
	out_file = open(output_file,"w")
	out_file.write("Score\tPrediction\tlabel\tsample")
	for sample in user_data:
		realname = key.split("*")
		val_dict = score_all(tissue_list, all_atributes,user_data[sample])
		if threshold_dict != None:
			found = False
			for tissue,val in sorted(val_dict.items(), key=lambda x: x[1],reverse=True):
				if val >= threshold_dict[tissue]:
					found = True
					out_file.write("\n%s\t%s\t%s\t%s" % (val,tissue,realname[0],sample))
					if scoring:
						if tissue == realname[0]:
							correct += 1
						else:
							incorrect += 1
					break
			if not found:
				#if not found get the maximum one
				result = max(stats.items(), key=operator.itemgetter(1))
				out_file.write("\n%s\t%s\t%s\t%s" % (result[1],result[0],realname[0],sample))
				if scoring:
					if tissue == realname[0]:
						correct += 1
					else:
						incorrect += 1

		else:
			result = max(stats.items(), key=operator.itemgetter(1))
			out_file.write("\n%s\t%s\t%s\t%s" % (result[1],result[0],realname[0],sample))
			if scoring:
				if tissue == realname[0]:
					correct += 1
				else:
					incorrect += 1

	out_file.close()
	if scoring:
		print("The Number of correct guesses are: %s" % correct)
		print("The Number of incorrect guesses are: %s" % incorrect)
		print("The correct ratio is %s" % (correct/(correct+incorrect)))

	if scoring == 'k-fold':
		return correct, incorrect






















