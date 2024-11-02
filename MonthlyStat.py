import pylab
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
from FetchData import fetch_data
import datetime
import calendar
import pandas_market_calendars as mcal

# Set a font that supports Chinese characters (e.g., SimHei for Simplified Chinese)
rcParams['font.sans-serif'] = ['SimHei']  # Use 'SimHei' for Chinese fonts
rcParams['axes.unicode_minus'] = False  # Ensure that minus signs are displayed properly

def plot_monthly_array(data,ticker,mx, mn):
    items = [[],[],[],[],[],[],[],[],[],[],[],[]]
    HO = [[],[],[],[],[],[],[],[],[],[],[],[]]
    OL = [[],[],[],[],[],[],[],[],[],[],[],[]]

    print(f"{ticker.upper()}:")
    for item in data:
        items[item["month"]-1].append(item['diff'])
        HO[item["month"]-1].append(item['up'])
        OL[item["month"]-1].append(item['down'])
    for i, array in enumerate(items):
        x_values = np.full(len(array), i+1)  # x-values for each array (1, 2, ..., 12)
        r_values = np.random.uniform(-1, 1, x_values.shape) * 0.2
        arr = np.array(array)
    #   Calculate the mean for up and down month
    #   remove the high and low
    #    nm =  np.min(arr)
    #    nx =  np.max(arr)
    #    arr = arr[arr > nm]
    #    arr = arr[arr < nx] """
    #   calculate adjusted average
        pavg = np.mean(arr[arr >0 ])
        navg = np.mean(arr[arr < 0 ])
    #   add value back
    #   arr = np.append(arr, [nm,nx])       
    #   Calculate the mean for up swings
        uarr = np.array(HO[i])
        nx =  np.max(uarr)
        uarr = uarr[uarr < nx]
        uavg = np.mean(uarr)
    #   Calculate the mean for down swings
        darr = np.array(OL[i])
        nm =  np.min(darr)
        darr = darr[darr > nm]
        davg = np.mean(darr)

    # Plot image
        plt.scatter(x_values + r_values, array, s=6, label=f"{i+1}月 {np.sum(arr > 0)}/{np.sum(arr < 0)}")
        print(f"\n{i+1}:", end=' ')
        if not np.isnan(pavg):
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
            print(f'/{davg:.2f}%')
        
    y_limit = max( 20, (mx - mn)/10)
    plt.ylim(mn -y_limit - 10, mx + 20)

    # Step 3: Customize the plot
    plt.title(f"Dot Plot of {ticker.upper()} each month for the past {len(items[1])} years")
    plt.xlabel('Month Number')
    plt.ylabel('Percentage')
    plt.legend(loc='lower center', ncol=6)
# Draw a horizontal line at y = 0
    plt.axhline(y=10, color='lightgrey', linestyle=':')
    plt.axhline(y=-10, color='lightgrey', linestyle=':')
    plt.axhline(y=5, color='lightgrey', linestyle=':')
    plt.axhline(y=-5, color='lightgrey', linestyle=':')
    plt.axhline(y=0, color='grey', linestyle='--')
 
def plot_monthly(ticker):
    stock_monthly = fetch_data(ticker, 'm')
    # if not pass last trading day of month, remove the current month data
    today = datetime.datetime.now()
    # Use the NYSE (New York Stock Exchange) calendar
    nyse = mcal.get_calendar('NYSE')
    # Get the schedule for the current month
    # Get the first and last date of the current month
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    month_schedule = nyse.schedule(start_date = f'{today.year}-{today.month}-01', end_date =f'{last_day.year}-{last_day.month}-{last_day.day}')
    # Get the last trading day of the month
    last_trading_day = month_schedule.index[-1]
    last_record_date = datetime.datetime.strptime(stock_monthly[0]['Date'], "%Y-%m-%d")
    # Output result
    if today < last_trading_day or last_record_date < last_trading_day:
        print(f"No, today is not the last trading day of the month, which is {last_trading_day}, removing")
        stock_monthly = stock_monthly[1:]

    # limit data up to the last 15 years
    stock_monthly = stock_monthly[0:10*12]
    df = pd.DataFrame(stock_monthly)
    df["Date"] = pd.to_datetime(df['Date'])
    df["month"] = df["Date"].dt.month
    df["diff"] = pd.to_numeric(df['OC'])
    df['up'] =  pd.to_numeric(df['HO'])
    df['down'] = pd.to_numeric(df['OL'])
    max_v = df.max()
    min_v = df.min()
    data = plot_monthly_array(df.to_dict(orient='records'), ticker, max_v['diff'], min_v['diff'])

if __name__ == "__main__":
    ticker = 'alny'
    plt.figure(figsize=(10, 6))
    # Display the plot
    plot_monthly(ticker)
    plt.show(block=True)




