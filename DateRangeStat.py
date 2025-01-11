# chart for a certain date range
import pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from FetchData import fetch_data
import datetime
import calendar
import pandas_market_calendars as mcal
import settings

def get_weekly_diff(stock_history):
    items = []
    for item in stock_history:
        diff = float(item['OC'])
        items.append(diff)

    return items

def get_up_and_down_avg(sorted_data):
    gtz = sorted_data[sorted_data >0 ]
    ltz = sorted_data[sorted_data < 0 ]

    return np.mean(gtz), np.mean(ltz)

def plot_daily_array( data_array, params):
    year_dict = {}
    HO = []
    OL = []
    LB=[]
    annots = {}
    ticker = params["ticker"];
    start = params["start"]
    end = params["end"]
    start_mon = start.month
    start_day = start.day
    print(f"{ticker.upper()}:")

  # find the number of trading days
    nyse = mcal.get_calendar('NYSE')
    # Get the schedule for the period
    date_schedule = nyse.schedule(start_date = start.strftime("%Y-%m-%d") , end_date = end.strftime("%Y-%m-%d"))
    num_trading_days = date_schedule.shape[0]

    #filter data
    current_year = "Empty"
    data = sorted(data_array, key=lambda x: x['Date'])
    for item in data:          
        if ( item["month"] == start_mon and item["day"] >= start_day and not year_dict.get(str(item["Date"].year)) ): # start adding data          
            current_year = str(item["Date"].year)
            year_dict[current_year] = [item]
        elif year_dict.get(current_year) and len(year_dict[current_year]) < num_trading_days:
            year_dict[current_year].append(item)
    mn = []
    mx = []
    for key in year_dict.keys():
        array = pd.DataFrame(year_dict[key])
        x_values = list(range(1, len(array)+1))  # x-values for each array (1, 2, ..., 12)
        y_values = array["Close"].to_list()
    
        arr = np.array(array["Low"].to_list())
    #   get the high and low
        mn.append(np.min(arr))
        mnL = np.mean(arr)/array["Open"][0] -1
        arr = np.array(array["High"])
        mnH = np.mean(arr)/array["Open"][0] -1
        mx.append(np.max(arr))
        open_close = float(array["Close"].tail(1) - array["Open"][0])/array["Open"][0]*100

    # Plot image
        plt.plot(x_values , y_values, 'o-', label=f"{key}:{open_close:.2f}%  HI/LW vs open {mnH*100:.2f}%/{mnL*100:.2f}%")
        for index, point in enumerate(x_values) :
            k = f"{point}.00,{float(array["Close"][index]):.2f}"
            annots[k] = f"{array["Date"][index].strftime("%Y-%m-%d")} H:{array["High"][index]} L:{array["Low"][index]} O:{array["Open"][index]} C:{array["Close"][index]}"
        ### print(f"\n{i+1}: ({np.sum(arr > 0)}/{np.sum(arr < 0)}, ", end='')
        """       if not np.isnan(pavg):
            plt.text(  i+1, np.max(arr[arr >0 ]) + 5,f'{pavg:.2f}%', color='green', verticalalignment='top', horizontalalignment='center', fontsize=11)
            print(f'{pavg:.2f}%', end='')
        if not np.isnan(navg):
            plt.text(  i+1, np.min(arr[arr <0 ]) -5,f'{navg:.2f}%', color='red', verticalalignment='bottom', horizontalalignment='center', fontsize=11)
            print(f'/{navg:.2f}%', end='')
        print(',  ~', end='')
        if not np.isnan(uavg):
            pos = np.max(arr[arr >0 ]) if len(arr[arr > 0]) > 0 else 0
            plt.text(  i+0.5, pos + 10, f'H {uavg:.2f}%',fontsize=10)
            print(f'{uavg:.2f}%', end='')
        if not np.isnan(davg):
            pos = np.min(arr[arr <0 ]) if len(arr[arr <0 ]) > 0 else 0
            plt.text(  i+0.5, pos -10, f'L{davg:.2f}%',  fontsize=10)
            print(f'/{davg:.2f}%', end='')
        print(')') 
    y_limit = max( 20, (mx - mn)/10) """
    plt.ylim( -100, max(mx) + 60)

    # Step 3: Customize the plot
    plt.title(f"Line Plot of {ticker.upper()} for the past {len(year_dict)} years")
    plt.xlabel(f'Days from {start.strftime("%m-%d")} to {end.strftime("%m-%d")} ')
    plt.ylabel('Price')
    plt.legend(loc='lower center', ncol=3)
# Draw a horizontal line at y = 0
    """   plt.axhline(y=10, color='lightgrey', linestyle=':')
    plt.axhline(y=-10, color='lightgrey', linestyle=':')
    plt.axhline(y=5, color='lightgrey', linestyle=':')
    plt.axhline(y=-5, color='lightgrey', linestyle=':')
    plt.axhline(y=0, color='grey', linestyle='--')"""
    settings.annot_data = annots

def plot_date_range(params):
    ticker = params["ticker"]
    today = datetime.datetime.now()
    end = params["end"] + " 16:00:00"
    # Define the format of the date string
    date_format = "%Y-%m-%d %H:%M:%S"
    # Convert string to datetime
    last_day = datetime.datetime.strptime(end, date_format)
    start = datetime.datetime.strptime(params["start"], "%Y-%m-%d" ) if params["start"] else today
    sstock_daily = fetch_data(ticker, 'd')
    df = pd.DataFrame(sstock_daily)
    df["Date"] = pd.to_datetime(df['Date'])
    df["month"] = df["Date"].dt.month
    df["day"] = df["Date"].dt.day
    df["Open"] = pd.to_numeric(df['Open'])
    df['High'] =  pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    # filter out the range for current year if has not ended
    filtered_daily_dict = df.to_dict(orient='records')
    if last_day > today:

        filtered_daily = df[df['Date'] < start]
        filtered_daily_dict = filtered_daily.to_dict(orient='records')
    # limit data up to the last 10 years
    stock_daily = filtered_daily_dict[0:5*52*10]   

    plot_daily_array( stock_daily, { "ticker" : ticker, "start": start, "end": last_day })

    # Step 4: Plot the mean and standard deviations
    """plt.axvline(mean, color='r', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')
    plt.axvline(mean + std_dev, color='b', linestyle='--', linewidth=2, label=f'+1 Std Dev = {mean + std_dev:.2f}')
    plt.axvline(mean - std_dev, color='b', linestyle='--', linewidth=2, label=f'-1 Std Dev = {mean - std_dev:.2f}')
    plt.axvline(mean + 2 * std_dev, color='orange', linestyle=':', linewidth=2, label=f'+2 Std Dev = {mean + 2 * std_dev:.2f}')
    plt.axvline(mean - 2 * std_dev, color='orange', linestyle=':', linewidth=2, label=f'-2 Std Dev = {mean - 2 * std_dev:.2f}')

    plt.axvline(pavg, color='grey', linestyle=':', linewidth=2, label=f'Up avg = {pavg:.2f}')
    plt.axvline(navg, color='grey', linestyle=':', linewidth=2, label=f'Down avg = {navg:.2f}')

    plt.text( mean, -5, f'{mean:.2f}%', color='r', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text( mean + std_dev, -5, f' {mean + std_dev:.2f}%', color='b', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text( mean - std_dev, -5, f' {mean - std_dev:.2f}%', color='b', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  mean + 2 * std_dev, -5, f'{mean + 2 * std_dev:.2f}%', color='orange', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  mean - 2 * std_dev, -5, f'{mean - 2 * std_dev:.2f}%', color='orange', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  pavg, -10, f'{pavg:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  navg, -10, f'{navg:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)
    # Step 5: Customize the plot
    plt.title(f'{ticker.upper()} Weekly Move Mean and Standard Deviations for the past {len(sorted_data)/52:.0f} years', fontsize=15)
    # plt.xlabel('Price', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend() """

def on_hover(sel):
        # Access attributes of the selected artist
        xdata = sel.target[0]
        ydata = sel.target[1]

        # Customize annotation text
        key = f"{xdata:.2f},{ydata:.2f}"
        if key in settings.annot_data:
            sel.annotation.set_text(f"{settings.annot_data[key]}")
        else:
            sel.annotation.set_text(f"{ydata:.2f}")
        
if __name__ == "__main__":
    from mplcursors import cursor , HoverMode
    param = {}
    param["ticker"] = 'anet'
    param["start"] = '2025-1-9'
    param["end"] = '2025-2-17'

    plt.figure(figsize=(16, 6))
    # Display the plot
    plot_date_range(param)

    cursor = cursor(hover=HoverMode.Transient)
    cursor.connect("add", on_hover)
    
    plt.show(block=True)
