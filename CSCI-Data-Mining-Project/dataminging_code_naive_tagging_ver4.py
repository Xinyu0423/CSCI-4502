
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
import math
import scipy.stats as stats
from matplotlib import dates

get_ipython().run_line_magic('matplotlib', 'inline')


# In[36]:


def naivetagging():
    filepath = "datafile"
    df = pd.read_csv(filepath, header=None).dropna()
    df.dropna(how='all', axis=1)
    df.rename(columns={0:'Activity',1:'Start-time',2:'End-time',3:'Note',4:'Location',5:'Tag',6:'Duration'},inplace=True)
    keywords=["Meeting","Party","Work","Class","Movie","Tennis","Gym","Lab","HW","Due","Flight","Ceremony"]
    tags=["Meeting","Works","Sports","Leisure","Miscellaneous"]
    df['Tag']=np.nan
    df['Duration']=np.nan
    df.rename(columns={0:'Activity',1:'Start-time',2:'End-time',3:'Note',4:'Location',5:'Tag',6:'Duration'},inplace=True)
    df2=pd.DataFrame(columns=['Activity','Tag','Duration','Part of day','Weekday'])
    df=df.dropna(how='all')
    for i,row in df.iterrows():  # tag data each row
        currentcelltags=[]
        s=str(row['Activity'])
        update="Miscellaneous"
        for j in range(len(keywords)):
        
            if (keywords[j] in s) or (keywords[j].lower() in s):
                update=str(keywords[j])
                break
        duration=0
        timespan="unknown"
        st=row['Start-time'].split('+')
        et=row['End-time'].split('+')
        st2=st[0].split(' ')
        et2=et[0].split(' ')
        if len(st2)>1:
            s1=st2[1]
            date_time_start = datetime.datetime.strptime(s1[:7], "%H:%M:%S")
        dt=st2[0]
        year,month,day=(int(x) for x in dt.split('-'))
        
        date_time=datetime.date(year,month,day).weekday()

        if len(et2)>1:
            s2=et2[1]
            date_time_end=datetime.datetime.strptime(s2[:7],"%H:%M:%S")
        duration=date_time_end-date_time_start
        morning=datetime.datetime.strptime("12:00:00","%H:%M:%S")
        afternoon=datetime.datetime.strptime("18:00:00","%H:%M:%S")
        
        if date_time_start<morning:
            timespan="Morning"
        elif (date_time_start>morning) and (date_time_start<afternoon):
            timespan="Afternoon"
        else:
            timespan="Evening"
        if duration==0:
            duration=24
        
        data=pd.DataFrame({'Activity':[s],'Tag':[update],'Duration':[duration],'Part of day':[timespan],'Weekday':[date_time]}) # tag
        df2=df2.append(data)
    print(df2)
   
    
naivetagging()
#academic, Entertainment,health, miscellanous, personal, 
 #the activities in the new column, group the times into weeks, morning, afternoon and evening. 
# tag the activities, come up tags as much as we can, create a new column for tag, create new column for duration, create new column for morning/afternoon/evening

