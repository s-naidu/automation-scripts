from datetime import timedelta, date
import requests
import json
import snowflake.connector 
import pandas as pd
import os
import config
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def get_file():
    cd = os.getcwd()
    files = os.listdir(cd)
    path = ""
    for file in files:
        if (file.lower().endswith(".p8")):
            path = file
            break
    return path

def connection(path):
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

    db_connection = snowflake.connector.connect( 
        user=config.SNOWFLAKE_USER_NAME, 
        account=config.SNOWFLAKE_ACCOUNT, 
        private_key=private_key, 
        database=config.SNOWFLAKE_DATABASE, 
        schema=config.SNOWFLAKE_SCHEMA, 
        warehouse=config.SNOWFLAKE_WAREHOUSE, 
        role=config.SNOWFLAKE_ROLE
        )
    return db_connection

def query(yesterday, today, db_connection):
    db_data = pd.read_sql_query(f"""SELECT encoding_order.entry_date, xy.* 
    FROM (
        SELECT encoding_order.encoding_order_id,
            COUNT(DISTINCT encoding_order_detail.upc) AS eo_upcs_count, 
            COUNT(DISTINCT encoding_queue_detail.upc) AS eq_upcs_count
        FROM orchard_app_reporting.art_relations.encoding_order
        INNER JOIN orchard_app_reporting.art_relations.encoding_order_detail 
            ON encoding_order_detail.encoding_order_id = encoding_order.encoding_order_id
        INNER JOIN orchard_app_reporting.direct_delivery.encoding_queue 
            ON encoding_queue.encoding_order_id = encoding_order.encoding_order_id
        INNER JOIN orchard_app_reporting.direct_delivery.encoding_queue_detail
            ON encoding_queue_detail.encoding_queue_id = encoding_queue.encoding_queue_id
        WHERE encoding_order.order_status = 'close' AND encoding_order.processed = 'Y'
            AND encoding_order.entry_date BETWEEN '{yesterday}' AND '{today}'
        GROUP BY encoding_order.encoding_order_id
    ) AS xy
    INNER JOIN orchard_app_reporting.art_relations.encoding_order 
        ON encoding_order.encoding_order_id = xy.encoding_order_id
    WHERE xy.eo_upcs_count <> xy.eq_upcs_count
    ORDER BY 2
    LIMIT 100""", db_connection)
    message(db_data)

def message(db_data):
    for index, row in db_data.iterrows():
        i = row['ENCODING_ORDER_ID']
        eo_count = row['EO_UPCS_COUNT']
        eq_count = row['EQ_UPCS_COUNT']
        web_hook = config.SLACK_WEBHOOK_URL
        slack_msg = { "username" : "#distro-incomplete-encoding-orders", 
        "channel" : config.SLACK_CHANNEL_NAME, 
        "attachments" : [
            { "fallback" : "Encoding Order Discrepancies found", 
            "color" : "danger", 
            "fields" : [
                { "title" : "Discrepencies in encoding order ID - " + str(i), 
                "value" : "Info : {encoding_order_detail_total : " + str(eo_count) + ", encoding_queue_detail_total : " + str(eq_count) + " }"
                            }
                        ]
                    }
                ]
        }
        requests.post(web_hook, data=json.dumps(slack_msg))

def main():
    today = date.today()
    yesterday = (today - timedelta(1))
    path = get_file() 
    db_connection = connection(path)
    query(yesterday, today, db_connection)

if __name__ == '__main__':
    main()
