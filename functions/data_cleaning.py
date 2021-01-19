from datetime import datetime
import pandas as pd
import numpy as np


def timestamp(form='%H:%M:%S'):

	'''

	Function to retrieve the current time as a string.


	Optional input
	--------------
	form : str
		Format for output (default = '%H:%M:%S').
		For more format options, visit:
		`https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior`


	Output
	------
	current_time : str
		Current time as a string.

	'''

	# current time
	now = datetime.now()

	# convert to string and desired format
	current_time = now.strftime(form)

	return current_time


def status_update(msg):

	'''

	Function to print current time and an input message.


	Input
	-----
	msg : str
		Message to print under the current time.


	Output
	------
	None

	'''

	# current time
	print('Current time =', timestamp())

	# separating line
	print('-----------------------')

	# input message
	print(msg)

	# blank line to separate subsequent messages
	print('')



def transform_category(df, col, values, replacer):

	'''

	Function to lump multiple values within a Pandas DataFrame column 
	with dtype of 'category' into one label.


	Input
	-----
	df : Pandas DataFrame
		DataFrame containing the column to transform.

	col : str
		Name of the column to transform.

	values : list (str)
		List of value(s) to transform.

	replacer : str
		Value to replace each value in values with.


	Output
	------
	converted : Pandas Series
		Transformed column.

	'''

	# pandas 'category' object
	converted = pd.Categorical(

		# replace values
	    np.where(df[col].isin(values), replacer, df[col])
	)

	return converted



def load_multi_df(data_path, file_prefix, num_files, compression='infer', verbose=0):

	'''

	Function to load multiple Pickle files and concatenate them into one Pandas DataFrame.

	NOTE: Files must have a consistent naming structure, with sequential numerical
	endings.
		For example, `file_1`, `file_2`, `file_3`, etc. The `file_prefix` in this 
		instance would be 'file_'.


	Input
	-----

	data_path : str
		Pathway that contains the files to load.
		NOTE: Must end in '/'.

	file_prefix : str
		Consistent prefix of each file.

		For example, `file_1`, `file_2`, `file_3`, etc. The `file_prefix` in this 
		instance would be 'file_'.

	num_files : int
		Number of files to load.


	Optional input
	--------------
	compression : str
		String denoting type of compression, if any (default='infer').

		For more info, visit:
		`https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_pickle.html`

	verbose : int
		Setting of status updates (including timestamps). Valid options are 0, 1, or 2.
		0 : No updates/printouts.
		1 : Only update when load begins or is complete.
		2 : Update after each file is successfully loaded and successfully added to
			the DataFrame. 


	Output
	------
	df : Pandas DataFrame
		Single DataFrame from all loaded parts.

	'''

	if verbose:
		# print status/time
		status_update('Begin load...')

	# load first part
	df = pd.read_pickle(data_path + file_prefix + '1', compression=compression)

	if verbose == 2:
		# print status/time
		status_update('File 1 loaded successfully.')

	# iterate through files
	for i in range(2, num_files+1):

	    # load parts 2 through num_files
	    to_add = pd.read_pickle(data_path + file_prefix + str(i), compression=compression)
	    
	    if verbose == 2:
		    # print status/time
		    status_update(f'File {i} loaded successfully.')

	    # combine with previous part
	    df = pd.concat([df, to_add], ignore_index=True)
	    
	    if verbose == 2:
		    # print status/time
		    status_update(f'Concatenation successful. DataFrame consists of files 1-{i}.')
	
	if verbose:
		# print status/time
		status_update('Load complete!')

	return df