import time
from datetime import datetime, timedelta
import pandas as pd
import requests
import os

def flatten_dict(d):
    items = []
    for k, v in d.items():
        nv = {}
        nv['Date'] = k
        nv['Open'] = v['1. open']
        nv['High'] =v['2. high']
        nv['Low'] = v['3. low']
        nv['Close']=v['4. close']
        nv['Volume'] = v['5. volume']
        nv['HL'] = (float(v['2. high']) - float(v['3. low'])) * 100 / float(v['1. open'])
        nv['OC'] = (float(v['4. close']) - float(v['1. open'])) * 100 / float(v['1. open'])
        nv['HO'] = (float(v['2. high']) - float(v['1. open']) ) * 100 / float(v['1. open'])
        nv['OL'] = (float(v['3. low']) - float(v['1. open']) ) * 100 / float(v['1. open'])
        items.append(nv)
    return items

def fetch_data(symbol, time_interval):    # fetch_data('MSFT', 'd')
    apiKey = "4YACG8H1XDKSSW6I"     # "7HMUMJ9DCMIOGGK0"
    intervals = { 'd': "TIME_SERIES_DAILY",
                  'D': "TIME_SERIES_DAILY",
                  'w': "TIME_SERIES_WEEKLY",
                  'W': "TIME_SERIES_WEEKLY",
                  'm': "TIME_SERIES_MONTHLY",
                  "M": "TIME_SERIES_MONTHLY"
                }
    ticker = symbol.upper()
    file_path = f"J:/My Drive/Tech/Python/SPX500/hist_data/{ticker}_{intervals[time_interval]}_output_table.csv"
    # Check if the file exists
    if os.path.exists(file_path):
        # Get the current time
        current_time = datetime.now()
        
        # Get the last modification time of the file
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Calculate the time 24 hours ago
        time_24_hours_ago = current_time - timedelta(hours=24)
        
        # Check if the file was modified within the last 24 hours
        if last_modified_time > time_24_hours_ago:
            df = pd.read_csv(file_path)
            flat_data = df.to_dict(orient='records')
            return flat_data
    else:
        print(f"{file_path} does not exist.")

    interval = intervals[time_interval]
    query_string = f"https://www.alphavantage.co/query?function={interval}&symbol={ticker}&apikey={apiKey}"
    response = requests.get(query_string)

    data = response.json()
    try:
        data_fields = {
            "TIME_SERIES_DAILY": "Daily Time Series",
            "TIME_SERIES_WEEKLY": "Weekly Time Series",
            "TIME_SERIES_MONTHLY": "Monthly Time Series"
        }
        flat_data = flatten_dict(data[data_fields[intervals[time_interval]]])
    except KeyError:
        print(data["Information"])
        df = pd.read_csv(file_path)
        flat_data = df.to_dict(orient='records')
        return flat_data
    else:
        df = pd.json_normalize(flat_data)
        df.to_csv(file_path, index=False)
        return flat_data


if __name__ == "__main__":
    ticker = 'SPY'
    hist_data = fetch_data(ticker, 'w')
    print(hist_data)
    # Step Save the DataFrame to a CSV file
    print(f"Table saved to 'hist_data/{ticker}_*_output_table.csv'")