import matplotlib.pyplot as plt
import pandas as pd

data = {
    'PostGresql+PostGis': [3, 7, 16, 35, 58],
    'ArcGis+FileSystem': [2, 9, 23, 49, 70],
    'Geotrellis': [5, 13, 23, 66, 89],
    'Geotrellis+GeoSOT': [2.9, 5, 9, 29, 45]
}
x = [0.1, 0.5, 1, 3.7, 5.5]

# Create a figure and two subplots for line chart and table
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [20, 1]}, figsize=(8, 6))

# Plotting the line chart
for label, values in data.items():
    ax1.plot(x, values, label=label)

ax1.legend()
ax1.set_xlabel('raster data size(GB)')
ax1.set_ylabel('Build pyramid and put it into storage(min)')

# Creating a DataFrame for the table
# table_data = pd.DataFrame(data, index=[str(val) + 'GB' for val in x])
#
# # Plotting the table
# table = ax2.table(cellText=table_data.values, colLabels=table_data.columns, rowLabels=table_data.index,
#                   cellLoc='center', rowLoc='center', loc='center')

# Hide the axes of the table
ax2.axis('off')

plt.subplots_adjust(hspace=0.15)  # Adjusting the spacing between subplots
plt.savefig('fig5.png')
plt.show()