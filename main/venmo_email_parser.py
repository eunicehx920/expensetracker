from parser import Parser
import sys
import re
import base64
import logging
from typing import List, Dict

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

class Venmo_Email_Parser(Parser):

    def __init__(self):
        self.schema = {
            "charger": "VARCHAR",
            "item" : "VARCHAR",
            "date" : "TIMESTAMP",
            "amount": "NUMERIC",
            "payment_method": "VARCHAR"
        }

    def process_list_of_messages(self, list_of_messages):
        logger.info("Parsering messages...")
        processed_messages = []

        for message in list_of_messages:
            snippet = message.get("snippet")
            matches = self.process_message_snippet(snippet)
            processed_message_info = []

            if matches:
                # For clarity of code reading, a dictionary representation would make more sense:
                # processed_message_info = {
                #     "charger" : matches.group(1),
                #     "item" : matches.group(2),
                #     "date" : matches.group(3),
                #     "amount" : matches.group(4),
                #     "payment_method" : self.clean_payment_method(matches.group(5))
                #     "message_id" : message_id
                #      }

                # message info is saved as a list so that it is easy to insert into postgres table.      
                processed_message_info = [matches.group(1),matches.group(2),matches.group(3),matches.group(4), self.clean_payment_method(matches.group(5))]     
                processed_message_result = {
                    "payload" : processed_message_info,
                    "email_message_id" : message.get("id")
                }
                processed_messages.append(processed_message_result)
            else:
                logger.error("Could not match message to regex. Message: {message}".format(message=snippet))
                continue
            
        logger.info("{len_msgs} messages parsed".format(len_msgs=len(processed_messages)))

        return processed_messages

    def process_message_snippet(self, email_snippet: str):
    # """
    # Fang Shuo Deng charged You Towels Transfer Date and Amount: Jun 06, 2020 PDT · - $4.46 Like Comment Completed via your Venmo balance. Payment ID: 3025969980949660524 Invite Friends! For any issues,
    # Lim Mingjun charged You Lyft from SF Transfer Date and Amount: Jun 06, 2020 PDT · - $31.00 Like Comment Completed via a bank transfer from your Bank Of
    #  """
        regex_pattern_main = "^(.*) charged You (.*) Transfer Date and Amount: (.*) P[SD]T · - \$(.*) Like Comment Completed via (.*)"
        m = re.search(regex_pattern_main, email_snippet)
        return (m)

    def clean_payment_method(self, payment_method_str: str):
        regex_pattern = "Venmo balance"
        m = re.search(regex_pattern, payment_method_str)
        if m:
            return "venmo balance"
        else:
            return "bank transfer"
