from utils.google_services import get_gmail_service
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


    def get_messages(self, label_name: str) -> ListOfMessages:
        """Gets list of messages given label id

            Args:
                label_id: str of label id
            Returns:
                list of messages
            Raises:
            ValueError: If no such label is found
        """
        label_id = self.get_label_id(label_name)
        results = self.service.users().messages().list(userId='me', labelIds=label_id).execute()
        messages = []
        logger.info("Retrieving messages with label {label_name}...".format(label_name=label_name))
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

    def modify_message_label(self, labels_to_add: List, labels_to_delete: List, message_id: str, convert_to_label_id: bool) -> Dict:
        """
            Modifies the labels of a message

            Args:
                label_name: full name of label. If label has a parent label, the full name is <parent_label>/<label>
            Returns:
                None
            Raises:
            ValueError: If no such label is found

        """
        if convert_to_label_id:
            add_label_ids = []
            remove_label_ids = []
            for label_a in labels_to_add:
                add_label_ids.append(self.get_label_id(label_a))
            for label_d in labels_to_delete:
                remove_label_ids.append(self.get_label_id(label_d)) 
        else:
            add_label_ids = labels_to_add
            remove_label_ids = labels_to_delete

        request_body = {
            "addLabelIds" : add_label_ids,
            "removeLabelIds" : remove_label_ids
        }
        
        results = self.service.users().messages().modify(userId='me', id=message_id, body=request_body).execute()
                    
        return