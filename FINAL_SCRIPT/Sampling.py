import random
import argparse
def random_sampling(input_file,output_train,output_sample,number):
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
							selected = random.sample(data_holder[key],number)
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


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Script that makes random training and testing sets.")

	parser.add_argument(    '-i', '--input',
                dest= "infile",
                action= "store",
                required=True,
                help="Gtex file with up and downs.")

	parser.add_argument(    '-t', '--output_training',
                dest="trainfile",
                action="store",
                required=True,
                help="Ouput file name to print training set.")

	parser.add_argument('-s', '--output_sample',
    			dest="testfile",
    			action="store",
    			required=True,
    			help="Output file name to print testing set.")

	parser.add_argument(    '-z', '--size',
                dest="size",
                action="store",
                required=True,
                type=int,
                help="Number of elements of each tissue for training set.")

	options = parser.parse_args()

	random_sampling(options.infile,options.trainfile,options.testfile,options.size)





