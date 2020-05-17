'''
There are two types of business rules:  
    Common: Words that have no consequence on the name of the company.
    Those words that when they are removed, and if the strings compared after
    are a perfect match, then they are the same company. 

    Identifiers: Words if they are present, they make a big impact, and is a key 
    identifier in spotting different companies. 

    For Common words, we can simply take them out of the text, and then compute 
    group/ individual scores

    For Identifiers, we can add a strong scaling factor, to drastically drop the 
    individual scores. The group score can be scaled by the mean of the individual 
    scaling factors. 
'''
import pdb

def stopword_removal(listofnames):

    stopwords = ['Bank', 
                 'BV',
                 'Stichting',
                 'Ltd', 
                 'Limited', 
                 'Van', 
                 'LLC', 
                 'van',
                 'C.V.',
                 'Vastgoed',
                 'B.V.',
                 'Fund', 
                 'and',
                 'of',
                 'Investments', 
                 'der', 
                 'N.V.', 
                 'Maatschap', 
                 'Family',
                 'Robeco',
                 'V.O.F.',
                 '-',
                 'eo',
                 'Trust', 
                 'De',
                 'de',
                 'Scheepvaartonderneming' ]
    listtoreturn = []
    for names in listofnames:
        names = ' '.join(x for x in names.split() if x not in stopwords)
        listtoreturn.append(names)
        
        #data['BR_'+gcols]
    return listtoreturn

def scaling_scores(group_scores):
    identifiers = ['group', 'beheer', 'groep', 'holding', 'international', 
                    'i', 'ii', 'iii', 'iv', 'v', 'vi' ]
    scores = []
    for keys in group_scores.keys():
        names = keys.split("_") 
        for name in names:
            for iden in identifiers:
                for word in name.split():
                    if iden == word.lower():
                        scores.append(group_scores[keys] * 0.5)
    #pdb.set_trace()
    if scores == []:
        scores = list(group_scores.values())
    return scores