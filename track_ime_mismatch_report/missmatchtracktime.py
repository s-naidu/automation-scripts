import pandas as pd
import config
import os
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

#Find the key inside the directory 
cd=os.getcwd()
files=os.listdir(cd)
path=""
for f in files:
    if (f.lower().endswith(".p8")):
        path=f
        break
   
SNOWFLAKE_PRIVATE_KEY_PATH = path
SNOWFLAKE_KEY_PASSPHRASE = config.SNOWFLAKE_PASSPHRASE
if SNOWFLAKE_KEY_PASSPHRASE:
    if not SNOWFLAKE_PRIVATE_KEY_PATH:
        print('SNOWFLAKE_PRIVATE_KEY_PATH missing')
    with open(SNOWFLAKE_PRIVATE_KEY_PATH, 'rb') as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            password=SNOWFLAKE_KEY_PASSPHRASE.encode(),
            backend=default_backend()
        )
    private_key = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
else:
    private_key = None

#Connect to snowflake
ctx = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER_NAME,
        account=config.SNOWFLAKE_ACCOUNT,
        private_key=private_key,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        role=config.SNOWFLAKE_ROLE
        )

#Find the excel file inside diectory
cd=os.getcwd()
files=os.listdir(cd)
path_excel=""
for f in files:
    if (f.lower().endswith(".xlsx")):
        path_excel=f
        break

#Read the excel 
excel=pd.read_excel(path_excel,header=0)
#Get the list of upc 
l1 = excel['Upc']
tracks=[]
#Remove duplicate upc's
for i in l1:
    if i not in tracks:
        tracks.append(i)
        
#Read query and get data in a dataframe
data=pd.read_sql_query(f"""SELECT r.upc, t.track_id, t.cd
        FROM ART_RELATIONS.RELEASES r
        INNER JOIN ART_RELATIONS.ARTIST_INFO ai ON ai.artist_id = r.artist_id
        AND r.not_for_distribution = 'N'
        INNER JOIN ART_RELATIONS.VENDOR v ON v.vendor_id = ai.vendor_id
        INNER JOIN ART_RELATIONS.TRACK t ON t.upc = r.upc
        INNER JOIN (
            DIRECT_DELIVERY.ASSET a
            INNER JOIN DIRECT_DELIVERY.ASSET_LOCATION aloc
                ON aloc.asset_id = a.asset_id
            INNER JOIN DIRECT_DELIVERY.ASSET_LOCATION_DETAIL ald
                ON ald.asset_location_id = aloc.asset_location_id
            INNER JOIN DIRECT_DELIVERY.STORAGE_DRIVE sd
                ON sd.storage_drive_id = aloc.storage_drive_id
            INNER JOIN DIRECT_DELIVERY.STORAGE s
                ON s.storage_id = sd.storage_id AND s.physical_location_id = 1
        ) ON a.upc = r.upc
            AND ald.filename =
                  CONCAT(CONCAT(CONCAT(CONCAT(CONCAT(t.upc,'_'),t.cd),'_'),t.track_id),'.wav')
            AND a.asset_type_id = 1
        WHERE
            (
                (
                    COALESCE(t.length_minute, 0) * 60
                ) + COALESCE(t.length_seconds, 0) = 0
                OR COALESCE(ald.duration, 0) = 0
                OR
                (
                    ABS(
                        (
                            (
                                COALESCE(t.length_minute, 0) * 60
                            ) + COALESCE(t.length_seconds, 0)
                        ) - COALESCE(ald.duration, 0)
                    ) > 10
                )
            )
            AND r.release_status = 'in_content'
            AND r.deletions <> 'Y'
            AND v.vendor_id NOT IN (7123, 25824,16055)
            AND r.upc in {str(tuple(tracks))}
        GROUP BY r.upc, r.release_status, v.owner, v.vendor_id,
            t.length_minute,t.length_seconds, ald.duration, t.track_id, t.cd
        ORDER BY r.upc""",ctx)

if data.empty==False:
#Convert the dataframe result to a csv file
    data.to_csv("result.csv",index=False)
