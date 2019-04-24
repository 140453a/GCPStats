import feedparser
import re
import numpy as np
import matplotlib.pyplot as plt

feed = feedparser.parse("https://audioboom.com/channels/4072907.rss")

outer_list = []

for entry in feed['entries']:
    if re.search("^.*Cannon", entry.title) is None:
        outer_list.append((entry.title, entry.itunes_duration))

for x in outer_list:
    print(x)
