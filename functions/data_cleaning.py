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


def status_update(msg, timestamp_form='%H:%M:%S'):
    '''

    Function to print current time and an input message.


    Input
    -----
    msg : str
            Message to print under the current time.


    Optional input
    --------------
    timestamp_form : str
            Format for current time (default = '%H:%M:%S').
            For more format options, visit:
            `https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior`


    Output
    ------
    None

    '''

    # current time
    time_status = f'Current time = {timestamp(form=timestamp_form)}'
    print(time_status)

    # separating line
    print('-' * len(time_status))

    # input message
    print(msg)

    # blank line to separate subsequent messages
    print('')


def transform_category(df, search_col, transform_col, values, replacer):
    '''

    Function to lump multiple values within a Pandas DataFrame column
    with dtype of 'category' into one label.


    Input
    -----
    df : Pandas DataFrame
            DataFrame containing the column to transform.

    search_col : str
            Name of the column to search for values.

    transform_col : str
            Name of the column with values to transform.

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
        np.where(df[search_col].isin(values), replacer, df[transform_col])
    )

    return converted


def load_multi_df(
        data_path,
        file_prefix,
        ext,
        num_files,
        compression='infer',
        verbose=0):
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

    ext : str
            Extension of the files.
            NOTE: This should not include any leading dots,
                      i.e. 'pkl' should be used over '.pkl'.

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
    df = pd.read_pickle(
        f'{data_path}{file_prefix}1.{ext}',
        compression=compression)

    if verbose == 2:
        # print status/time
        status_update('File 1 loaded successfully.')

    # iterate through files
    for i in range(2, num_files + 1):

        # load parts 2 through num_files
        to_add = pd.read_pickle(
            f'{data_path}{file_prefix}{i}.{ext}',
            compression=compression)

        if verbose == 2:
            # print status/time
            status_update(f'File {i} loaded successfully.')

        # combine with previous part
        df = pd.concat([df, to_add], ignore_index=True)

        if verbose == 2:
            # print status/time
            status_update(
                f'Concatenation successful. DataFrame consists of files 1-{i}.')

    if verbose:
        # print status/time
        status_update('Load complete!')

    return df


def name_splitter(name, cutoff):
    '''

    Function to split long strings for use in horizontal bar chart.


    Input
    -----
    name : str
            Name of object to graph.

    cutoff : int
            Number of characters to include on one line of graph.


    Output
    ------
    name : str
            Name with endline character splitting string.

    '''

    # split string into separate words
    splitted = name.split()

    # instantiate empty string
    name = ''

    # instantiate index counter
    i = 0

    # while string is below threshold
    while len(name) <= cutoff - 5:

        # add word and space to list
        name += splitted[i] + ' '

        # iterate through index
        i += 1

    # add endline character and remaining words of string
    name += '\n' + ' '.join(splitted[i:])

    return name


def name_beautifier(name, cutoff=25, **kwargs):
    '''

    Function to split long strings and beautify them for use in horizontal bar chart.


    Input
    -----
    name : str
            Name of object to graph.


    Optional input
    --------------
    cutoff : int
            Number of characters to include on one line of graph (default=25).


    Output
    ------
    name : str
            Input capitalized, with endline character and/or ellipsis if too long.

    '''

    # strings more than twice as long as cutoff
    if len(name) > cutoff * 2:

        # split into two lines
        name = name_splitter(name, cutoff)

        # split first 50 characters into two strings
        resplitted = name[:50].split('\n')

        # split second string into words
        resplitted[1] = resplitted[1].split()

        # replace last word with ellipsis
        resplitted[1][-1] = '...'

        # rejoin words
        resplitted[1] = ' '.join(resplitted[1])

        # rejoin two strings
        name = '\n'.join(resplitted)

    # strings longer than cutoff
    elif len(name) > cutoff:

        # split into two lines
        name = name_splitter(name, cutoff)

    # strings shorter than cutoff --> do nothing
    else:
        pass

    return name.title()


def imputer(df, ind, col, window, unit='W'):
    '''
    Function to impute values based on the average of previous and future values.


    Input
    -----
    df : Pandas DataFrame
        DataFrame with source values.

    ind : timestamp
        Index of row to impute.

    col : str
        Name of column containing value to impute.

    window : int
        Number of previous and future units to consider in tallying the average.


    Optional input
    --------------
    unit : str
        The unit of time to consider in tallying the average.
        For possible values, refer to:
                `https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html`


    Output
    ------
    avg : float
        Average value of values within previous and future window.

    '''

    # instantiate empty list
    values = []

    # loop through each value within the index
    for i in range(1, window + 1):

        # previous timestamp
        prev_time = ind - pd.to_timedelta(i, unit=unit)

        # future timestamp
        next_time = ind + pd.to_timedelta(i, unit=unit)

        # value for previous timestamp
        prev_val = df[df.index == prev_time][col].values[0]

        # value for future timestamp
        next_val = df[df.index == next_time][col].values[0]

        # append to list
        values.append(prev_val)
        values.append(next_val)

    # remove any NaN values
    values = [val for val in values if not np.isnan(val)]

    # if there are values in the list
    if values:
        # calculate the average value and round
        avg = round(sum(values) / len(values))
        return avg

    # if list is empty, return NaN
    else:
        return np.nan
