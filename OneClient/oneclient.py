# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:46:01 2019

@author: KatreAR
"""

import pandas 
import pdb 
from analyse import scoring_columns
import datafile 

def standard_preprocess(data, column):
    """
    Small preprocessing steps, does the following:
        1. Converts column to string, for consistency
        2. Makes str to lower case
        3. Removes spaces
        4. Removes full stops 
        5. Removes commas
        
    Action: 
        Adds a new columns to the dataframe, with a 
        suffix "_processed"
        
    Returns: 
        Name of the new column. 
        
    To do: 
        1. Ensure that KvKs are int type - Fixed! 
        2. A better list of things to replace apart from 
        commas and full-stops
    """
    newname = data[column].name + '_processed'    
    data[newname] = data[column].apply(lambda x: 
        str(x).lower().replace(" ", "").replace(".", "").replace(",", "")
        if type(x) == str else x)
    return newname

data = pandas.read_excel("../OneObligor.xlsx")
data = datafile.data
## Replace spaces in column names
data.rename(columns= {c: c.replace(" ", "_") 
                        for c in data.columns}, inplace=True)

## Since we will group all columns, except the WWid    
columnstopreprocess = list(data.columns.drop('WWid'))
columnstopreprocess = ['Legal_Name', 'Fulladdress' , 'Short_Name', 'KvK_code']
columnstogroup = []
for cols in columnstopreprocess: 
    columnstogroup.append(standard_preprocess(data, cols))

## For all the columns that we want grouped, run a loop, 
## group them and make new csv files
#pdb.set_trace()
for gcols in columnstogroup:
    print("Grouping by: ", gcols)
    subset = data[data.groupby(gcols)[gcols].transform('count') > 1].dropna(subset=[gcols])
  #  pdb.set_trace()
    print(subset.sort_values(gcols,ascending=True).shape)
    print("Number of unique {0}: ".format(gcols), len(subset[gcols].unique()))
    scoring_columns(subset, gcols, suffix=gcols, typeofscoring=['group_score', 'individual_score'], scoringon=['Legal_Name', 'Fulladdress'], applybusinessrules=True)
    subset.to_csv("Grouped_by_{0}.csv".format(gcols), sep=',')
    print(subset.dtypes)
    