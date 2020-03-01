import keras
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import os

data_size = 1000

def image_gen():
    datagen = ImageDataGenerator(
            rotation_range=90,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range = 0.2,
            rescale=1./255,
            fill_mode='nearest')

   
    im_path = os.getcwd() + "\\tf_dataset"

    for dat in os.listdir(im_path):
        print(dat)
        file_path = os.path.join(im_path,dat)

        len_dat = len(os.listdir(file_path))

        if (len_dat < data_size):
            remaining = data_size - len_dat
            i = 0
            files = os.listdir(file_path)

            while (remaining > 0):

                im_pth = os.path.join(file_path, files[i])

                img = load_img(im_pth)
                x = img_to_array(img)
                x = x.reshape((1,) + x.shape)

                save_dir = 'tf_dataset\\' + dat

                for batch in datagen.flow(x, batch_size=1,
                                            save_to_dir=save_dir, save_format='jpg'):
                    break

                i = (i + 1) % len_dat
                remaining -= 1

if __name__ == "__main__":
    image_gen()
