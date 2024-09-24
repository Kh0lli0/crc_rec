
import glob
import re
import numpy as np
import pandas as pd
from pathlib import Path
from os import listdir,path,getcwd,walk
import glob
from itertools import chain
import torchvision.models
from sklearn.model_selection import train_test_split

######################################################

metadata = pd.read_csv('/athena/marchionnilab/scratch/lab_data/bagio/projects/colon/raw_data/colon_neoplasm.csv')
# create a column called label ( met status)
metadata['label'] = metadata['New Neoplasm Event Post Initial Therapy Indicator']

# rename
metadata['label'].replace('Yes', 'rec', inplace=True)
metadata['label'].replace('No', 'no_rec', inplace=True)

#metadata.dropna(subset = ['label'], inplace = True)
#metadata = metadata[metadata.label != 'n']

## Extract the important clinical label: ERG
metStatus = pd.DataFrame({'label':metadata['label'], 'case_id':metadata['Patient ID']})

# replace the '.' with '-'
metStatus['case_id'] =  [i.replace('.', '-') for i in metStatus['case_id']]

#################################
## Get the IDs for the WSIs and patients
slide_dir = '/athena/marchionnilab/scratch/lab_data/bagio/projects/colon/raw_data/tiles_clam_512_TCGA_lvl0/patches'
slides = listdir(slide_dir)



# make a dataframe: slide_id: slide ID! // case_id: patient ID
MetaData_clam = pd.DataFrame({'slide_id': slides})

MetaData_clam['case_id'] =  [i.replace(i, '-'.join(i.split("-")[0:3])) for i in MetaData_clam['slide_id']]

print(MetaData_clam['case_id'].value_counts())
print(MetaData_clam['slide_id'].value_counts())

# Remove the .h5 extension from the slide_id
MetaData_clam['slide_id'] = MetaData_clam['slide_id'].str.replace('.h5','')
#MetaData_clam['case_id'] = MetaData_clam['case_id'].str.replace('.h5','')


## Add labels
MetaData_clam = pd.merge(MetaData_clam, metStatus, left_on='case_id', right_on='case_id')
MetaData_clam = MetaData_clam.dropna()
print(MetaData_clam.shape)

# subset to the ones with feature extraction
filt = listdir('/athena/marchionnilab/scratch/lab_data/bagio/projects/colon/raw_data/features_TCGA_size_512_mag40x/h5_files')
filt = pd.DataFrame({'slide_id': filt})
filt['slide_id'] = filt['slide_id'].str.replace('.h5','')

MetaData_clam = MetaData_clam.loc[MetaData_clam['slide_id'].isin(filt['slide_id']),:]

MetaData_clam = MetaData_clam.drop_duplicates()
# print the slides/patients
print(MetaData_clam['label'].value_counts())
print(MetaData_clam['case_id'].value_counts())
print(MetaData_clam['slide_id'].value_counts())
print(MetaData_clam.shape)



# Save to disk
MetaData_clam.to_csv('dataset_csv/crc_metStatus_TCGA.csv')

