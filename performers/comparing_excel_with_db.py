import pandas as pd
from sqlalchemy import types,create_engine


performers=int(input("enter no of performers"))
csv=pd.read_excel("path",header=1,encoding='latin1')

csv['Performer Type'].replace({"Primary Performer":"primary","Featured Performer":"featured","Non Featured Performer":"non-featured"},inplace=True)
csv_data=csv.sort_values(by=['Track ID'])

#creating list of track id in csv
new_columns=[]
for item in csv_data.columns:
    counter=0
    newitem=item
    while newitem in new_columns:
        counter+=1
        newitem="{}_{}".format(item,counter)
    new_columns.append(newitem)
csv_data.columns=new_columns

csv_data.columns=csv_data.columns.str.replace(" ","_")
csv_data.columns=csv_data.columns.str.replace(".","_")

#creating list of track id in csv
track=tuple(csv_data['Track_ID'])

engine=create_engine('mysql+mysqlconnector://db_username:db_password@hostname:3306/database',echo=False)
data_role=pd.read_sql_query('SELECT performer_role, performer_role_id FROM performer_role',engine)
database_data=pd.read_sql_query("select birth_name,performer_role_id,unique_track_id,performer_type from performer where unique_track_id in "+str(track),engine)
    
database_list=list()
csv_list=list()

for  i in track:
    csv_list=list()
    database_list=list()
    new_csv=csv_data.loc[csv_data['Track_ID']==i]
    new_db=database_data.loc[database_data['unique_track_id']==i]
        
    for j in range(0,performers):
        if j==0:
            performer_type=new_csv['Performer_Type'].values[0]
            performer_name=new_csv['Performer_Legal/Birth_Name'].values[0]
            performer_role=new_csv['Performer_Role'].values[0]
            csv_list.append(i)
        else:
            new_csv['Performer_Type_'+str(j)].replace({"Primary Performer":"primary","Featured Performer":"featured","Non Featured Performer":"non-featured"},inplace=True)
            performer_type=new_csv['Performer_Type_'+str(j)].values[0]
            performer_name=new_csv['Performer_Legal/Birth_Name_'+str(j)].values[0]
            performer_role=new_csv['Performer_Role'].values[0]
        if isinstance(performer_name,str):
            performer_name=performer_name.strip()
        if (pd.notnull(performer_name) and performer_name != ''):
            if performer_name not in csv_list:
                
                csv_list.append(performer_type)
                csv_list.append(performer_name)
                csv_list.append(performer_role)
    
    database_list.append(i)
    for index,row in new_db.iterrows():
        temp=row['performer_role_id']
        new_role_db=data_role.loc[data_role['performer_role_id']==temp]
        db_performer_role=new_role_db['performer_role'].values[0]
        
        db_performer_type=row['performer_type']
        
        db_performer_name=row['birth_name']
        
        if isinstance(db_performer_name,str):
            db_performer_name=db_performer_name.strip()
        if db_performer_name not in database_list and db_performer_role not in database_list:
            database_list.append(db_performer_type)
            database_list.append(db_performer_name)
            database_list.append(db_performer_role)
    
    for ind in csv_list:
        if ind in database_list:
            pass
        else:
            print(f"value {ind} missing in database for track id {i}")

           
        
