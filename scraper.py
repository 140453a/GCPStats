import feedparser
import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

feed = feedparser.parse("https://audioboom.com/channels/4072907.rss") # GCP RSS feed

outer_list = []
prev = [0]
for entry in feed['entries']:
    if re.search("^.*Cannon", entry.title) is None: # regex to remove non-GCP episodes
        curr = [int(s) for s in entry.title.split() if s.isdigit()] # extracting first number
        
        if not curr: # there was no number in the episode, for some reason. Standards changed?
            print("Standards have changed, this program needs to be updated!")
            sys.exit()
            
        if curr[0] == prev[0]: # multi-episode
            if re.search("part|Part", entry.title) is None:  # This gets rid of duplicates
                print("Duplicate!", entry.title)		
                continue		
                
            # This is not a duplicate, it is a multi-part episode.
            saved = outer_list.pop()  # popping the previous part.
            new_duration = int(entry.itunes_duration) + int(saved[1]) # appending their durations
            outer_list.append((entry.title, new_duration)) # re-adding combined episode to the list.
            prev = curr
            continue
            
        prev = curr
        outer_list.append((entry.title, entry.itunes_duration))



# Getting the data ready for pandas
times = []
names = []
for x in outer_list[::-1]: # Iterate backwards from oldest to most recent, also converting seconds into minutes.
    times.append(float(x[1]) / 60 )
    names.append(x[0])
    print(x, float(x[1]) / 60 )


# produce an array of major labels for the x-axis.
major_x = (list(range(25, len(times), 25)))
major_x.insert(0, 1)
print(major_x)


# pandas visualization
data_set = list(zip(names, times))

df = pd.DataFrame(data = data_set, columns=['Episode', 'Episode Length'], index=list(range(1, len(times) + 1)))

rolling_a = 8
df['Moving Average (' + str(rolling_a) + ')'] = df['Episode Length'].rolling(rolling_a).mean() #rolling average over 8 episodes

avg = df['Episode Length'].mean()
df['Average(' + str(avg)[:4] + ')'] = avg # truncating the decimal places in average.


lines = df.plot.line(title='GCP Episodes and Running Time (' + str(datetime.datetime.now().date()) + ')')
lines.set_xlabel("Episode #")
lines.set_ylabel("Running Time (Minutes)")

plt.xticks(major_x)
plt.yticks((np.arange(min(times), max(times)+1, 5))) # Want every 5 minutes to be a y-tick
plt.show() # showing the plot. 

#WIP outputting screenshot with pandas
