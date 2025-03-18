import pylab
import matplotlib.pyplot as plt
import numpy as np
from FetchData import fetch_data
import os

def get_daily_diff_compare_previous_day(stock_history):
    items = []
    last = len(stock_history) -1 
    for index, item in enumerate(stock_history):
        if index != last:
            prevClose = float(stock_history[index +1]['Close'])
            diff = (float(item['Close']) - prevClose) * 100 / prevClose
            items.append(diff)

    return items

def get_up_and_down_avg(sorted_data):
    gtz = sorted_data[sorted_data >0 ]
    ltz = sorted_data[sorted_data < 0 ]

    return np.mean(gtz), np.mean(ltz), len(gtz), len(ltz), np.median(gtz), np.median(ltz)

def plot_daily(ticker, length = 25):  # length is number of years
    stock_daily = fetch_data(ticker, 'd')
    data = get_daily_diff_compare_previous_day(stock_daily)
    if length < 25: #define length for daily
        data = data[:length * 240]
    sorted_data = np.sort(data)
    mean = np.mean(sorted_data)
    std_dev = np.std(sorted_data)

    pavg, navg, upC, dwnC, upM, dwnM = get_up_and_down_avg(sorted_data)

    onePercent = sorted_data[sorted_data <= 1 ]
    onePercent = onePercent[onePercent >=  -1 ]
    twoPercent = sorted_data[sorted_data <= 2 ]
    twoPercent = twoPercent[twoPercent >=  -2 ] 

    # Step 4: Plot the data as a line plot
    plt.hist(sorted_data, bins=100, color='g', edgecolor='black', label=f'{ticker.upper()} day to day range')


    # Step 4: Plot the mean and standard deviations
    plt.axvline(mean, color='r', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')
    plt.axvline(mean + std_dev, color='b', linestyle='--', linewidth=2, label=f'+1 Std Dev = {mean + std_dev:.2f}')
    plt.axvline(mean - std_dev, color='b', linestyle='--', linewidth=2, label=f'-1 Std Dev = {mean - std_dev:.2f}')
    plt.axvline(mean + 2 * std_dev, color='orange', linestyle=':', linewidth=2, label=f'+2 Std Dev = {mean + 2 * std_dev:.2f}')
    plt.axvline(mean - 2 * std_dev, color='orange', linestyle=':', linewidth=2, label=f'-2 Std Dev = {mean - 2 * std_dev:.2f}')

    plt.axvline(pavg, color='grey', linestyle=':', linewidth=2, label=f'Up avg = {pavg:.2f}')
    plt.axvline(navg, color='grey', linestyle=':', linewidth=2, label=f'Down avg = {navg:.2f}')

    plt.axvline(upM, color='#5edc1f', linestyle=':', linewidth=2, label=f'Up median = {upM:.2f}')
    plt.axvline(dwnM, color='#7C0A02', linestyle=':', linewidth=2, label=f'Down median = {dwnM:.2f}')

    

    plt.text( mean, -15, f'{mean:.2f}%', color='r', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text( mean + std_dev + 0.25, -15, f' {mean + std_dev:.2f}%', color='b', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text( mean - std_dev - 0.25, -15, f' {mean - std_dev:.2f}%', color='b', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  mean + 2 * std_dev + 0.45, -15, f'{mean + 2 * std_dev:.2f}%', color='orange', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  mean - 2 * std_dev - 0.45, -15, f'{mean - 2 * std_dev:.2f}%', color='orange', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  pavg, -25, f'{pavg:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(  navg, -25, f'{navg:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)

    plt.text(   -5, -25, f'Within 1% {onePercent.size*100/sorted_data.size:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)
    plt.text(   5, -25, f'Within 2% {twoPercent.size*100/sorted_data.size:.2f}%', color='grey', verticalalignment='top', horizontalalignment='center', fontsize=10)
    # Step 5: Customize the plot
    plt.title(f'{ticker.upper()} Day to Day Move for the past {len(sorted_data)/240:.0f} years, UP vs DOWN: {upC/len(sorted_data)*100: .1f}%/{dwnC/len(sorted_data)*100:.1f}%', fontsize=15)
    # plt.xlabel('Price', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend()

    print(f"{ticker.upper()}({mean:.2f}, {mean + std_dev:.2f}/{mean - std_dev:.2f}, avg:{pavg:.2f}/{navg:.2f}, median: {upM:.2f}/{dwnM:.2f},  UP/DOWN: {upC/len(sorted_data)*100: .1f}%/{dwnC/len(sorted_data)*100:.1f}%)")

if __name__ == "__main__":
    ticker = 'spy'
    plt.figure(figsize=(10, 6))
    # Display the plot
    plot_daily(ticker, 10)
    username = os.environ['USERNAME']
    default_save_dir = f"C:/Users/{username}/OneDrive/Documents/Stock_Charts"
    filepath = f"{default_save_dir}/{ticker.upper()}_DayToDay.png"
    plt.savefig(filepath)
    plt.show(block=True)
