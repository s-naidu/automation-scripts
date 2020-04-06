import os
from dotenv import load_dotenv

load_dotenv('.env')
DATABASE_HOSTNAME = os.environ.get('DATABASE_HOSTNAME')
DATABASE_USER_NAME = os.environ.get('DATABASE_USER_NAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE = os.environ.get('DATABASE')
TICKET_NO = os.environ.get('TICKET_NO')
