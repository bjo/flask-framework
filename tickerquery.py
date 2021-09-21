import requests
import json
import pandas as pd
import numpy as np
import datetime as dt
# hide APIKEY for alphavantage
from dotenv import dotenv_values

config = dotenv_values(".env")
APIKEY = config['APIKEY']

# putting this all together, we can finalize the search4ticker function
def search4ticker(phrase: str = 'GOOG', start_date: str = '2019-12-21', end_date: str = '2021-03-19') -> dict:
    """Return a dict of dates and prices."""
    param_dict = {}
    param_dict['symbol'] = phrase
    param_dict['outputsize'] = 'full'
    # Query daily time series for now
    hist_data = api_query('TIME_SERIES_DAILY', param_dict, APIKEY)
    # The returned index is 'Time Series (Daily)'
    hist_df = pd.DataFrame.from_dict(hist_data['Time Series (Daily)'], orient = 'index')
    hist_df['datetimes'] = [dt.datetime.strptime(date, '%Y-%m-%d') for date in hist_df.index]
    # Series of filtering logic
    filtered = hist_df.loc[hist_df.datetimes >= dt.datetime.strptime(start_date, "%Y-%m-%d")]
    filtered = filtered.loc[filtered.datetimes < dt.datetime.strptime(end_date, "%Y-%m-%d")]
    # reverse the dataframe
    filtered = filtered.iloc[::-1]
    # finally, restrict to first 60 rows if the range exceeds it
    filtered = filtered.iloc[range(min(60, filtered.shape[0]))]
    query_result = {}
    query_result['dates'] = np.array(filtered.datetimes, dtype = 'datetime64[D]')
    query_result['prices'] = np.array(filtered['4. close'], dtype = 'float')
    return query_result

# query function
def api_query(function, param_dict, api_key):
    req_url = 'https://www.alphavantage.co/'
    req_body = '/query?function='
    req_body = req_body + function + '&'
    param_dict['apikey'] = api_key
    param_dict['datatype'] = 'json'
    req_body = req_body + '&'.join([key+'='+param_dict[key] for key in param_dict])
    
    myResponse = requests.get(req_url + req_body)
    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        return(jData)
    else:
      # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()
        return(None)