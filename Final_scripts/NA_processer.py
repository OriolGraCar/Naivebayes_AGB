import argparse
import sys

def calculate_NA(input_filename,output_file):
    """Calculates the number of splicing sites that have each one of the proportion of NAs."""
    ratios_dict = {}
    output_file = output_file + "_ratio.txt"
    with open(input_filename) as fl:
        for line in fl:
            line = line.rstrip()
            data = line.split("\t")
            ratio = data.count('NA')/len(data)
            if ratio in ratios_dict:
                ratios_dict[ratio] += 1
            else:
                ratios_dict[ratio] = 1
    with open(output_file,"w") as outfl:
        for key, value in sorted(ratios_dict.items()):
            outfl.write("%s ratio: %s\n" % (key,value))
        



def accumulative_NA(input_file, output_file):
    """Calculates the accumulative number of splicing sites that have each ratio or lower. Formats the output to be analyzed by R."""
    output_file = output_file + "_sum.txt"
    file = open(input_file)
    out = open(output_file, 'w')
    value = 0
    out.write("ratio\tcounts\n")
    for line in file:
        data = line.split()
        value = value + int(data[2])
        out.write("%s\t%d\n" %(data[0], value))

def remove_na(input_file,output_file,to_remove):
    """Removes the splicing sites that have more than the decidided ration of NAs."""
    count = 0
    output_file = output_file + ".txt"
    with open(input_file) as fl:
        with open(output_file,'w') as out:
            for line in fl:
                line = line.rstrip()
                data = line.split("\t")
                number_of_na = data.count('NA')
                ratio = number_of_na/len(data)
                if ratio >= to_remove:
                    count += 1
                    print('Removed %s lines with ratio %s' % (count,ratio))
                else:
                    out.write(line+"\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script that removes NAs given a ration or analyses the number of NAs.")

    parser.add_argument(    '-i', '--input',
                dest= "infile",
                action= "store",
                default=None,
                help="Gtex file with up and downs.")

    parser.add_argument(    '-o', '--output',
                dest="outfile",
                action="store",
                default=None,
                help="Ouput prefix to print results.")

    parser.add_argument(    '-r', '--remove',
                dest="remove",
                action="store",
                default=None,
                type=float,
                help="If defined, removes the desired NA ratio. If not defined, analyse NAs.")

    options = parser.parse_args()

    if not options.infile or not options.outfile:
        sys.stderr.write("No input or output prefix given. Use -h to check usage.\n")
    else:
        if options.remove:
            remove_na(options.infile,options.outfile,options.remove)
        else:
            calculate_NA(options.infile,options.outfile)
            accumulative_NA(options.outfile + "_ratio.txt",options.outfile)
        
        