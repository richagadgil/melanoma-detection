import csv 
import os
import random
import shutil
from datagen import image_gen


def main():
    with open("disease_dataset_1000.csv", mode="w") as outfile:
        writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        im_path = os.getcwd() + "\\tf_dataset"

        for dat in os.listdir(im_path):
            print(dat)
            file_path = os.path.join(im_path,dat)

            for files in os.listdir(file_path):

                im_pth = os.path.join(file_path, files)
                writer.writerow(["gs://diseases_1000/" + files, dat])

if __name__ == '__main__':
    main()

