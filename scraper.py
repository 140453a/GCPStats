import feedparser
import re
import datetime
import pandas as pd
import matplotlib.pyplot as plt

feed = feedparser.parse("https://audioboom.com/channels/4072907.rss")

outer_list = []
prev = [0]
for entry in feed['entries']:
    if re.search("^.*Cannon", entry.title) is None:
            curr = [int(s) for s in entry.title.split() if s.isdigit()]
            if curr[0] == prev[0]: # multi-episode
                if re.search("part|Part", entry.title) is None: # duplicate
                    print("Duplicate!", entry.title)
                    continue
                saved = outer_list.pop()
                new_duration = int(entry.itunes_duration) + int(saved[1])
                outer_list.append((entry.title, new_duration))
                prev = curr
                continue
            prev = curr

            outer_list.append((entry.title, entry.itunes_duration))


times = []
names = []
for x in outer_list[::-1]: # Iterate backwards from oldest to most recent
    times.append(float(x[1]) / 60 )
    names.append(x[0])
    print(x, float(x[1]) / 60 )





data_set = list(zip(names, times))
df = pd.DataFrame(data = data_set, columns=['Episode', 'Episode Length'])
df['Moving Average (8)'] = df['Episode Length'].rolling(8).mean()
avg = df['Episode Length'].mean()
df['Average(' + str(avg)[:4] + ')'] = avg

lines = df.plot.line(title='GCP Episodes and Running Time (' + str(datetime.datetime.now().date()) + ')')
lines.set_xlabel("Episode #")
lines.set_ylabel("Running Time (Minutes)")


plt.show()
