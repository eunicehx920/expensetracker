from venmo_email_parser import Venmo_Email_Parser
from gmail import gmailService, Message, ListOfMessages
from parser import Parser
from utils.databases import PostgresConnection
import sys
import logging

from typing import List

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

Vector = List[float]

LABEL_TO_READ_VENMO = "Venmo/Venmo Completed Unprocessed"
LABEL_FOR_PROCESSED_VENMO = "Venmo/Venmo Completed Processed"
VENMO_DB_TABLE_NAME = "venmo_paid"

def main(label_to_process: str, label_processed: str, db_table: str, parser: Parser):
    # Get emails to process
    gmail_service =  gmailService()
    list_of_messages = gmail_service.get_messages(label_to_process)

    # Parsering
    parser = parser()
    processed_messages = parser.process_list_of_messages(list_of_messages)

    #Uploading
    db_connection =  PostgresConnection()
    upload_to_database(db_connection, db_table, parser.schema, processed_messages, gmail_service, label_processed, label_to_process)

    return

def upload_to_database(db_connection, table_name, table_schema, processed_messages, gmail_service, label_name_for_processed, old_label):
    logger.info("Uploading rows to database...")
    success_count = 0
    for message in processed_messages:
        values = message.get("payload")
        try:
            db_connection.insert_values_to_table(table_name, table_schema, values)
            success_count += 1
            mark_email_processed(gmail_service, message.get("email_message_id"), label_name_for_processed, old_label)
        except Exception as e:
            logging.error(e)
            continue

    logger.info("{success_count} rows uploaded to db".format(success_count=success_count))
    return

def mark_email_processed(gmail_service: gmailService, email_message_id, label_name_for_processed, old_label):
    labels_to_add = [label_name_for_processed]
    labels_to_delete = [old_label]
    gmail_service.modify_message_label(labels_to_add, labels_to_delete, email_message_id, True)
    return



if __name__ == '__main__':
    main(LABEL_TO_READ_VENMO, LABEL_FOR_PROCESSED_VENMO, VENMO_DB_TABLE_NAME, Venmo_Email_Parser)
