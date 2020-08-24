from venmo_email_parser import process_messages
from gmail import gmailService
LABEL_TO_READ = "Venmo/Venmo Completed Unprocessed"

def main():
    return

if __name__ == '__main__':
    gmail_service = 
    label_id = get_label_id(LABEL_TO_READ)
    list_of_messages = get_messages(label_id)
    processed_messages = process_messages(list_of_messages)
    upload_to_database(processed_messages)