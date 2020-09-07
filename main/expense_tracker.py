from venmo_email_parser import Venmo_Email_Processor
from gmail import gmailService, Message, ListOfMessages
from processor import Processor
import sys
import logging

from typing import List

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

Vector = List[float]

LABEL_TO_READ_VENMO = "Venmo/Venmo Completed Unprocessed"

def main(label: str, processor: Processor):
    gmail_service =  gmailService()
    label_id = gmail_service.get_label_id(label)
    list_of_messages = gmail_service.get_messages(label_id)
    processor = processor()
    processed_messages = processor.process_list_of_messages(list_of_messages)
    upload_to_database(processed_messages)
    return

def upload_to_database(list_of_messages: ListOfMessages):
    pass

if __name__ == '__main__':
    main(LABEL_TO_READ_VENMO, Venmo_Email_Processor)
