START = True
columns = set()
rows = []
count = 0
with open('gtex_brain_samples_formatted.psi') as fl:
	for line in fl:
		count += 1
		na_flag = False
		if START:
			START = False
			continue
		else:
			data = line.split("\t")
			for i in range(len(data)):
				if data[i] == 'NA':
					columns.add(i)
					na_flag = True
			if na_flag:
				rows.append(count)

print(len(columns))

print(len(rows))

