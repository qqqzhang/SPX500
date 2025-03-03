# chart for a certain date range
import pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from FetchData import fetch_data_new
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

 # find the number of trading days between 2 days, inclusive
def get_num_of_trading_days(start, end):
    nyse = mcal.get_calendar('NYSE')
    # Get the schedule for the period
    date_schedule = nyse.schedule(start_date = start.strftime("%Y-%m-%d") , end_date = end.strftime("%Y-%m-%d"))
    return date_schedule.shape[0]

def week_of_month(date):
    """
    Calculate the week of the month for a given date.
    A week starts on Monday (ISO-8601 standard).
    """
    # First day of the month
    first_day = date.replace(day=1)
    
    # Calculate the day offset from Monday (0=Monday, 6=Sunday)
    first_weekday = first_day.weekday()
    
    # Calculate the week number
    week_number = (date.day + first_weekday - 1) // 7 + 1
    
    return week_number

def weekday_in_nth_week(date, nth_week, weekday):
    """
    Find the specific weekday in the nth week of a given month.
    The week starts on Sunday.
    
    Args:
        year (int): The year (e.g., 2025).
        month (int): The month (1-12).
        weekday (int): The day of the week (0=Sunday, ..., 6=Saturday).
        nth_week (int): The nth week (1-based index).
    
    Returns:
        date: The corresponding date.
    """
    # Set the first day of the week to Sunday
    calendar.setfirstweekday(calendar.SATURDAY)
    year = date.year
    month = date.month
    # Get the calendar matrix for the month
    calendar_month = calendar.monthcalendar(year, month)

    
    # Ensure the nth week exists
    if nth_week > len(calendar_month):
        print(f"Month {month} in {year} has no {nth_week} weeks, using previous week instead")
        nth_week -= 1
    
    # Get the nth week's list
    week = calendar_month[nth_week - 1]
    
    # Check if the specified weekday exists in the week
    day = week[weekday]
    if day == 0:
        print(f"Week {nth_week} of {calendar.month_name[month]} {year} does not have a {calendar.day_name[weekday]}. using the next week instead")
        if nth_week < len(calendar_month):  # does not go to next month
            week = calendar_month[nth_week]
            day = week[weekday]
        else:
            month += 1
            i = 0
            while(week[i] != 0):
                week[i] = i + 1
                i += 1
            w = [0] *(7-i) + week[:i]
            day = w[weekday]



    # Return the date
    r = datetime.datetime(year, month, day)
    print(r.strftime("%A"))
    return r

# get the list of start dates based on the alignWeek param
def  get_start_date_list(start, end, algnWk, low_day, upper_day):
    start_dates = []
    start_mon = start.month
    start_day = start.day
    check_year = low_day.year

    dateToCheck = datetime.datetime(check_year, start_mon, start_day)

    # find the first start inside the day range
    while( dateToCheck < low_day) :
        check_year += 1
        dateToCheck = datetime.datetime(check_year, start_mon, start_day)

    # now adding start days to the list
    algn_d = ( start.weekday() + 2 ) % 7  # Saturday based
    algn_w = week_of_month(start)

    while(dateToCheck < upper_day):
        if algnWk :  # need to align with the week day (example, from a Thur as start of range)
            wk_d = (dateToCheck.weekday()+ 2 ) % 7  # Saturday based
            if algn_d != wk_d:  # if not same day of week as start date, shift to find the same week day and add that instead
                start_dates.append( weekday_in_nth_week(dateToCheck,algn_w, algn_d) )
                """
                diff_d = wk_d - algn_d
                if diff_d > 0:  # checked date is after what we are looking for, reduce ( looking for Thu, get Fri)
                    start_dates.append(dateToCheck - datetime.timedelta(days=diff_d) )
                else: # before what we are looking for, add days ( looking for Thu, get Tue)
                    start_dates.append(dateToCheck + datetime.timedelta(days=-diff_d) )
                """
            else:
                start_dates.append(dateToCheck)        
        else:
            start_dates.append(dateToCheck)      
        check_year += 1
        dateToCheck = datetime.datetime(check_year, start_mon, start_day)
    
    return start_dates

def plot_daily_array( data_array, params):
    year_dict = {}
    HO = []
    OL = []
    LB=[]
    annots = {}
    ticker = params["ticker"];
    start = params["start"]
    end = params["end"]
    algnWk = params["alignWeek"]
    compareDaily = params["compareDaily"]

    # find the number of trading days
    num_trading_days = get_num_of_trading_days(start, end)

    # get the list of start dates
    df = pd.DataFrame(data_array)
    allDays = df["Date"].to_list()

    startDateList = get_start_date_list(start, end, algnWk, min(allDays), max(allDays))

    #filter data
    data = sorted(data_array, key=lambda x: x['Date'])
    startDateList.sort()
    print(startDateList)
    lookFor = startDateList.pop(0)

    for index, item in enumerate(data):          
        if ( item["Date"] >= lookFor and not year_dict.get(str(item["Date"].year)) ): # found first date, add         
            current_year = str(item["Date"].year)
            year_dict[current_year] = data[index:index + num_trading_days]
            if item["Date"] > lookFor:
                 print(f"Looking for {lookFor.strftime('%Y-%m-%d')}, Found {year_dict[current_year][0]['Date'].strftime('%Y-%m-%d')} ")
            if startDateList:
                lookFor = startDateList.pop(0)
            else:
                break
        

    # Time to plot
    print(f"{ticker.upper()}:")
    mn = []
    mx = []
    line_points = []
    upC = 0
    downC =  0
    total = 0
    x_values = list(range(1, num_trading_days+1))  # x-values for each array (1, 2, ..., 12)
    for key in year_dict.keys():
        array = pd.DataFrame(year_dict[key])
       
     #   y_values = array["Close"].to_list()

        close_array = np.array(array["Close"].to_list())
        if compareDaily:
            open_array = np.array(array["Open"].to_list())
            difference = (close_array - open_array)
            upC += np.sum(difference > 0)
            downC += np.sum(difference < 0)
            total += len(difference)
            close_array = difference/open_array*100
        else:
            open_price = array["Open"][0]
            close_array = (close_array - open_price)*100/open_price    # percentage compare to first open price
        y_values = np.round(close_array, 2).tolist()
        line_points.append(y_values)
        # Plot image
        plt.scatter(x_values, y_values, s=6, label=f"{key}")
        """
        arr = np.array(array["Low"].to_list())
        get the high and low
        mn.append(np.min(arr))
        mnL = np.mean(arr)/array["Open"][0] -1
        arr = np.array(array["High"])
        mnH = np.mean(arr)/array["Open"][0] -1
        mx.append(np.max(arr))
        open_close = float(array["Close"].tail(1) - array["Open"][0])/array["Open"][0]*100
        """       
        for index, point in enumerate(x_values) :
            k = f"{point}.00,{float(y_values[index]):.2f}"
            day_away = array["Date"][index] - array["Date"][0]
            annots[k] = f"{array["Date"][index].strftime("%Y-%m-%d %a")} +{day_away.days} Days Change:{y_values[index]:.2f}% H:{array["High"][index]} L:{array["Low"][index]} O:{array["Open"][index]} C:{array["Close"][index]}"
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
    year_list = np.array(line_points)
    median_column = np.median(year_list, axis=0)
    plt.plot(x_values , median_column.tolist(), label=f"")
    plt.ylim( np.min(year_list) -20, np.max(year_list) + 20)

    # Step 3: Customize the plot
    if compareDaily:
        plt.title(f"Line Plot of {ticker.upper()} for the past {len(year_dict)} years, compared Daily {upC}/{downC} ({upC/total*100:.2f}%/{downC/total*100:.2f}%)")
    else:
        plt.title(f"Line Plot of {ticker.upper()} for the past {len(year_dict)} years, compare to the Start Date")
    plt.xlabel(f'Days from {start.strftime("%m-%d")} to {end.strftime("%m-%d")}')
    plt.text(  np.max(year_list)/2, -30, f'Week Day Aligned: { "Yes" if algnWk else "No"}', color='r', verticalalignment='top', horizontalalignment='center', fontsize=12)
    plt.ylabel('Price % range')
    plt.legend(loc='lower center', ncol=10)
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

    while start.isoweekday() > 5 : # find the first weekday in case start is on weekend
        start = start+ datetime.timedelta(days=1) 
    f_y = today.year - 1
    f_m = last_day.month
    f_d = last_day.day
    f = datetime.datetime(f_y, f_m, f_d)
    keepFor = (today-f).days - 30
    fetch_param = { "symbol": ticker, "time_interval": 'd', "keepFor": keepFor}
    sstock_daily = fetch_data_new(fetch_param)
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
    if last_day > today:    # end of range is in the future, so we don't have this year's range, remove the last data from start 
        filtered_daily = df[df['Date'] < start]
        filtered_daily_dict = filtered_daily.to_dict(orient='records')
    # limit data up to the last 10 years
    stock_daily = filtered_daily_dict[0:5*52*10]   

    plot_daily_array( stock_daily, { "ticker" : ticker, "start": start, "end": last_day , "alignWeek": params["alignWeek"] or False, "compareDaily": param["compare_range"]=="daily" })
 
    plt.axhline(0, color='grey', linestyle='-', linewidth=1)
    plt.axhline(5, color='grey', linestyle='--', linewidth=1, label=f'5%')
    plt.axhline(-5, color='grey', linestyle='--', linewidth=1, label=f'-5%')
    plt.axhline(10, color='grey', linestyle='--', linewidth=1, label=f'10%')
    plt.axhline(-10, color='grey', linestyle='--', linewidth=1, label=f'-10%')
    plt.axhline(20, color='grey', linestyle='--', linewidth=1, label=f'20%')
    plt.axhline(-20, color='grey', linestyle='--', linewidth=1, label=f'-20%')
    
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
            sel.annotation.set_text(f"{ydata:.2f}%")
        
if __name__ == "__main__":
    from mplcursors import cursor , HoverMode
    param = {}
    param["ticker"] = 'iwm'
    param["start"] = '2021-3-1'
    param["end"] = '2021-3-31'
    param["alignWeek"] = False
#    param["alignWeek"] = True
#    param["compare_range"] = "range"
    param["compare_range"] = "daily"
 

    plt.figure(figsize=(16, 6))
    # Display the plot
    plot_date_range(param)

    cursor = cursor(hover=HoverMode.Transient)
    cursor.connect("add", on_hover)
    
    plt.show(block=True)
