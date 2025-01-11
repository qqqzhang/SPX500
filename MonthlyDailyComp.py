import pylab
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
from FetchData import fetch_data
import datetime
import calendar
import pandas_market_calendars as mcal
import settings

# Set a font that supports Chinese characters (e.g., SimHei for Simplified Chinese)
rcParams['font.sans-serif'] = ['SimHei']  # Use 'SimHei' for Chinese fonts
rcParams['axes.unicode_minus'] = False  # Ensure that minus signs are displayed properly

def plot_monthly_array_daily_compare(data,ticker,month, plot_month):
    items = {}
    annots = {}
    day_dict = {}

    for item in data:
        y = item["year"]
        if not y  in items:
            items[y] = {"x":[], "y":[]}
        items[y]["x"].append(item["day"])
        items[y]["y"].append(item["diff"])

    ML = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]    
    for p, ki in enumerate(items.keys()): # loop through each year
        array=items[ki]
        m_dict = dict(zip(array["x"], array["y"]))
        # Appending each OC value to its month day array
        for key, value in m_dict.items():
            if not key in day_dict:
                day_dict[key] = []  # create entry if values not exists
            day_dict[key].append(value)

        if month == plot_month:  #plot the specified month if it matches
        # Plot line
            plt.scatter(array["x"], array["y"], s=20, label=f"{ki}")
            for index, point in enumerate(array["x"]) :
                k = str(point) +"," + str(array["y"][index])
                annots[k] = f"{ki}-{month}-{point}"

    # Checking for only up/down days
    print(f"{ML[month-1]}:")
    for d, v in day_dict.items():
        ca = np.array(v)
        if np.max(ca) <= 0 and len(v) > 1 :
            print(f"{month}/{d:02d}: 0/{len(v)}  down ")
        elif np.min(ca) >= 0 and len(v) > 1 :
            print(f"{month}/{d:02d}: {len(v)}/0  up ")

    # Customize the plot
    if month == plot_month:
        plt.title(f"{ticker.upper()} in {ML[month-1]} for the past {len(items.keys())-1} years")
        plt.xlabel('Day of Month')
        plt.ylabel('Percentage')
        plt.legend(loc='lower center', ncol=6)
    # Draw a horizontal line at y = 0
        plt.axhline(y=10, color='lightgrey', linestyle=':')
        plt.axhline(y=-10, color='lightgrey', linestyle=':')
        plt.axhline(y=5, color='lightgrey', linestyle=':')
        plt.axhline(y=-5, color='lightgrey', linestyle=':')
        plt.axhline(y=0, color='grey', linestyle='--')
        settings.annot_data = annots
 
def plot_monthly_daily_compare(ticker, month):
    stock_monthly = fetch_data(ticker, 'd', "7HMUMJ9DCMIOGGK0")
    
    # limit data up to the last 10 years
    stock_monthly = stock_monthly[0:10*52*5]
    df = pd.DataFrame(stock_monthly)
    df["Date"] = pd.to_datetime(df['Date'])
    df["month"] = df["Date"].dt.month
    df["year"] = df["Date"].dt.year
    df["day"] = df["Date"].dt.day
    df["diff"] = pd.to_numeric(df['OC'])
    df['up'] =  pd.to_numeric(df['HO'])
    df['down'] = pd.to_numeric(df['OL'])
    
    print(f"{ticker.upper()}:")

    for imonth in range(1,13):
        filtered_df = df.loc[df["month"] == imonth]
        sorted_df = filtered_df.sort_values(by=["year", "day"], ascending=[True, True])
        plot_monthly_array_daily_compare(sorted_df.to_dict(orient='records'), ticker, imonth, month)

def on_hover(sel):
        # Access attributes of the selected artist
        xdata = sel.target[0]
        ydata = sel.target[1]

        # Customize annotation text
        key = f"{int(xdata)},{ydata}"
        if key in settings.annot_data:
            sel.annotation.set_text(f"{settings.annot_data[key]}:{ydata:.2f}%")
        else:
            sel.annotation.set_text(f"{ydata:.2f}%")

if __name__ == "__main__":
    from mplcursors import cursor , HoverMode
    ticker = 'xlb'
    month = 11  # 1 based
    plt.figure(figsize=(12, 8))
    # Display the plot
    plot_monthly_daily_compare(ticker, month)
    cursor = cursor(hover=HoverMode.Transient)
    cursor.connect("add", on_hover)
    
    plt.show(block=True)