import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
from FetchData import fetch_data_new

# Simulate a DataFrame with sample closing prices
# Replace this with actual data

def get_data():
    param = {"symbol": 'SPY', "time_interval": 'd'}
    sstock_daily = fetch_data_new(param)
    return sstock_daily[0:5*52*10]

today = datetime.today()

start_date = today.replace(year=today.year-10)  #for 10 years
"""
data = {
    "date": pd.date_range(start=start_date.strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d"), freq="B"),  # Business days
    "closing_price": np.random.uniform(100, 200, 261)  # Random closing prices
}
df = pd.DataFrame(data)
"""

# Convert date column to datetime
#df["date"] = pd.to_datetime(df["date"])

df = pd.DataFrame(get_data())
df['date']=pd.to_datetime(df["Date"])
df['closing_price'] = df["Close"]

# Find Triple Witching Fridays
def is_triple_witching_friday(date):
    """Check if a date is a Triple Witching Friday."""
    if date.month in [3, 6, 9, 12] and date.weekday() == 4:  # Check for Friday
        # Get the third Friday of the month
        calendar_month = calendar.monthcalendar(date.year, date.month)
        third_friday = [week[4] for week in calendar_month if week[4] != 0][2]
        return date.day == third_friday
    return False

# Identify Triple Witching Fridays
df["is_triple_witching"] = df["date"].apply(is_triple_witching_friday)

# Calculate differences
triple_witching_days = df[df["is_triple_witching"]]
# triple_witching_days["previous_day_price"] = triple_witching_days["closing_price"].shift(1)
triple_witching_day_previous_indexes = triple_witching_days.index -1
triple_witching_days["previous_day_price"] = df.iloc[triple_witching_day_previous_indexes]["closing_price"]
triple_witching_days["price_difference"] = (
    triple_witching_days["closing_price"] - triple_witching_days["previous_day_price"]
)

# Plot the scatter chart
plt.figure(figsize=(10, 6))
plt.scatter(
    triple_witching_days["date"],
    triple_witching_days["price_difference"],
    color="blue",
    alpha=0.7,
    label="Price Difference"
)
plt.axhline(0, color="red", linestyle="--", label="No Difference")
plt.title("Price Differences on Triple Witching Fridays")
plt.xlabel("Date")
plt.ylabel("Price Difference")
plt.legend()
plt.grid(True)
plt.show(block=True)
