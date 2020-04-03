import pymysql
import config


def database_connection():
    db_connection = pymysql.connect(
        host=config.DATABASE_HOSTNAME,
        user=config.DATABASE_USER_NAME,
        password=config.DATABASE_PASSWORD,
        db=config.DATABASE
    )
    return db_connection
