import pandas as pd
import numpy as np
import random
import copy
import os
import cv2

##########################
# make directory (if directory does not exist)
def makedir(path):
    folder = os.path.exists(path)
    
    if not folder:
        os.makedirs(path)
        print("--- new folder... ---")
        print("--- OK ---")

    else:
        print("--- There is this folder! ---")

##########################
# Generating PBP sequences
# parameters
## dirct: input directory (for images)
## dirctout: output directory (for .npy's)
## list_n: list of names of files under the input directory
## l: one-sided proportion of cropping in length 
## h: one-sided proportion of cropping in height
# output: .npy files of PBP sequences in the specified directory

def pbpGen (dirct, dirctout, list_n, l, h): 
    for p in range(len(list_n)):
        imgdirct = os.path.join(dirct,list_n[p])
        images = os.listdir(imgdirct)
        i_num = len(images)
        time_per = 1   # i_num: 照片总数
        image_names = [os.path.join(imgdirct, str(i+1)+'.png') for i in range(i_num)]

        num_blood = []
        for image_name in image_names:
            whole_image = cv2.imread(image_name)
            whole_image1 = cv2.cvtColor(whole_image, cv2.COLOR_BGR2GRAY)  # 灰度
            # consider truncated images
            image_hight = whole_image.shape[0]
            image_length = whole_image.shape[1]
            crop_image = whole_image[(int(image_hight/h)):(int(image_hight/h*(h-1))),(int(image_length/l)):(int(image_length/l*(l-1)))]
            crop_image1 = whole_image1[(int(image_hight/h)):(int(image_hight/h*(h-1))),(int(image_length/l)):(int(image_length/l*(l-1)))]

            ratio = np.sum(whole_image1) / np.sum(whole_image[:, :, 2])  # Gray/R
            threshold1 = 0.47 * ratio + 0.15
            minshold_blue = 2 
            maxshold_red = 141
            image = copy.copy(crop_image1)

            crop_image1[image >= threshold1 * crop_image[:, :, 2]] = 255
            crop_image1[crop_image[:, :, 0] >= minshold_blue] = 255
            crop_image1[crop_image[:, :, 2] <= maxshold_red] = 255
            crop_image1[crop_image1 < 255] = 0
            num_bl = np.sum(crop_image1 == 0) / (crop_image1.shape[0] * crop_image1.shape[1])

            num_blood.append(num_bl)  # 无滤波
            
            
        npdirct = os.path.join(dirctout, list_n[p] + '_'+ str(l) + '_' + str(h) + '.npy')
        np.save(npdirct, num_blood, allow_pickle=True, fix_imports=True)