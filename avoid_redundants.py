import operator

def count_up_down(input_file):
	START = True
	tissue_list = []
	different_tissue = set()
	all_info = {}
	result = []
	with open(input_file) as fl:
		for line in fl:
			line = line.rstrip()
			data = line.split("\t")
			if START:
				tissue_list = data
				START = False
				for element in data:
					different_tissue.add(element)
			else:
				MI = data.pop()

				all_info[data[0]] = {}
				all_info[data[0]]['up'] = {}
				all_info[data[0]]['down'] = {}
				all_info[data[0]]['NA'] = {}

				for different in different_tissue:
					all_info[data[0]]['up'][different] = 0
					all_info[data[0]]['down'][different] = 0
					all_info[data[0]]['NA'][different] = 0

				for i in range(1,len(data)):
					all_info[data[0]][data[i]][tissue_list[i-1]] += 1

				all_info[data[0]]['MI'] = MI

	return (all_info, tissue_list)

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
		

tup = count_up_down("test2.txt")
mat = construct_matrix(tup[0], tup[1])
print(select_splicings(mat, tup[0], 5))