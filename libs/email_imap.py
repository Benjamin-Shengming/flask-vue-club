#!/usr/bin/python

import email
from imapclient import IMAPClient

class EmailClientIMAP():
    '''
    This class is used to find/check emails on server through imap protocol
    '''
    def __init__(self, 
                 host,
                 port,
                 user,
                 passwd,
                 ssl=True):
        self.imap_server = IMAPClient(host=host,
                                      port=port,
                                      use_uid=True,
                                      ssl=ssl,
                                      stream=False,
                                      ssl_context=None,
                                      timeout=10)
        self.imap_server.login(user, passwd)

    def select_folder(self, folder_name):
        self.imap_server.select_folder(folder_name)

    # return id sequence of messages    
    def search(self, criteria='ALL', charset=None):
        return self.imap_server.search(criteria, charset)

    # get emails by id sequence
    def fetch(self, id_sequence):
        response = self.imap_server.fetch(id_sequence, ['RFC822'])        
        print(type(response))
        email_list = []
        for key, values in response.items():
            raw_msg = values['RFC822']
            email_list.append(email.message_from_string(raw_msg))
        return email_list