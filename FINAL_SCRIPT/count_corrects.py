
def count_corrects_tissue(input_file, output_file):
	"""
	Counts correct predicitions for each tissue and formats a file suitable for R.
	"""
	tissues_dict = {}
	with open(input_file) as fl:
		fl.readline()
		for line in fl:
			line = line.rstrip()
			data = line.split('\t')
			if not data[2] in tissues_dict:
				tissues_dict[data[2]] = {'correct':0,'incorrect':0}
			if data[2] == data[1]:
				tissues_dict[data[2]]['correct'] += 1
			else:
				tissues_dict[data[2]]['incorrect'] += 1

	with open(output_file,'w') as out:
		first = True
		tissue_order = []
		#print tissue
		for tissue in tissues_dict:
			if first:
				tissue_order.append(tissue)
				out.write(tissue)
				first = False
			else:
				out.write("\t%s" % tissue)
				tissue_order.append(tissue)
		out.write("\n")
		first = True
		#prints corrects
		for tissue in tissue_order:
			if first:
				out.write(str(tissues_dict[tissue]['correct']))
				first = False
			else:
				out.write("\t%s" % str(tissues_dict[tissue]['correct']))

		out.write("\n")
		first = True
		#prints incorrects
		for tissue in tissue_order:
			if first:
				out.write(str(tissues_dict[tissue]['incorrect']))
				first = False
			else:
				out.write("\t%s" % str(tissues_dict[tissue]['incorrect']))



count_corrects_tissue("predictions.txt", "corr_inc_data.txt")


