

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from keras.preprocessing import image
from keras.applications import xception
import cv2
import time
from os import listdir
from os.path import isfile, join

data_folder = 'input'

start_time = time.time()


#masking function
def create_mask_for_plant(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_hsv = np.array([0,0,250])
    upper_hsv = np.array([250,255,255])

    mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask

#image segmentation function
def segment_image(image):
    mask = create_mask_for_plant(image)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output/255


def read_img(filepath, size):
    img = image.load_img(os.path.join(data_folder, filepath), target_size=size)
    #convert image to array
    img = image.img_to_array(img)
    return img

def sharpen_image(image):
    image_blurred = cv2.GaussianBlur(image, (0, 0), 3)
    image_sharp = cv2.addWeighted(image, 1.5, image_blurred, -0.5, 0)
    return image_sharp

# function to get an image
def read_img(filepath, size):
    img = image.load_img(os.path.join(data_folder, filepath), target_size=size)
    #convert image to array
    img = image.img_to_array(img)
    return img





json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")

files = [f for f in listdir('input') if isfile(join('input', f))]
train_data = [[x, 0, ''] for x in files if x != '.DS_Store']

#train_data = [['test1.jpg', 0, ''], ['test2.jpg', 0, ''], ['test3.png', 0, ''], ['test4.jpg', 1, ''], ['test5.jpg', 0, ''], ['test6.jpg', 0, ''], ['test7.jpg', 0, ''], ['test8.jpg', 1, '']]
df = pd.DataFrame(train_data, columns=['file', 'id', 'label'])




INPUT_SIZE=255
##preprocess the input
X_train = np.zeros((len(df), INPUT_SIZE, INPUT_SIZE, df.shape[1]), dtype='float')
for i, file in tqdm(enumerate(df['file'])):
    #read image
    img = read_img(file,(INPUT_SIZE,INPUT_SIZE))
    #masking and segmentation
    image_segmented = segment_image(img)
    #sharpen
    image_sharpen = sharpen_image(image_segmented)
    x = xception.preprocess_input(np.expand_dims(image_sharpen.copy(), axis=0))
    X_train[i] = x

y = df['id']
train_val = X_train

xception_bf = xception.Xception(weights='imagenet', include_top=False, pooling='avg')
train_x = xception_bf.predict(train_val, batch_size=32, verbose=1)



predictions = model.predict(train_x)

print('--------------------------')

for h, i in enumerate(predictions):
    if 1-i[0] > 0.8: output = 'For review'
    if 1-i[0] > 0.95: output = 'Likely contains first'
    if 1-i[0] < 0.8: output = 'Very likely does not contain fire'
    print(train_data[h][0], str(np.round(1-i[0], 2)*100) + '%', output)


print('TIME: {} seconds'.format(np.round(time.time()-start_time, 2)))
print('TIME PER IMAGE: {} seconds'.format(np.round((time.time()-start_time)/len(train_data), 2)))
