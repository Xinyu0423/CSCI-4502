#!/usr/bin/env python
# coding: utf-8

# In[154]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
import math
import scipy.stats as stats
from matplotlib import dates


get_ipython().run_line_magic('matplotlib', 'inline')


# In[161]:


filepath = "10-02-2019.ics_1.orage"
df = pd.read_csv(filepath, header=None)
df.dropna(how='all', axis=1)
keywords=["Meeting","homework","party","Work","CA","TA","class","movie","tennis",""]
tags=["Meeting","Works","Sports","Leisure","Miscellaneous"]
df['Tag']=np.nan
df['Duration']=np.nan
df.rename(columns={0:'Activity',1:'Start-time',2:'End-time',3:'Note',4:'Location',5:'Tag',6:'Duration'},inplace=True)
df2=pd.DataFrame(columns=['Activity','Tag'])

for i,row in df.iterrows():
    currentcelltags=[]
    s=str(row['Activity'])
    for j in range(len(keywords)):
        
        if (keywords[j] in s) or (keywords[j].lower() in s):
            update=str(keywords[j])
            currentcelltags.append(update)
    
   
    if len(currentcelltags)!=1:
        st=row['Start-time'].split('+')
        et=row['End-time'].split('+')
        date_time_start = datetime.datetime.strptime(st[0], '%Y-%m-%d %H:%M:%S')
        date_time_end = datetime.datetime.strptime(et[0], '%Y-%m-%d %H:%M:%S')
        duration=date_time_end.minute-date_time_start.minute
        data=pd.DataFrame({'Activity':[s],'Start-time':[row['Start-time']],'End-time':[row['End-time']],'Duration':[duration],'Tag':[currentcelltags]})
        df2=df2.append(data)
    else:
        st=row['Start-time'].split('+')
        et=row['End-time'].split('+')
        date_time_start = datetime.datetime.strptime(st[0], '%Y-%m-%d %H:%M:%S')
        date_time_end = datetime.datetime.strptime(et[0], '%Y-%m-%d %H:%M:%S')
        duration=date_time_end.minute-date_time_start.minute
        data=pd.DataFrame({'Activity':[s],'Start-time':[row['Start-time']],'End-time':[row['End-time']],'Duration':[duration],'Tag':['Miscellaneous']})
        df2=df2.append(data)

df2

 #the activities in the new column, group the times into weeks, morning, afternoon and evening. 
# tag the activities, come up tags as much as we can, create a new column for tag, create new column for duration, create new column for morning/afternoon/evening


# In[ ]:




