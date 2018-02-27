import math
import sys

def entropy(splicing_info):
	total_tissues = len(splicing_info['up'])
	prob_up = 0
	prob_down = 0
	count_up = 0
	count_down = 0
	conditional_prob_up = []
	conditional_prob_down = []
	summatory_up = 0
	summatory_down = 0


	for element in splicing_info['up']:
		conditional_prob_up.append(splicing_info['up'][element])
		count_up += splicing_info['up'][element]

	for element in splicing_info['down']:
		conditional_prob_down.append(splicing_info['down'][element])
		count_down += splicing_info['down'][element]


	prob_up = count_up/(count_up + count_down)
	prob_down = count_down/(count_up + count_down)

	summatory_up = sum([(x/count_up)*(math.log(x/count_up)/math.log(2)) for x in conditional_prob_up if x != 0])
	summatory_up = summatory_up * prob_up
	summatory_down = sum([(x/count_down)*(math.log(x/count_down)/math.log(2)) for x in conditional_prob_down if x != 0])
	summatory_down = summatory_down * prob_down

	return -(summatory_up + summatory_down)

def calculate_MSI(all_info, number, output_file = None):
	to_send = {}
	result = [(splicing,entropy(val)) for splicing,val in all_info.items()]
	result = sorted(result, key = lambda x: x[1])
	if output_file:
		with open(output_file,'w') as out:
			for element in result:
				out.write("%s\t%s\n" % (element[0],element[1]))

	for i in range(number):
		to_send[result[i][0]] = all_info[result[i][0]]
		to_send[result[i][0]]['MI'] = result[i][1]

	return to_send

def construct_matrix(info, tissues):
	splicings = list(info.keys())
	vals = ["up", "down"]
	tissues = set(tissues)
	matrix = {}
	i = 0
	while i < len(splicings)-1:
		j = i + 1
		while j < len(splicings):
			matches = 0
			for val in vals:
				for tis in tissues:
					if info[splicings[i]][val][tis] == info[splicings[j]][val][tis]:
						matches += 1
			matrix[(splicings[i], splicings[j])] = matches
			j += 1
		i += 1
	return matrix

def select_splicings(matrix, info, splicings):
	list_delete = []
	comparisions = (splicings*splicings)/2-splicings/2

	while (len(matrix) > comparisions):
		to_delete = max(matrix.items(), key=operator.itemgetter(1))[0]
		if info[to_delete[0]]["MI"] < info[to_delete[1]]["MI"]:
			delete = to_delete[0]
		elif info[to_delete[0]]["MI"] == info[to_delete[1]]["MI"]:
			continue
		else:
			delete = to_delete[1]
		for tup in matrix:
			if delete in tup:
				list_delete.append(tup)
		for tup in list_delete:
			matrix.pop(tup, None)

	return matrix

def get_final_splicings(matrix):
	splicings = set()
	comparisions = list(matrix.keys())

	for tup in comparisions:
		for spl in tup:
			splicings.add(spl)

	return splicings


if __name__ == "__main__":
	import Gtex_Loader
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	all_info, tissue_list = Gtex_Loader.Gtex_load(input_file)
	filtered_info = calculate_MSI(all_info,100)
	splice_matrix = construct_matrix(filtered_info, tissue_list)
	final_ids = get_final_splicings(select_splicings(splice_matrix, filtered_info, 5))
	for ids in final_ids:
		print("Splicing %s Selected." % ids)

	Gtex_Loader.filter_data(input_file,final_ids)
	exit(0)



	





