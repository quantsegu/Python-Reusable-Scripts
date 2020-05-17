# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:20:41 2019

@author: KatreAR
"""

import pandas
import itertools
from fuzzywuzzy import fuzz
import numpy
import pdb
import math
from matching_tools import match_scores, match_scores_ind
from businessrules import stopword_removal, scaling_scores

def grouping(df, col):
    cond = df.groupby(col)[col]
    ret_df = df[cond.transform('count') > 1]
    ret_df = ret_df.sort_values(by=col)
    return ret_df


# fulllegal_match = grouping(data, "Legal_Name_processed")
# fullkvk_match = grouping(data, "KvK_code_processed")

# combined = fulllegal_match.append(fullkvk_match)
# combined = combined.drop_duplicates()

## Drop all the combined rows - 20 rows 
#data = data.drop(index=combined.index)

## On these, we should group on the main grouping and then check for partial 
## matches 
#data
## Just looking at everything grouped by Legal Name and has only two companies
## associated with it
#data = data[data.groupby("Fulladdress_processed").Legal_Name_processed.transform('count') ==2]

def scoring_columns(data, gcols, suffix='_', typeofscoring=None, scoringon=None, applybusinessrules=False):
    """
    type of scoring: individual/ group 
    """

    if typeofscoring is None or scoringon is None:
        print("This won't work, you need to mention a scoring method")
        return 


    for groups in data.groupby(gcols):
        for scoreon in scoringon:
            names = [name for name in groups[1].loc[:, scoreon].values.tolist()]
            names_tomatch = stopword_removal(names)
            if 'group_score' in typeofscoring:
                groupscoring = match_scores(names_tomatch, matchtype='mixed')
                groupscore = numpy.mean(list(groupscoring.values()))

            if 'individual_score' in typeofscoring:
                indscore = match_scores_ind(names, matchtype='mixed')
            
            if 'Legal_Name' in scoreon:
                #pdb.set_trace()
                groupscore_scaled = numpy.mean(scaling_scores(groupscoring))
                #pdb.set_trace()

            for ind in groups[1].index:
        #       data.loc[ind, 'scores']= matching_val 
                if 'group_score' in typeofscoring:
                    data.loc[ind, scoreon+'_group_score'+suffix] = groupscore
                    if  'Legal_Name' in scoreon:
                        data.loc[ind, scoreon+'_group_score_'+suffix+'_scaled'] = groupscore_scaled
                    
                if 'individual_score' in typeofscoring:
                  #  pdb.set_trace()
                    individual_score = numpy.mean(indscore[groups[1].loc[ind][scoreon]])
                    data.loc[ind, scoreon+'_ind_score'+suffix] = individual_score
            #allvals.append(matching_val)
        
    