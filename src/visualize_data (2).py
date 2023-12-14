import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Given data
data = {
    'date': ['2023-11-01', '2023-11-02', '2023-11-03', '2023-11-04', '2023-11-05', '2023-11-06', '2023-11-07', '2023-11-08', '2023-11-09', '2023-11-10'],
    'glucode': [88.37, 89.99, 90.37, 88.99, 91.37, 88.99, 89.99, 72.12, 50.0, 71.96]
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Streamlit app title
st.title('Glucose Levels over Time')

# Line plot for Glucose levels over time with enhanced styling
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df['date'], df['glucode'], marker='o', linestyle='-', color='blue', linewidth=2)

# Title and labels
ax.set_title('Glucose Levels over Time', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Glucose Level', fontsize=12)

# Grid, ticks, and date formatting
ax.grid(True, linestyle='--', alpha=0.7)
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

# Annotations
for i, txt in enumerate(df['glucode']):
    ax.annotate(f'{txt:.2f}', (df['date'].iloc[i], df['glucode'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Display the line plot in Streamlit
st.pyplot(fig)
