from processor import Processor

class Venmo_Email_Processor(Processor):

    def process_list_of_messages(self, list_of_messages):
        for messages in list_of_messages:
            print (messages.get("header"))
        return list_of_messages



if __name__ == '__main__':
    list_of_messages = [{'id': '1743eb41ba6f1d5a', 'threadId': '1743eb41ba6f1d5a'}]
    processor = Venmo_Email_Processor()
    Venmo_Email_Processor.process_list_of_messages(list_of_messages)