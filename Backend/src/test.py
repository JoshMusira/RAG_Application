import plotly.express as px

# Define the topics and frequencies
topics = [
    "Biden's Political Performance and Strategy",
    "Elections and Campaigns",
    "Health and Age Concerns of Politicians",
    "Media and Public Opinion",
    "Legislative and Judiciary Topics",
    "Foreign Policy and International Relations",
    "Climate Change and Environmental Issues",
    "Economic Policies and Market Analysis",
    "Social Issues and Healthcare",
    "Technology and Innovation"
]

frequencies = [18, 15, 12, 11, 10, 8, 5, 4, 3, 2]

# Create a dataframe
import pandas as pd
df = pd.DataFrame({'Topic': topics, 'Frequency': frequencies})

# Create the bar chart
fig = px.bar(df, x='Topic', y='Frequency', title='Topic  10 Topics and Frequencies')

# Show the plot
fig.show()