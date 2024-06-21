
import re
import numpy as np
import pandas as pd
from pathlib import Path
from os import listdir,path,getcwd,walk
import glob
from itertools import chain
from sklearn.model_selection import train_test_split

## Metadata for training

# Read original csv file
orig = pd.read_csv('raw_data/tiles_clam_512_TCGA_lvl0/process_list_autogen.csv')

ExisSlides = listdir('raw_data/tiles_clam_512_TCGA_lvl0/patches')

# Remove the .svs extension
orig['slide_id'] = orig['slide_id'].str.replace('.svs','')
orig['slide_id'] = orig['slide_id'].astype(str)

# filter to existing slides
ExisSlides = pd.DataFrame({'slide_id': ExisSlides})
ExisSlides['slide_id'] = ExisSlides['slide_id'].str.replace('.h5','')

orig = orig.loc[orig['slide_id'].isin(ExisSlides['slide_id']),:]

print(orig.columns)
print(orig)

# Save to disk
orig.to_csv('raw_data/tiles_clam_512_TCGA_lvl0/process_list_autogen_featExt.csv')






