#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
df = pd.read_csv('County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')


# In[7]:


df.head()


# In[8]:


import pandas as pd
import matplotlib.pyplot as plt

# Assuming your dataframe is called df
# Filter for Los Angeles County and Santa Clara County
counties = df[df['RegionName'].isin(['Los Angeles County', 'Santa Clara County'])]

# Select only date columns (assuming they are from column index 10 onward)
date_cols = df.columns[10:]  # adjust if date columns start elsewhere
time_df = counties[['RegionName'] + list(date_cols)]

# Melt the dataframe for easier plotting
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Plot
plt.figure(figsize=(12,6))
for county in time_df_melted['RegionName'].unique():
    subset = time_df_melted[time_df_melted['RegionName'] == county]
    plt.plot(subset['Date'], subset['HomeValue'], label=county)

plt.title('Zillow Home Values: Los Angeles County vs Santa Clara County', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Home Value (Millions)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[9]:


plt.ylabel('Home Value (Millions $)')
plt.plot(subset['Date'], subset['HomeValue']/1_000_000, label=county)


# In[10]:


import pandas as pd
import matplotlib.pyplot as plt

# Filter for LA County and Santa Clara County
counties = df[df['RegionName'].isin(['Los Angeles County', 'Santa Clara County'])]

# Select date columns (adjust index if needed)
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt for plotting
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Plot
plt.figure(figsize=(12,8))

for county in time_df_melted['RegionName'].unique():
    subset = time_df_melted[time_df_melted['RegionName'] == county]

    # Plot in millions for readability
    plt.plot(subset['Date'], subset['HomeValue']/1_000_000, label=county)

    # Annotate min and max points
    min_idx = subset['HomeValue'].idxmin()
    max_idx = subset['HomeValue'].idxmax()

    min_row = subset.loc[min_idx]
    max_row = subset.loc[max_idx]

    plt.annotate(f"{min_row['HomeValue']/1_000_000:.2f}M", 
                 xy=(min_row['Date'], min_row['HomeValue']/1_000_000),
                 xytext=(0, -15), textcoords='offset points',
                 ha='center', color='red', fontsize=10)

    plt.annotate(f"{max_row['HomeValue']/1_000_000:.2f}M", 
                 xy=(max_row['Date'], max_row['HomeValue']/1_000_000),
                 xytext=(0, 10), textcoords='offset points',
                 ha='center', color='green', fontsize=10)

plt.title('Zillow Home Values: Los Angeles County vs Santa Clara County', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Home Value (Millions $)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[11]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Filter for Santa Clara County only
counties = df[df['RegionName'] == 'Santa Clara County']

# Select date columns (adjust index if needed)
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt for plotting
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Plot
plt.figure(figsize=(12,8))

# Plot Santa Clara County
subset = time_df_melted[time_df_melted['RegionName'] == 'Santa Clara County']
line_color = '#AA0000'

plt.plot(subset['Date'], subset['HomeValue']/1_000_000, 
         label='Santa Clara County', color=line_color, linewidth=2.5)

# Annotate min and max points
min_idx = subset['HomeValue'].idxmin()
max_idx = subset['HomeValue'].idxmax()

min_row = subset.loc[min_idx]
max_row = subset.loc[max_idx]

plt.annotate(f"{min_row['HomeValue']/1_000_000:.2f}M", 
             xy=(min_row['Date'], min_row['HomeValue']/1_000_000),
             xytext=(0, -15), textcoords='offset points',
             ha='center', color='red', fontsize=10)

plt.annotate(f"{max_row['HomeValue']/1_000_000:.2f}M", 
             xy=(max_row['Date'], max_row['HomeValue']/1_000_000),
             xytext=(0, 10), textcoords='offset points',
             ha='center', color='green', fontsize=10)

# Key events with labels at top and data labels slightly above line
key_years = {
    '2008': 'Financial Crisis',
    '2014': "Levi's Stadium Opens",
    '2020': 'COVID-19 Pandemic'
}

y_max = (subset['HomeValue']/1_000_000).max()

for year, label in key_years.items():
    date = pd.to_datetime(f'{year}-01-01')

    # Interpolate the value for that date
    value = np.interp(date.timestamp(), 
                      subset['Date'].map(pd.Timestamp.timestamp), 
                      subset['HomeValue']/1_000_000)

    # Vertical dashed line for event
    plt.axvline(x=date, color='gray', linestyle='--', linewidth=1.5)

    # Event label at top of graph, slightly left of the line
    plt.text(date - pd.Timedelta(days=200), y_max*0.98, label, rotation=90,
             verticalalignment='top', horizontalalignment='right',
             color='black', fontsize=10)

    # Data label directly above the line (offset to avoid overlap)
    plt.text(date, value + 0.03*value, f"{value:.2f}M", color=line_color, 
             ha='center', va='bottom', fontsize=10)

plt.title('Zillow Home Values: Santa Clara County', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Home Value (Millions $)')
plt.legend()
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "SantaClara_HomeValues.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Figure saved to: {file_path}")


# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Filter for LA County and Santa Clara County
counties = df[df['RegionName'].isin(['Los Angeles County', 'Santa Clara County'])]

# Select date columns (adjust index if needed)
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt for plotting
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Calculate YoY % change
time_df_melted['YoYChange'] = time_df_melted.groupby('RegionName')['HomeValue'].pct_change(periods=12) * 100

# Plot
plt.figure(figsize=(12,8))

for county in time_df_melted['RegionName'].unique():
    subset = time_df_melted[time_df_melted['RegionName'] == county]

    plt.plot(subset['Date'], subset['YoYChange'], label=county)

    # Annotate min and max YoY change
    min_idx = subset['YoYChange'].idxmin()
    max_idx = subset['YoYChange'].idxmax()

    min_row = subset.loc[min_idx]
    max_row = subset.loc[max_idx]

    plt.annotate(f"{min_row['YoYChange']:.1f}%", 
                 xy=(min_row['Date'], min_row['YoYChange']),
                 xytext=(0, -15), textcoords='offset points',
                 ha='center', color='red', fontsize=10)

    plt.annotate(f"{max_row['YoYChange']:.1f}%", 
                 xy=(max_row['Date'], max_row['YoYChange']),
                 xytext=(0, 10), textcoords='offset points',
                 ha='center', color='green', fontsize=10)

plt.title('YoY % Change in Home Values: Los Angeles County vs Santa Clara County', fontsize=14)
plt.xlabel('Date')
plt.ylabel('YoY % Change')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "LA_vs_SantaClara_YoYChange.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Figure saved to: {file_path}")


# In[13]:


import pandas as pd

# Filter for LA County and Santa Clara County
counties = df[df['RegionName'].isin(['Los Angeles County', 'Santa Clara County'])]

# Select date columns (adjust index if needed)
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt for easier calculation
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Calculate YoY % change
time_df_melted['YoYChange'] = time_df_melted.groupby('RegionName')['HomeValue'].pct_change(periods=12) * 100

# Function to compute summary stats per county
def summary_stats(group):
    min_value = group['HomeValue'].min()
    max_value = group['HomeValue'].max()
    total_growth = (group['HomeValue'].iloc[-1] - group['HomeValue'].iloc[0]) / group['HomeValue'].iloc[0] * 100
    avg_yoy = group['YoYChange'].mean()
    return pd.Series({
        'Min Home Value ($)': round(min_value,0),
        'Max Home Value ($)': round(max_value,0),
        'Total Growth (%)': round(total_growth,1),
        'Average YoY Change (%)': round(avg_yoy,2)
    })

# Apply to each county
summary_table = time_df_melted.groupby('RegionName').apply(summary_stats)

# Display table
print(summary_table)

# Optional: save table to CSV on Desktop
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
csv_path = os.path.join(desktop_path, "LA_SantaClara_HomeValue_Summary.csv")
summary_table.to_csv(csv_path)
print(f"Summary table saved to: {csv_path}")


# In[14]:


df2 = pd.read_csv('attendance.csv')


# In[15]:


df2.head()


# In[16]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# --- Step 1: df2 already loaded ---
# Columns: team, team_name, year, total, home, away, week, weekly_attendance

# --- Step 2: Filter for SF 49ers only ---
teams_of_interest = ['49ers']  # Only 49ers now
df_filtered = df2[df2['team_name'].isin(teams_of_interest)].copy()

# --- Step 3: Ensure numeric ---
df_filtered['weekly_attendance'] = pd.to_numeric(df_filtered['weekly_attendance'], errors='coerce')

# --- Step 4: Aggregate total seasonal attendance by team & year ---
attendance_yearly = (
    df_filtered.groupby(['team_name', 'year'])['weekly_attendance']
    .sum()
    .reset_index()
    .rename(columns={'weekly_attendance':'TotalSeasonAttendance'})
)

# --- Step 5: Define team color ---
team_colors = {'49ers': '#AA0000'}

# --- Step 6: Plot line chart with min/max data labels ---
plt.figure(figsize=(12,8))

team = '49ers'
team_data = attendance_yearly[attendance_yearly['team_name'] == team]
plt.plot(team_data['year'], team_data['TotalSeasonAttendance'], 
         marker='o', color=team_colors[team], linewidth=2)

# annotate min value (bold)
min_idx = team_data['TotalSeasonAttendance'].idxmin()
min_row = team_data.loc[min_idx]
plt.annotate(f"{int(min_row['TotalSeasonAttendance']):,}",
             xy=(min_row['year'], min_row['TotalSeasonAttendance']),
             xytext=(0,-15), textcoords='offset points',
             ha='center', color='red', fontsize=10, fontweight='bold')

# annotate max value (bold)
max_idx = team_data['TotalSeasonAttendance'].idxmax()
max_row = team_data.loc[max_idx]
plt.annotate(f"{int(max_row['TotalSeasonAttendance']):,}",
             xy=(max_row['year'], max_row['TotalSeasonAttendance']),
             xytext=(0,10), textcoords='offset points',
             ha='center', color='green', fontsize=10, fontweight='bold')

# --- Step 7: Add vertical lines for events ---
plt.axvline(x=2014, color='black', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0] + (plt.ylim()[1]-plt.ylim()[0])*0.05, 
         'Levi\'s Stadium Opened', rotation=90, verticalalignment='bottom', color='black', fontweight='bold')

# --- Step 8: Formatting ---
plt.title('San Francisco 49ers Attendance per Season', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.ylabel('Total Season Attendance (Millions)', fontweight='bold')
plt.xticks(sorted(attendance_yearly['year'].unique()), fontweight='bold')
plt.yticks(fontweight='bold')

# Remove legend
# plt.legend()  # not needed

plt.grid(False)
plt.tight_layout()

# --- Step 10: Save figure to Desktop ---
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "49ers_TotalAttendance_Events.png")
plt.savefig(file_path, dpi=300)
plt.show()
print(f"Figure saved to: {file_path}")


# In[17]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data preparation
sectors = ['Information', 'Manufacturing', 'Prof & Business', 
           'Financial', 'Trade & Transport', 'Education & Health', 
           'Leisure & Hospitality', 'Construction']

# Average pay data
avg_pay_2013 = [256957, 154149, 113671, 108918, 65322, 63356, 24859, 68981]
avg_pay_2014 = [266564, 168226, 123053, 112869, 68063, 65233, 26032, 71378]

# Employment data
employment_2013 = [58582, 152241, 190718, 33302, 133496, 135289, 86004, 36496]
employment_2014 = [65751, 155179, 199628, 34513, 135107, 139842, 89967, 38201]

# Calculate growth rates
emp_growth = [(e14 - e13) / e13 * 100 for e13, e14 in zip(employment_2013, employment_2014)]
wage_growth = [(w14 - w13) / w13 * 100 for w13, w14 in zip(avg_pay_2013, avg_pay_2014)]

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Santa Clara County Employment Analysis (2013-2014)', 
             fontsize=16, fontweight='bold', y=0.995)

# 1. Average Pay Comparison by Sector
ax1 = plt.subplot(2, 3, 1)
x = np.arange(len(sectors))
width = 0.35
bars1 = ax1.barh(x - width/2, avg_pay_2013, width, label='2013', color='#3b82f6', alpha=0.8)
bars2 = ax1.barh(x + width/2, avg_pay_2014, width, label='2014', color='#10b981', alpha=0.8)
ax1.set_xlabel('Average Annual Pay ($)', fontweight='bold')
ax1.set_title('Average Pay by Sector', fontweight='bold')
ax1.set_yticks(x)
ax1.set_yticklabels(sectors, fontsize=9)
ax1.legend()
ax1.grid(axis='x', alpha=0.3)
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

# 2. Employment by Sector
ax2 = plt.subplot(2, 3, 2)
bars1 = ax2.barh(x - width/2, employment_2013, width, label='2013', color='#3b82f6', alpha=0.8)
bars2 = ax2.barh(x + width/2, employment_2014, width, label='2014', color='#10b981', alpha=0.8)
ax2.set_xlabel('Number of Employees', fontweight='bold')
ax2.set_title('Employment by Sector', fontweight='bold')
ax2.set_yticks(x)
ax2.set_yticklabels(sectors, fontsize=9)
ax2.legend()
ax2.grid(axis='x', alpha=0.3)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))

# 3. Growth Rates Comparison
ax3 = plt.subplot(2, 3, 3)
x_pos = np.arange(len(sectors))
bars1 = ax3.bar(x_pos - width/2, emp_growth, width, label='Employment Growth', 
                color='#f59e0b', alpha=0.8)
bars2 = ax3.bar(x_pos + width/2, wage_growth, width, label='Wage Growth', 
                color='#8b5cf6', alpha=0.8)
ax3.set_ylabel('Growth Rate (%)', fontweight='bold')
ax3.set_title('Year-over-Year Growth Rates', fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(sectors, rotation=45, ha='right', fontsize=8)
ax3.legend()
ax3.grid(axis='y', alpha=0.3)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 4. Scatter Plot: Pay vs Employment
ax4 = plt.subplot(2, 3, 4)
colors_scatter = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', 
                  '#8b5cf6', '#ec4899', '#f97316', '#06b6d4']
for i, sector in enumerate(sectors):
    ax4.scatter(employment_2014[i], avg_pay_2014[i], s=200, 
               color=colors_scatter[i], alpha=0.7, label=sector, edgecolors='white', linewidth=2)
ax4.set_xlabel('Employment (2014)', fontweight='bold')
ax4.set_ylabel('Average Pay (2014)', fontweight='bold')
ax4.set_title('Pay vs Employment Size', fontweight='bold')
ax4.legend(fontsize=8, loc='upper right')
ax4.grid(alpha=0.3)
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

# 5. Overall County Metrics
ax5 = plt.subplot(2, 3, 5)
metrics = ['Total\nEmployment', 'Total Wages\n($Billions)', 'Avg Annual\nPay ($K)']
values_2013 = [938114, 92.5, 98.576]
values_2014 = [973668, 102.6, 105.382]
x_metrics = np.arange(len(metrics))
bars1 = ax5.bar(x_metrics - width/2, values_2013, width, label='2013', color='#3b82f6', alpha=0.8)
bars2 = ax5.bar(x_metrics + width/2, values_2014, width, label='2014', color='#10b981', alpha=0.8)
ax5.set_title('Overall County Metrics', fontweight='bold')
ax5.set_xticks(x_metrics)
ax5.set_xticklabels(metrics, fontsize=9)
ax5.legend()
ax5.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 1000:
            label = f'{height/1000:.0f}K'
        else:
            label = f'{height:.1f}'
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontsize=8)

# 6. Top 3 Sectors Contribution
ax6 = plt.subplot(2, 3, 6)
top_sectors = ['Information', 'Manufacturing', 'Prof & Business']
top_wages_2014 = [17526971183, 26105136331, 24564862603]
total_private_wages = 96723155370
other_wages = total_private_wages - sum(top_wages_2014)

pie_data = top_wages_2014 + [other_wages]
pie_labels = top_sectors + ['All Other\nSectors']
colors_pie = ['#3b82f6', '#10b981', '#f59e0b', '#e5e7eb']
explode = (0.05, 0.05, 0.05, 0)

wedges, texts, autotexts = ax6.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
                                     colors=colors_pie, explode=explode, startangle=90,
                                     textprops={'fontsize': 9, 'weight': 'bold'})
ax6.set_title('Share of Total Private Sector Wages (2014)', fontweight='bold', pad=20)

plt.tight_layout()
plt.show()

# Print summary statistics
print("\n" + "="*60)
print("SANTA CLARA COUNTY EMPLOYMENT SUMMARY (2013-2014)")
print("="*60)
print(f"\nOverall Growth:")
print(f"  Employment: +3.8% ({973668 - 938114:,} jobs added)")
print(f"  Total Wages: +10.9% (${102.6 - 92.5:.1f}B increase)")
print(f"  Average Pay: +6.9% (${105382 - 98576:,} increase)")

print(f"\nTop Paying Sectors (2014):")
for i in range(3):
    print(f"  {sectors[i]}: ${avg_pay_2014[i]:,}")

print(f"\nFastest Growing Sectors (Employment):")
growth_sorted = sorted(zip(sectors, emp_growth), key=lambda x: x[1], reverse=True)
for sector, growth in growth_sorted[:3]:
    print(f"  {sector}: +{growth:.1f}%")

print(f"\nLargest Employers (2014):")
emp_sorted = sorted(zip(sectors, employment_2014), key=lambda x: x[1], reverse=True)
for sector, emp in emp_sorted[:3]:
    print(f"  {sector}: {emp:,} employees")
print("="*60)


# In[18]:


import pandas as pd
import matplotlib.pyplot as plt

# =======================
# MANUALLY ENTERED RAW DATA
# =======================

data = {
    "Area": [
        "Santa Clara County, California", "Santa Clara County, California", "Santa Clara County, California",
        "Los Angeles County, California", "Los Angeles County, California", "Los Angeles County, California",
        "United States", "United States", "United States"
    ],
    "Year_Q": [
        "Annual 2013", "Annual 2014", "Annual 2015",
        "Annual 2013", "Annual 2014", "Annual 2015",
        "Annual 2013", "Annual 2014", "Annual 2015"
    ],
    "Establishments": [
        75098, 75409, 78592,
        242675, 239831, 240300,
        9446450, 9494801, 9613991
    ],
    "Employment": [
        966784, 1027574, 1088564,
        3899282, 3998047, 4054363,
        135418526, 137090247, 139369423
    ],
    "Avg_Weekly_Wage": [
        2132, 2265, 2415,
        1087, 1159, 1229,
        1000, 1035, 1072
    ],
    "Location_Quotient": [
        1.56, 1.58, 1.58,
        1.41, 1.41, 1.41,
        1.0, 1.0, 1.0
    ]
}

df = pd.DataFrame(data)

# Extract year as integer
df["Year"] = df["Year_Q"].str.extract(r"(\d{4})").astype(int)

# =======================
# PLOTS
# =======================

def plot_metric(metric, ylabel, title):
    plt.figure(figsize=(10,6))

    for area in df["Area"].unique():
        sub = df[df["Area"] == area]
        plt.plot(sub["Year"], sub[metric], marker="o", label=area)

    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Employment
plot_metric("Employment", "Employment", "Employment Over Time (2013–2015)")

# Establishments
plot_metric("Establishments", "Establishments", "Number of Establishments (2013–2015)")

# Weekly Wages
plot_metric("Avg_Weekly_Wage", "Avg Weekly Wage ($)", "Average Weekly Wage (2013–2015)")

# Location Quotient
plot_metric("Location_Quotient", "LQ", "Location Quotient (2013–2015)")


# In[19]:


import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Data preparation - each row is a separate entry
data = {
    'Year': ['2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013', '2013',
             '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014', '2014',
             '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015', '2015'],
    'Ownership': ['Total Covered', 'Federal Government', 'State Government', 'Local Government', 'Private', 'Private - Goods', 
                 'Private - Natural Resources', 'Private - Construction', 'Private - Manufacturing', 'Private - Service', 
                 'Private - Trade/Transport', 'Private - Information', 'Private - Financial', 'Private - Prof/Business', 
                 'Private - Education/Health', 'Private - Leisure', 'Private - Other Services', 'Private - Unclassified',
                 'Total Covered', 'Federal Government', 'State Government', 'Local Government', 'Private', 'Private - Goods',
                 'Private - Natural Resources', 'Private - Construction', 'Private - Manufacturing', 'Private - Service',
                 'Private - Trade/Transport', 'Private - Information', 'Private - Financial', 'Private - Prof/Business',
                 'Private - Education/Health', 'Private - Leisure', 'Private - Other Services', 'Private - Unclassified',
                 'Total Covered', 'Federal Government', 'State Government', 'Local Government', 'Private', 'Private - Goods',
                 'Private - Natural Resources', 'Private - Construction', 'Private - Manufacturing', 'Private - Service',
                 'Private - Trade/Transport', 'Private - Information', 'Private - Financial', 'Private - Prof/Business',
                 'Private - Education/Health', 'Private - Leisure', 'Private - Other Services', 'Private - Unclassified'],
    'Establishments': [62755, 93, 197, 968, 61496, 5588, 227, 2881, 2480, 55909, 7252, 984, 4161, 10731, 20924, 4451, 4382, 3024,
                      65277, 96, 197, 985, 63999, 5826, 233, 3082, 2512, 58173, 7385, 1040, 4381, 11239, 22462, 4567, 4958, 2143,
                      67491, 96, 204, 975, 66216, 5975, 226, 3228, 2521, 60241, 7338, 1114, 4437, 11119, 23576, 4684, 5102, 2872],
    'Employment': [938114, 9821, 5119, 67300, 855875, 192314, 3578, 36496, 152241, 663561, 133496, 58582, 33302, 190718, 135289, 86004, 23894, 2277,
                  973668, 9820, 5325, 68512, 890012, 197145, 3765, 38201, 155179, 692867, 135107, 65751, 34513, 199628, 139842, 89967, 25018, 3040,
                  1017071, 9844, 5525, 70845, 930858, 204196, 3941, 42045, 158210, 726662, 135629, 74397, 34816, 212590, 145164, 93741, 25462, 4865],
    'Total_Wages': [92475629194, 852978783, 290359497, 4431536450, 86900754464, 26122123173, 136885416, 2517489361, 23467748396, 60778631291, 
                   8720247297, 15052973498, 3627227495, 21679024870, 8571376887, 2138009894, 856494685, 133276665,
                   102606999591, 871821345, 305919983, 4706102893, 96723155370, 28985898136, 154074481, 2726687324, 26105136331, 67737257234,
                   9195770555, 17526971183, 3895456926, 24564862603, 9122279589, 2342012215, 910911509, 178992654,
                   115325372474, 909738085, 326676398, 4974958438, 109113999553, 30868225051, 160472413, 3184958569, 27522794069, 78245774502,
                   9679019498, 21845779270, 4210563636, 28851891218, 9815490887, 2543902640, 981514037, 317613316],
    'Avg_Pay': [98576, 86855, 56727, 65848, 101534, 135831, 38259, 68981, 154149, 91595, 65322, 256957, 108918, 113671, 63356, 24859, 35845, 58538,
               105382, 88779, 57452, 68690, 108676, 147029, 40921, 71378, 168226, 97764, 68063, 266564, 112869, 123053, 65233, 26032, 36410, 58871,
               113390, 92416, 59129, 70224, 117219, 151170, 40718, 75751, 173964, 107678, 71364, 293640, 120938, 135716, 67617, 27138, 38549, 65288]
}

df = pd.DataFrame(data)

# Create dashboard with multiple subplots
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Employment Growth by Year', 
                    'Average Annual Pay by Year',
                    'Top 10 Industries by Employment (2015)',
                    'Top 10 Industries by Average Pay (2015)',
                    'Employment by Ownership Type',
                    'Total Wages Trend'),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "scatter"}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# 1. Employment Growth by Year
total_data = df[df['Ownership'] == 'Total Covered']
fig.add_trace(
    go.Bar(x=total_data['Year'], y=total_data['Employment'],
           text=total_data['Employment'].apply(lambda x: f'{x:,.0f}'),
           textposition='outside',
           marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
           name='Total Employment',
           showlegend=False),
    row=1, col=1
)

# 2. Average Pay by Year
fig.add_trace(
    go.Bar(x=total_data['Year'], y=total_data['Avg_Pay'],
           text=total_data['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
           textposition='outside',
           marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
           name='Avg Pay',
           showlegend=False),
    row=1, col=2
)

# 3. Top 10 Industries by Employment (2015) - Descending order
industry_2015 = df[(df['Year'] == '2015') & (df['Ownership'].str.startswith('Private -'))]
industry_2015_sorted = industry_2015.sort_values('Employment', ascending=True).tail(10)
fig.add_trace(
    go.Bar(y=industry_2015_sorted['Ownership'].str.replace('Private - ', ''),
           x=industry_2015_sorted['Employment'],
           orientation='h',
           text=industry_2015_sorted['Employment'].apply(lambda x: f'{x:,.0f}'),
           textposition='outside',
           marker_color='#2ca02c',
           name='Employment',
           showlegend=False),
    row=2, col=1
)

# 4. Top 10 Industries by Average Pay (2015) - Descending order
industry_pay_sorted = industry_2015.sort_values('Avg_Pay', ascending=True).tail(10)
fig.add_trace(
    go.Bar(y=industry_pay_sorted['Ownership'].str.replace('Private - ', ''),
           x=industry_pay_sorted['Avg_Pay'],
           orientation='h',
           text=industry_pay_sorted['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
           textposition='outside',
           marker_color='#d62728',
           name='Avg Pay',
           showlegend=False),
    row=2, col=2
)

# 5. Employment by Ownership Type
ownership_types = ['Private', 'Local Government', 'Federal Government', 'State Government']
for own in ownership_types:
    own_data = df[df['Ownership'] == own]
    fig.add_trace(
        go.Bar(x=own_data['Year'], y=own_data['Employment'],
               name=own,
               text=own_data['Employment'].apply(lambda x: f'{x:,.0f}'),
               textposition='outside'),
        row=3, col=1
    )

# 6. Total Wages Trend
fig.add_trace(
    go.Scatter(x=total_data['Year'], 
               y=total_data['Total_Wages']/1e9,
               mode='lines+markers+text',
               text=total_data['Total_Wages'].apply(lambda x: f'${x/1e9:.1f}B'),
               textposition='top center',
               marker=dict(size=12, color='#9467bd'),
               line=dict(width=3, color='#9467bd'),
               name='Total Wages',
               showlegend=False),
    row=3, col=2
)

# Update layout
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_xaxes(title_text="Year", row=1, col=2)
fig.update_xaxes(title_text="Employment", row=2, col=1)
fig.update_xaxes(title_text="Average Pay ($)", row=2, col=2)
fig.update_xaxes(title_text="Year", row=3, col=1)
fig.update_xaxes(title_text="Year", row=3, col=2)

fig.update_yaxes(title_text="Employment", row=1, col=1)
fig.update_yaxes(title_text="Average Pay ($)", row=1, col=2)
fig.update_yaxes(title_text="Industry", row=2, col=1)
fig.update_yaxes(title_text="Industry", row=2, col=2)
fig.update_yaxes(title_text="Employment", row=3, col=1)
fig.update_yaxes(title_text="Total Wages (Billions $)", row=3, col=2)

fig.update_layout(
    height=1400,
    title_text="Santa Clara County Employment Dashboard (2013-2015)",
    title_font_size=24,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5)
)

fig.show()

# Additional detailed analysis charts
print("\nGenerating additional analysis charts...\n")

# Chart: Private sector breakdown over time
private_sectors = df[df['Ownership'].str.startswith('Private -')]
pivot_employment = private_sectors.pivot(index='Ownership', columns='Year', values='Employment')
pivot_employment = pivot_employment.sort_values('2015', ascending=False)

fig2 = go.Figure()
for year in ['2013', '2014', '2015']:
    fig2.add_trace(go.Bar(
        name=year,
        y=pivot_employment.index.str.replace('Private - ', ''),
        x=pivot_employment[year],
        orientation='h',
        text=pivot_employment[year].apply(lambda x: f'{x:,.0f}'),
        textposition='outside'
    ))

fig2.update_layout(
    title='Private Sector Employment by Industry (2013-2015)',
    xaxis_title='Employment',
    yaxis_title='Industry',
    height=600,
    barmode='group',
    showlegend=True
)
fig2.show()

# Chart: Year-over-year growth rates
growth_data = df[df['Ownership'] == 'Total Covered'].copy()
growth_data = growth_data.reset_index(drop=True)
growth_data['Employment_Growth'] = growth_data['Employment'].pct_change() * 100
growth_data['Wage_Growth'] = growth_data['Total_Wages'].pct_change() * 100
growth_data['Pay_Growth'] = growth_data['Avg_Pay'].pct_change() * 100

fig3 = go.Figure()
metrics = ['Employment_Growth', 'Wage_Growth', 'Pay_Growth']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
names = ['Employment', 'Total Wages', 'Average Pay']

for metric, color, name in zip(metrics, colors, names):
    fig3.add_trace(go.Bar(
        x=growth_data['Year'][1:],
        y=growth_data[metric][1:],
        name=name,
        text=growth_data[metric][1:].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        marker_color=color
    ))

fig3.update_layout(
    title='Year-over-Year Growth Rates',
    xaxis_title='Year',
    yaxis_title='Growth Rate (%)',
    height=500,
    barmode='group',
    showlegend=True
)
fig3.show()

print("Dashboard generation complete!")


# In[20]:


import pandas as pd
import plotly.graph_objects as go
import os

# Data preparation
data = {
    'Year': ['2013']*18 + ['2014']*18 + ['2015']*18,
    'Ownership': ['Total Covered', 'Federal Government', 'State Government', 'Local Government', 'Private', 'Private - Goods', 
                  'Private - Natural Resources', 'Private - Construction', 'Private - Manufacturing', 'Private - Service', 
                  'Private - Trade/Transport', 'Private - Information', 'Private - Financial', 'Private - Prof/Business', 
                  'Private - Education/Health', 'Private - Leisure', 'Private - Other Services', 'Private - Unclassified']*3,
    'Establishments': [62755, 93, 197, 968, 61496, 5588, 227, 2881, 2480, 55909, 7252, 984, 4161, 10731, 20924, 4451, 4382, 3024,
                       65277, 96, 197, 985, 63999, 5826, 233, 3082, 2512, 58173, 7385, 1040, 4381, 11239, 22462, 4567, 4958, 2143,
                       67491, 96, 204, 975, 66216, 5975, 226, 3228, 2521, 60241, 7338, 1114, 4437, 11119, 23576, 4684, 5102, 2872],
    'Employment': [938114, 9821, 5119, 67300, 855875, 192314, 3578, 36496, 152241, 663561, 133496, 58582, 33302, 190718, 135289, 86004, 23894, 2277,
                   973668, 9820, 5325, 68512, 890012, 197145, 3765, 38201, 155179, 692867, 135107, 65751, 34513, 199628, 139842, 89967, 25018, 3040,
                   1017071, 9844, 5525, 70845, 930858, 204196, 3941, 42045, 158210, 726662, 135629, 74397, 34816, 212590, 145164, 93741, 25462, 4865],
    'Total_Wages': [92475629194, 852978783, 290359497, 4431536450, 86900754464, 26122123173, 136885416, 2517489361, 23467748396, 60778631291, 
                    8720247297, 15052973498, 3627227495, 21679024870, 8571376887, 2138009894, 856494685, 133276665,
                    102606999591, 871821345, 305919983, 4706102893, 96723155370, 28985898136, 154074481, 2726687324, 26105136331, 67737257234,
                    9195770555, 17526971183, 3895456926, 24564862603, 9122279589, 2342012215, 910911509, 178992654,
                    115325372474, 909738085, 326676398, 4974958438, 109113999553, 30868225051, 160472413, 3184958569, 27522794069, 78245774502,
                    9679019498, 21845779270, 4210563636, 28851891218, 9815490887, 2543902640, 981514037, 317613316],
    'Avg_Pay': [98576, 86855, 56727, 65848, 101534, 135831, 38259, 68981, 154149, 91595, 65322, 256957, 108918, 113671, 63356, 24859, 35845, 58538,
                105382, 88779, 57452, 68690, 108676, 147029, 40921, 71378, 168226, 97764, 68063, 266564, 112869, 123053, 65233, 26032, 36410, 58871,
                113390, 92416, 59129, 70224, 117219, 151170, 40718, 75751, 173964, 107678, 71364, 293640, 120938, 135716, 67617, 27138, 38549, 65288]
}

df = pd.DataFrame(data)
df.columns = df.columns.str.strip()

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
TRACE_COLORS = ['#AA0000', '#B3995D', '#000000']  # Red, Gold, Black

def get_transparent_layout(title, height=700, width=1200):
    return dict(
        title=dict(text=title, font=dict(size=20, color='black')),
        height=height,
        width=width,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        font=dict(size=12, color='black')
    )

def get_alternating_colors(num_bars):
    return [TRACE_COLORS[i % len(TRACE_COLORS)] for i in range(num_bars)]

print("Generating charts without gridlines...\n")

# ----------------------------
# 1. Employment Growth
total_data = df[df['Ownership'] == 'Total Covered']
num_bars = len(total_data['Year'])
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=total_data['Year'],
    y=total_data['Employment'],
    text=total_data['Employment'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker_color=get_alternating_colors(num_bars),
    width=0.4,
    name='Total Employment'
))
fig1.update_layout(**get_transparent_layout('Employment Growth by Year'))
fig1.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'))
fig1.update_yaxes(title_text="Employment", showgrid=False, tickfont=dict(color='black'))
fig1.write_image(os.path.join(desktop_path, "01_employment_growth.png"))
fig1.show()

# ----------------------------
# 2. Average Pay
num_bars = len(total_data['Year'])
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=total_data['Year'],
    y=total_data['Avg_Pay'],
    text=total_data['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker_color=get_alternating_colors(num_bars),
    width=0.4,
    name='Average Pay'
))
fig2.update_layout(**get_transparent_layout('Average Annual Pay by Year'))
fig2.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'))
fig2.update_yaxes(title_text="Average Pay ($)", showgrid=False, tickfont=dict(color='black'))
fig2.write_image(os.path.join(desktop_path, "02_average_pay.png"))
fig2.show()

# ----------------------------
# 3. Top Industries by Employment (2015)
industry_2015 = df[(df['Year']=='2015') & (df['Ownership'].str.startswith('Private -'))]
industry_2015_sorted = industry_2015.sort_values('Employment', ascending=True).tail(10)
num_bars = len(industry_2015_sorted)
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    y=industry_2015_sorted['Ownership'].str.replace('Private - ', ''),
    x=industry_2015_sorted['Employment'],
    orientation='h',
    text=industry_2015_sorted['Employment'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker_color=get_alternating_colors(num_bars),
    width=0.4
))
fig3.update_layout(**get_transparent_layout('Top 10 Industries by Employment (2015)', height=700))
fig3.update_xaxes(title_text="Employment", showgrid=False, tickfont=dict(color='black'))
fig3.update_yaxes(title_text="Industry", showgrid=False, tickfont=dict(color='black'))
fig3.write_image(os.path.join(desktop_path, "03_top_industries_employment.png"))
fig3.show()

# ----------------------------
# 4. Top Industries by Avg Pay (2015)
industry_pay_sorted = industry_2015.sort_values('Avg_Pay', ascending=True).tail(10)
num_bars = len(industry_pay_sorted)
fig4 = go.Figure()
fig4.add_trace(go.Bar(
    y=industry_pay_sorted['Ownership'].str.replace('Private - ', ''),
    x=industry_pay_sorted['Avg_Pay'],
    orientation='h',
    text=industry_pay_sorted['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker_color=get_alternating_colors(num_bars),
    width=0.4
))
fig4.update_layout(**get_transparent_layout('Top 10 Industries by Average Pay (2015)', height=700))
fig4.update_xaxes(title_text="Average Pay ($)", showgrid=False, tickfont=dict(color='black'))
fig4.update_yaxes(title_text="Industry", showgrid=False, tickfont=dict(color='black'))
fig4.write_image(os.path.join(desktop_path, "04_top_industries_pay.png"))
fig4.show()

# ----------------------------
# 5. Employment by Ownership
ownership_types = ['Private', 'Local Government', 'Federal Government', 'State Government']
fig5 = go.Figure()
for i, own in enumerate(ownership_types):
    own_data = df[df['Ownership'] == own]
    color = TRACE_COLORS[i % len(TRACE_COLORS)]
    fig5.add_trace(go.Bar(
        x=own_data['Year'],
        y=own_data['Employment'],
        name=own,
        text=own_data['Employment'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        textfont=dict(size=12, color='black', family='Arial Black'),
        marker_color=color,
        width=0.4
    ))
fig5.update_layout(**get_transparent_layout('Employment by Ownership Type'))
fig5.update_layout(barmode='group', bargap=0.3)
fig5.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'))
fig5.update_yaxes(title_text="Employment", showgrid=False, tickfont=dict(color='black'))
fig5.write_image(os.path.join(desktop_path, "05_employment_by_ownership.png"))
fig5.show()

# ----------------------------
# 6. Total Wages Trend
fig6 = go.Figure()
fig6.add_trace(go.Scatter(
    x=total_data['Year'],
    y=total_data['Total_Wages']/1e9,
    mode='lines+markers+text',
    text=total_data['Total_Wages'].apply(lambda x: f'${x/1e9:.1f}B'),
    textposition='top center',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker=dict(size=10, color='black'),
    line=dict(width=3, color=TRACE_COLORS[0]),
    name='Total Wages'
))
fig6.update_layout(**get_transparent_layout('Total Wages Trend (2013-2015)'))
fig6.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'), linecolor='black')
fig6.update_yaxes(title_text="Total Wages (Billions $)", showgrid=False, tickfont=dict(color='black'), linecolor='black')
fig6.write_image(os.path.join(desktop_path, "06_total_wages_trend.png"))
fig6.show()

# ----------------------------
# 7. Private Sector Employment by Industry
private_sectors = df[df['Ownership'].str.startswith('Private -')]
pivot_employment = private_sectors.pivot(index='Ownership', columns='Year', values='Employment')
pivot_employment = pivot_employment.sort_values('2015', ascending=False)
fig7 = go.Figure()
for i, year in enumerate(['2013','2014','2015']):
    color = TRACE_COLORS[i % len(TRACE_COLORS)]
    fig7.add_trace(go.Bar(
        name=year,
        y=pivot_employment.index.str.replace('Private - ', ''),
        x=pivot_employment[year],
        orientation='h',
        text=pivot_employment[year].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        textfont=dict(size=12, color='black', family='Arial Black'),
        marker_color=color,
        width=0.4
    ))
fig7.update_layout(**get_transparent_layout('Private Sector Employment by Industry (2013-2015)', height=800))
fig7.update_xaxes(title_text="Employment", showgrid=False, tickfont=dict(color='black'))
fig7.update_yaxes(title_text="Industry", showgrid=False, tickfont=dict(color='black'))
fig7.update_layout(barmode='group', bargap=0.3)
fig7.write_image(os.path.join(desktop_path, "07_private_sector_breakdown.png"))
fig7.show()

# ----------------------------
# 8. Year-over-Year Growth Rates
growth_data = df[df['Ownership'] == 'Total Covered'].copy().reset_index(drop=True)
growth_data['Employment_Growth'] = growth_data['Employment'].pct_change()*100
growth_data['Wage_Growth'] = growth_data['Total_Wages'].pct_change()*100
growth_data['Pay_Growth'] = growth_data['Avg_Pay'].pct_change()*100
fig8 = go.Figure()
metrics = ['Employment_Growth','Wage_Growth','Pay_Growth']
names = ['Employment','Total Wages','Average Pay']
for i, (metric, name) in enumerate(zip(metrics, names)):
    color = TRACE_COLORS[i % len(TRACE_COLORS)]
    fig8.add_trace(go.Bar(
        x=growth_data['Year'][1:],
        y=growth_data[metric][1:],
        name=name,
        text=growth_data[metric][1:].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(size=12, color='black', family='Arial Black'),
        marker_color=color,
        width=0.4
    ))
fig8.update_layout(**get_transparent_layout('Year-over-Year Growth Rates'))
fig8.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'))
fig8.update_yaxes(title_text="Growth Rate (%)", showgrid=False, tickfont=dict(color='black'))
fig8.update_layout(barmode='group', bargap=0.3)
fig8.write_image(os.path.join(desktop_path, "08_growth_rates.png"))
fig8.show()

# ----------------------------
# 9. Establishments Growth
num_bars = len(total_data['Year'])
fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=total_data['Year'],
    y=total_data['Establishments'],
    text=total_data['Establishments'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    textfont=dict(size=12, color='black', family='Arial Black'),
    marker_color=get_alternating_colors(num_bars),
    width=0.4,
    name='Establishments'
))
fig9.update_layout(**get_transparent_layout('Total Establishments by Year'))
fig9.update_xaxes(title_text="Year", showgrid=False, tickfont=dict(color='black'))
fig9.update_yaxes(title_text="Number of Establishments", showgrid=False, tickfont=dict(color='black'))
fig9.write_image(os.path.join(desktop_path, "09_establishments_growth.png"))
fig9.show()

print("\n✓ All charts generated, bold labels, no gridlines, and saved as PNG on Desktop!")


# In[21]:


df3 = pd.read_csv('TaxSalesByCounty.csv')


# In[22]:


df3.head()


# In[23]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    label='Total Taxable Transactions'
)

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions ($)', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

# Optional: format y-axis with commas
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
)

plt.tight_layout()

# Step 4: Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[24]:


import matplotlib.pyplot as plt

# Data
years = [2023, 2024, 2025]
values = [16826101, 16385557, 18761741]

# Create figure and axes
fig, ax = plt.subplots(figsize=(8,6), facecolor='none')

# Create bar graph with thinner bars
bars = ax.bar(years, values, color='#AA0000', width=0.4)  # width smaller than default

# Add data labels formatted as currency
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width()/2,          # X position
        bar.get_height(),                         # Y position
        f'${bar.get_height():,}',                 # Currency format
        ha='center', va='bottom', fontsize=10
    )

# Title
ax.set_title("Net Assessed Property Value (Levi's Stadium)", fontsize=14)

# Set x-axis ticks to only whole years
ax.set_xticks(years)

# Remove axes background for transparency
ax.patch.set_alpha(0)

# Layout adjustment
plt.tight_layout()

# Save to desktop (adjust path if needed)
desktop_path = '/Users/rishicheruvu/Desktop/Net_Assessed_Property_Value_Levis.png'
plt.savefig(desktop_path, transparent=True)

# Display the plot
plt.show()


# In[25]:


df4 = pd.read_csv('Zip codes.csv')


# In[26]:


df4.head()


# In[27]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Filter for zip codes
zip_list = ['95051', '95134', '94086', '95050', '95196', '95035', '95054']
df_zip = df4[df4['RegionName'].astype(str).isin(zip_list)].copy()

# Date columns
date_cols = [c for c in df_zip.columns if c[:4].isdigit()]

# Transpose and filter 2012+
df_dates = df_zip[date_cols].transpose()
df_dates.index = pd.to_datetime(df_dates.index)
df_dates = df_dates[df_dates.index >= "2012-01-01"]

# Average price
df_dates['AveragePrice'] = df_dates.mean(axis=1)

# Plot
plt.figure(figsize=(20,12))
plt.plot(df_dates.index, df_dates['AveragePrice'], color="#AA0000", linewidth=2)

# Max and min
max_idx = df_dates['AveragePrice'].idxmax()
max_val = df_dates.loc[max_idx, 'AveragePrice']
min_idx = df_dates['AveragePrice'].idxmin()
min_val = df_dates.loc[min_idx, 'AveragePrice']

# Horizontal offset for labels: 3 points to the left (-3)
x_offset = -5  

plt.annotate(f"${max_val:,.0f}", xy=(max_idx, max_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', color="green", fontsize=16, fontweight="bold")

plt.annotate(f"${min_val:,.0f}", xy=(min_idx, min_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', color="red", fontsize=16, fontweight="bold")

# Vertical trend line for Levi's Stadium
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)
plt.text(pd.Timestamp("2014-01-01"), df_dates['AveragePrice'].min()*2,
         "Levi's Stadium Opened", rotation=90, verticalalignment='bottom',
         horizontalalignment='left', fontsize=10, fontweight="bold")

# Specific year labels (skip max/min, remove 2012 since min/max already labeled)
years_to_label = [2014, 2016, 2018, 2020, 2022, 2024, 2025]

for year in years_to_label:
    date_match = df_dates[df_dates.index.year == year]
    if len(date_match) > 0:
        date_val = date_match.index[0]
        price_val = date_match['AveragePrice'].iloc[0]
        # Skip if already labeled as max or min
        if date_val in [max_idx, min_idx]:
            continue
        # Adjust offsets for 2025
        y_offset = 14 if year == 2025 else 17
        plt.annotate(f"${price_val:,.0f}", xy=(date_val, price_val),
                     xytext=(x_offset, y_offset), textcoords='offset points',
                     ha='center', va='bottom', fontsize=16, fontweight="bold", color='black')

# Formatting
plt.title("Average Zillow Home Value - Zip Codes Near Stadium Only", fontsize=18, fontweight="bold")
plt.xlabel("Year", fontsize=16, fontweight="bold")
plt.ylabel("Average Home Value (USD)", fontsize=16, fontweight="bold")
plt.grid(False)
plt.tight_layout()

# Save
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "Zillow_Average_Stadium_ZIPs_FINAL.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[28]:


import pandas as pd
import plotly.graph_objects as go
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)

# Function for transparent layout
def get_transparent_layout(title, height=700, width=1200):
    return dict(
        title=title,
        title_font_size=20,
        height=height,
        width=width,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(size=12)
    )

# --- Employment by Year Line Chart ---
fig = go.Figure()

# Red employment line
fig.add_trace(go.Scatter(
    x=df_emp['Year'],
    y=df_emp['Employment'],
    mode='lines+markers+text',
    line=dict(color='#B22222', width=4),  # Red line
    marker=dict(color='#B22222', size=10), # Red markers
    text=df_emp['Employment'].apply(lambda x: f'{x:,.0f}'),
    textposition='top center',
    textfont=dict(size=12, color='black', family='Arial', weight='bold')
))

# Add vertical black trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_emp['Employment']) * 0.98,
    y1=max(df_emp['Employment']) * 1.02,
    line=dict(color='black', width=3, dash='dash')
)

# Add annotation for Levi's Stadium
fig.add_annotation(
    x=2014,
    y=max(df_emp['Employment']) * 1.02,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=12, family='Arial', weight='bold')
)

# Layout and axes
fig.update_layout(**get_transparent_layout('Santa Clara County: Employment by Year (2010-2018)'))

# Ensure axes lines are visible
fig.update_xaxes(
    title_text="Year",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black')
)
fig.update_yaxes(
    title_text="Employment",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black')
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Employment_by_Year_2010_2018_Line_Levis.png"))
fig.show()

print(f"✓ Saved: Employment_by_Year_2010_2018_Line_Levis.png on Desktop")


# In[29]:


import pandas as pd
import plotly.graph_objects as go
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)

# Function for transparent layout
def get_transparent_layout(title, height=700, width=1200):
    return dict(
        title=title,
        title_font_size=23,
        height=height,
        width=width,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(size=15)
    )

# --- Employment by Year Line Chart ---
fig = go.Figure()

# Red employment line
fig.add_trace(go.Scatter(
    x=df_emp['Year'],
    y=df_emp['Employment'],
    mode='lines+markers',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    showlegend=False
))

# Add vertical black trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_emp['Employment']) * 0.98,
    y1=max(df_emp['Employment']) * 1.02,
    line=dict(color='black', width=3, dash='dash')
)

# Add annotation for Levi's Stadium
fig.add_annotation(
    x=2014,
    y=max(df_emp['Employment']) * 1.02,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=15, family='Arial', weight='bold')
)

# Add data labels manually with font size 16 and offset 3 points to the left
x_offset = -0.3  # horizontal offset (left)
y_offset = 500    # small vertical offset
for x, y in zip(df_emp['Year'], df_emp['Employment']):
    fig.add_annotation(
        x=x + x_offset,
        y=y + y_offset,
        text=f'{y:,}',
        showarrow=False,
        font=dict(size=16, color='black', family='Arial', weight='bold'),
        xanchor='center',
        yanchor='bottom'
    )

# Layout and axes
fig.update_layout(**get_transparent_layout('Santa Clara County: Employment by Year (2010-2018)'))
fig.update_xaxes(
    title_text="Year",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black', size=15)
)
fig.update_yaxes(
    title_text="Employment",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black', size=15)
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Employment_by_Year_2010_2018_Line_Levis_Final.png"))
fig.show()

print(f"✓ Saved: Employment_by_Year_2010_2018_Line_Levis_Final.png on Desktop")


# In[30]:


import pandas as pd
import plotly.graph_objects as go
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Avg pay data
pay_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Avg_Pay': [86200, 91000, 94600, 98576, 109900, 113390, 122980, 133900, 139000]
}

df_pay = pd.DataFrame(pay_data)

def get_transparent_layout(title, height=700, width=1200):
    return dict(
        title=dict(text=title, font=dict(size=23, color='black', family='Arial', weight='bold')),
        height=height,
        width=width,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(size=15, color='black', family='Arial', weight='bold')
    )

fig = go.Figure()

# Minimal offset: add 200 to y for labels
label_offset = 200

fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'],
    mode='lines+markers+text',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    text=(df_pay['Avg_Pay'] + label_offset).apply(lambda x: f'${x:,.0f}'),
    textposition='top center',
    textfont=dict(size=16, color='black', family='Arial', weight='bold')
))

# Trend line at 2014 (Levi's Stadium opening)
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_pay['Avg_Pay']) * 0.95,
    y1=max(df_pay['Avg_Pay']) * 1.05,
    line=dict(color='black', width=3, dash='dash')
)
fig.add_annotation(
    x=2014,
    y=max(df_pay['Avg_Pay']) * 1.05,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=15, family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(**get_transparent_layout('Santa Clara County: Average Annual Pay (2010–2018)'))
fig.update_xaxes(
    title_text="Year",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black', size=15, family='Arial', weight='bold')
)
fig.update_yaxes(
    title_text="Average Annual Pay ($)",
    showgrid=False,
    showline=True,
    linecolor='black',
    tickfont=dict(color='black', size=15, family='Arial', weight='bold')
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Avg_Pay_2010_2018_Line_Levis.png"))
fig.show()
print("✓ Saved: Avg_Pay_2010_2018_Line_Levis.png on Desktop")


# In[31]:


import plotly.graph_objects as go
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Data
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
total_wages = [
    72887820000,  # 2010
    79079000000,  # 2011
    87079260000,  # 2012
    92500000000,  # 2013
    102600000000, # 2014
    115300000000, # 2015
    129186885000, # 2016 (estimate)
    141952350000, # 2017
    151020700000  # 2018
]

# Convert to billions for easier reading
total_wages_billions = [x/1e9 for x in total_wages]

# Create figure
fig = go.Figure()

# Total wages line
fig.add_trace(go.Scatter(
    x=years,
    y=total_wages_billions,
    mode='lines+markers+text',
    text=[f"${x:.1f}B" for x in total_wages_billions],
    textposition='top center',
    textfont=dict(size=14, color='black', family='Arial', weight='bold'),
    line=dict(color='#B3995D', width=4),
    marker=dict(size=12),
    name='Total Wages'
))

# Vertical trend line for Levi's Stadium opening 2014
fig.add_trace(go.Scatter(
    x=[2014,2014],
    y=[0, max(total_wages_billions)*1.05],
    mode='lines+text',
    line=dict(color='black', width=3, dash='dash'),
    text=['Levi\'s Stadium Opens'],
    textposition='top right',
    name='Levi\'s Stadium'
))

# Layout formatting
fig.update_layout(
    title="Santa Clara County: Total Wages Trend (2010-2018)",
    title_font_size=24,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(
        title="Year",
        title_font=dict(size=17, color='black'),
        tickfont=dict(size=14, color='black'),
        showline=True,
        linecolor='black',
        linewidth=2,
        showgrid=False
    ),
    yaxis=dict(
        title="Total Wages (Billions $)",
        title_font=dict(size=17, color='black'),
        tickfont=dict(size=14, color='black'),
        showline=True,
        linecolor='black',
        linewidth=2,
        showgrid=False
    ),
    font=dict(size=14)
)

# Save to Desktop
fig.write_image(os.path.join(desktop_path, "06_total_wages_trend.png"))
fig.show()
print(f"✓ Saved: {os.path.join(desktop_path, '06_total_wages_trend.png')}")


# In[32]:


import plotly.graph_objects as go
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Data
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
total_wages = [
    72887820000,  # 2010
    79079000000,  # 2011
    87079260000,  # 2012
    92500000000,  # 2013
    102600000000, # 2014
    115300000000, # 2015
    129186885000, # 2016 (estimate)
    141952350000, # 2017
    151020700000  # 2018
]

# Convert to billions
total_wages_billions = [x/1e9 for x in total_wages]

# Create figure
fig = go.Figure()

# Total wages line
fig.add_trace(go.Scatter(
    x=years,
    y=total_wages_billions,
    mode='lines+markers+text',
    text=[f"${x:.1f}B" for x in total_wages_billions],
    textposition='top center',
    textfont=dict(size=17, color='black', family='Arial', weight='bold'),
    line=dict(color='#B3995D', width=4),
    marker=dict(size=12),
    name='Total Wages'
))

# Vertical trend line for Levi's Stadium opening 2014
fig.add_shape(
    type="line",
    x0=2014,
    y0=0,
    x1=2014,
    y1=max(total_wages_billions)*0.98,
    line=dict(color="black", width=3, dash="dash")
)

# Annotation above line with downward arrow
fig.add_annotation(
    x=2014,
    y=max(total_wages_billions)*1.02,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,  # horizontal offset of arrow tail
    ay=-30,  # vertical offset of arrow tail (points downward)
    font=dict(size=17, color='black', family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(
    title="Santa Clara County: Total Wages Trend (2010-2018)",
    title_font=dict(size=24, color='black', family='Arial', weight='bold'),
    height=700,
    width=1200,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(
        title="Year",
        title_font=dict(size=17, color='black', family='Arial', weight='bold'),
        tickfont=dict(size=17, color='black', family='Arial', weight='bold'),
        showline=True,
        linecolor='black',
        linewidth=2,
        showgrid=False
    ),
    yaxis=dict(
        title="Total Wages (Billions $)",
        title_font=dict(size=17, color='black', family='Arial', weight='bold'),
        tickfont=dict(size=17, color='black', family='Arial', weight='bold'),
        showline=True,
        linecolor='black',
        linewidth=2,
        showgrid=False
    ),
    font=dict(size=17, family='Arial', weight='bold')
)

# Save and show
fig.write_image(os.path.join(desktop_path, "06_total_wages_trend.png"))
fig.show()
print(f"✓ Saved: {os.path.join(desktop_path, '06_total_wages_trend.png')}")


# In[33]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data (replace with your actual YoY growth data)
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'YoY_Growth': [2.5, 3.1, 2.9, 3.0, 3.6, 3.8, 4.0, 3.9, 4.2]
}
df = pd.DataFrame(data)

# Create the plot
plt.figure(figsize=(10,6), facecolor='none')  # transparent background

plt.plot(df['Year'], df['YoY_Growth'], color='#AA0000', linewidth=2, marker='o')  # red line to match 49ers
plt.title('Year-over-Year Employment Growth', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Growth (%)', fontsize=12)

# Add data labels on each point
for x, y in zip(df['Year'], df['YoY_Growth']):
    plt.text(x, y + 0.05, f"{y:.1f}%", ha='center', va='bottom', fontsize=10)

# Trend line
z = np.polyfit(df['Year'], df['YoY_Growth'], 1)
p = np.poly1d(z)
plt.plot(df['Year'], p(df['Year']), linestyle='--', color='black', linewidth=1.5)  # dashed trend line

# Highlight key event (example: Levi's Stadium Opened in 2014)
plt.axvline(x=2014, color='grey', linestyle='--', linewidth=1)
plt.text(2014, max(df['YoY_Growth'])+0.2, "Levi's Stadium Opened\n(arrow)", 
         rotation=0, ha='center', va='bottom', fontsize=10)

# Formatting
plt.xticks(df['Year'])
plt.grid(axis='y', linestyle=':', linewidth=0.7)
plt.tight_layout()

# Save with transparent background
plt.savefig('YoY_Growth_Chart.png', transparent=True, dpi=300)
plt.show()


# In[34]:


import matplotlib.pyplot as plt
import numpy as np

# Years
years = np.arange(2011, 2019)

# Growth rates
employment_growth = [2.7, 6.1, 1.7, 3.8, 4.4, 4.6, -0.3, 2.5]
pay_growth = [5.5, 3.9, 4.2, 11.5, 3.2, 7.6, 9.7, 3.8]
wages_growth = [8.5, 10.1, 6.2, 10.9, 12.4, 12.0, 9.9, 6.3]

# Plotting
plt.figure(figsize=(10,6))

plt.plot(years, employment_growth, marker='o', color='#1f77b4', label='Employment Growth (%)')
plt.plot(years, pay_growth, marker='s', color='#ff7f0e', label='Average Pay Growth (%)')
plt.plot(years, wages_growth, marker='^', color='#2ca02c', label='Total Wages Growth (%)')

# Add data labels for each point
for x, y in zip(years, employment_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, color='#1f77b4')
for x, y in zip(years, pay_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, color='#ff7f0e')
for x, y in zip(years, wages_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, color='#2ca02c')

# Labels, title, legend
plt.xlabel('Year')
plt.ylabel('Growth (%)')
plt.title('Year-over-Year Growth Rates: Employment, Pay, and Total Wages (2011-2018)')
plt.xticks(years)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


# In[35]:


import matplotlib.pyplot as plt
import numpy as np

# Years
years = np.arange(2011, 2019)

# Growth rates
employment_growth = [2.7, 6.1, 1.7, 3.8, 4.4, 4.6, -0.3, 2.5]
pay_growth = [5.5, 3.9, 4.2, 11.5, 3.2, 7.6, 9.7, 3.8]

# Plotting
plt.figure(figsize=(10,6))

# Lines with 49ers colors
plt.plot(years, employment_growth, marker='o', color='#AA0000', label='Employment Growth (%)')
plt.plot(years, pay_growth, marker='s', color='#B3995D', label='Average Pay Growth (%)')

# Add bold data labels
for x, y in zip(years, employment_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, fontweight='bold', color='#AA0000')
for x, y in zip(years, pay_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, fontweight='bold', color='#B3995D')

# Labels, title, legend
plt.xlabel('Year')
plt.ylabel('Growth (%)')
plt.title('Year-over-Year Growth: Employment vs Average Pay (2011-2018)')
plt.xticks(years)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


# In[36]:


import matplotlib.pyplot as plt
import numpy as np

# Years
years = np.arange(2011, 2019)

# Growth rates
employment_growth = [2.7, 6.1, 1.7, 3.8, 4.4, 4.6, -0.3, 2.5]
pay_growth = [5.5, 3.9, 4.2, 11.5, 3.2, 7.6, 9.7, 3.8]

# Plotting
plt.figure(figsize=(10,6))

# Lines with 49ers colors
plt.plot(years, employment_growth, marker='o', color='#AA0000', label='Employment Growth (%)')
plt.plot(years, pay_growth, marker='s', color='#B3995D', label='Average Pay Growth (%)')

# Add bold data labels
for x, y in zip(years, employment_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, fontweight='bold', color='#AA0000')
for x, y in zip(years, pay_growth):
    plt.text(x, y+0.3, f'{y:.1f}%', ha='center', fontsize=9, fontweight='bold', color='#B3995D')

# Vertical line for Levi's Stadium opening
plt.axvline(x=2014, color='black', linestyle='--', linewidth=1.5)
plt.text(2014+0.1, max(max(employment_growth), max(pay_growth)), "Levi's Stadium Opened\n↓", 
         rotation=0, fontsize=10, fontweight='bold', va='top', color='black')

# Labels, title, legend
plt.xlabel('Year')
plt.ylabel('Growth (%)')
plt.title('Year-over-Year Growth: Employment vs Average Pay (2011-2018)')
plt.xticks(years)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


# In[37]:


import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Average_Pay': [86200, 91000, 94600, 98576, 105382, 113390, 121500, 133900, 139000],
    'Total_Wages': [72887820000, 79079000000, 87079260000, 92500000000, 102600000000,
                    115300000000, 129186885000, 141952350000, 151020700000]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
plt.plot(df['Year'], df['Average_Pay'], color='#AA0000', marker='o', label='Average Pay')
plt.plot(df['Year'], df['Total_Wages'], color='#FFB81C', marker='o', label='Total Wages')

# Add data labels at the last point of each line
plt.text(df['Year'].iloc[-1], df['Average_Pay'].iloc[-1], f"${df['Average_Pay'].iloc[-1]:,}", 
         color='#AA0000', fontsize=10, va='bottom', ha='right')
plt.text(df['Year'].iloc[-1], df['Total_Wages'].iloc[-1], f"${df['Total_Wages'].iloc[-1]:,}", 
         color='#FFB81C', fontsize=10, va='bottom', ha='right')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[1]*0.95, "Levi's Stadium Opened", rotation=90, va='top', ha='right', fontsize=9)

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Amount ($)')
plt.title('Santa Clara County: Average Pay and Total Wages (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

plt.show()


# In[38]:


import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Average_Pay': [86200, 91000, 94600, 98576, 105382, 113390, 121500, 133900, 139000],
    'Total_Wages': [72887820000, 79079000000, 87079260000, 92500000000, 102600000000,
                    115300000000, 129186885000, 141952350000, 151020700000]
}

df = pd.DataFrame(data)

# Calculate YoY % change
df['Avg_Pay_YoY'] = df['Average_Pay'].pct_change() * 100
df['Total_Wages_YoY'] = df['Total_Wages'].pct_change() * 100

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
plt.plot(df['Year'][1:], df['Avg_Pay_YoY'][1:], color='#AA0000', marker='o', label='Average Pay YoY %')
plt.plot(df['Year'][1:], df['Total_Wages_YoY'][1:], color='#FFB81C', marker='o', label='Total Wages YoY %')

# Add data labels at the last point of each line
plt.text(df['Year'].iloc[-1], df['Avg_Pay_YoY'].iloc[-1], f"{df['Avg_Pay_YoY'].iloc[-1]:.1f}%", 
         color='#AA0000', fontsize=10, va='bottom', ha='right')
plt.text(df['Year'].iloc[-1], df['Total_Wages_YoY'].iloc[-1], f"{df['Total_Wages_YoY'].iloc[-1]:.1f}%", 
         color='#FFB81C', fontsize=10, va='bottom', ha='right')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[1]*0.95, "Levi's Stadium Opened", rotation=90, va='top', ha='right', fontsize=9)

# Formatting
plt.xticks(df['Year'][1:])
plt.ylabel('Year-over-Year % Change')
plt.title('Santa Clara County: YoY % Change in Average Pay and Total Wages (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

plt.show()


# In[39]:


import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Average_Pay': [86200, 91000, 94600, 98576, 105382, 113390, 121500, 133900, 139000],
    'Total_Wages': [72887820000, 79079000000, 87079260000, 92500000000, 102600000000,
                    115300000000, 129186885000, 141952350000, 151020700000]
}

df = pd.DataFrame(data)

# Calculate YoY % change
df['Avg_Pay_YoY'] = df['Average_Pay'].pct_change() * 100
df['Total_Wages_YoY'] = df['Total_Wages'].pct_change() * 100

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
plt.plot(df['Year'][1:], df['Avg_Pay_YoY'][1:], color='#AA0000', marker='o', label='Average Pay YoY %')
plt.plot(df['Year'][1:], df['Total_Wages_YoY'][1:], color='#B3995D', marker='o', label='Total Wages YoY %')

# Add data labels for all points
for x, y in zip(df['Year'][1:], df['Avg_Pay_YoY'][1:]):
    plt.text(x, y, f"{y:.1f}%", color='#AA0000', fontsize=9, ha='center', va='bottom')
for x, y in zip(df['Year'][1:], df['Total_Wages_YoY'][1:]):
    plt.text(x, y, f"{y:.1f}%", color='#B3995D', fontsize=9, ha='center', va='bottom')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0]*1.05, "Levi's Stadium Opened", rotation=90, va='bottom', ha='right', fontsize=9)

# Formatting
plt.xticks(df['Year'][1:])
plt.ylabel('Year-over-Year % Change')
plt.title('Santa Clara County: YoY % Change in Average Pay and Total Wages (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

plt.show()


# In[40]:


import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900],
    'Average_Pay': [86200, 91000, 94600, 98576, 105382, 113390, 121500, 133900, 139000]
}

df = pd.DataFrame(data)

# Calculate YoY % change
df['Employment_YoY'] = df['Employment'].pct_change() * 100
df['Avg_Pay_YoY'] = df['Average_Pay'].pct_change() * 100

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
plt.plot(df['Year'][1:], df['Employment_YoY'][1:], color='#B3995D', marker='o', label='Employment YoY %')
plt.plot(df['Year'][1:], df['Avg_Pay_YoY'][1:], color='#AA0000', marker='o', label='Average Pay YoY %')

# Add data labels for all points
for x, y in zip(df['Year'][1:], df['Employment_YoY'][1:]):
    plt.text(x, y, f"{y:.1f}%", color='#B3995D', fontsize=9, ha='center', va='bottom')
for x, y in zip(df['Year'][1:], df['Avg_Pay_YoY'][1:]):
    plt.text(x, y, f"{y:.1f}%", color='#AA0000', fontsize=9, ha='center', va='bottom')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0]*1.05, "Levi's Stadium Opened", rotation=90, va='bottom', ha='right', fontsize=8)

# Formatting
plt.xticks(df['Year'][1:])
plt.ylabel('Year-over-Year % Change')
plt.title('Santa Clara County: YoY % Change in Employment and Average Pay (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

plt.show()


# In[41]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900],
    'Average_Pay': [86200, 91000, 94600, 98576, 105382, 113390, 121500, 133900, 139000]
}

df = pd.DataFrame(data)

# Calculate YoY % change
df['Employment_YoY'] = df['Employment'].pct_change() * 100
df['Avg_Pay_YoY'] = df['Average_Pay'].pct_change() * 100

# Plot
plt.figure(figsize=(15,15), facecolor='none')  # transparent background
plt.plot(df['Year'][1:], df['Employment_YoY'][1:], color='#B3995D', marker='o', label='Employment YoY %')
plt.plot(df['Year'][1:], df['Avg_Pay_YoY'][1:], color='#AA0000', marker='o', label='Average Pay YoY %')

# Small offset to avoid intersecting with the line
offset = 0.3  # percentage points

# Add **large bold data labels** (font size 16)
for x, y in zip(df['Year'][1:], df['Employment_YoY'][1:]):
    plt.text(x, y + offset, f"{y:.1f}%", color='#B3995D',
             fontsize=16, fontweight='bold', ha='center', va='bottom')

for x, y in zip(df['Year'][1:], df['Avg_Pay_YoY'][1:]):
    plt.text(x, y + offset, f"{y:.1f}%", color='#AA0000',
             fontsize=16, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0]*1.05, "Levi's Stadium Opened",
         rotation=0, va='bottom', ha='right', fontsize=9, fontweight='bold')

# Formatting
plt.xticks(df['Year'][1:], fontweight='bold')
plt.yticks(fontweight='bold')
plt.ylabel('Year-over-Year % Change', fontweight='bold')
plt.xlabel('Year', fontweight='bold')
plt.title('Santa Clara County: YoY % Change in Employment and Average Pay (2010-2018)', fontweight='bold')

# Bold legend
leg = plt.legend()
for text in leg.get_texts():
    text.set_fontweight('bold')

plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Employment_AvgPay_YoY.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[42]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
plt.plot(df['Year'], df['Establishments'], color='#B3995D', marker='o', linewidth=2, label='Establishments')

# Add bold data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='#B3995D', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0]*1.05, "Levi's Stadium Opened", rotation=90, va='bottom', ha='right', fontsize=9)

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[43]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Calculate linear trend line
z = np.polyfit(df['Year'], df['Establishments'], 1)  # linear fit
p = np.poly1d(z)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
plt.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Trend line (black dashed)
plt.plot(df['Year'], p(df['Year']), color='#000000', linestyle='--', linewidth=2, label='Trend Line')

# Add bold data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='#AA0000', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
plt.text(2014, plt.ylim()[0]*1.05, "Levi's Stadium Opened", rotation=90, va='bottom', ha='right', fontsize=9)

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[44]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
plt.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='#AA0000', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line
plt.axvline(x=2014, color='gray', linestyle='--', linewidth=1)
# Add text above the line with arrow pointing down
plt.annotate("Levi's Stadium Opened",
             xy=(2014, max(df['Establishments'])*0.97),   # arrow points to top of chart
             xytext=(2014, max(df['Establishments'])*1.03), # text above
             ha='center',
             va='bottom',
             fontsize=9,
             arrowprops=dict(arrowstyle='-|>', color='gray'))

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[45]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
plt.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold black data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
plt.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Add text above line with arrow pointing down, within chart bounds
plt.annotate("Levi's Stadium Opened",
             xy=(2014, max(df['Establishments'])*0.97),    # arrow points near top
             xytext=(2014, max(df['Establishments'])*1.01), # text just above arrow
             ha='center',
             va='bottom',
             fontsize=9,
             arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[46]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
plt.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold black data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
plt.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Add text above line pointing down, **inside chart bounds**
y_max = df['Establishments'].max()
text_y = y_max - (y_max * 0.02)  # slightly below top to fit
plt.text(2014, text_y, "Levi's Stadium Opened", ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')
# Optionally add a small downward arrow
plt.annotate('', xy=(2014, text_y-200), xytext=(2014, text_y), arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[47]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(20,15), facecolor='none')  # transparent background

# Actual data line (red)
plt.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold black data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    plt.text(x, y, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
plt.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Add text above line with downward arrow, **fully inside plot and above data line**
y_max = df['Establishments'].max()
text_y = y_max + 2000  # slightly above top data point to avoid overlap
arrow_y = y_max  # arrow points to top of data line
plt.annotate("Levi's Stadium Opened",
             xy=(2014, arrow_y),
             xytext=(2014, text_y),
             ha='center',
             va='bottom',
             fontsize=9,
             fontweight='bold',
             color='black',
             arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
plt.xticks(df['Year'])
plt.ylabel('Number of Establishments')
plt.title('Santa Clara County: Establishments per Year (2010-2018)')
plt.legend()
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[48]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
ax.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold black data labels for all points
for x, y in zip(df['Year'], df['Establishments']):
    ax.text(x, y, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
ax.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Get axis limits
y_min, y_max = ax.get_ylim()

# Add text above trend line **inside axis**, arrow pointing down
ax.annotate("Levi's Stadium Opened",
            xy=(2014, y_max * 0.95),   # arrow points slightly below top
            xytext=(2014, y_max * 0.99), # text near top but inside chart
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
            color='black',
            arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
ax.set_xticks(df['Year'])
ax.set_ylabel('Number of Establishments')
ax.set_title('Santa Clara County: Establishments per Year (2010-2018)')
ax.legend()
ax.grid(False)
ax.patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[49]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
ax.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold black data labels for all points **above the line**
for x, y in zip(df['Year'], df['Establishments']):
    ax.text(x, y + 800, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
ax.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Get axis limits
y_min, y_max = ax.get_ylim()

# Add text above trend line **inside axis**, arrow pointing down
ax.annotate("Levi's Stadium Opened",
            xy=(2014, y_max * 0.95),    # arrow points slightly below top
            xytext=(2014, y_max * 0.99), # text near top but inside chart
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
            color='black',
            arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
ax.set_xticks(df['Year'])
ax.set_ylabel('Number of Establishments')
ax.set_title('Santa Clara County: Establishments per Year (2010-2018)')
ax.legend()
ax.grid(False)
ax.patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[50]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(12,12), facecolor='none')  # transparent background

# Actual data line (red)
ax.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2)

# Add bold data labels with larger font size (16)
label_offset = 300
for x, y in zip(df['Year'], df['Establishments']):
    ax.text(x, y + label_offset, f"{y:,}",
            color='black', fontsize=16, fontweight='bold', ha='center', va='bottom')

# Levi's Stadium vertical trend line (black)
ax.axvline(x=2014, color='black', linestyle='--', linewidth=1)

# Add text above trend line with arrow
ax.annotate("Levi's Stadium Opened",
            xy=(2014, max(df['Establishments'])*0.97),
            xytext=(2014, max(df['Establishments'])*0.99),
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
            color='black',
            arrowprops=dict(arrowstyle='-|>', color='black'))

# Formatting
ax.set_xticks(df['Year'])

# Bold axis labels
ax.set_ylabel('Number of Establishments', fontweight='bold')
ax.set_xlabel('Year', fontweight='bold')

# Bold title
ax.set_title('Santa Clara County: Establishments per Year (2010-2018)', fontweight='bold')

# Bold tick labels
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')

ax.grid(False)
ax.patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[51]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Example data (replace with your actual taxable sales data)
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Taxable_Sales': [16_000_000_000, 16_500_000_000, 17_000_000_000, 17_500_000_000,
                      18_000_000_000, 18_500_000_000, 19_000_000_000, 19_500_000_000, 20_000_000_000]
}

df = pd.DataFrame(data)

# Identify min and max values
min_val = df['Taxable_Sales'].min()
max_val = df['Taxable_Sales'].max()

# Plot
plt.figure(figsize=(12,6), facecolor='none')  # transparent background
bars = plt.bar(df['Year'], df['Taxable_Sales'], color='#003594')  # example color

# Add bold data labels on min and max values
for bar, value in zip(bars, df['Taxable_Sales']):
    if value == min_val or value == max_val:
        plt.text(bar.get_x() + bar.get_width()/2, value, f"${value:,.0f}", 
                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')

# Formatting
plt.ylabel('Taxable Sales ($)')
plt.title('Santa Clara County: Taxable Transactions (2010-2018)')
plt.xticks(df['Year'])
plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Taxable_Transactions.png")
plt.savefig(desktop_path, transparent=True, dpi=300)

plt.show()


# In[52]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold data labels with a tiny offset
offset = df_yearly['Total Taxable Transactions'].max() * 0.01  # 1% offset
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    ax.text(x, y + offset, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold', 
            ha='center', va='bottom')

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions ($)', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

# Optional: format y-axis with commas
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
)

plt.tight_layout()

# Step 4: Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[53]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with small offset
offset = df_yearly['Total Taxable Transactions'].max() * 0.01  # 1% offset
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val or y == max_val:
        ax.text(x, y + offset, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions ($)', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

# Optional: format y-axis with commas
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
)

plt.tight_layout()

# Step 4: Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[54]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with adjusted offsets
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y + max_val*0.015, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions ($)', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

# Optional: format y-axis with commas
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
)

plt.tight_layout()

# Step 4: Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[55]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        # Put label below the point
        ax.text(x, y - max_val*0.015, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        # Put label above the point
        ax.text(x, y + max_val*0.01, f"${y:,.0f}", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions ($)', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

# Optional: format y-axis with commas
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))
)

plt.tight_layout()

# Step 4: Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[56]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        # Label below the line
        ax.text(x, y - max_val*0.015,  color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        # Label above the line
        ax.text(x, y + max_val*0.01,  color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        # Label below the line
        ax.text(x, y - max_val*0.015, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        # Label above the line
        ax.text(x, y + max_val*0.01, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Total Taxable Transactions ($B)', color='black', fontweight='bold')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black', fontweight='bold')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Total Taxable Transactions ($B)', color='black', fontweight='bold')

# Make tick labels bold
ax.tick_params(axis='x', colors='black', labelsize=10)
ax.tick_params(axis='y', colors='black', labelsize=10)
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black', fontweight='bold')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Identify min and max values
min_val = df['Establishments'].min()
max_val = df['Establishments'].max()

# Plot
fig, ax = plt.subplots(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
ax.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold labels on min and max with offsets
for x, y in zip(df['Year'], df['Establishments']):
    if y == min_val:
        ax.text(x, y - 500, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + 500, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Number of Establishments', color='black', fontweight='bold')

# Make tick labels bold
ax.tick_params(axis='x', colors='black', labelsize=10)
ax.tick_params(axis='y', colors='black', labelsize=10)
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(x=2014, color='black', linestyle='--', label="Levi's Stadium Opened")

# Title and legend
plt.title('Santa Clara County: Establishments per Year (2010-2018)', color='black', fontweight='bold')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)
plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Data: Establishments per year 2010-2018
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Establishments': [59500, 60750, 61900, 62755, 65277, 67491, 69200, 70500, 72100]
}

df = pd.DataFrame(data)

# Identify min and max values
min_val = df['Establishments'].min()
max_val = df['Establishments'].max()

# Plot
fig, ax = plt.subplots(figsize=(12,6), facecolor='none')  # transparent background

# Actual data line (red)
ax.plot(df['Year'], df['Establishments'], color='#AA0000', marker='o', linewidth=2, label='Establishments')

# Add bold labels on min and max with offsets (same placement as previous graph)
for x, y in zip(df['Year'], df['Establishments']):
    if y == min_val:
        ax.text(x, y - 500, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + 500, f"{y:,}", color='black', fontsize=9, fontweight='bold', ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Number of Establishments', color='black', fontweight='bold')

# Make tick labels bold (keep positions unchanged)
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(x=2014, color='black', linestyle='--', label="Levi's Stadium Opened")

# Title and legend (bold)
plt.title('Santa Clara County: Establishments per Year (2010-2018)', color='black', fontweight='bold')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Establishments_Per_Year.png")
plt.savefig(desktop_path, transparent=True, dpi=300)
plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Filter for zip codes
zip_list = ['95051', '95134', '94086', '95050', '95196', '95035', '95054']
df_zip = df4[df4['RegionName'].astype(str).isin(zip_list)].copy()

# Date columns
date_cols = [c for c in df_zip.columns if c[:4].isdigit()]

# Transpose and filter 2012+
df_dates = df_zip[date_cols].transpose()
df_dates.index = pd.to_datetime(df_dates.index)
df_dates = df_dates[df_dates.index >= "2012-01-01"]

# Average price
df_dates['AveragePrice'] = df_dates.mean(axis=1)

# Plot
plt.figure(figsize=(20,10))
plt.plot(df_dates.index, df_dates['AveragePrice'], color="#AA0000", linewidth=2)

# Max and min
max_idx = df_dates['AveragePrice'].idxmax()
max_val = df_dates.loc[max_idx, 'AveragePrice']
min_idx = df_dates['AveragePrice'].idxmin()
min_val = df_dates.loc[min_idx, 'AveragePrice']

plt.annotate(f"${max_val:,.0f}", xy=(max_idx, max_val),
             xytext=(0,17), textcoords='offset points',
             ha='center', color="green", fontsize=12, fontweight="bold")

plt.annotate(f"${min_val:,.0f}", xy=(min_idx, min_val),
             xytext=(0,17), textcoords='offset points',
             ha='center', color="red", fontsize=12, fontweight="bold")

# Vertical trend line for Levi's Stadium
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)
plt.text(pd.Timestamp("2014-01-01"), df_dates['AveragePrice'].min()*2,
         "Levi's Stadium Opened", rotation=90, verticalalignment='bottom',
         horizontalalignment='left', fontsize=10, fontweight="bold")

# Specific year labels (skip max/min)
years_to_label = [2014, 2016, 2018, 2020, 2022, 2024, 2025]

for year in years_to_label:
    date_match = df_dates[df_dates.index.year == year]
    if len(date_match) > 0:
        date_val = date_match.index[0]
        price_val = date_match['AveragePrice'].iloc[0]
        if date_val in [max_idx, min_idx]:
            continue
        y_offset = 14 if year == 2025 else 17
        plt.annotate(f"${price_val:,.0f}", xy=(date_val, price_val),
                     xytext=(0, y_offset), textcoords='offset points',
                     ha='center', fontsize=12, fontweight="bold", color='black')

# Formatting (ALL BOLD NOW)
plt.title("Average Zillow Home Value - Zip Codes Near Stadium Only", fontweight="bold")
plt.xlabel("Year", fontweight="bold")
plt.ylabel("Average Home Value (USD)", fontweight="bold")

# Bold ticks
plt.xticks(fontweight="bold")
plt.yticks(fontweight="bold")

plt.grid(False)
plt.tight_layout()

# Save
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "Zillow_Average_Stadium_ZIPs_FINAL.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Assuming df_yoy is already prepared with columns: Year, EmploymentYoY, PayYoY
plt.figure(figsize=(20,10))

plt.plot(df_yoy['Year'], df_yoy['EmploymentYoY'], color="#AA0000", linewidth=2)
plt.plot(df_yoy['Year'], df_yoy['PayYoY'], color="#003594", linewidth=2)

# DATA LABELS (4 font sizes bigger than before → fontsize=16)
for i in range(len(df_yoy)):
    plt.annotate(f"{df_yoy['EmploymentYoY'].iloc[i]:.1f}%", 
                 xy=(df_yoy['Year'].iloc[i], df_yoy['EmploymentYoY'].iloc[i]),
                 xytext=(0, 14), textcoords="offset points",
                 ha="center", fontsize=16, fontweight="bold")

    plt.annotate(f"{df_yoy['PayYoY'].iloc[i]:.1f}%", 
                 xy=(df_yoy['Year'].iloc[i], df_yoy['PayYoY'].iloc[i]),
                 xytext=(0, -20), textcoords="offset points",
                 ha="center", fontsize=16, fontweight="bold")

# Formatting: bold title, labels, ticks
plt.title("Santa Clara County: YoY % Change in Employment and Average Pay (2010–2018)",
          fontweight="bold", fontsize=18)

plt.xlabel("Year", fontweight="bold", fontsize=16)
plt.ylabel("Year-over-Year % Change", fontweight="bold", fontsize=16)

plt.xticks(fontweight="bold", fontsize=14)
plt.yticks(fontweight="bold", fontsize=14)

# Remove legend (you asked for this earlier)
# If you want legend back, uncomment the next line.
# plt.legend(["Employment YoY", "Pay YoY"], fontsize=14)

plt.grid(False)
plt.gca().patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "YoY_Growth_BOLD_LABELS.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import plotly.graph_objects as go
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Avg pay data
pay_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Avg_Pay': [86200, 91000, 94600, 98576, 109900, 113390, 122980, 133900, 139000]
}
df_pay = pd.DataFrame(pay_data)

fig = go.Figure()

# Main line + markers
fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'],
    mode='lines+markers',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    name='Avg Pay'
))

# Separate text trace with minimal offset above each point
offset = 200  # minimal vertical offset
fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'] + offset,
    mode='text',
    text=df_pay['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
    textfont=dict(size=16, color='black', family='Arial', weight='bold'),
    showlegend=False
))

# Trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_pay['Avg_Pay']) * 0.95,
    y1=max(df_pay['Avg_Pay']) * 1.05,
    line=dict(color='black', width=3, dash='dash')
)
fig.add_annotation(
    x=2014,
    y=max(df_pay['Avg_Pay']) * 1.05,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=15, family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(
    title=dict(text='Santa Clara County: Average Annual Pay (2010–2018)', font=dict(size=23, color='black', family='Arial', weight='bold')),
    height=700,
    width=1200,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(title='Year', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold')),
    yaxis=dict(title='Average Annual Pay ($)', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold'))
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Avg_Pay_2010_2018_Line_Levis.png"))
fig.show()
print("✓ Saved: Avg_Pay_2010_2018_Line_Levis.png on Desktop")


# In[ ]:


import pandas as pd
import plotly.graph_objects as go
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Avg pay data
pay_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Avg_Pay': [86200, 91000, 94600, 98576, 109900, 113390, 122980, 133900, 139000]
}
df_pay = pd.DataFrame(pay_data)

# Small offset = 0.5% of each value
offset = df_pay['Avg_Pay'] * 0.005

fig = go.Figure()

# Main line + markers + data labels with offset
fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'],
    mode='lines+markers+text',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    text=(df_pay['Avg_Pay'] + offset).apply(lambda x: f'${x:,.0f}'),
    textposition='top center',
    textfont=dict(size=16, color='black', family='Arial', weight='bold'),
    name='Avg Pay'
))

# Trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_pay['Avg_Pay']) * 0.95,
    y1=max(df_pay['Avg_Pay']) * 1.05,
    line=dict(color='black', width=3, dash='dash')
)
fig.add_annotation(
    x=2014,
    y=max(df_pay['Avg_Pay']) * 1.05,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=16, family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(
    title=dict(text='Santa Clara County: Average Annual Pay (2010–2018)', font=dict(size=23, color='black', family='Arial', weight='bold')),
    height=700,
    width=1200,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(title='Year', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold')),
    yaxis=dict(title='Average Annual Pay ($)', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold'))
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Avg_Pay_2010_2018_Line_Levis.png"))
fig.show()
print("✓ Saved: Avg_Pay_2010_2018_Line_Levis.png on Desktop")


# In[ ]:


import pandas as pd
import plotly.graph_objects as go
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Avg pay data
pay_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Avg_Pay': [86200, 91000, 94600, 98576, 109900, 113390, 122980, 133900, 139000]
}
df_pay = pd.DataFrame(pay_data)

# Small vertical offset = 0.5% of each value
offset = df_pay['Avg_Pay'] * 0.005
# Small horizontal offset to the left
x_offset = -0.15  # years

fig = go.Figure()

# Main line + markers + data labels with vertical offset and slight left shift
fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'],
    mode='lines+markers',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    name='Avg Pay'
))

# Add labels as separate trace for precise horizontal adjustment
fig.add_trace(go.Scatter(
    x=df_pay['Year'] + x_offset,  # shift left
    y=df_pay['Avg_Pay'] + offset, # slight vertical offset
    mode='text',
    text=df_pay['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
    textposition='top center',
    textfont=dict(size=16, color='black', family='Arial', weight='bold'),
    showlegend=False
))

# Trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_pay['Avg_Pay']) * 0.95,
    y1=max(df_pay['Avg_Pay']) * 1.05,
    line=dict(color='black', width=3, dash='dash')
)
fig.add_annotation(
    x=2014,
    y=max(df_pay['Avg_Pay']) * 1.05,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=16, family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(
    title=dict(text='Santa Clara County: Average Annual Pay (2010–2018)', font=dict(size=23, color='black', family='Arial', weight='bold')),
    height=700,
    width=1200,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(title='Year', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold')),
    yaxis=dict(title='Average Annual Pay ($)', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold'))
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Avg_Pay_2010_2018_Line_Levis.png"))
fig.show()
print("✓ Saved: Avg_Pay_2010_2018_Line_Levis.png on Desktop")


# In[ ]:


import pandas as pd
import plotly.graph_objects as go
import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Avg pay data
pay_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Avg_Pay': [86200, 91000, 94600, 98576, 109900, 113390, 122980, 133900, 139000]
}
df_pay = pd.DataFrame(pay_data)

# Small vertical offset = 0.5% of each value
offset = df_pay['Avg_Pay'] * 0.005
# Small horizontal offset to the left
x_offset = -0.35  # shifted more to the left

fig = go.Figure()

# Main line + markers
fig.add_trace(go.Scatter(
    x=df_pay['Year'],
    y=df_pay['Avg_Pay'],
    mode='lines+markers',
    line=dict(color='#B22222', width=4),
    marker=dict(color='#B22222', size=10),
    name='Avg Pay'
))

# Labels as separate trace for precise horizontal adjustment
fig.add_trace(go.Scatter(
    x=df_pay['Year'] + x_offset,
    y=df_pay['Avg_Pay'] + offset,
    mode='text',
    text=df_pay['Avg_Pay'].apply(lambda x: f'${x:,.0f}'),
    textposition='top center',
    textfont=dict(size=16, color='black', family='Arial', weight='bold'),
    showlegend=False
))

# Trend line at 2014
fig.add_shape(
    type='line',
    x0=2014, x1=2014,
    y0=min(df_pay['Avg_Pay']) * 0.95,
    y1=max(df_pay['Avg_Pay']) * 1.05,
    line=dict(color='black', width=3, dash='dash')
)
fig.add_annotation(
    x=2014,
    y=max(df_pay['Avg_Pay']) * 1.05,
    text="Levi's Stadium Opens",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='black', size=16, family='Arial', weight='bold')
)

# Layout formatting
fig.update_layout(
    title=dict(text='Santa Clara County: Average Annual Pay (2010–2018)', font=dict(size=23, color='black', family='Arial', weight='bold')),
    height=700,
    width=1200,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(title='Year', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold')),
    yaxis=dict(title='Average Annual Pay ($)', showgrid=False, showline=True, linecolor='black', tickfont=dict(color='black', size=15, family='Arial', weight='bold'))
)

# Save and show
fig.write_image(os.path.join(desktop_path, "Avg_Pay_2010_2018_Line_Levis.png"))
fig.show()
print("✓ Saved: Avg_Pay_2010_2018_Line_Levis.png on Desktop")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Filter for zip codes
zip_list = ['95051', '95134', '94086', '95050', '95196', '95035', '95054']
df_zip = df4[df4['RegionName'].astype(str).isin(zip_list)].copy()

# Date columns
date_cols = [c for c in df_zip.columns if c[:4].isdigit()]

# Transpose and filter 2012+
df_dates = df_zip[date_cols].transpose()
df_dates.index = pd.to_datetime(df_dates.index)
df_dates = df_dates[df_dates.index >= "2012-01-01"]

# Average price
df_dates['AveragePrice'] = df_dates.mean(axis=1)

# Plot
plt.figure(figsize=(20,13))
plt.plot(df_dates.index, df_dates['AveragePrice'], color="#AA0000", linewidth=2)  # line only

# Max and min
max_idx = df_dates['AveragePrice'].idxmax()
max_val = df_dates.loc[max_idx, 'AveragePrice']
min_idx = df_dates['AveragePrice'].idxmin()
min_val = df_dates.loc[min_idx, 'AveragePrice']

# Horizontal offset for labels: 3 points to the left
x_offset = -30

# Annotate max
plt.annotate(f"${max_val:,.0f}", xy=(max_idx, max_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', color="green", fontsize=16, fontweight="bold")
plt.plot(max_idx, max_val, 'o', color="green", markersize=6)  # dot for max

# Annotate min
plt.annotate(f"${min_val:,.0f}", xy=(min_idx, min_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', color="red", fontsize=16, fontweight="bold")
plt.plot(min_idx, min_val, 'o', color="red", markersize=6)  # dot for min

# Vertical trend line for Levi's Stadium
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)

# Specific year labels (skip max/min)
years_to_label = [2014, 2016, 2018, 2020, 2022, 2024, 2025]

for year in years_to_label:
    date_match = df_dates[df_dates.index.year == year]
    if len(date_match) > 0:
        date_val = date_match.index[0]
        price_val = date_match['AveragePrice'].iloc[0]
        if date_val in [max_idx, min_idx]:
            continue
        y_offset = 14 if year == 2025 else 17
        plt.annotate(f"${price_val:,.0f}", xy=(date_val, price_val),
                     xytext=(x_offset, y_offset), textcoords='offset points',
                     ha='center', va='bottom', fontsize=16, fontweight="bold", color='black')
        plt.plot(date_val, price_val, 'o', color="black", markersize=6)  # dot only for labeled points

# Formatting: bold axis labels and tick marks
plt.xlabel("Year", fontsize=16, fontweight="bold")
plt.ylabel("Average Home Value (USD)", fontsize=16, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.grid(False)
plt.tight_layout()

# Save
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "Zillow_Average_Stadium_ZIPs_FINAL.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)
df_emp['Date'] = pd.to_datetime(df_emp['Year'], format='%Y')

# Plot
plt.figure(figsize=(20,10))
plt.plot(df_emp['Date'], df_emp['Employment'], color="#B22222", linewidth=2)  # line only

# Max and min
max_idx = df_emp['Employment'].idxmax()
max_val = df_emp.loc[max_idx, 'Employment']
min_idx = df_emp['Employment'].idxmin()
min_val = df_emp.loc[min_idx, 'Employment']

# Horizontal offset for labels: 3 points left
x_offset = -3  

# Annotate max
plt.annotate(f"{max_val:,}", xy=(df_emp['Date'][max_idx], max_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="green")
plt.plot(df_emp['Date'][max_idx], max_val, 'o', color="green", markersize=6)

# Annotate min
plt.annotate(f"{min_val:,}", xy=(df_emp['Date'][min_idx], min_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="red")
plt.plot(df_emp['Date'][min_idx], min_val, 'o', color="red", markersize=6)

# Vertical trend line for Levi's Stadium 2014
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)
plt.text(pd.Timestamp("2014-01-01"), df_emp['Employment'].min()*0.98,
         "Levi's Stadium Opens", rotation=90, verticalalignment='bottom',
         horizontalalignment='left', fontsize=12, fontweight="bold")

# Specific year labels (skip max/min)
years_to_label = [2011,2013,2015,2016,2017,2018]

for year in years_to_label:
    date_match = df_emp[df_emp['Year'] == year]
    if len(date_match) > 0:
        date_val = date_match['Date'].iloc[0]
        emp_val = date_match['Employment'].iloc[0]
        if date_val in [df_emp['Date'][max_idx], df_emp['Date'][min_idx]]:
            continue
        y_offset = 17
        plt.annotate(f"{emp_val:,}", xy=(date_val, emp_val),
                     xytext=(x_offset, y_offset), textcoords='offset points',
                     ha='center', va='bottom', fontsize=16, fontweight="bold", color='black')
        plt.plot(date_val, emp_val, 'o', color="black", markersize=6)

# Formatting
plt.title("Santa Clara County: Employment by Year (2010-2018)", fontsize=18, fontweight="bold")
plt.xlabel("Year", fontsize=16, fontweight="bold")
plt.ylabel("Employment", fontsize=16, fontweight="bold")
plt.grid(False)
plt.tight_layout()

# Save
file_path = os.path.join(desktop, "Employment_by_Year_2010_2018_Line_Levis_FINAL.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")








# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)
df_emp['Date'] = pd.to_datetime(df_emp['Year'], format='%Y')

# Plot
plt.figure(figsize=(20,10))
plt.plot(df_emp['Date'], df_emp['Employment'], color="#B22222", linewidth=2)  # line only

# Max and min
max_idx = df_emp['Employment'].idxmax()
max_val = df_emp.loc[max_idx, 'Employment']
min_idx = df_emp['Employment'].idxmin()
min_val = df_emp.loc[min_idx, 'Employment']

# Horizontal offset for labels: 3 points left
x_offset = -3  

# Annotate max
plt.annotate(f"{max_val:,}", xy=(df_emp['Date'][max_idx], max_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="green")
plt.plot(df_emp['Date'][max_idx], max_val, 'o', color="green", markersize=6)

# Annotate min
plt.annotate(f"{min_val:,}", xy=(df_emp['Date'][min_idx], min_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="red")
plt.plot(df_emp['Date'][min_idx], min_val, 'o', color="red", markersize=6)

# Vertical trend line for 2014 (no text)
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)

# Specific year labels (skip max/min)
years_to_label = [2011,2013,2015,2016,2017,2018]

for year in years_to_label:
    date_match = df_emp[df_emp['Year'] == year]
    if len(date_match) > 0:
        date_val = date_match['Date'].iloc[0]
        emp_val = date_match['Employment'].iloc[0]
        if date_val in [df_emp['Date'][max_idx], df_emp['Date'][min_idx]]:
            continue
        y_offset = 17
        plt.annotate(f"{emp_val:,}", xy=(date_val, emp_val),
                     xytext=(x_offset, y_offset), textcoords='offset points',
                     ha='center', va='bottom', fontsize=16, fontweight="bold", color='black')
        plt.plot(date_val, emp_val, 'o', color="black", markersize=6)

# Formatting
plt.xlabel("Year", fontsize=16, fontweight="bold")
plt.ylabel("Employment", fontsize=16, fontweight="bold")
plt.grid(False)
plt.tight_layout()

# Save
file_path = os.path.join(desktop, "Employment_by_Year_2010_2018_Line_Levis_FINAL_v2.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)
df_emp['Date'] = pd.to_datetime(df_emp['Year'], format='%Y')

# Plot
plt.figure(figsize=(20,13))
plt.plot(df_emp['Date'], df_emp['Employment'], color="#B22222", linewidth=2)  # line only

# Max and min
max_idx = df_emp['Employment'].idxmax()
max_val = df_emp.loc[max_idx, 'Employment']
min_idx = df_emp['Employment'].idxmin()
min_val = df_emp.loc[min_idx, 'Employment']

# Horizontal offset for labels: 3 points left
x_offset = -7

# Annotate max
plt.annotate(f"{max_val:,}", xy=(df_emp['Date'][max_idx], max_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="green")
plt.plot(df_emp['Date'][max_idx], max_val, 'o', color="green", markersize=6)

# Annotate min
plt.annotate(f"{min_val:,}", xy=(df_emp['Date'][min_idx], min_val),
             xytext=(x_offset,17), textcoords='offset points',
             ha='center', va='bottom', fontsize=16, fontweight="bold", color="red")
plt.plot(df_emp['Date'][min_idx], min_val, 'o', color="red", markersize=6)

# Vertical trend line for 2014 (no text)
plt.axvline(x=pd.Timestamp("2014-01-01"), color="black", linestyle="--", linewidth=1)

# Specific year labels (skip max/min)
years_to_label = [2011,2013,2015,2016,2017,2018]

for year in years_to_label:
    date_match = df_emp[df_emp['Year'] == year]
    if len(date_match) > 0:
        date_val = date_match['Date'].iloc[0]
        emp_val = date_match['Employment'].iloc[0]
        if date_val in [df_emp['Date'][max_idx], df_emp['Date'][min_idx]]:
            continue
        y_offset = 17
        plt.annotate(f"{emp_val:,}", xy=(date_val, emp_val),
                     xytext=(x_offset, y_offset), textcoords='offset points',
                     ha='center', va='bottom', fontsize=16, fontweight="bold", color='black')
        plt.plot(date_val, emp_val, 'o', color="black", markersize=6)

# Formatting
plt.xlabel("Year", fontsize=16, fontweight="bold")
plt.ylabel("Employment", fontsize=16, fontweight="bold")

# Bold ticks
plt.xticks(fontsize=14, fontweight="bold")
plt.yticks(fontsize=14, fontweight="bold")

plt.grid(False)
plt.tight_layout()

# Save
file_path = os.path.join(desktop, "Employment_by_Year_2010_2018_Line_Levis_FINAL_BOLD.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data 2010-2018
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)

# Plot
fig, ax = plt.subplots(figsize=(25,20), facecolor='none')  # transparent background

# Plot line
ax.plot(df_emp['Year'], df_emp['Employment'], color='#B22222', marker='o', linewidth=3)

# Add data labels with small offset and bold font
label_offset = 3000  # small vertical offset
for x, y in zip(df_emp['Year'], df_emp['Employment']):
    ax.text(x-0.2, y + label_offset, f"{y:,}", color='black', fontsize=20, fontweight='bold', ha='center', va='bottom')

# Vertical trend line at 2014 (no text)
ax.axvline(x=2014, color='black', linestyle='--', linewidth=2)

# Axis labels and title
ax.set_xlabel('Year', fontweight='bold', fontsize=16)
ax.set_ylabel('Employment', fontweight='bold', fontsize=16)

# Bold tick labels
ax.tick_params(axis='both', which='major', labelsize=16, labelcolor='black')
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')

ax.grid(False)
ax.patch.set_alpha(0)  # transparent background
plt.tight_layout()

# Save to Desktop
file_path = os.path.join(desktop_path, "Employment_2010_2018_Labels_Bold.png")
plt.savefig(file_path, transparent=True, dpi=300)
plt.show()

print(f"✓ Saved: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)

# Plot
fig, ax = plt.subplots(figsize=(15,15), facecolor='none')

# Employment line
ax.plot(df_emp['Year'], df_emp['Employment'], color='#B22222', marker='o', linewidth=4)

# Data labels (text only, bigger)
label_offset = 3000  # adjust vertical offset so labels don't intersect line
for x, y in zip(df_emp['Year'], df_emp['Employment']):
    ax.text(x - 0.2, y + label_offset, f'{y:,}', color='black',
            fontsize=16, fontweight='bold', ha='center', va='bottom')  # 22pt bold text

# Vertical trend line for 2014
ax.axvline(x=2014, color='black', linestyle='--', linewidth=3)

# Bold axis labels and ticks
ax.set_xlabel('Year', fontsize=18, fontweight='bold')
ax.set_ylabel('Employment', fontsize=18, fontweight='bold')
ax.tick_params(axis='both', labelsize=18, width=2)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('bold')

ax.grid(False)
ax.patch.set_alpha(0)
plt.tight_layout()

# Save
file_path = os.path.join(desktop_path, "Employment_with_Big_DataLabels.png")
plt.savefig(file_path, dpi=300, transparent=True)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Employment data
employment_data = {
    'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018],
    'Employment': [846100, 869000, 922100, 938114, 973668, 1017071, 1063990, 1060500, 1086900]
}

df_emp = pd.DataFrame(employment_data)

# Plot
fig, ax = plt.subplots(figsize=(15,15), facecolor='none')

# Employment line
ax.plot(df_emp['Year'], df_emp['Employment'], color='#B22222', marker='o', linewidth=4)

# Data labels (text only, bigger)
label_offset = 3000  # vertical offset so labels don't intersect line
for x, y in zip(df_emp['Year'], df_emp['Employment']):
    # Move 2010 label slightly to the right, others to the left
    if x == 2010:
        x_pos = x + 0.6
    else:
        x_pos = x - 0.3
    ax.text(x_pos, y + label_offset, f'{y:,}', color='black',
            fontsize=16, fontweight='bold', ha='center', va='bottom')

# Vertical trend line for 2014
ax.axvline(x=2014, color='black', linestyle='--', linewidth=3)

# Bold axis labels and ticks
ax.set_xlabel('Year', fontsize=18, fontweight='bold')
ax.set_ylabel('Employment', fontsize=18, fontweight='bold')
ax.tick_params(axis='both', labelsize=18, width=2)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('bold')

ax.grid(False)
ax.patch.set_alpha(0)
plt.tight_layout()

# Save
file_path = os.path.join(desktop_path, "Employment_with_Big_DataLabels_Adjusted2010.png")
plt.savefig(file_path, dpi=300, transparent=True)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Year-over-Year Employment Growth Data
growth_data = {
    'Year': [2011,2012,2013,2014,2015,2016,2017,2018],
    'YoY_Growth': [2.7, 6.2, 1.7, 3.8, 4.5, 4.7, -0.3, 2.5]  # percentages
}

df_growth = pd.DataFrame(growth_data)

# Plot
fig, ax = plt.subplots(figsize=(15,15), facecolor='none')

# Growth line
ax.plot(df_growth['Year'], df_growth['YoY_Growth'], color='#B22222', marker='o', linewidth=4)

# Data labels (text only, bigger)
for x, y in zip(df_growth['Year'], df_growth['YoY_Growth']):
    # Move 10.2% (i.e., 2012 label) down by 0.2 units
    if x == 2012:
        y_offset = -0.2
    else:
        y_offset = 0.2
    ax.text(x, y + y_offset, f'{y:.1f}%', color='black',
            fontsize=16, fontweight='bold', ha='center', va='bottom')

# Bold axis labels and ticks
ax.set_xlabel('Year', fontsize=18, fontweight='bold')
ax.set_ylabel('Year-over-Year Growth (%)', fontsize=18, fontweight='bold')
ax.tick_params(axis='both', labelsize=18, width=2)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('bold')

ax.grid(False)
ax.patch.set_alpha(0)
plt.tight_layout()

# Save
file_path = os.path.join(desktop_path, "YoY_Employment_Growth_Adjusted_Label.png")
plt.savefig(file_path, dpi=300, transparent=True)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


import matplotlib.pyplot as plt

# Data
years = [2023, 2024, 2025]
values = [16826101, 16385557, 18761741]
colors = ['#AA0000', '#B3995D', 'black']  # alternate colors

# Create figure and axes
fig, ax = plt.subplots(figsize=(8,6), facecolor='none')

# Create bar graph with thinner bars
bars = ax.bar(years, values, color=colors, width=0.4)  # width smaller than default

# Add data labels formatted as currency (bold)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width()/2,          # X position
        bar.get_height(),                         # Y position
        f'${bar.get_height():,}',                 # Currency format
        ha='center', va='bottom', fontsize=12, fontweight='bold', color='black'
    )

# Title
ax.set_title("Net Assessed Property Value (Levi's Stadium)", fontsize=16, fontweight='bold')

# Axis labels
ax.set_xlabel("Year", fontsize=14, fontweight='bold')
ax.set_ylabel("Value (USD)", fontsize=14, fontweight='bold')

# Set x-axis ticks to only whole years and bold them
ax.set_xticks(years)
ax.tick_params(axis='x', labelsize=12, width=2)
ax.tick_params(axis='y', labelsize=12, width=2)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('bold')

# Remove axes background for transparency
ax.patch.set_alpha(0)

# Layout adjustment
plt.tight_layout()

# Save to desktop
desktop_path = '/Users/rishicheruvu/Desktop/Net_Assessed_Property_Value_Levis.png'
plt.savefig(desktop_path, transparent=True, dpi=300)

# Display the plot
plt.show()

print(f"Saved to Desktop: {desktop_path}")


# In[ ]:


import matplotlib.pyplot as plt

# Data
years = [2023, 2024, 2025]
values = [16826101, 16385557, 18761741]
colors = ['#AA0000', '#B3995D', 'black']  # alternate colors

# Convert values to millions for plotting
values_millions = [v/1_000_000 for v in values]

# Create figure and axes
fig, ax = plt.subplots(figsize=(8,6), facecolor='none')

# Create bar graph with thinner bars
bars = ax.bar(years, values_millions, color=colors, width=0.4)  # width smaller than default

# Add data labels formatted as currency in millions (bold)
for bar, val in zip(bars, values_millions):
    ax.text(
        bar.get_x() + bar.get_width()/2,          # X position
        bar.get_height(),                         # Y position
        f'{val:.1f}M',                            # Label in millions
        ha='center', va='bottom', fontsize=12, fontweight='bold', color='black'
    )

# Title
ax.set_title("Net Assessed Property Value (Levi's Stadium)", fontsize=16, fontweight='bold')

# Axis labels
ax.set_xlabel("Year", fontsize=14, fontweight='bold')
ax.set_ylabel("Value (Millions)", fontsize=14, fontweight='bold')

# Set x-axis ticks to only whole years and bold them
ax.set_xticks(years)
ax.tick_params(axis='x', labelsize=12, width=2)
ax.tick_params(axis='y', labelsize=12, width=2)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontweight('bold')

# Set y-axis in increments of 5 million
ax.set_yticks([5, 10, 15, 20])  # in millions
ax.set_yticklabels([f'{i}M' for i in [5, 10, 15, 20]])

# Remove axes background for transparency
ax.patch.set_alpha(0)

# Layout adjustment
plt.tight_layout()

# Save to desktop
desktop_path = '/Users/rishicheruvu/Desktop/Net_Assessed_Property_Value_Levis.png'
plt.savefig(desktop_path, transparent=True, dpi=300)

# Display the plot
plt.show()

print(f"Saved to Desktop: {desktop_path}")


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------- PART 1: SANTA CLARA COUNTY LINE ----------
# Filter for Santa Clara County only
counties = df[df['RegionName'] == 'Santa Clara County']

# Select date columns
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt
time_df_melted = time_df.melt(id_vars='RegionName',
                              var_name='Date',
                              value_name='HomeValue')

# Convert dates
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Santa Clara subset
sc_subset = time_df_melted[time_df_melted['RegionName'] == 'Santa Clara County']
sc_subset['Value_M'] = sc_subset['HomeValue'] / 1_000_000

# ---------- PART 2: ZIP CODE AVERAGE LINE ----------
zip_list = ['95051', '95134', '94086', '95050', '95196', '95035', '95054']
df_zip = df4[df4['RegionName'].astype(str).isin(zip_list)].copy()

# Date columns
date_cols_zip = [c for c in df_zip.columns if c[:4].isdigit()]

# Transpose + 2012 forward
df_dates = df_zip[date_cols_zip].transpose()
df_dates.index = pd.to_datetime(df_dates.index)
df_dates = df_dates[df_dates.index >= "2012-01-01"]

# Average ZIP price (convert to millions)
df_dates['AvgZip_M'] = df_dates.mean(axis=1) / 1_000_000

# ---------- COMBINED PLOT ----------
plt.figure(figsize=(20,13))

# 49ers RED Line
plt.plot(sc_subset['Date'], sc_subset['Value_M'],
         color="#AA0000", linewidth=2.5, label="Santa Clara County (49ers Red)")

# ZIP AVERAGE GOLD Line
plt.plot(df_dates.index, df_dates['AvgZip_M'],
         color="#B3995D", linewidth=2.5, label="Stadium ZIP Avg (Gold)")

# ---------- LABEL MAX/MIN FOR BOTH LINES ----------
### Santa Clara County ###
sc_max = sc_subset.loc[sc_subset['Value_M'].idxmax()]
sc_min = sc_subset.loc[sc_subset['Value_M'].idxmin()]

plt.annotate(f"{sc_max['Value_M']:.2f}M", xy=(sc_max['Date'], sc_max['Value_M']),
             xytext=(-30,18), textcoords='offset points',
             ha='center', color="green", fontsize=16, fontweight="bold")
plt.plot(sc_max['Date'], sc_max['Value_M'], 'o', color="green", markersize=6)

plt.annotate(f"{sc_min['Value_M']:.2f}M", xy=(sc_min['Date'], sc_min['Value_M']),
             xytext=(-30,18), textcoords='offset points',
             ha='center', color="red", fontsize=16, fontweight="bold")
plt.plot(sc_min['Date'], sc_min['Value_M'], 'o', color="red", markersize=6)

### ZIP AVERAGE ###
zip_max = df_dates['AvgZip_M'].idxmax()
zip_min = df_dates['AvgZip_M'].idxmin()

plt.annotate(f"{df_dates.loc[zip_max,'AvgZip_M']:.2f}M",
             xy=(zip_max, df_dates.loc[zip_max,'AvgZip_M']),
             xytext=(-30,18), textcoords='offset points',
             ha='center', color="green", fontsize=16, fontweight="bold")
plt.plot(zip_max, df_dates.loc[zip_max,'AvgZip_M'], 'o', color="green", markersize=6)

plt.annotate(f"{df_dates.loc[zip_min,'AvgZip_M']:.2f}M",
             xy=(zip_min, df_dates.loc[zip_min,'AvgZip_M']),
             xytext=(-30,18), textcoords='offset points',
             ha='center', color="red", fontsize=16, fontweight="bold")
plt.plot(zip_min, df_dates.loc[zip_min,'AvgZip_M'], 'o', color="red", markersize=6)

# ---------- LEVI’S STADIUM EVENT ----------
levi_date = pd.Timestamp("2014-01-01")
plt.axvline(x=levi_date, color="black", linestyle="--", linewidth=1.3)

plt.text(levi_date - pd.Timedelta(days=200),
         max(sc_subset['Value_M'].max(), df_dates['AvgZip_M'].max()) * 0.98,
         "Levi's Stadium Opens",
         rotation=90, verticalalignment='top',
         horizontalalignment='right', fontsize=16, fontweight="bold")

# ---------- FORMATTING ----------
plt.title("Home Values: Santa Clara County vs Stadium ZIPs", fontsize=20, fontweight="bold")
plt.xlabel("Year", fontsize=18, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=18, fontweight="bold")

plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")

plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# Save to Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "Combined_Zillow_49ers_ZIPs.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Saved to Desktop: {file_path}")


# In[ ]:


df4.head()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------- FILTER / AGGREGATE SANTA CLARA COUNTY (SUM METHOD) ----------
sc = df4[df4["CountyName"] == "Santa Clara County"].copy()

# Select all date columns (YYYY-MM-DD)
date_cols = [c for c in sc.columns if c[:4].isdigit()]

# Sum across all Santa Clara County regions
sc_sum = sc[date_cols].sum().to_frame(name="SC_Value")

# Convert index to datetime
sc_sum.index = pd.to_datetime(sc_sum.index)

# Convert values to millions
sc_sum["SC_M"] = sc_sum["SC_Value"] / 1_000_000


# ---------- FILTER STADIUM ZIP CODES ----------
stadium_zips = ["95054", "95050", "95051"]  # add/remove if needed
st = df4[df4["City"].isin(stadium_zips) | df4["RegionName"].isin(stadium_zips)].copy()

# Sum stadium ZIP values
st_sum = st[date_cols].sum().to_frame(name="Stadium_Value")

# Convert index to datetime
st_sum.index = pd.to_datetime(st_sum.index)

# Convert values to millions
st_sum["Stadium_M"] = st_sum["Stadium_Value"] / 1_000_000


# ---------- OPTIONAL: MERGE INTO ONE SERIES FOR PLOTTING ----------
merged = sc_sum.join(st_sum, how="inner")


# ---------- EXAMPLE PLOT (same style as your other graphs) ----------
plt.figure(figsize=(10,5))
plt.plot(merged.index, merged["SC_M"], label="Santa Clara County")
plt.plot(merged.index, merged["Stadium_M"], label="Stadium ZIP Codes")

plt.title("Zillow Housing Values – Santa Clara County vs Stadium Area")
plt.xlabel("Year")
plt.ylabel("Value (Millions)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


df4.head()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Filter for Santa Clara County only
counties = df[df['RegionName'] == 'Santa Clara County']

# Select date columns (adjust index if needed)
date_cols = df.columns[10:]
time_df = counties[['RegionName'] + list(date_cols)]

# Melt for plotting
time_df_melted = time_df.melt(id_vars='RegionName', 
                              var_name='Date', 
                              value_name='HomeValue')

# Convert Date to datetime
time_df_melted['Date'] = pd.to_datetime(time_df_melted['Date'])

# Plot
plt.figure(figsize=(12,8))

# Plot Santa Clara County
subset = time_df_melted[time_df_melted['RegionName'] == 'Santa Clara County']
line_color = '#AA0000'

plt.plot(subset['Date'], subset['HomeValue']/1_000_000, 
         label='Santa Clara County', color=line_color, linewidth=2.5)

# Annotate min and max points
min_idx = subset['HomeValue'].idxmin()
max_idx = subset['HomeValue'].idxmax()

min_row = subset.loc[min_idx]
max_row = subset.loc[max_idx]

plt.annotate(f"{min_row['HomeValue']/1_000_000:.2f}M", 
             xy=(min_row['Date'], min_row['HomeValue']/1_000_000),
             xytext=(0, -15), textcoords='offset points',
             ha='center', color='red', fontsize=10)

plt.annotate(f"{max_row['HomeValue']/1_000_000:.2f}M", 
             xy=(max_row['Date'], max_row['HomeValue']/1_000_000),
             xytext=(0, 10), textcoords='offset points',
             ha='center', color='green', fontsize=10)

# Key events with labels at top and data labels slightly above line
key_years = {
    '2008': 'Financial Crisis',
    '2014': "Levi's Stadium Opens",
    '2020': 'COVID-19 Pandemic'
}

y_max = (subset['HomeValue']/1_000_000).max()

for year, label in key_years.items():
    date = pd.to_datetime(f'{year}-01-01')

    # Interpolate the value for that date
    value = np.interp(date.timestamp(), 
                      subset['Date'].map(pd.Timestamp.timestamp), 
                      subset['HomeValue']/1_000_000)

    # Vertical dashed line for event
    plt.axvline(x=date, color='gray', linestyle='--', linewidth=1.5)

    # Event label at top of graph, slightly left of the line
    plt.text(date - pd.Timedelta(days=200), y_max*0.98, label, rotation=90,
             verticalalignment='top', horizontalalignment='right',
             color='black', fontsize=10)

    # Data label directly above the line (offset to avoid overlap)
    plt.text(date, value + 0.03*value, f"{value:.2f}M", color=line_color, 
             ha='center', va='bottom', fontsize=10)

plt.title('Zillow Home Values: Santa Clara County', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Home Value (Millions $)')
plt.legend()
plt.tight_layout()

# Save to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "SantaClara_HomeValues.png")
plt.savefig(file_path, dpi=300)
plt.show()

print(f"Figure saved to: {file_path}")


# In[ ]:


import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# -------------------- SETTINGS --------------------
red = "#AA0000"       # 49ers red
gold = "#B3995D"      # 49ers-ish gold
zip_list = ['95051', '95134', '94086', '95050', '95196', '95035', '95054']  # stadium zips (adjust if needed)
levi_date = pd.Timestamp("2014-01-01")

# -------------------- DATE COLUMNS --------------------
# Robust detection: columns that look like YYYY-MM-DD
date_cols = [c for c in df4.columns if re.match(r'^\d{4}-\d{2}-\d{2}$', str(c))]
if not date_cols:
    raise ValueError("No date columns found in df4 using YYYY-MM-DD pattern.")

# Sort date columns in chronological order (just in case)
date_cols = sorted(date_cols, key=lambda x: pd.to_datetime(x))

# -------------------- SANTA CLARA COUNTY (SUM) --------------------
sc_rows = df4[df4["CountyName"] == "Santa Clara County"]
if sc_rows.empty:
    raise ValueError("No rows found for CountyName == 'Santa Clara County' in df4.")

# Sum across rows for each date (gives Series indexed by date strings)
sc_sum = sc_rows[date_cols].sum(axis=0).astype(float)
sc_sum.index = pd.to_datetime(sc_sum.index)    # convert index to datetime
sc_m = sc_sum / 1_000_000                       # convert to millions

# -------------------- STADIUM ZIP AVERAGE (MEAN ACROSS ZIPS) --------------------
# There are 2 ways users encode zips in Zillow files: RegionName might include the zip string or City column may
# include the zip. We'll check RegionName first, then City as fallback.
df_zip_candidates = df4[df4["RegionName"].astype(str).isin(zip_list)]
if df_zip_candidates.empty:
    df_zip_candidates = df4[df4["City"].astype(str).isin(zip_list)]

if df_zip_candidates.empty:
    # fallback: sometimes RegionName contains suffix like "95051 (San Jose)" so we check for contains
    df_zip_candidates = df4[df4["RegionName"].astype(str).str.contains('|'.join(zip_list), na=False)]

if df_zip_candidates.empty:
    raise ValueError("No stadium ZIP rows found in df4 using the provided zip_list. Check RegionName/City contents.")

# Average across the selected ZIP rows for each date
zip_mean = df_zip_candidates[date_cols].mean(axis=0).astype(float)
zip_mean.index = pd.to_datetime(zip_mean.index)
zip_m = zip_mean / 1_000_000  # convert to millions

# -------------------- ALIGN SERIES --------------------
# Use inner join on dates so both series share the same x-axis
common_index = sc_m.index.intersection(zip_m.index).sort_values()
sc_m = sc_m.reindex(common_index)
zip_m = zip_m.reindex(common_index)

# -------------------- PLOTTING --------------------
plt.figure(figsize=(20, 13))

# plot lines
plt.plot(common_index, sc_m, color=red, linewidth=3.0, label="Santa Clara County (49ers Red)")
plt.plot(common_index, zip_m, color=gold, linewidth=3.0, label="Stadium ZIP Avg (Gold)")

# annotate max/min for a series (helper)
def annotate_series(series, color_label):
    # if series all-NaN, skip
    if series.dropna().empty:
        return
    idx_max = series.idxmax()
    idx_min = series.idxmin()
    val_max = series.loc[idx_max]
    val_min = series.loc[idx_min]

    plt.plot(idx_max, val_max, 'o', color='green', markersize=7)
    plt.annotate(f"{val_max:.2f}M",
                 xy=(idx_max, val_max),
                 xytext=(-30, 20),
                 textcoords='offset points',
                 fontsize=14, fontweight='bold', color='green',
                 ha='center', va='bottom')

    plt.plot(idx_min, val_min, 'o', color='red', markersize=7)
    plt.annotate(f"{val_min:.2f}M",
                 xy=(idx_min, val_min),
                 xytext=(-30, 20),
                 textcoords='offset points',
                 fontsize=14, fontweight='bold', color='red',
                 ha='center', va='bottom')

# annotate both
annotate_series(sc_m, red)
annotate_series(zip_m, gold)

# Levi's Stadium vertical line and label
y_top = max(sc_m.max(skipna=True), zip_m.max(skipna=True))
plt.axvline(levi_date, color="black", linestyle="--", linewidth=1.8)
plt.text(levi_date - pd.Timedelta(days=200),
         y_top * 0.98,
         "Levi's Stadium Opens",
         rotation=90,
         fontsize=16,
         fontweight="bold",
         verticalalignment='top',
         horizontalalignment='right')

# Formatting: bold labels, ticks, title
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")

plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")

plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# Save to Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
outpath = os.path.join(desktop, "Combined_49ers_vs_StadiumZIPs.png")
plt.savefig(outpath, dpi=300)
plt.show()

print("Saved to:", outpath)


# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------- DATA --------------------
# Santa Clara County (millions)
sc_years = [2000, 2008, 2014, 2020, 2025]
sc_values = [0.37, 0.68, 0.70, 1.13, 1.65]

# Stadium ZIPs (millions)
zip_years = [2000, 2014, 2016, 2018, 2020, 2025]
zip_values = [446476, 662870, 886358, 957889, 1143860, 1603212]
zip_values_m = [v/1_000_000 for v in zip_values]

# -------------------- PLOT --------------------
plt.figure(figsize=(18, 10))

# Santa Clara County line (red)
plt.plot(sc_years, sc_values, color="#AA0000", linewidth=3, marker='o', label="Santa Clara County")

# Stadium ZIPs line (gold)
plt.plot(zip_years, zip_values_m, color="#B3995D", linewidth=3, marker='o', label="Stadium ZIP Avg")

# Annotate points
for x, y in zip(sc_years, sc_values):
    plt.text(x, y+0.03, f"{y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#AA0000")

for x, y in zip(zip_years, zip_values_m):
    plt.text(x, y+0.03, f"{y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#B3995D")

# Levi's Stadium vertical line
plt.axvline(x=2014, color='black', linestyle='--', linewidth=2)
plt.text(2014-0.5, max(max(sc_values), max(zip_values_m))*0.95, "Levi's Stadium Opens",
         rotation=90, fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='right')

# -------------------- FORMATTING --------------------
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# -------------------- SAVE --------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "sell.png")
plt.savefig(file_path, dpi=300)
plt.show()

print("Saved to Desktop as:", file_path)


# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------- DATA --------------------
# Santa Clara County (millions)
sc_years = [2000, 2008, 2014, 2020, 2025]
sc_values = [0.37, 0.68, 0.70, 1.13, 1.65]

# Stadium ZIPs (millions)
zip_years = [2000, 2014, 2016, 2018, 2020, 2025]
zip_values = [446476, 662870, 886358, 957889, 1143860, 1603212]
zip_values_m = [v/1_000_000 for v in zip_values]

# -------------------- PLOT --------------------
plt.figure(figsize=(18, 10))

# Santa Clara County line (red)
plt.plot(sc_years, sc_values, color="#AA0000", linewidth=3, marker='o', label="Santa Clara County")

# Stadium ZIPs line (gold)
plt.plot(zip_years, zip_values_m, color="#B3995D", linewidth=3, marker='o', label="Stadium ZIP Avg")

# Annotate points with vertical offsets
for x, y in zip(sc_years, sc_values):
    plt.text(x, y+0.03, f"{y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#AA0000")  # up by 3 points

for x, y in zip(zip_years, zip_values_m):
    plt.text(x, y-0.03, f"{y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#B3995D")  # down by 3 points

# Levi's Stadium vertical line
plt.axvline(x=2014, color='black', linestyle='--', linewidth=2)
plt.text(2014-0.5, max(max(sc_values), max(zip_values_m))*0.95, "Levi's Stadium Opens",
         rotation=90, fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='right')

# -------------------- FORMATTING --------------------
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# -------------------- SAVE --------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "sell.png")
plt.savefig(file_path, dpi=300)
plt.show()

print("Saved to Desktop as:", file_path)


# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------- DATA --------------------
# Santa Clara County (millions)
sc_years = [2000, 2008, 2014, 2020, 2025]
sc_values = [0.37, 0.68, 0.70, 1.13, 1.65]

# Stadium ZIPs (raw values, convert to millions)
zip_years = [2000, 2014, 2016, 2018, 2020, 2025]
zip_values = [446476, 662870, 886358, 957889, 1143860, 1603212]
zip_values_m = [v/1_000_000 for v in zip_values]

# -------------------- PLOT --------------------
plt.figure(figsize=(25, 15))

# Santa Clara County line (red)
plt.plot(sc_years, sc_values, color="#AA0000", linewidth=3, marker='o', label="Santa Clara County")

# Stadium ZIPs line (gold)
plt.plot(zip_years, zip_values_m, color="#B3995D", linewidth=3, marker='o', label="Stadium ZIP Avg")

# -------------------- ANNOTATE POINTS --------------------
# Red labels: push UP by 0.03 + extra 5 points (0.05 million)
for x, y in zip(sc_years, sc_values):
    plt.text(x, y + 0.08, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#AA0000")

# Gold labels: push DOWN by 0.03 + extra 5 points (0.05 million)
for x, y in zip(zip_years, zip_values_m):
    plt.text(x, y - 0.08, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#B3995D")

# Levi's Stadium vertical line
plt.axvline(x=2014, color='black', linestyle='--', linewidth=2)
plt.text(2014-0.5, max(max(sc_values), max(zip_values_m))*0.95, "Levi's Stadium Opens",
         rotation=90, fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='right')

# -------------------- FORMATTING --------------------
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# -------------------- SAVE --------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "sell.png")
plt.savefig(file_path, dpi=300)
plt.show()

print("Saved to Desktop as:", file_path)


# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------- DATA --------------------
# Santa Clara County (millions)
sc_years = [2000, 2008, 2014, 2020, 2025]
sc_values = [0.37, 0.68, 0.70, 1.13, 1.65]

# Stadium ZIPs (millions)
zip_years = [2000, 2014, 2016, 2018, 2020, 2025]
zip_values = [446476, 662870, 886358, 957889, 1143860, 1603212]
zip_values_m = [v/1_000_000 for v in zip_values]

# -------------------- PLOT --------------------
plt.figure(figsize=(18, 10))

# Santa Clara County line (red)
plt.plot(sc_years, sc_values, color="#AA0000", linewidth=3, marker='o', label="Santa Clara County")

# Stadium ZIPs line (gold)
plt.plot(zip_years, zip_values_m, color="#B3995D", linewidth=3, marker='o', label="Stadium ZIP Avg")

# -------------------- ANNOTATE POINTS --------------------
# Red labels: move DOWN by 0.03 (from previous) for better fit
for x, y in zip(sc_years, sc_values):
    plt.text(x, y + 0.08 - 0.03, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#AA0000")

# Gold labels: move RIGHT by 5 points (horizontal), keep slightly below points
for x, y in zip(zip_years, zip_values_m):
    plt.text(x + 0.2, y - 0.08, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#B3995D")

# Levi's Stadium vertical line
plt.axvline(x=2014, color='black', linestyle='--', linewidth=2)
plt.text(2014-0.5, max(max(sc_values), max(zip_values_m))*0.95, "Levi's Stadium Opens",
         rotation=90, fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='right')

# -------------------- FORMATTING --------------------
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# -------------------- SAVE --------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "sell.png")
plt.savefig(file_path, dpi=300)
plt.show()

print("Saved to Desktop as:", file_path)


# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import os

# -------------------- DATA --------------------
# Santa Clara County (millions)
sc_years = [2000, 2008, 2014, 2020, 2025]
sc_values = [0.37, 0.68, 0.70, 1.13, 1.65]

# Stadium ZIPs (millions)
zip_years = [2000, 2014, 2016, 2018, 2020, 2025]
zip_values = [446476, 662870, 886358, 957889, 1143860, 1603212]
zip_values_m = [v/1_000_000 for v in zip_values]

# -------------------- PLOT --------------------
plt.figure(figsize=(18, 15))

# Santa Clara County line (red)
plt.plot(sc_years, sc_values, color="#AA0000", linewidth=3, marker='o', label="Santa Clara County")

# Stadium ZIPs line (gold)
plt.plot(zip_years, zip_values_m, color="#B3995D", linewidth=3, marker='o', label="Stadium ZIP Avg")

# -------------------- ANNOTATE POINTS --------------------
# Red labels: move DOWN slightly for fit
for x, y in zip(sc_years, sc_values):
    plt.text(x, y + 0.08 - 0.03, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#AA0000")

# Gold labels: move RIGHT by 0.5 units (approx 3 points)
for x, y in zip(zip_years, zip_values_m):
    plt.text(x + 0.5, y - 0.08, f"${y:.2f}M", ha='center', fontsize=14, fontweight='bold', color="#B3995D")

# Levi's Stadium vertical line
plt.axvline(x=2014, color='black', linestyle='--', linewidth=2)
plt.text(2014-0.5, max(max(sc_values), max(zip_values_m))*0.95, "Levi's Stadium Opens",
         rotation=90, fontsize=16, fontweight='bold', verticalalignment='top', horizontalalignment='right')

# -------------------- FORMATTING --------------------
plt.title("Zillow Home Values: Santa Clara County vs Stadium ZIPs", fontsize=24, fontweight="bold")
plt.xlabel("Year", fontsize=20, fontweight="bold")
plt.ylabel("Home Value (Millions USD)", fontsize=20, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.legend(fontsize=16)
plt.grid(False)
plt.tight_layout()

# -------------------- SAVE --------------------
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "sell.png")
plt.savefig(file_path, dpi=300)
plt.show()

print("Saved to Desktop as:", file_path)


# In[57]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets (no currency)
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black (removed $B)
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[ ]:


df.head()


# In[58]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets (no currency)
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black (removed $B)
ax.set_xlabel('Year', color='black')
ax.set_ylabel('Total Taxable Transactions', color='black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Title and legend
plt.title("Santa Clara County: Total Taxable Transactions (2012-Present)", color='black')
ax.legend()

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[59]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets (no currency)
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"{y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black (removed $B), bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Total Taxable Transactions', color='black', fontweight='bold')

# Tick labels bold
ax.tick_params(axis='x', colors='black', labelsize=10, labelrotation=0)
ax.tick_params(axis='y', colors='black', labelsize=10)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

# Format y-axis in billions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Legend bold
legend = ax.legend()
for text in legend.get_texts():
    text.set_fontweight('bold')

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[60]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-present
df_scc = df3[(df3['County'] == 'Santa Clara') & (df3['Calendar Year'] >= 2012)]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with offsets (currency added)
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Total Taxable Transactions', color='black', fontweight='bold')

# Tick labels bold
ax.tick_params(axis='x', colors='black', labelsize=10, labelrotation=0)
ax.tick_params(axis='y', colors='black', labelsize=10)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

# Format y-axis in billions (without $)
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Legend bold
legend = ax.legend()
for text in legend.get_texts():
    text.set_fontweight('bold')

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[61]:


import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Filter for Santa Clara County and 2012-2024 (exclude 2025)
df_scc = df3[
    (df3['County'] == 'Santa Clara') &
    (df3['Calendar Year'] >= 2012) &
    (df3['Calendar Year'] <= 2024)
]

# Step 2: Aggregate by year (sum quarters)
df_yearly = df_scc.groupby('Calendar Year')[['Total Taxable Transactions']].sum().reset_index()

# Identify min and max values
min_val = df_yearly['Total Taxable Transactions'].min()
max_val = df_yearly['Total Taxable Transactions'].max()

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10,6))

# Total Taxable Transactions (49ers red)
ax.plot(
    df_yearly['Calendar Year'],
    df_yearly['Total Taxable Transactions'],
    color='#AA0000',       # 49ers red
    marker='o',
    linewidth=2,
    label='Total Taxable Transactions'
)

# Add bold labels on min and max with currency
for x, y in zip(df_yearly['Calendar Year'], df_yearly['Total Taxable Transactions']):
    if y == min_val:
        ax.text(x, y - max_val*0.015, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='top')
    elif y == max_val:
        ax.text(x, y + max_val*0.01, f"${y/1_000_000_000:.2f}B", color='black', fontsize=9, fontweight='bold',
                ha='center', va='bottom')

# Axis labels and axis color = black, bold
ax.set_xlabel('Year', color='black', fontweight='bold')
ax.set_ylabel('Total Taxable Transactions', color='black', fontweight='bold')

# Tick labels bold
ax.tick_params(axis='x', colors='black', labelsize=10, labelrotation=0)
ax.tick_params(axis='y', colors='black', labelsize=10)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

# Format y-axis in billions (without $)
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x/1_000_000_000:.0f}B")
)

# Vertical trend line for Levi's Stadium opening — black
ax.axvline(
    x=2014,
    color='black',
    linestyle='--',
    label="Levi's Stadium Opening (2014)"
)

# Legend bold
legend = ax.legend()
for text in legend.get_texts():
    text.set_fontweight('bold')

plt.tight_layout()

# Save figure to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "SantaClara_TaxableTransactions.png")
plt.savefig(desktop_path, dpi=300)
plt.show()

print(f"Figure saved to: {desktop_path}")


# In[ ]:




