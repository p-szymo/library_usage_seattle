# standard dataframe packages
import pandas as pd
import numpy as np

# api library
from sodapy import Socrata

from functions.data_cleaning import status_update, transform_category



def api_date_caller(
    url_addon_code,
    api_token,
    date_column,
    begin_date,
    end_date,
    limit=1000000,
    base_url='data.seattle.gov',
    **kwargs
):

    '''
    Function to call the API for Seattle Open Data based on a range of dates.

    Input
    -----
    url_addon_code : str
        Code for particular dataset.

    api_token : str
        Unique user token for calling to API.

    date_column : str
        Name of the column containing date information.

    begin_date : str
        Date or timestamp at which to begin collecting data.
            Built using '%Y-%m-%d' formatting (e.g. '2020-09-14'), but should
            also be able to accept '%Y-%m-%dT%H:%M:%S' (e.g. '2020-09-14T13:14:15')
            formatting.

    end_date : str
        Date or timestamp at which to stop collecting data, not inclusive.
            Built using '%Y-%m-%d' formatting (e.g. '2020-09-14'), but should
            also be able to accept '%Y-%m-%dT%H:%M:%S' (e.g. '2020-09-14T13:14:15')
            formatting.

    Optional input
    --------------
    limit : int
        Maximum number of items (rows) to return (default=1000000, i.e. 1 million).

    base_url : str
        URL for site containing API (default='data.seattle.gov')

    **kwargs
        Possible arguments include:
            select : the set of columns to be returned, defaults to *
            where : filters the rows to be returned, defaults to limit
            order : specifies the order of results
            group : column to group results on
            limit : max number of results to return, defaults to 1000
            offset : offset, used for paging. Defaults to 0
            q : performs a full text search for a value
            query : full SoQL query string, all as one parameter
            exclude_system_fields : defaults to true. If set to false, the
                response will include system fields (:id, :created_at, and
                :updated_at)

    Output
    ------
    results_df : Pandas DataFrame
        Returned items as rows in a Pandas DataFrame.



    Code heavily borrowed from `https://dev.socrata.com/foundry/data.seattle.gov/5src-czff` 
    '''
    
    # instantiate API object, including user's unique token
    client = Socrata(base_url, api_token)
    
    # results returned as JSON from API / converted to Python list of
    # dictionaries by sodapy
    results = client.get(
        url_addon_code,
        where=f"{date_column} between '{begin_date}' and '{end_date}'",
        limit=limit,
        **kwargs
    )
    
    # convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    return results_df


def data_dict_prepper(file_path):

    # load data
    dd = pd.read_csv(file_path)

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

    return dd




def data_transformer(
    df,
    dd_file_path,
    usecols=None, 
    rename=None,
    dt_format='%Y-%m-%dT%H:%M:%S.%f',
    date_col='date',
    code_col='collection'):

    # subset if `usecols` argument
    if usecols:
        df = df[usecols]

    # rename columns if `rename` argument
    if rename:
        df.columns = rename

    # convert to datetime, dropping the hour-minute-second stamp using the `dt.date` attribute
    df[date_col] = pd.to_datetime(df[date_col], format=dt_format).dt.date

    # prep data dictionary for merge
    dd = data_dict_prepper(dd_file_path)

    # merge checkouts dataframe with info from data dictionary
    df_merged = df.merge(dd, left_on=code_col, right_on='code')

    # drop columns
    df_merged.drop(columns=[code_col, 'code'], inplace=True)

    # items to transform
    to_transform = ['SPL HotSpot connecting Seattle', 'FlexTech Laptops',
                    'In Building Device Checkout']

    # custom function to transform format_group column
    df_merged['format_group'] = transform_category(
        df_merged, 'title', 'format_group', to_transform, 'Equipment'
    )

    # custom function to transform format_subgroup column
    df_merged['format_subgroup'] = transform_category(
        df_merged, 'title', 'format_subgroup', to_transform, 'Kit'
    )

    # values to convert
    to_transform = ['Electronic']

    # custom function to transform
    df_merged['format_group'] = transform_category(
        df_merged, 'format_group', 'format_group', to_transform, 'Other'
    )

    # values to convert
    to_transform = ['Miscellaneous', 'On Order', 'Temporary', 'WTBBL', 'Periodical']

    # custom function to transform
    df_merged['category_group'] = transform_category(
        df_merged, 'category_group', 'category_group', to_transform, 'Other'
    )

    return df_merged
