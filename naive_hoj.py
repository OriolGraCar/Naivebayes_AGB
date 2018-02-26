import sys
from math import log


def training(input_file, pseudo=False):

    START = True
    tissue_list = []
    different_tissue = set()
    all_info = {}
    result = []
    with open(input_file) as fl:
        for line in fl:
            line = line.rstrip()
            data = line.split("\t")
            if START:
                tissue_list = data
                START = False
                for element in data:
                    different_tissue.add(element)
            else:
                all_info[data[0]] = {}
                all_info[data[0]]['up'] = {}
                all_info[data[0]]['down'] = {}

                for different in different_tissue:
                    all_info[data[0]]['up'][different] = 0
                    all_info[data[0]]['down'][different] = 0

                for i in range(1, len(data)):
                    if data[i] != 'NA':
                        all_info[data[0]][data[i]][tissue_list[i - 1]] += 1

    # Counts how many of tissues we have asumes uniform training set.
    total = tissue_list.count(tissue_list[0])

    # check if the data has 0 counts and raise error
    for key1 in all_info:
        for key2 in all_info[key1]:
            zeros = len([x for y, x in all_info[key1][key2].items() if x == 0])
            if zeros:
                sys.stderr.write("WARNING: %s Atributes with 0 ocurrences had been found\n" % (zeros))
                if pseudo:
                    # now the normal more in future
                    for key3 in all_info[key1][key2]:
                        if all_info[key1][key2][key3] == 0:
                            all_info[key1][key2][key3] += 1
                        else:
                            all_info[key1][key2][key3] += zeros
            for key3 in all_info[key1][key2]:
                if pseudo:
                    to_divide = total + zeros
                else:
                    to_divide = total
                all_info[key1][key2][key3] = all_info[key1][key2][key3] / to_divide

    return different_tissue, all_info


def predict(classes, all_atributes, user_data):
    # reads a dictionary of the user data and gives predictions
    valist = []
    max_val = "NA"
    max_class = ""
    for clas in classes:
        tmp_list = [all_atributes[key][value][clas] for key, value in user_data.items()]
        if 0 not in tmp_list:
            val = sum([log(x) / log(2) for x in tmp_list])
            valist.append(val)
            if max_val == 'NA':
                max_val = val
                max_class = clas
            elif val >= max_val:
                max_val = val
                max_class = clas
    # Normalize results
    if sum(valist) != 0:
        normalized_result = max_val / sum(valist)
    else:
        normalized_result = 'NA'
        max_class = 'NA'
    return max_class, normalized_result


def load_user_data(input_file):
    START = True
    header_order = []
    user_info = {}
    with open(input_file) as fl:
        for line in fl:
            line = line.rstrip()
            data = line.split("\t")
            if START:
                START = False
                count = 0
                for element in data:
                    count = count + 1
                    element = element +"*" + str(count)
                    user_info[element] = {}
                    header_order.append(element)
            else:
                important_data = data[1:]
                for i in range(len(important_data)):
                    if important_data[i] != 'NA':
                        user_info[header_order[i]][data[0]] = important_data[i]
    return (user_info)


if __name__ == '__main__':
    correct = 0
    incorrect = 0
    different_tissue, all_info = training('training_1%.txt')
    user_data = load_user_data('training_1%.txt')
    for key in user_data:
        max_class, max_val = predict(different_tissue, all_info, user_data[key])
        #print("The tissue %s is %s with an score of %s" % (key, max_class, max_val))
        realname = key.split("*")
        if realname[0] == max_class:
            correct = correct + 1
        else:
            incorrect = incorrect + 1
    correct_ratio = correct/(correct+incorrect) * 100
    incorrect_ratio = incorrect/(correct+incorrect) * 100
    print("The correct ratio is %s, and the inncorrect is %s" % (correct_ratio,incorrect_ratio))



