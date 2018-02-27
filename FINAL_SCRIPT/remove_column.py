import sys

def remove_column(input_file, output_file, column_name):
	"""Removes the colum (tissue) that you don't want to work with."""
	first = True
	index = []
	with open(input_file) as inp:
		for line in inp:
			if first:
				line = line.strip()
				header = line.split("\t")
				i = 0
				for tissue in header:
					if tissue == column_name:
						index.append(i)
					i += 1
				first = False
				out = open(output_file, "w")
				init = True
				for j in range(len(header)):
					if not j in index:
						if init:
							out.write("%s" %(header[j]))
							init = False
						else:
							out.write("\t%s" %(header[j]))
				out.write("\n")
			else:
				line = line.strip()
				line = line.split("\t")
				out.write("%s" %(line[0]))
				for j in range(len(line)):
					if not j-1 in index and j != 0:
						out.write("\t%s" %(line[j]))
				out.write("\n")

if __name__ == "__main__":

	if len(sys.argv) == 4:
		remove_column(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print("Wrong usage:\nInput should be:\n 1. input file name\n 2. output file name\n 3. column name to remove.\n")