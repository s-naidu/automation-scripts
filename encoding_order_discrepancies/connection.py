import snowflake.connector
import config


def snowflake_connection():
    db_connection = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER_NAME,
        password=config.SNOWFLAKE_PASSWORD,
        account=config.SNOWFLAKE_ACCOUNT,
        database=config.SNOWFLAKE_DATABASE
    )
    return db_connection
