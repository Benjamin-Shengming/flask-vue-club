#!/usr/bin/python

#To do: move some code from email sender to here
# major job is get/set information from/to a email message

import email
import re
from email.message import Message
import dns.resolver

from ..log import logger
log = logger.GetLogger(__name__)

def get_multi_parts(msg):
    return_list = []
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        return_list.append(part)
    return return_list
    
def get_subject(msg):
    return msg['Subject']

def get_from_address(msg):
    return msg['From']

def get_to_address(msg):
    return msg['To']

# check whether email server exists
def test_email_server_exists(email_address):
    try:
        mail_server_name = email_address.split("@")[1]
        answers = dns.resolver.Resolver().query(mail_server_name, 'MX')
        if len(answers) <= 0:
            log.info("No mail server found for destination: " + mail_server_name)
            return False
        return True
    except:
        log.info("No mail server found for destination: " + mail_server_name)
        return False

def get_RFC_2822_email_regex():
    # The section of RFC 2822 from which each pattern component is
    # derived is given in an accompanying comment.
    #
    # (To make things simple, every string below is given as 'raw',
    # even when it's not strictly necessary.  This way we don't forget
    # when it is necessary.)
    WSP = r'[\s]'                                        # see 2.2.2. Structured Header Field Bodies
    CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
    NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
    QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
    FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
        WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
    CTEXT = r'[' + NO_WS_CTL + \
            r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
    CCONTENT = r'(?:' + CTEXT + r'|' + \
            QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
    # as well, but that would be circular.)
    COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
            r')*' + FWS + r'?\)'                       # see 3.2.3
    CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
        FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
    ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
    ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
    DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
    DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' # see 3.2.4
    QTEXT = r'[' + NO_WS_CTL + \
            r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
    QCONTENT = r'(?:' + QTEXT + r'|' + \
            QUOTED_PAIR + r')'                        # see 3.2.5
    QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                    r'?' + QCONTENT + r')*' + FWS + \
                    r'?' + r'"' + CFWS + r'?'
    LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
                QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
    DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
    DCONTENT = r'(?:' + DTEXT + r'|' + \
            QUOTED_PAIR + r')'                        # see 3.4.1
    DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                    r'(?:' + FWS + r'?' + DCONTENT + \
                    r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
    DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
            DOMAIN_LITERAL + r')'                       # see 3.4.1
    ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

    # A valid address will match exactly the 3.4.1 addr-spec.
    VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'
    return VALID_ADDRESS_REGEXP

def is_valid_email_str(email_str):
    if re.match(get_RFC_2822_email_regex(), email_str) != None:
        return True
    return False#