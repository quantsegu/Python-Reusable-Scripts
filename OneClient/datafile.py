import pandas 

data = pandas.read_excel("../OneObligor_extrainfo_small.xlsx")
data['Fulladdress'] = data['Zip Code'].apply(lambda x: str(x).replace(" ","")) + data['Street Number'].apply(lambda x: str(x).replace(" ", "" ))
colstodrop = ['CLASSIFICATIE CRE RRR', 'CLASSIFICATIE COREP RRR', 
                'KvK code adjusted', 'KvK code dubbel', 
                 'LegalNameadjusted', 'Legal Name dubbel',
                  'ShortNameadjusted', 'ShortNameadjusted dubbel', 'Fulladdress dubbel',
                  'User Name', 'Secondary NAICS', 'Secondary NAICS Percentage',
       'Tertiary NAICS', 'Tertiary NAICS Percentage', 'LQC Date', 'Sequence',
        'City', 'Zip Code', 'Street', 'Street Number', 'Country of Residence', 'Assessment Date', 'Descriptive User Name']

data = data.drop(columns=colstodrop, axis=1)