# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# %%

!pip install pillow
!pip install matplotlib
!pip install numpy 
!pip install pandas
!pip install patchify
# %%

from PIL import Image
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from patchify import patchify
# %%

#defining file path
file_path = "/Users/blenl/Desktop/og"

#checking if the images exist.
for file in os.listdir(file_path):
    print(f"The images in the folder are {os.path.join(file_path, file)}")
    
# %%

#importing images using the pillow library

img_list=[]

for file in os.listdir(file_path):
    if file.lower().endswith((".tif")):
        full_path=os.path.join(file_path, file)
        img_var=Image.open(full_path)
        #by default, matplotlib introduces hues to the image, so doing cmpa="gray" removes that.
        img_list.append(img_var)
        plt.imshow(img_var,cmap="gray")
        plt.show()

#Each image has a size of 4506 by 3011 pixels and is now contained inside the img_list list.
# %%
# I need to find the pixel-by-pixel representation:
#the only adjustment needed is to convert the img_var into an array before putting it inside a list
img_arr=np.array (img_list)

# %%


num_list=[]
for i in range (len(img_list)):
    num_list.append(i)
print (num_list)

#the original img_array needs to be flattened first
#stacking columns on top of eachother. 
#use a for loop:
img_arr_flat=[]
for i in range (len(img_list)):
    img_arr_flat_single=img_arr[i].flatten()
    img_arr_flat.append(img_arr_flat_single)


df_img = pd.DataFrame({
    'Image Number': num_list,                
    'Images': img_arr_flat
})
print (df_img)
# %%

img0 = img_arr[0]  # shape (3011, 4506)

# Patch into 64x64 blocks
patches = patchify(img0, (64, 64), step=64)
patch_img=Image.fromarray(patches[0,0,:,:])
display(patch_img)
patch_img.size 
#gives 64,64 as intended.

print("Patches shape:", patches.shape)
len(patches)
len(patches[0])
#this is the right shape: 47, 70
# the patched shapes: 64, 64


#how is the data arranged in arrays.
# %%

#now making it into a for loop that does this for all images
patched_arr=[]
for i in range (len(img_arr)):
    patches= patchify(img_arr[i], (64,64), step=64)
    patched_arr.append (patches)
#print (patched_arr)
len(patched_arr)
len(patched_arr[0])
#these show that there are four main arrays inside patched_array adn each one is further classified into 47 arrays.
# %%
# num_list_img=[]
# num_list_subimg=[]
# num_list_cols=[]
# pixels=[]

# %%
num_list_img = []
num_list_subimg = []
num_list_patch = []
flat_pixels = []

for img_idx, patches in enumerate(patched_arr):
    for subimg_row, patch_row in enumerate(patches):
        for subimg_col, patch in enumerate(patch_row):
            num_list_img.append(img_idx)
            num_list_subimg.append(subimg_row)
            num_list_patch.append(subimg_col)
            flat_pixels.append(patch.flatten())  # 64*64 = 4096 pixels
            
df_pixels = pd.DataFrame(flat_pixels)
df_pixels.insert(0, 'Patch Col', num_list_patch)
df_pixels.insert(0, 'Patch Row', num_list_subimg)
df_pixels.insert(0, 'Image Number', num_list_img)

df_pixels.to_csv("/enter path", index=False)







