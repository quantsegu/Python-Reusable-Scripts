# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:20:41 2019

@author: KatreAR

This code is to process the combined datasets. 
To make sure the dtypes are correct and to combine scores etc. 
"""

import pandas, glob, functools, numpy
from matplotlib import pyplot as plt 
pandas.set_option('display.width', 200)
pandas.set_option('max_columns', 99)

#def processing():
datasets = glob.glob('*.csv')
data = functools.reduce(lambda x,y : pandas.merge(x,y, how='outer'), 
        [pandas.read_csv(x, dtype='object') for x in datasets])

scorecolumns = [x for x in data.columns if 'score' in x]

for scorecolumn in scorecolumns:
    data[scorecolumn] = data[scorecolumn].apply(lambda x: float(x))
    ## Risky, but lets try it.
    data[scorecolumn] = data[scorecolumn].fillna(0)   

#data['finalscore_LN']  = ((1.4 * data.Legal_Name_group_scoreFulladdress_processed) + (0.8* data.Legal_Name_group_scoreKvK_code_processed) + (0.8 * data.Legal_Name_group_scoreShort_Name_processed) + (1.4*data.Legal_Name_group_scoreLegal_Name_processed))/4
#data['finalscore_FA']  = ((1.3 * data.Fulladdress_group_scoreFulladdress_processed) + (0.8* data.Fulladdress_group_scoreKvK_code_processed) + (0.9 * data.Fulladdress_group_scoreShort_Name_processed) + (1.4*data.Fulladdress_group_scoreLegal_Name_processed))
#data['finalscore_LN_scaled']  = ((0.3 * data.Legal_Name_group_score_Fulladdress_processed_scaled) + (0.2* data.Legal_Name_group_score_KvK_code_processed_scaled) + (0.2 * data.Legal_Name_group_score_Short_Name_processed_scaled) + (0.3*data.Legal_Name_group_score_Legal_Name_processed_scaled))


data = data.replace(0.0, numpy.nan) 

#data['finalscore_LN_means']  = data[['Legal_Name_group_scoreFulladdress_processed', 'Legal_Name_group_scoreKvK_code_processed', 'Legal_Name_group_scoreShort_Name_processed', 'Legal_Name_group_scoreLegal_Name_processed']].mean(axis=1)
data['finalscore_FA_means']  = data[['Fulladdress_group_scoreFulladdress_processed', 'Fulladdress_group_scoreKvK_code_processed', 'Fulladdress_group_scoreShort_Name_processed', 'Fulladdress_group_scoreLegal_Name_processed']].mean(axis=1)

data['finalscore_LN_means_scaled']  = data[['Legal_Name_group_score_Fulladdress_processed_scaled', 'Legal_Name_group_score_KvK_code_processed_scaled', 'Legal_Name_group_score_Short_Name_processed_scaled', 'Legal_Name_group_score_Legal_Name_processed_scaled']].mean(axis=1)


def plotmaker(data1, data2, labelx, labely):
        fig, ax = plt.subplots(figsize=(12,14))
        ax.set_aspect('equal')
        hist, xbins, ybins, im = ax.hist2d(data1, data2, cmap=plt.cm.BuGn, bins=(10, 10), range=[(0, 100), (0, 100)])
        for i in range(len(ybins)-1):
                for j in range(len(xbins)-1):
                        ax.text(xbins[i]+5,ybins[j]+5, hist[i,j], 
                                color="black", ha="center", va="center", fontweight="bold")
        fig.colorbar(im)
        plt.xlabel(labelx)
        plt.ylabel(labely)

#plotmaker(data.finalscore_LN.fillna(-1), data.finalscore_FA.fillna(-1), 'Final score Legal Name', 'Final score Full address')
#plotmaker(data.finalscore_LN_scaled.fillna(-1), data.finalscore_FA.fillna(-1), 'Final score Legal Name scaled', 'Final score Full address')
#plotmaker(data.finalscore_LN_means.fillna(-1), data.finalscore_FA_means.fillna(-1), 'Final score Legal Name means', 'Final score address means')
plotmaker(data.finalscore_LN_means_scaled.fillna(-1), data.finalscore_FA_means.fillna(-1), 'Final score Legal Name means scaled', 'Final score Full address means')


allcolumns = data.columns
cols_scores = [name for name in allcolumns if 'score' in name]
#cols_fins = [name for name in cols_scores if 'final' in name]

cols_scores = [names for names in cols_scores if 'final' not in names]
cols_scores.append(data.columns[0])
data = data.drop(cols_scores, axis=1)

## Rounding scores
finalscores = [names for names in allcolumns if 'final' in names]
for final in finalscores:
        data[final] = data[final].apply(lambda x: round(x,2))

## conditional assessments


## Condition 1 - If their names do not match
## These therefore have to be marked as 'nd'
condition1 = ((data.finalscore_LN_means_scaled < 40))
conditional = numpy.where(condition1, 'nd', numpy.nan)

## Condition 2 - If their addresses do not match
## These are not duplicate, therefore marked as 'nd'
condition2 = ((data.finalscore_FA_means < 40))
conditional = numpy.where(condition2, 'nd', conditional)

## Condition 3 - They are the same companies if the address and the legal names match above 80
## These therefore are classified as 'f'
condition3 = ((data.finalscore_FA_means > 80) & (data.finalscore_LN_means_scaled > 80))
conditional = numpy.where(condition3, 'f', conditional)

## Condition 4 - They are different companies when the address is not a match, BUT the names are a match
condition4 = ((data.finalscore_LN_means_scaled > 60) & (data.finalscore_FA_means < 40))
conditional = numpy.where(condition4, 'nd', conditional)

## Condition 5 - The address match 100% however the names are between 40-80. This needs verification
## but it can be assumed, these are the ones that have been scaled. 
## Assigning them to  'nd' for now
condition5 = ((data.finalscore_FA_means == 100) & (data.finalscore_LN_means_scaled >=40) & (data.finalscore_LN_means_scaled <= 80))
conditional = numpy.where(condition5, 'nd', conditional)


data.insert(1, 'classification', conditional)

#return data