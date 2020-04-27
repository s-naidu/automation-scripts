import connection
import argparse
import sys
import logging


log = logging.getLogger('main')
log.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(fmt)
log.addHandler(sh)


def get_data():
    log.info('Running script to clear bacon history')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'youtube_video_id', nargs='+', help='please enter youtube_video_id'
    )
    args = parser.parse_args()
    return args.youtube_video_id


def execute_query(db_connection, youtube_id_list):
    cursor = db_connection.cursor()
    ids_string = ','.join('"{}"'.format(i) for i in youtube_id_list)
    log.info('argument is %s' % ids_string)
    sql_delete = """DELETE FROM youtube_channel_video_status
    WHERE youtube_video_id IN ({})""".format(ids_string)
    cursor.execute(sql_delete)
    db_connection.commit()
    log.info('records deleted: %s' % cursor.rowcount)
    db_connection.close()


def main():
    youtube_id_list = get_data()
    db_connection = connection.database_connection()
    execute_query(db_connection, youtube_id_list)


if __name__ == '__main__':
    main()
