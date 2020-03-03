import pandas as pd
from sqlalchemy import create_engine
import os
#Get current working directory
cd=os.getcwd()
#Get the list of files in this directory
files=os.listdir(cd)
path=""

#find file with .csv extension
for f in files:
    if (f.lower().endswith(".csv")):
        path=f
        break

performers=int(input("enter no of performers "))

if performers==1:
    n=0
elif performers>1:
    n=1
    
#read the csv/excel file as pandas dataframe
csv=pd.read_csv(path,header=n,encoding='utf-8')
#sort the dataframe according to track id
csv_data=csv.sort_values(by=['Track ID'])

#used to name the columns continues like Performer_Name_1,Performer_Name_2 for multiple performers
new_columns=[]
for item in csv_data.columns:
    counter=0
    newitem=item
    while newitem in new_columns:
        counter+=1
        newitem="{}_{}".format(item,counter)
    new_columns.append(newitem)
csv_data.columns=new_columns

#replace empty spaces and '.' from column name 
csv_data.columns=csv_data.columns.str.replace(" ","_")
csv_data.columns=csv_data.columns.str.replace(".","_")

#create a list of track id's
track=csv_data['Track_ID']

#create the connection engine
engine=create_engine('mysql+mysqlconnector://db_username:db_password@db_hostname:3306/database_name',echo=False)

#read the database data as pandas dataframe
database_data=pd.read_sql_query("select birth_name,performer_role_id,unique_track_id,performer_type from performer where unique_track_id in "+str(tuple(track)),engine)

missmatch_tracks=list()
empty_tracks=list()

#iterate each track id inside the track list
for  i in track:
    csv_list=list()
    database_list=list()
    #create new dataframe which has track id equal to current track id
    new_csv=csv_data.loc[csv_data['Track_ID']==i]
    new_db=database_data.loc[database_data['unique_track_id']==i]
    #iterate each performer data
    for j in range(0,performers):
        if j==0:
            #first performer
            #get the performer_birth_name from the dataframe
            performer_name=new_csv['Performer_Legal/Birth_Name'].values[0]
            
            #checks whether the performer_name is of string type or not
            if isinstance(performer_name,str):
                #strip is used to remove empty spaces from front and the end 
                performer_name=performer_name.strip()
                #append the name to the list
                csv_list.append(performer_name)
        else:
            #for every other performer
            performer_name=new_csv['Performer_Legal/Birth_Name_'+str(j)].values[0]
            if isinstance(performer_name,str):
                performer_name=performer_name.strip()
                if (pd.notnull(performer_name) and performer_name != ''):
                    csv_list.append(performer_name)
                
    #iterate the rows in dataframe which contain database values        
    for index,row in new_db.iterrows():
        if new_db.empty==False:
            #get the birth_name
            db_performer_name=row['birth_name']        
            if isinstance(db_performer_name,str):
                db_performer_name=db_performer_name.strip()
                #check whether name is empty or not
                if db_performer_name !='':
                    #append to the database_list
                    database_list.append(db_performer_name)
                else:
                    pass
                
    count=0
    #check whether database_list is empty or not
    if database_list !=[]:
        #iterate each element inside csv_list
        for ind in csv_list:
            #each element inside database list
            for db in database_list:
                #compare the single value from csv_list with all the values inside database_list
                if ind==db :
                    count=1
                    #break the loop as soon as it finds a match
                    break
                else:
                    count=-1
            if count ==-1:
                #break the loop if even a single value from csv_list doesn't match any value inside database_list after iterating the whole database_list
                    break
                    
    elif database_list==[]:
        #if database_list is empty append the track id to a list
        empty_tracks.append(i)
        
    if count==1:
        pass  
    elif count==-1:
        #if missmatch occurs append the track id to a list
        missmatch_tracks.append(i)
        
print(f"missmatched tracks:- \n")
print(len(missmatch_tracks))
if missmatch_tracks!=[]:
    #create a new dataframe from the list of missmatch values and export that dataframe to a excel file
    df=pd.DataFrame()
    df['missmatched_tracks']= missmatch_tracks[0:]
    df.to_excel('result_missmatch.xlsx',index=False)
print("****************************************")
print("empty-tracks:- \n")
print(len(empty_tracks))
if empty_tracks!=[]:
    #create a new dataframe from the list of empty values and export that dataframe to a excel file
    df1=pd.DataFrame()
    df1['empty_tracks']= empty_tracks[0:]
    df1.to_excel('result_empty.xlsx',index=False)
print("done")
