import csv 
import os
import random
import shutil

mel_set = {}
nv_set = {}
bcc_set = {}
ak_set = {}
bkl_set = {}
df_set = {}
vasc_set = {}
scc_set = {}
unk_set = {}

cats = ["MEL", "NV", "BCC", "AK", "BKL", "DF", "VASC", "SCC", "UNK"]

sets_per_class = 1000
gen_data = True

def check_label(input_data):
    for i in range(len(input_data)):
        if input_data[i] == '1':
            return cats[i]

def add_to_set(set_data, label):
    if label == "MEL":
        mel_set[set_data] = "MEL"

    elif label == "NV":
        nv_set[set_data] = "NV"

    elif label == "BCC":
        bcc_set[set_data] = "BCC"
    
    elif label == "AK":
        ak_set[set_data] = "AK"
    
    elif label == "BKL":
        bkl_set[set_data] = "BKL"
    
    elif label == "DF":
        df_set[set_data] = "DF"
    
    elif label == "VASC":
        vasc_set[set_data] = "VASC"
    
    elif label == "SCC":
        scc_set[set_data] = "SCC"
    
    else:
        unk_set[set_data] = "UNK"

def split_data(dataset, trainset, testset, validset):
    
    set_len = len(dataset)
    test_len = int(set_len * 0.1)
    train_len = set_len - (test_len * 2)
    set_list = list(dataset.keys())

    for train_data in set_list[:train_len]:
        trainset[train_data] = dataset[train_data]

    for test_data in set_list[train_len: train_len + test_len]:
        testset[test_data] = dataset[test_data]
    
    for valid_data in set_list[train_len + test_len:set_len]:
        validset[valid_data] = dataset[valid_data]
    
    return validset, testset, trainset

def shuffle_dataset(dataset):
    data_list = list(dataset.keys())
    random.shuffle(data_list)

    return_set = {}

    for data in data_list:
        return_set[data] = dataset[data]

    return return_set

def main():
    stats = []

    with open("ISIC_2019_Training_Metadata.csv", "r") as read_csv:
        csv_reader = csv.reader(read_csv)
        for row in csv_reader:
            stats.append(row)
        stats = stats[1:]
    random.shuffle(stats)

    for row in stats:
        dat = check_label(row[5:])
        add_to_set(row[0], dat) 

    trainset = {}
    testset = {}
    validset = {}

    validset, testset, trainset = split_data(mel_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(nv_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(bcc_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(ak_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(bkl_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(df_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(vasc_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(scc_set, trainset, testset, validset) 
    validset, testset, trainset = split_data(unk_set, trainset, testset, validset) 
    
    print("\n\nmel: ", len(mel_set))  
    print("nv: ", len(nv_set))
    print("bcc: ", len(bcc_set))
    print("ak: ", len(ak_set))
    print("bkl: ", len(bkl_set))
    print("df: ", len(df_set))
    print("vasc: ", len(vasc_set))
    print("scc: ", len(scc_set))
    print("unk: ", len(unk_set))

    print("\n\ntrain: ", len(trainset))
    print("test: ", len(testset))
    print("valid: ", len(validset))

    trainset = shuffle_dataset(trainset)
    testset = shuffle_dataset(testset)
    validset = shuffle_dataset(validset)

    with open("disease_dataset.csv", mode="w") as outfile:
        writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for data in trainset.keys():
            writer.writerow(["TRAIN" ,"gs://disease_train/disease_train/" + data, trainset[data]])
            shutil.copyfile(os.getcwd() + "\\ISIC_2019_Training_Input\\ISIC_2019_Training_Input\\" + data + ".jpg", os.getcwd() + "\\dataset\\" + data + ".jpg")
        for data in testset.keys():
            writer.writerow(["TEST","gs://disease_train/disease_train/" + data, testset[data]])
            shutil.copyfile(os.getcwd() + "\\ISIC_2019_Training_Input\\ISIC_2019_Training_Input\\" + data + ".jpg" , os.getcwd() + "\\dataset\\" + data + ".jpg")
        for data in validset.keys():
            writer.writerow(["VALIDATE" ,"gs://disease_train/disease_train/" + data, validset[data]])
            shutil.copyfile(os.getcwd() + "\\ISIC_2019_Training_Input\\ISIC_2019_Training_Input\\" + data + ".jpg" , os.getcwd() + "\\dataset\\" + data + ".jpg")

if __name__ == '__main__':
    main()

