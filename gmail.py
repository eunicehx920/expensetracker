from google_services import get_gmail_service
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class gmailService:
    def __init__(self):
        self.service = get_gmail_service()

    def get_label_id(label_name) -> str:
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


    def get_messages(label_id):
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
        while results:
            messages = messages + results.get('messages')
            if results.get('nextPageToken'):
                results = self.service.users().messages().list(userId='me', labelIds=label_id, pageToken=next_page)
            else:
                results = None
        return messages


if __name__ == '__main__':
    label_id = get_label_id(LABEL_TO_READ)
    get_messages(label_id)