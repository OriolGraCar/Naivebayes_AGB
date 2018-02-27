
def Gtex_load(input_file):
	START = True
	tissue_list = []
	different_tissue = set()
	all_info = {}
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

	return all_info, tissue_list

def load_user_data(input_file):
    START = True
    header_order = []
    user_info = {}
    with open(input_file) as fl:
        for line in fl:
            line = line.rstrip()
            data = line.split("\t")
            if START:
                START = False
                count = 0
                for element in data:
                    count = count + 1
                    element = element +"*" + str(count)
                    user_info[element] = {}
                    header_order.append(element)
            else:
                important_data = data[1:]
                for i in range(len(important_data)):
                    if important_data[i] != 'NA':
                        user_info[header_order[i]][data[0]] = important_data[i]
    return user_info


def filter_data(input_file,to_filter):
	START = True
	output_name = "Filtered_" + input_file
	with open(input_file) as fl:
		with open(output_name) as out:
			for line in fl:
				line = line.rstrip()
				if START:
					START = False
					out.write("%s\n" % line)
				else:
					data = line.split("\t")
					if data[0] in to_filter:
						out.write("%s\n" % line)

