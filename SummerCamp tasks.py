

import pandas as pd
import numpy

#========================================================================

#importing dataset

df = pd.read_csv("C:/Users/zahra/OneDrive/Desktop/Divar.csv")
df.head()

#========================================================================

# Question 2

#calculating dark query percent:

#finding queries with less than 10 result (removeing duplicates)
dark_query = df.loc[(df['post_page_offset'] == 0) & (df['tokens'].str.len() <= 90) ]

#finding all queries (only with load_post_page action)
all_query = df.loc[(df['post_page_offset'] == 0) & (df['action'] == "load_post_page")]
all_query = all_query.drop_duplicates(subset='source_event_id')

#calculating percent
dark_query_size = dark_query.index
dark_query_size = len(dark_query_size)
all_query_size = all_query.index
all_query_size = len(all_query_size)
dark_query_percent = (dark_query_size/all_query_size)*100
print("dark query percent = ", dark_query_percent)
print("")

#========================================================================

# Question 2

#calculating query bounce rate:
    
#finding queries which are in load_post_page (removeing duplicates)
query_in_load = df.loc[(df['action'] == "load_post_page") & (df['post_page_offset'] == 0)]
query_in_load = query_in_load.drop_duplicates(subset='source_event_id')

#finding queries which are in click_post(removeing duplicates)
query_in_click = df.loc[(df['action'] == 'click_post')]
query_in_click = query_in_click.drop_duplicates(subset='source_event_id')

#finding queries which are in load_post_page but not in click_post (which means query bounce)
query_bounce = pd.concat([query_in_load, query_in_click]).drop_duplicates(subset='source_event_id',keep=False)
query_bounce = query_bounce.loc[(query_bounce['action'] == "load_post_page")]    

#calculating percent 
query_bounce_size = query_bounce.index
query_bounce_size = len(query_bounce_size)
query_in_load_size = query_in_load.index
query_in_load_size = len(query_in_load_size)
query_bounce_rate = (query_bounce_size/query_in_load_size)*100

print("query bounce rate = ", query_bounce_rate)
print("")

#========================================================================

# Question 3

#Percentage of clicked ads compared to loaded ads 

#finding loaded queries (removing duplicates) and max post page offset for each
only_loads = df.loc[(df['action'] == "load_post_page")]
queries = only_loads[['source_event_id','post_page_offset']]
queries = queries.drop_duplicates(subset='source_event_id')
queries = queries.set_index('source_event_id')
queries = queries.max(level='source_event_id')

#calculating loaded ads (each post page offset considered including 24 ads)
queries['post_page_offset'] = queries['post_page_offset']*24
queries['post_page_offset'].replace({0: 24}, inplace=True)

print("showing approximately number of loaded ads for each query:")
print("")
print(queries)

#finding clicked ads
only_clicks = df.loc[(df['action'] == "click_post")]
queries2 = only_clicks[['source_event_id']]
queries2 = queries2.groupby('source_event_id').size()

print("showing approximately number of clicked ads for each query:")
print("")
print(queries2)



   















