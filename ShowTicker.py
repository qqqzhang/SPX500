import matplotlib.pyplot as plt
import numpy as np
from WeeklyStats import plot_weekly 
from MonthlyStat import plot_monthly 

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
plt.show(block=True)
