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

def get_rawdata(input_file):
	"""Returns a list of tuples with the first tupple value the name of the splicing event 
	and the rest are the values corresponding to that splicng event.
	Each tuple corresponds to a sampling event"""
	splicing_values = []
	with open(input_file) as data_file:
		line = data_file.readline()
		line = line.strip("\n")
		samples = line.split("\t")
		for line in data_file:
			line = line.strip("\n")
			splicing = tuple(line.split("\t"))
			splicing_values.append(splicing)
	data_file.close()
	return (splicing_values, samples)

def get_outputdata(names_file, data_file, output_filename):
	"""writes the final file with first row as splicing event names,
	first column as sample names,
	and values as up or down"""
	dic_ids = get_samplename_by_id(names_file)
	splicing_values = get_rawdata(data_file)[0]
	samples = get_rawdata(data_file)[1]
	output_file = open(output_filename, 'w')
	for splicing in splicing_values:
		output_file.write("\t%s" %(splicing[0]))
	output_file.write("\n")
	i = 1
	for sample in samples:
		output_file.write("%s" %(dic_ids[sample]))
		for splicing in splicing_values:
			if splicing[i] == "NA":
				bool_val = "NA"
			elif float(splicing[i]) >= 0.5:
				bool_val = "up"
			elif float(splicing[i]) < 0.5:
				bool_val = "down"
			else:
				print("an unexpected value appeared")
			output_file.write("\t%s" %(bool_val))
		output_file.write("\n")
		i += 1
	output_file.close()
	

# --- RUNNING ---
get_outputdata("gtex_Brain_phenotype.txt", "gtex_brain_samples_formatted.psi.txt", "updown_data.txt")