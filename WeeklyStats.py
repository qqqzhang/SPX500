import pylab
import matplotlib.pyplot as plt
import numpy as np
from FetchData import fetch_data


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

def plot_weekly(ticker):
    stock_weekly = fetch_data(ticker, 'w')
    data = get_weekly_diff(stock_weekly)
    sorted_data = np.sort(data)
    mean = np.mean(sorted_data)
    std_dev = np.std(sorted_data)

    pavg, navg = get_up_and_down_avg(sorted_data)

    # Step 4: Plot the data as a line plot
    plt.hist(sorted_data, bins=100, color='g', edgecolor='black', label=f'{ticker.upper()} weekly range')


    # Step 4: Plot the mean and standard deviations
    plt.axvline(mean, color='r', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')
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
    plt.legend()

if __name__ == "__main__":
    ticker = 'anet'
    plt.figure(figsize=(10, 6))
    # Display the plot
    plot_weekly(ticker)
    plt.show(block=True)



