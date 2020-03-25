import snowflake.connector 
import config
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

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
