
def Gtex_load(input_file):
	"""
	Function that loads an Splicing Gtex File and loads it in a dictionary of dictionarys.
	Then returns a set with the different tissues and the diccionari.
	The dictionary has the splicing events as keys and another dictionary as value with the events up, down and NA as keys and
	another dictionary as value. This last dictionary has the tissues as keys and the times that the tissue had been found with the given event as value.
	"""
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
    """
	Loads the sample data in a dictionary with the different tissues as keys and the splicing events as values.
    """
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
	"""
	Function that takes as arguments one file and the desired splicing events,
	and produces another file with only those events. 
	The file has the same name as the original file but with the prefix Filtered_
	"""
	START = True
	output_name = "Filtered_" + input_file
	with open(input_file) as fl:
		with open(output_name,'w') as out:
			for line in fl:
				line = line.rstrip()
				if START:
					START = False
					out.write("%s\n" % line)
				else:
					data = line.split("\t")
					if data[0] in to_filter:
						out.write("%s\n" % line)

