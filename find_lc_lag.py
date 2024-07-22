#!/usr/bin/env python3
''' 
This program calculates:
 Files that lagging more than 1 hour
 Percentage of upload to s3.
 Missing files.
Copyright IBM 2024
Written by Andrew Lee
'''
import csv
import  time
import requests
def find_24(date1,date2):
    temp=date1.split()
    if len(temp[1][0:2]) == 3:
        new_date=int(temp[1][0:2])
    else:
        new_date=int(temp[1][0:1])
    temp=date2.split('-')
    new_date2=int(temp[2])
    day_delay=new_date-new_date2
    return((day_delay)*24)

def find_lag(data):
    d,h,m,date_ch,chat,store=data
    b=(h.split(':'))
    b=int(b[0]) # hour
    m=int(m)/60 #convert minute to decimal
    time1=b+m
    t=chat.split('-')
    temp=t[0].split(':')
    temp_hour=int(temp[0])
    temp_min=int(temp[1])/60
    time2=temp_hour+temp_min
    
    x=find_24(d,date_ch)
    delay=round(time1-time2,3)+x
    
    return(delay)
def find_mqtt():
    with open('/Users/andrewlee/Downloads/CMS,-MQTT,-and-RAW-Audio.csv','r',newline='') as f:
        reader=csv.reader(f)
        for record in reader:
            if 'Timestamp' in record[0]:
                pass
            else:
                if record[3] != '5':
                    print(record)

def find_percentage():
    with open('/Users/andrewlee/Downloads/Total-Files-upload.csv','r',newline='') as f:
        print()
        reader=csv.reader(f)
        for record in reader:
            if 'Timestamp' in record[0]:
                pass
            else:
                if record[4] != '' and float(record[3]) != 0:
                    x=float(record[2])/float(record[3])
                    #print(record)
                    
                    if x <= 0.9 and x > 0.0:
                        
                        print(record,'--->x=',x)
                    

def main():
    with open('/Users/andrewlee/Downloads/is-there-delay-uploading_.csv','r',newline='') as f:
        reader=csv.reader(f)
        for record in reader:
            
            if 'Timestamp' in record[0]:
                pass
            else:
                #print(record)
                delay=find_lag(record)
                record.append(delay)
                if delay > 1.0:    #print anything more than 1 hour lag
                    print(record[5:]) 


            
if __name__=='__main__':
    main()
    find_mqtt()
    find_percentage()







    
