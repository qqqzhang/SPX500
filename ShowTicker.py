import matplotlib.pyplot as plt
from mplcursors import cursor  # separate package must be installed
import os
import numpy as np
from WeeklyStats import plot_weekly 
from MonthlyStat import plot_monthly , on_hover
import settings

# Create a figure and two subplots (1 row, 2 columns)
plt.figure(figsize=(18, 8))

ticker = 'alny'
# First subplot (1st row, 1st column)
plt.subplot(1, 2, 1)  # 1 row, 2 columns, subplot 1
plot_monthly(ticker)

# Second subplot (1st row, 2nd column)
plt.subplot(1, 2, 2)  # 1 row, 2 columns, subplot 2
plot_weekly(ticker)

# Display the plot
plt.subplots_adjust(left=0.05, right=0.99)
plt.subplots_adjust(wspace=0.1, hspace=0)

default_save_dir = "C:/Users/Qun Zhang/OneDrive/Documents/Stock_Charts"
filepath = f"{default_save_dir}/{ticker.upper()}.png"
plt.savefig(filepath)
cursor = cursor(hover=True)
cursor.connect("add", on_hover)
plt.show(block=True)

