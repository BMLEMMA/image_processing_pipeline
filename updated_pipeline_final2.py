

# %%

!pip install pillow
!pip install matplotlib
!pip install numpy 
!pip install pandas
!pip install patchify
# %%

#importing libraries:
from PIL import Image
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from patchify import patchify
# %%

#function to import data:
def create_array (file_path):
    img_list=[]

    for file in os.listdir(file_path):
        if file.lower().endswith((".tif")):
            full_path=os.path.join(file_path, file)
            img_var=Image.open(full_path)
            img_list.append(img_var)
    img_arr=np.array (img_list)
    return(img_arr)
# %%
            
#function to patch images:
def patching (img_arr):
    patched_arr=[]
    for i in range (len(img_arr)):
        patches= patchify(img_arr[i], (64,64), step=64)
        patched_arr.append (patches)
    return (patched_arr)
# %%

#creating the CSV file:
def csv_file(file_name, patched_arr):
    #takes in the file name + a patched array to put the results in.
    #initializing lists:
    num_list_img = []
    num_list_subimg = []
    num_list_patch = []
    flat_pixels = []

#loop through each oatch (sub-image)
    for img_idx, patches in enumerate(patched_arr):
        #loop through each row of each sub-image:
        for subimg_row, patch_row in enumerate(patches):
            #loop through each patch inside a row (loops through columns)
            for subimg_col, patch in enumerate(patch_row):
                #appending to each empty list:
                #image number:
                num_list_img.append(img_idx)
                #sub-image number:
                num_list_subimg.append(subimg_row)
                #each patch (column-wise):
                num_list_patch.append(subimg_col)
                #flattening:
                flat_pixels.append(patch.flatten()) 
    #creating the data frame:
    data_array = np.array(flat_pixels)
    # df_pixels.insert(0, 'Patch Col', num_list_patch)
    # df_pixels.insert(0, 'Patch Row', num_list_subimg)
    # df_pixels.insert(0, 'Image Number', num_list_img)
    #return (df_pixels.to_csv(f"/Users/blenl/Desktop/{file_name}.csv", index=False))
    return (np.save(file_name, data_array))
# %%
    
#calling the function for training data:

og_path= "path"
img_arr_og= create_array(og_path)
patched_array_og = patching(img_arr_og)
csv_file("original_imgs", patched_array_og)


# %%

# #function call for testing data:
# testing_path="/Users/blenl/Desktop/segmented_imgs"
# img_arr_seg=create_array(testing_path)
# patched_arr=patching(img_arr_seg)
# csv_file ("segmented_imgs")

seg_path=  "/path"
img_arr_seg= create_array(seg_path)
patched_array_seg = patching(img_arr_seg)
csv_file("segmented_imgs", patched_array_seg)
