
def get_message(message_id):
    message = self.service.users().messages().get(ids=message_id).execute()
