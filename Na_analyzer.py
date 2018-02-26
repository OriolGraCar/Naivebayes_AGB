
def calculate_NA(input_filename):
	ratios_dict = {}
	with open(input_filename) as fl:
		for line in fl:
			line = line.rstrip()
			data = line.split("\t")
			ratio = data.count('NA')/len(data)
			if ratio in ratios_dict:
				ratios_dict[ratio] += 1
			else:
				ratios_dict[ratio] = 1
	return ratios_dict

if __name__ == "__main__":

	for key, value in sorted(calculate_NA('updown_data.txt').items()):
		print("%s ratio: %s" % (key,value))
		
