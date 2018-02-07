import random
def random_sampling(input_file,output_train,output_sample):
	header_flag = True
	data_holder = {}
	ids_list = []
	with open(input_file) as fl:
		with open(output_train,'w') as train:
			with open(output_sample,'w') as sample:
				for line in fl:
					line = line.rstrip()
					data = line.split("\t")
					if header_flag:
						header_flag = False
						for i in range(len(data)):
							if data[i] in data_holder:
								data_holder[data[i]].append(i)
							else:
								data_holder[data[i]] = [i]
						for key in data_holder:
							selected = random.sample(data_holder[key],55)
							for cosa in selected:
								ids_list.append(cosa)
						to_train = ""
						to_sample = ""
						for i in range(len(data)):
							if i in ids_list:
								to_train += "%s\t" % data[i]
							else:
								to_sample += "%s\t" % data[i]
						train.write(to_train[:-1]+"\n")
						sample.write(to_sample[:-1]+"\n")
						
					else:
						to_train = ""
						to_sample = ""
						for i in range(len(data)):
							if i != 0:
								j = i - 1
								if j in ids_list:
									to_train += "%s\t" % data[i]
								else:
									to_sample += "%s\t" % data[i]
							else:
								to_train += "%s\t" % data[0]
								to_sample += "%s\t" % data[0]
						train.write(to_train[:-1]+"\n")
						sample.write(to_sample[:-1]+"\n")



random_sampling('updown_data_filtred.txt','training.txt','sample.txt')







