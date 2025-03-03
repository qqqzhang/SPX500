import time
from datetime import datetime, timedelta
import pandas as pd
import requests
import os
import json


##
#  import pandas_datareader as web  # only for test data; must be installed with conda or pip
#  df = web.DataReader('aapl', data_source='yahoo', start='2021-03-09', end='2022-06-13')

def flatten_dict(d, over_writes):
    items = []
    for k, v in d.items():
        nv = {}
        if k in over_writes:
            nv = over_writes[k]
            nv['Open'] = str(nv['Open'])
            nv['High'] = str( nv['High'])
            nv['Low'] = str(nv['Low'])
            nv['Close']= str(nv['Close'])
            nv['Volume'] = str(nv['Volume'])
        else :
            nv['Date'] = k
            nv['Open'] = v['1. open']
            nv['High'] =v['2. high']
            nv['Low'] = v['3. low']
            nv['Close']=v['4. close']
            nv['Volume'] = v['5. volume']
        
        nv['HL'] = (float(nv['High']) - float(nv['Low'])) * 100 / float(nv['Open'])
        nv['OC'] = (float(nv['Close']) - float(nv['Open'])) * 100 / float(nv['Open'])
        nv['HO'] = (float(nv['High']) - float(nv['Open']) ) * 100 / float(nv['Open'])
        nv['OL'] = (float(nv['Low']) - float(nv['Open']) ) * 100 / float(nv['Open'])
        items.append(nv)
    return items

def fetch_data_new(param):
    default_dict = { "passKey" : "CWPXMQM12O4J6184", "keepFor" : 1 }
    default_dict.update(param)
    return fetch_data(default_dict["symbol"], default_dict["time_interval"], default_dict["passKey"], default_dict["keepFor"] )

def fetch_data(symbol, time_interval, passKey = "N9A5OUT2ZGS36JAR", keepFor = 1 ):    # fetch_data('MSFT', 'd')
    apiKey = passKey
    intervals = { 'd': "TIME_SERIES_DAILY",
                  'D': "TIME_SERIES_DAILY",
                  'w': "TIME_SERIES_WEEKLY",
                  'W': "TIME_SERIES_WEEKLY",
                  'm': "TIME_SERIES_MONTHLY",  # : "TIME_SERIES_MONTHLY_ADJUSTED"
                  "M": "TIME_SERIES_MONTHLY"
                }
    ticker = symbol.upper()
 #  file_dir= "J:/My Drive/Tech/Python/SPX500/hist_data/"
 #  Get the current file's absolute path
    current_file_path = os.path.abspath(__file__)
    # Get the directory containing the file
    current_directory = os.path.dirname(current_file_path)
    file_dir= current_directory + "/hist_data/"
    file_path = f"{file_dir}{ticker}_{intervals[time_interval]}_output_table.csv"
    # Check if the file exists
    if os.path.exists(file_path):
        # Get the current time
        current_time = datetime.now()
        
        # Get the last modification time of the file
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Calculate the time 24 hours ago
        time_24_hours_ago = current_time - timedelta(hours=24*keepFor)
        
        # Check if the file was modified within the last 24 hours
        if last_modified_time > time_24_hours_ago:
            df = pd.read_csv(file_path)
            flat_data = df.to_dict(orient='records')
            return flat_data
    else:
        print(f"{file_path} does not exist.")

    interval = intervals[time_interval]
    query_string = f"https://www.alphavantage.co/query?function={interval}&symbol={ticker}&apikey={apiKey}&outputsize=full"
    response = requests.get(query_string)

    data = response.json()
    try:
        data_fields = {
            "TIME_SERIES_DAILY": "Time Series (Daily)",
            "TIME_SERIES_WEEKLY": "Weekly Time Series",
            "TIME_SERIES_MONTHLY": "Monthly Time Series",
            "TIME_SERIES_MONTHLY_ADJUSTED": 'Monthly Adjusted Time Series'
        }
        
        overwrite_interval = "daily"
        if intervals[time_interval] == "TIME_SERIES_WEEKLY":
            overwrite_interval="weekly"
        elif intervals[time_interval] == "TIME_SERIES_MONTHLY":
            overwrite_interval="monthly"

        over_writes = {}
        overwrite_file = f"{file_dir}{overwrite_interval}_over_writes.json"
        if os.path.exists(overwrite_file):
            with open(overwrite_file, 'r') as f:
                dict_overwrites = json.load(f)
                if dict_overwrites.get(ticker):
                    over_writes = dict_overwrites.get(ticker)
        
        flat_data = flatten_dict(data[data_fields[intervals[time_interval]]], over_writes)
        
    except KeyError:
        print(data["Information"]) if "Information" in data else print(data)
        df = pd.read_csv(file_path)
        flat_data = df.to_dict(orient='records')
        return flat_data
    else:
        df = pd.json_normalize(flat_data)
        df.to_csv(file_path, index=False)
        return flat_data


if __name__ == "__main__":
    ticker = 'alny'
    hist_data = fetch_data(ticker, 'w')
    print(hist_data)
    # Step Save the DataFrame to a CSV file
    print(f"Table saved to 'hist_data/{ticker}_*_output_table.csv'")