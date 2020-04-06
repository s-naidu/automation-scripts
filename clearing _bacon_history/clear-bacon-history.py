import connection
import sys
import config


def get_data():
    arg = sys.argv
    youtube_id_list = arg[1].split(',')
    return youtube_id_list


def execute_query(db_connection, youtube_id_list):
    cursor = db_connection.cursor()
    sql_create = """CREATE TABLE `ROLLBACK-DISTRO-{}_youtube_channel_video_status` AS
    SELECT * FROM youtube_channel_video_status
    WHERE youtube_video_id IN {}
    """.format(config.TICKET_NO, tuple(youtube_id_list))
    cursor.execute(sql_create)

    sql_delete = """DELETE yt.* FROM youtube_channel_video_status yt
    INNER JOIN `ROLLBACK-DISTRO-{}_youtube_channel_video_status`
    rp2829
        ON rp2829.youtube_video_id = yt.youtube_video_id
        """.format(config.TICKET_NO)
    cursor.execute(sql_delete)
    db_connection.commit()
    db_connection.close()


def main():
    youtube_id_list = get_data()
    db_connection = connection.database_connection()
    execute_query(db_connection, youtube_id_list)


if __name__ == '__main__':
    main()
