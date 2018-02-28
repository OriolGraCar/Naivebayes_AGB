import sys
import math
import operator


def training(all_info, different_tissue, pseudo=False):
	"""
	Function that trains the model, it can use pseudocounts or not
	It uses as input:
	all_info: dictionary with all the information of the Training Data
	different_tissue: set of diferents tissues
	pseudo: boolean to use pseudocounts or not
	Returns:
	A dict with all the conditional probabilities for each splicing event
	"""

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
                            all_info[splice][event][tissue] += 1

                for tissue in all_info[splice][event]:
                    if pseudo:
                        to_divide = all_info[splice]['up'][tissue] + all_info[splice]['down'][tissue] + 2 # 2 because we have two different states for each splicing site
                    else:
                        to_divide = all_info[splice]['up'][tissue] + all_info[splice]['down'][tissue]
                    all_info[splice][event][tissue] = all_info[splice][event][tissue] / to_divide

    return different_tissue, all_info


def score_all(tissue_list, all_atributes, user_tissue):
	"""
	This function is not meant to be used alone, its calle dby other functions.
	It gives the probability that each tissue is the sample
	Takes as arguments:
	all_atributes: dictionary with all the information of the trained model
	different_tissue: set of diferents tissues
	user_tissue: One sample of the User data
	Returns:
	A dict with the tissues as keys, and the probability of that sample beign the tissue as values.
	"""
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
	"""
	Function that creates files to make the roc curves.
	Generates one file per tissue, and adds the score for each sample.
	Takes as arguments:
	all_atributes: dictionary with all the information of the trained model
	tissue_list: set of diferents tissues
	user_data: dict with the data of the user
	output_prefix: Prefix used to make the files
	"""
    #open all the required files
    files = {}
    for tissue in tissue_list:
        files[tissue] = open(output_prefix +tissue,"w")
        files[tissue].write("%s\n" % tissue)
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
	"""
	Function that makes the predicition of the user data.
	Takes as arguments:
	all_atributes: dictionary with all the information of the trained model
	tissue_list: set of diferents tissues
	user_data: dict with the data of the user
	output_file: name of the file with the predictions
	threshold_dict: if defined uses the threshold provided to make the prediction instead of the max
	scoring: Default False. If enabled, shows the correct guesses, incorrect guesses and the ratio. (for testing the model only)
	"""
    correct = 0
    incorrect = 0
    out_file = open(output_file,"w")
    out_file.write("Score\tPrediction\tlabel\tsample")
    for sample in user_data:
        realname = sample.split("*")
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
                result = max(val_dict.items(), key=operator.itemgetter(1))
                out_file.write("\n%s\t%s\t%s\t%s" % (result[1],result[0],realname[0],sample))
                tissue = result[0]
                if scoring:
                    if tissue == realname[0]:
                        correct += 1
                    else:
                        incorrect += 1

        else:
            result = max(val_dict.items(), key=operator.itemgetter(1))
            out_file.write("\n%s\t%s\t%s\t%s" % (result[1],result[0],realname[0],sample))
            tissue = result[0]
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






