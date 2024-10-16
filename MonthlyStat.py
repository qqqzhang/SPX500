import pylab
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
from FetchData import fetch_data

# Set a font that supports Chinese characters (e.g., SimHei for Simplified Chinese)
rcParams['font.sans-serif'] = ['SimHei']  # Use 'SimHei' for Chinese fonts
rcParams['axes.unicode_minus'] = False  # Ensure that minus signs are displayed properly

def plot_monthly_array(data):
    items = [[],[],[],[],[],[],[],[],[],[],[],[]]

    for item in data:
        items[item["month"]-1].append(item['diff'])      
    plt.figure(figsize=(10, 6))
    for i, array in enumerate(items):
        x_values = np.full(len(array), i+1)  # x-values for each array (1, 2, ..., 12)
        r_values = np.random.uniform(-1, 1, x_values.shape) * 0.2
        arr = np.array(array)
        plt.scatter(x_values + r_values, array, s=4, label=f"{i+1}月 {np.sum(arr > 0)}/{np.sum(arr < 0)}")

    # Step 3: Customize the plot
    plt.title(f"Dot Plot of {ticker} each month for the past")
    plt.xlabel('Month Number')
    plt.ylabel('Values')
    plt.legend(loc='lower center', ncol=6)
# Draw a horizontal line at y = 0
    plt.axhline(y=10, color='lightgrey', linestyle=':')
    plt.axhline(y=-10, color='lightgrey', linestyle=':')
    plt.axhline(y=0, color='grey', linestyle='--')
    # Display the plot
    plt.show(block=True)

ticker = 'PYPL'
stock_monthly = fetch_data(ticker, 'm')
df = pd.DataFrame(stock_monthly)
df["Date"] = pd.to_datetime(df['Date'])
df["month"] = df["Date"].dt.month
df["diff"] = pd.to_numeric(df['OC'])

data = plot_monthly_array(df.to_dict(orient='records'))

