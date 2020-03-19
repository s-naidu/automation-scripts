import os
from dotenv import load_dotenv

load_dotenv('.env')
SNOWFLAKE_PASSPHRASE = os.environ.get('SNOWFLAKE_PASSPHRASE')
SNOWFLAKE_USER_NAME = os.environ.get('SNOWFLAKE_USER_NAME')
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE')
