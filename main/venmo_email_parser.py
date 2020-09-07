from processor import Processor
import sys
import re
import base64
import logging
from typing import List, Dict

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

class Venmo_Email_Processor(Processor):

    def process_list_of_messages(self, list_of_messages):
        processed_messages = []

        for messages in list_of_messages:
            snippet = messages.get("snippet")
            matches = self.process_message_snippet(snippet)
            processed_message_info = dict

            if matches:
                processed_message_info = {
                    "charger" : matches.group(1),
                    "item" : matches.group(2),
                    "date" : matches.group(3),
                    "amount" : matches.group(4),
                    "payment_method" : self.clean_payment_method(matches.group(5))
                     }
                processed_messages.append(processed_message_info)
            else:
                logger.error("Could not match message to regex. Message: {message}".format(message=snippet))
                continue
            
        logger.info("{len_msgs} messages processed".format(len_msgs=len(processed_messages)))

        return processed_messages

    def process_message_snippet(self, email_snippet: str):
    # """
    # Fang Shuo Deng charged You Towels Transfer Date and Amount: Jun 06, 2020 PDT · - $4.46 Like Comment Completed via your Venmo balance. Payment ID: 3025969980949660524 Invite Friends! For any issues,
    # Lim Mingjun charged You Lyft from SF Transfer Date and Amount: Jun 06, 2020 PDT · - $31.00 Like Comment Completed via a bank transfer from your Bank Of
    #  """
        regex_pattern_main = "^(.*) charged You (.*) Transfer Date and Amount: (.*) PDT · - \$(.*) Like Comment Completed via (.*)"
        m = re.search(regex_pattern_main, email_snippet)
        return (m)

    def clean_payment_method(self, payment_method_str: str):
        regex_pattern = "Venmo balance"
        m = re.search(regex_pattern, payment_method_str)
        if m:
            return "venmo balance"
        else:
            return "bank transfer"




    


if __name__ == '__main__':
    list_of_messages = [{'id': '1743eb41ba6f1d5a', 'threadId': '1743eb41ba6f1d5a'}]
    processor = Venmo_Email_Processor()
    processor.process_list_of_messages(list_of_messages)