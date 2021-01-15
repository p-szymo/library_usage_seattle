from datetime import datetime
import pandas as pd


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
