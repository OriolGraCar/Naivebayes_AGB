
def remove_na(input_file,output_file):
	count = 0
	with open(input_file) as fl:
		with open(output_file,'w') as out:
			for line in fl:
				line = line.rstrip()
				data = line.split("\t")
				number_of_na = data.count('NA')
				ratio = number_of_na/len(data)
				if ratio >= 0.5:
					count += 1
					print('Removed %s lines with ratio %s' % (count,ratio))
				else:
					out.write(line+"\n")



remove_na('updown_data.txt','updown_data_filtred.txt')

