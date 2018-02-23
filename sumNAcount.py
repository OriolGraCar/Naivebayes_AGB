file = open("NA_counts.txt")
out = open("Rplot_data.txt", 'w')
value = 0
out.write("ratio\tcounts\n")
for line in file:
	data = line.split()
	value = value + int(data[2])
	out.write("%s\t%d\n" %(data[0], value))

