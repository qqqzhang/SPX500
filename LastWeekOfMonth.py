import pandas as pd
import numpy as np

# Load the CSV file
raw_data = pd.read_csv('SPX500.csv')

raw_data['Date'] = pd.to_datetime(raw_data['Date'])
raw_data = raw_data.sort_values(by='Date').reset_index(drop=True)

def get_last_week_of_month(data):
 #   last_days = df.groupby([df['Date'].dt.year, df['Date'].dt.month]).tail(5)
 #   return last_days
    # Extract the day of the week (0=Monday, 6=Sunday) and the day of the month
    data['Day_of_Week'] = data['Date'].dt.dayofweek  # 0=Monday, ..., 6=Sunday
    data['Month_End'] = data['Date'].dt.is_month_end # | \
#      (data['Date']+ pd.Timedelta(days=1)).dt.is_month_end # | \
#      (data['Date']+ pd.Timedelta(days=0)).dt.is_month_end # Boolean flag for last day of the month

    # Filter data where the day is the end of the month and is Wednesday (2), Thursday (3), or Friday (4)
    filtered_data = data[(data['Month_End']) & (data['Day_of_Week'].isin([3,4]))]

    # Group the data by year and week number
    filtered_weeks = filtered_data['Date'].dt.strftime('%Y-%U')  # Week number (Sunday as start of week)

    data['Year_Week']=data['Date'].dt.strftime('%Y-%U')

    # Select relevant weeks by Year_Week
    selected_weeks = data[(data['Year_Week'].isin(filtered_weeks))];

    return selected_weeks.sort_values(by=['Year_Week', 'Day_of_Week'])


last_week_data = get_last_week_of_month(raw_data)

def get_diff(last_week) :
    first_day_open = last_week.iloc[0]['Open']
 #   if(last_week.iloc[0]['Day_of_Week'] == 0):  # Use Tuesday Open price
 #       first_day_open = last_week.iloc[1]['Open']
    last_day_close = last_week.iloc[-1]['Close/Last']
    if(len(last_week.values) < 4):
       print(f" ****************** Pontial bad data detected: ************************************\n {last_week.values} *********************************************************")
    return first_day_open, last_day_close 

def calculate_performance(last_week):
    open_price, close_price = get_diff(last_week)
    return close_price >= open_price

def select_down_day_percent(last_week):
    open_price, close_price = get_diff(last_week)
    if close_price >= open_price :
        return 0
    else:
        print(f"{last_week.iloc[0]['Date']} - {last_week.iloc[-1]['Date']} : { (close_price - open_price)/open_price * 100:.2f}%")
        return (close_price - open_price)/open_price * 100


last_week_group = last_week_data.groupby([last_week_data['Year_Week']])
# leftout =last_week_group.filter( lambda days_in_week: len(days_in_week) < 4)
#last_week_group = last_week_group[last_week_group['Open'].apply( lambda x: x.size >= 4) ]
last_week_performance = last_week_group.apply(calculate_performance)
percentage_higher = last_week_performance.mean() * 100

down_weeks = last_week_data.groupby([last_week_data['Year_Week']]).apply(select_down_day_percent)
percentage_lower = np.array([ num for num in down_weeks if num != 0 ])
bins = [0, 1,2,3,4,5, 50]
labels = ['0-1', '1-2', '2-3', '3-4', '4-5', '> 5']

print(f"Total weeks included: {last_week_performance.size} ")
print(f"Percentage of months with higher closes in last week of the month: {percentage_higher:.2f}%  -- {last_week_performance.sum()}")
print(f"Percentage of months with lower closes in last week of the month has mean: {percentage_lower.mean():.2f}%  max: {percentage_lower.min():.2f}%  min:  {percentage_lower.max():.2f}%   median:  {np.median(percentage_lower):.2f}%  ")

# Use histogram to get counts in each bin

hist, bin_edges = np.histogram(np.abs(percentage_lower), bins=bins)
print("Percentage of months with lower closes:\n")
# # Display results
for count, label in zip(hist, labels):
    print(f"Range {label}: {count * 100 /percentage_lower.size: .2f} % - {count}")
