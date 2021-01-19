# standard dataframe packages
import pandas as pd
import numpy as np

# saving packages
import pickle
import gzip

from data_cleaning import status_update


# path to data folder
data_path = '/Users/p.szymo/Documents/code_world/projects/library_usage_seattle/data/'


# status update
status_update('Script has begun!')


##----LOAD CHECKOUT DATA----##

# columns to load
usecols = [
	'Collection',
	'ItemTitle',
	'Subjects',
	'CheckoutDateTime'
	]

# load data
df = pd.read_csv(
	data_path + 'Checkouts_By_Title__Physical_Items_.csv',
	usecols=usecols
	)

# rename columns to my preferred format
df.columns = [
	'collection',
	'title',
	'subjects',
	'date'
	]

# status update
status_update('Checkout data loaded!')


##----CONVERT DATE COLUMN TO DATETIME----##

# specify the format
dt_format = '%m/%d/%Y %I:%M:%S %p'

# convert to datetime, dropping the hour-minute-second stamp using the `dt.date` attribute
df['date'] = pd.to_datetime(df.date, format=dt_format).dt.date


# status update
status_update('Date column converted to datetime!')


##----LOAD AND TRANSFORM DATA DICTIONARY----##

# load data
dd = pd.read_csv(data_path + 'data_dictionary.csv')

# rename columns to my preferred format
dd.columns = ['code', 'description', 'code_type', 'format_group', 'format_subgroup', 
              'category_group', 'category_subgroup', 'age_group']

# subset to only collection codes
dd = dd[dd.code_type == 'ItemCollection']

# drop columns
dd.drop(columns=['description', 'code_type', 'category_subgroup'], inplace=True)

# list of columns to convert
to_convert = ['format_group', 'format_subgroup', 'category_group', 'age_group']

# convert to category datatype
dd[to_convert] = dd[to_convert].apply(pd.Categorical)


# status update
status_update('Data dictionary loaded and transformed!')


##----MERGE INFO----##

# merge checkouts dataframe with info from data dictionary
df_merged = df.merge(dd, left_on='collection', right_on='code')


# status update
status_update('Checkout data merged with data dictionary info!')


##----DROP UNNECESSARY COLUMNS----##

# list of columns to keep
keep_cols = ['title', 'subjects', 'date', 'format_group', 'format_subgroup',
             'category_group', 'age_group']

# drop `collection` and `code` columns
df_merged = df_merged[keep_cols]


# status update
status_update('Collection and code columns dropped!')


##----SET DATE COLUMN AS INDEX----##

# set `date` column as index and sort by index
df_merged = df_merged.set_index('date').sort_index()

# status update
status_update('Date is now the index!')

# calculate and print number of rows and columns
n_rows = df_merged.shape[0]
n_cols = df_merged.shape[1]

print(f'The dataframe contains {n_rows} rows and {n_cols} columns.')


##----SAVE----##

# status update
status_update('Trying to save...')

# loop through index and multiples of 10 million
for ind, i in enumerate(range(0, 110000000, 10000000), 1):
	
	# save (via compressed pickle) a dataframe of 10 million rows, use index for unique file names
	df_merged.iloc[i:i+10000000].to_pickle(f'{data_path}seattle_lib_{ind}.pkl', compression='gzip')
    
	# print status/time
	status_update(f'File {ind} out of 11 saved successfully')\

# # compressed pickle
# df_merged.to_pickle(data_path + 'seattle_lib.pkl', compression='gzip')

# with gzip.open(data_path + 'seattle_lib.pkl', 'wb') as goodbye:
#     pickle.dump(df_merged, goodbye, protocol=pickle.HIGHEST_PROTOCOL)

# status update
status_update('Save successful!')


##----LOAD----##

# print status/time
status_update('Begin load...')

# load first part
df = pd.read_pickle('data/seattle_lib_1.pkl', compression='gzip')

# print status/time
status_update('File 1 loaded successfully.')

# iterate through 2-11
for i in range(2, 12):

    # load parts 2-11
    to_add = pd.read_pickle(f'data/seattle_lib_{i}.pkl', compression='gzip')
    
    # print status/time
    status_update(f'File {i} loaded successfully.')

    # combine with previous part
    df = pd.concat([df, to_add], ignore_index=True)
    
    # print status/time
    status_update(f'Concatenation successful. DataFrame consists of files 1-{i}.')
    
# print status/time
status_update('Load complete!')