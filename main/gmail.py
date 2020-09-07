from google_services import get_gmail_service
import logging
import sys
from typing import List, Dict

Message = Dict[str, str]
MessageContent = Dict[str, str]
ListOfMessages = List[Message]
ListOfMessageContent = List[MessageContent]

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

class gmailService:
    def __init__(self):
        self.service = get_gmail_service()

    def get_label_id(self, label_name: str) -> str:
        """
            Gets label id given label name

            Args:
                label_name: full name of label. If label has a parent label, the full name is <parent_label>/<label>
            Returns:
                str of label id
            Raises:
            ValueError: If no such label is found

        """

        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
            raise ValueError
        else:
            for label in labels:
                if label['name']==label_name:
                    label_id_to_read = label['id']
        
        if not label_id_to_read:
            print ("Given label name not found")
            raise ValueError
                    
        return label_id_to_read


    def get_messages(self, label_id: str) -> ListOfMessages:
        """Gets list of messages given label id

            Args:
                label_id: str of label id
            Returns:
                list of messages
            Raises:
            ValueError: If no such label is found
        """
        results = self.service.users().messages().list(userId='me', labelIds=label_id).execute()
        messages = []
        logger.info("Retrieving messages with label id: {label_id}...".format(label_id=label_id))
        while results:
            for msg in results.get('messages'):
                msg_id = msg.get('id')
                msg_content = self.service.users().messages().get(userId='me', id=msg_id).execute()
                messages.append(msg_content)
            if results.get('nextPageToken'):
                results = self.service.users().messages().list(userId='me', labelIds=label_id, pageToken=next_page)
            else:
                results = None
        logger.info("{len_msgs} messages retrieved".format(len_msgs=len(messages)))
        return messages



if __name__ == '__main__':
    label_id = get_label_id(LABEL_TO_READ)
    get_messages(label_id)