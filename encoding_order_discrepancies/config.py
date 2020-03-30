import os
from dotenv import load_dotenv

load_dotenv('.env')
SNOWFLAKE_USER_NAME = os.environ.get('SNOWFLAKE_USER_NAME')
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_CHANNEL_NAME = os.environ.get('SLACK_CHANNEL_NAME')
BOT_NAME = os.environ.get('BOT_NAME')
