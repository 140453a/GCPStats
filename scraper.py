import feedparser
import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

feed = feedparser.parse("https://audioboom.com/channels/4072907.rss")

outer_list = []

for entry in feed['entries']:
    if re.search("^.*Cannon", entry.title) is None:
        outer_list.append((entry.title, entry.itunes_duration))

times = []
names = []
for x in outer_list[::-1]: # Iterate backwards from oldest to most recent
    times.append(round(float(x[1]) / 60 ))
    names.append(x[0])

print(times)

data_set = list(zip(names, times))
df = pd.DataFrame(data = data_set, columns=['Episode', 'Episode Length'])
df['Moving Average (8)'] = df['Episode Length'].rolling(8).mean()
df['Average'] = df['Episode Length'].mean()

lines = df.plot.line(title='GCP Episodes and Running Time (' + str(datetime.datetime.now().date()) + ')')
lines.set_xlabel("Episode #")
lines.set_ylabel("Running Time (Minutes)")


plt.show()
