from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import os

def image_gen(data):
    datagen = ImageDataGenerator(
            rotation_range=90,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range = 0.2,
            rescale=1./255,
            fill_mode='nearest')

    img = load_img(data)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
 
    if x.shape[1] > 1024:
        print(x.shape[1])
    if x.shape[2] > 1024:
        print(x.shape[2])
    i = 0
    
    for batch in datagen.flow(x, batch_size=1,
                                save_to_dir='dataset1', save_format='jpg'):
        plt.figure(i)
        imgplot = plt.imshow(array_to_img(batch[0]))
        i += 1

        if i % 10 == 0:
            break

        plt.show()

if __name__ == "__main__":
    for data in os.listdir(os.getcwd() + "\\ISIC_2019_Training_Input\\ISIC_2019_Training_Input"):
        image_gen(os.getcwd() + "\\ISIC_2019_Training_Input\\ISIC_2019_Training_Input\\" + data)
