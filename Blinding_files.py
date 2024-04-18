#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:44:49 2023

@author: miramota
"""

import os
import pandas as pd
import random


def generate_alphabet():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    while True:
        for letter in alphabet:
            yield letter
        for prefix in alphabet:
            for letter in alphabet:
                yield prefix + letter


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


directory_path = ''
rename_files(directory_path)
