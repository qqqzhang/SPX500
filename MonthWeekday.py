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

def plot_monthly_array_weekday_compare(data,ticker,month, plot_month):
    items = {
        "Date": [],
        "WeekDay": [],
        "Change": [],
    }
 #   annots = {}
    dom = 0   # mark start of the month
    wmk = -1
    wc = 0
    ny = 0
    for item in data:
        if item['day'] < dom : # different year started
            dom = 0
            wc = 0
        if dom == 0: # a new year for the month started
            wmk = item["day"] + 7
            ny += 1
        if item['day'] >= wmk:
            wmk += 7
            wc += 1
        dom = item['day']
        y = f"{item['year']}-{month}-{dom}"
        w = item["Date"].day_of_week + wc*5   # Monday = 0 ...
        c = item["diff"]
        items["Date"].append(y)
        items["WeekDay"].append(w)
        items["Change"].append(c)


    ML = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df = pd.DataFrame(items)
    if month == plot_month:  #plot the specified month if it matches      
        df.plot.scatter(x = "WeekDay", y="Change", cmap="viridis")
 #               annots[k] = f"{ki}-{month}-{point}"

 # Checking for only up/down days
    WL = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    WO = ["1st", "2nd", "3rd", "4th", "5th"]
    print(f"{ML[month-1]}:")
    daylist = np.sort(df["WeekDay"].unique())
    for v in daylist:
        filtered_df = df[df['WeekDay'] == v]
        if filtered_df["Change"].max() <= 0:
             wo = int(v/5)
             wi = v - wo * 5
             avg = np.average(filtered_df["Change"])
             if wo != 4:
                 print(f"{WO[wo]} {WL[wi]}: 0/{filtered_df.size/3:.0f}  avg down: {avg}% ")       # 3 columns thus size/3
        elif filtered_df["Change"].min() >= 0 :
            wo = int(v/5)
            wi = v - wo * 5
            avg = np.average(filtered_df["Change"])
            if wo != 4: 
                print(f"{WO[wo]} {WL[wi]}: {filtered_df.size/3:.0f}/0  avg up: {avg}% ") 

    # Customize the plot
    if month == plot_month:
        plt.title(f"{ticker.upper()} in {ML[month-1]} for the past {ny} years")
        plt.xlabel('WeekDay')
        plt.ylabel('Percentage')
     #   plt.legend(loc='lower center', ncol=6)
    # Draw a horizontal line at y = 0
        plt.axhline(y=10, color='lightgrey', linestyle=':')
        plt.axhline(y=-10, color='lightgrey', linestyle=':')
        plt.axhline(y=5, color='lightgrey', linestyle=':')
        plt.axhline(y=-5, color='lightgrey', linestyle=':')
        plt.axhline(y=0, color='grey', linestyle='--')
     #   settings.annot_data = annots
 
def plot_monthly_weekday_compare(ticker, month):
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
        plot_monthly_array_weekday_compare(sorted_df.to_dict(orient='records'), ticker, imonth, month)

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
    ticker = 'spy'
    month = 11  # 1 based
 #   plt.figure(figsize=(12, 8))
    # Display the plot
    plot_monthly_weekday_compare(ticker, month)
#    cursor = cursor(hover=HoverMode.Transient)
#    cursor.connect("add", on_hover)
    
    plt.show(block=True)