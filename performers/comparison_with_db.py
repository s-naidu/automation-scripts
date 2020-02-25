import pandas as pd
import mysql.connector

from sqlalchemy import types,create_engine


def connection():
    engine=create_engine('mysql+mysqlconnector://asingh:*ABnR*Me*B9LbetYaM@qa-ows-track.cluster-cb22xqmk0y0q.us-east-1.rds.amazonaws.com:3306/ows_track',echo=False)
    data_new=pd.read_sql_query("select birth_name,unique_track_id,performer_type from performer where unique_track_id in "+str(track),engine)
    return data_new

csv=pd.read_csv("DISTRO-2357.csv",usecols=['Track ID','Performer Legal/Birth Name','Performer Role'])
csv_data=csv.sort_values(by=['Track ID'])
track=tuple(csv_data['Track ID'])
database_data=connection()
for i in track:
    new_db=database_data.loc[database_data['unique_track_id']==i]
    new_csv=csv_data.loc[csv_data['Track ID']==i]
    if new_csv['Performer Legal/Birth Name'].values[0]==new_db['birth_name'].values[0]:
       pass
    else:
        print(f"failed at track id {i} ")
        print(f"value in csv:-- {new_csv['Performer Legal/Birth Name'].values[0]} value in db :-- {new_db['birth_name'].values[0]} ")
print("end")
