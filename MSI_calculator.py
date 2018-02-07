import math


def entropy(splicing_info):
	total_tissues = len(splicing_info['up']) - 1
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





def calculate_MSI(input_file,output_file):
	START = True
	tissue_list = []
	different_tissue = set()
	all_info = {}
	result = []
	with open(input_file) as fl:
		for line in fl:
			line = line.rstrip()
			data = line.split("\t")
			all_info = {}
			if START:
				tissue_list = data
				START = False
				for element in data:
					different_tissue.add(element)
			else:
				all_info[data[0]] = {}
				all_info[data[0]]['up'] = {}
				all_info[data[0]]['down'] = {}

				for different in different_tissue:
					all_info[data[0]]['up'][different] = 0
					all_info[data[0]]['down'][different] = 0

				for i in range(1,len(data)):
					if data[i] == 'NA':
						continue
					else:						
						all_info[data[0]][data[i]][tissue_list[i-1]] += 1
				result.append([data[0],entropy(all_info[data[0]])])

	with open(output_file,'w') as out:
		for element in result.sort(key=lambda -x: x[1]):
			out.writte("%s\t%s\n" % (element[0],element[1]))





if __name__ == "__main__":
	#testing
	print(calculate_MSI('toymodel.psi'))






					




