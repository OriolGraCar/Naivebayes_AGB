def get_samplename_by_id(input_file):
	"""Returns a dictionary to convert gtex ids in sample tissues"""
	ids = {}
	with open(input_file) as names_file:
		for line in names_file:
			line = line.strip("\n")
			fields = line.split("\t")
			ids[fields[0]] = fields[1]
	names_file.close()
	return ids

def get_outputdata(names_file, data_file, output_filename):
	"""writes the final file with first row as splicing event names,
	first column as sample names,
	and values as up or down"""
	dic_ids = get_samplename_by_id(names_file)
	output_file = open(output_filename, 'w')

	with open(data_file) as data_file:
		line = data_file.readline()
		line = line.strip("\n")
		samples = line.split("\t")

		first = True
		for sample in samples:
			if first == True:
				output_file.write("%s" %(dic_ids[sample]))
				first = False
			else:
				output_file.write("\t%s" %(dic_ids[sample]))
		output_file.write("\n")

		for line in data_file:
				line = line.strip("\n")
				splicing = line.split("\t")
				first = True
				for value in splicing:
					if first == True:
						output_file.write("%s" %(value))
						first = False
					else:
						if value == "NA":
							bool_val = "NA"
						elif float(value) >= 0.5:
							bool_val = "up"
						elif float(value) < 0.5:
							bool_val = "down"
						else:
							print("an unexpected value appeared")
						output_file.write("\t%s" %(bool_val))
				output_file.write("\n")

	data_file.close()
	output_file.close()
	

# --- RUNNING ---
get_outputdata("test_names.txt", "test_data.txt", "test_output.txt")
#get_outputdata("gtex_Brain_phenotype.txt", "gtex_brain_samples_formatted.psi.txt", "updown_data.txt")