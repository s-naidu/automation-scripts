from datetime import timedelta, date
from snowflake.connector import DictCursor
import config
import connection
import requests
import json


def query(yesterday, today, db_connection):
    """
    Query the database to find discrepancies
    """
    cursor = db_connection.cursor(DictCursor)
    query = """SELECT encoding_order.entry_date, xy.*
    FROM (
        SELECT encoding_order.encoding_order_id,
            COUNT(DISTINCT encoding_order_detail.upc) AS eo_upcs_count,
            COUNT(DISTINCT encoding_queue_detail.upc) AS eq_upcs_count
        FROM orchard_app_reporting.art_relations.encoding_order
        INNER JOIN orchard_app_reporting.art_relations.encoding_order_detail
            ON encoding_order_detail.encoding_order_id =
                encoding_order.encoding_order_id
        INNER JOIN orchard_app_reporting.direct_delivery.encoding_queue
            ON encoding_queue.encoding_order_id =
                encoding_order.encoding_order_id
        INNER JOIN orchard_app_reporting.direct_delivery.encoding_queue_detail
            ON encoding_queue_detail.encoding_queue_id =
                encoding_queue.encoding_queue_id
        WHERE encoding_order.order_status = 'close'
            AND encoding_order.processed = 'Y'
            AND encoding_order.entry_date BETWEEN'{}' AND '{}'
        GROUP BY encoding_order.encoding_order_id
    ) AS xy
    INNER JOIN orchard_app_reporting.art_relations.encoding_order
        ON encoding_order.encoding_order_id =
            xy.encoding_order_id
    WHERE xy.eo_upcs_count <> xy.eq_upcs_count
    ORDER BY 2 """.format(yesterday, today)
    cursor.execute(query)
    send_message(cursor)


def send_message(cursor):
    """
    Send message to slack channel if any discrepancy is found
    """
    msg = ''
    for row in cursor:
        msg = 'Info: {encoding_order_detail_total: '
        + str(row['EO_UPCS_COUNT'])
        + ', encoding_queue_detail_total: '
        + str(row['EQ_UPCS_COUNT']) + '}'
        slack_msg = {
            'username': config.BOT_NAME,
            'channel': config.SLACK_CHANNEL_NAME,
            'attachments': [
                {
                    'fallback': 'Encoding Order Discrepancies found',
                    'color': '#DC143C',
                    'title': 'Discrepencies in encoding order ID - {}'
                        .format(row['ENCODING_ORDER_ID']),
                    'text': msg
                }
            ]
        }
        requests.post(config.SLACK_WEBHOOK_URL, data=json.dumps(slack_msg))


def main():
    today = date.today()
    yesterday = (today - timedelta(1))
    db_connection = connection.snowflake_connection()
    query(yesterday, today, db_connection)


if __name__ == '__main__':
    main()
