import feedparser
import re
import numpy as np
import matplotlib.pyplot as plt

feed = feedparser.parse("https://audioboom.com/channels/4072907.rss")

outer_list = []

for entry in feed['entries']:
    if re.search("^.*Cannon", entry.title) is None:
        outer_list.append((entry.title, entry.itunes_duration))

times = []
for x in outer_list[::-1]: # Iterate backwards from oldest to most recent
    times.append(int(x[1]))
    print(x)
y_mean = [np.mean(times)] * len(times)
print(y_mean[0])
fig,ax = plt.subplots()

data_line = ax.plot(times)
mean_line = ax.plot(y_mean, linestyle='--')

plt.show()
