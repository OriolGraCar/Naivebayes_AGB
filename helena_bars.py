import Gtex_Loader
import Gtex_Naive_Bayes

all_info, tissue_list = Gtex_Loader.Gtex_load("train_brain.txt")
different_tissue, all_info2 = Gtex_Naive_Bayes.training(all_info, tissue_list, True)
user_data = Gtex_Loader.load_user_data("test_brain.txt")
Gtex_Naive_Bayes.predict('output_file.txt',different_tissue, all_info2, user_data, None, True)