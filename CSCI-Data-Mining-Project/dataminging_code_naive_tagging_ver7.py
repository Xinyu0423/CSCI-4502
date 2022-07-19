#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
import math
import scipy.stats as stats
from matplotlib import dates



# In[14]:


def naivetagging():
    filepath = "datafile"
    df = pd.read_csv(filepath, header=None).dropna()
    df.dropna(how='all', axis=1)
    df.rename(columns={0:'Activity',1:'Start-time',2:'End-time',3:'Note',4:'Location',5:'Tag',6:'Duration'},inplace=True)
    
    #tags=["Meeting","Works","Sports","Leisure","Miscellaneous","School"]
    df['Tag']=np.nan
    df['Duration']=np.nan
    df2=pd.DataFrame(columns=['Activity','Tag','Duration','Part of day','Weekday','Holiday'])
    df.rename(columns={0:'Activity',1:'Start-time',2:'End-time',3:'Note',4:'Location',5:'Tag',6:'Duration'},inplace=True)
    df=df.dropna(how='all')
    
    
    df2=pd.DataFrame(columns=['Activity','Tag','Duration','Part of day','Weekday'])
    df=df.dropna(how='all')
    for i,row in df.iterrows():  # tag data each row
       
        s=str(row['Activity'])
        updatetag=activitytag(row)
        updatetag=checktags(s,updatetag)
        duration=durationtime(row)
        timespan=dayparttag(row)
        date_time=weekdaytag(row)
        holiday=holidaytag(row)
        
        data=pd.DataFrame({'Activity':[s],'Tag':[updatetag],'Duration':[duration],'Part of day':[timespan],'Weekday':[date_time],'Holiday':[holiday]}) # tag
        df2=df2.append(data)
    print(df2)
   


 #the activities in the new column, group the times into weeks, morning, afternoon and evening. 
# tag the activities, come up tags as much as we can, create a new column for tag, create new column for duration, create new column for morning/afternoon/evening


# In[15]:


def activitytag(currentrow):
    keywords=["Meet","Party","Work","Class","Movie","Tennis","Gym","Lab","HW","Due","Flight","Ceremony","School","Exam"]
    s=str(currentrow['Activity'])
    update="Miscellaneous"
    for j in range(len(keywords)):
        if (keywords[j] in s) or (keywords[j].lower() in s):
            update=str(keywords[j])
            
            
    return update


# In[16]:


def checktags(currentevent,currenttag):
    synonymoustag1=["Tennis","Yoga","Rec Center","Gym","Run"]
    synonymoustag2=["Homework","Due","Exam","CSCI","Final","Library","Campus","Class","Enrollment","Midterm","Graduate"]
    synonymoustag3=["Meet","Dinner","Lunch","Breakfast","Coffe","Visit","FEST"]
    for k in synonymoustag1:
        if (k in currentevent) or (k.lower() in currentevent):
            currenttag="Sports"
    for k2 in synonymoustag2:
        if (k2 in currentevent) or (k.lower() in currentevent):
            currenttag="Study"
    for k3 in synonymoustag3:
        if (k3 in currentevent) or (k3.lower() in currentevent):
            currenttag="Events and Meetings"
    
    return currenttag


# In[17]:


def durationtime(currentrow):
    
    duration="Unkown"
    st=currentrow['Start-time'].split('+')
    et=currentrow['End-time'].split('+')
    st2=st[0].split(' ')
    et2=et[0].split(' ')
    if len(st2)>1:
        s1=st2[1]
        date_time_start = datetime.datetime.strptime(s1[:7], "%H:%M:%S")
    else:
        return duration
    if len(et2)>1:
        s2=et2[1]
        date_time_end=datetime.datetime.strptime(s2[:7],"%H:%M:%S")
    else:
        return duration
    duration=date_time_end-date_time_start
    
    return duration


# In[18]:


def dayparttag(currentrow):
    timespan="Unknown"
    st=currentrow['Start-time'].split('+')
    st2=st[0].split(' ')
    if len(st2)>1:
        s1=st2[1]
        date_time_start = datetime.datetime.strptime(s1[:7], "%H:%M:%S")
    else:
        date_time_start=datetime.datetime.strptime("00:00:00","%H:%M:%S")
    morning=datetime.datetime.strptime("12:00:00","%H:%M:%S")
    afternoon=datetime.datetime.strptime("18:00:00","%H:%M:%S")
        
    if date_time_start<morning:
        timespan="Morning"
    elif (date_time_start>morning) and (date_time_start<afternoon):
        timespan="Afternoon"
    else:
        timespan="Evening"
    return timespan


# In[19]:


def weekdaytag(currentrow):
    st=currentrow['Start-time'].split('+')
    st2=st[0].split(' ')
    dt=st2[0]
    year,month,day=(int(x) for x in dt.split('-'))
    date_time=datetime.date(year,month,day).weekday()
    return date_time


# In[29]:


def holidaytag(currentrow):
    
    holiday="Not"
    winterbreakstart=datetime.datetime(2019,12,20)
    winterbreakend=datetime.datetime(2019,1,14)
    springbreakstart=datetime.datetime(2019,3,25)
    springbreakend=datetime.datetime(2019,4,10)
    summerbreakstart=datetime.datetime(2019,5,18)
    summerbreakend=datetime.datetime(2019,8,28)
    fallbreakstart=datetime.datetime(2019,11,20)
    fallbreakend=datetime.datetime(2019,12,2)
    st=currentrow['Start-time'].split(' ')
    date_time=datetime.datetime.strptime(st[0],"%Y-%M-%d")
    if (date_time<=winterbreakend) or (date_time>=winterbreakstart):
        holiday="Yes"
    elif (date_time>=springbreakstart) and (date_time<=springbreakend):
        holiday="Yes"
    elif (date_time>=summerbreakstart) and (date_time<=summerbreakend):
        holiday="Yes"
    elif (date_time>=fallbreakstart) and (date_time<=fallbreakend):
        holiday="Yes"
    return holiday


# In[30]:


naivetagging()


# In[ ]:




