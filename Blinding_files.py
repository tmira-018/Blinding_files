#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:44:49 2023

@author: miramota
"""
#importing all the packages needed
import os
import pandas as pd
import random

#creating a function that will be used to rename the files 
#output is a,b,c, and then go to aa,ab,ac etc
def generate_alphabet():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    while True:
        for letter in alphabet:
            yield letter
        for prefix in alphabet:
            for letter in alphabet:
                yield prefix + letter

#creating a function that will grab all the files in a given directory and put them into a list
# it will then copy the list and shuffle them, then iterate through the shuffled list and use the generate alphabet to rename the files
# using the zip function both the shuffled and the renamed list will be paired together as a key for unblinding
# the lists will then be copied into a newly generated excel list based on the current directory input

def rename_files(directory_path):
    file_list = []
    blinded = []
    #data = []
    generator = generate_alphabet()
    for file in os.listdir(directory_path):
        if not file.startswith('.'):  # Skip hidden files like .ds_store
            file_list.append(file)
        
    shuffled = file_list.copy()
    random.shuffle(shuffled)
    
    for new_shuffle in shuffled:
        new_filename = next(generator)
        blinded.append(new_filename)
        
    zipped_data = list(zip(shuffled, blinded))
    
    for item in zipped_data:
        shuffled_file, blinded_file = item
        old_path = os.path.join(directory_path, shuffled_file)
        new_path = os.path.join(directory_path, f"{blinded_file}{os.path.splitext(shuffled_file)[1]}")
        os.rename(old_path, new_path)
    
    column_names = ['Original Filename','Blinded Filename'] 
    df = pd.DataFrame(zipped_data, columns= column_names)
    blinded_excel = os.path.join(directory_path, 'blinded_reference.xlsx')
    df.to_excel(blinded_excel, index = False)
    
    print('The files are blinded and excel is created')
    return df

#give the directory folder to iterate through the files needing blinding
directory_path = ''
#apply the function to shuffle, rename, and create the excel sheet with the key
rename_files(directory_path)
