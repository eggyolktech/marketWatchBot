#!/usr/bin/python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint
import base64
from market_watch.telegram import bot_sender
from market_watch.util import redis_helper
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/root/google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    result = service.users().messages().list(userId='me', labelIds=['Label_1352622790776435189'], maxResults=10).execute()

    print(result)
    msgid_list = []
    for message in result['messages']:
        print("message id - %s" % message['id'])
        msgid_list.append(message['id'])

    print("message list [%s]" % msgid_list)
    redis_key = 'GMAIL:TRADEPA'
    #redis_key = 'GMAIL:TRADEPA:TEST'
    msgid_list = redis_helper.get_new_key_list(redis_key, msgid_list, 20)
    print("message list - only new [%s]" % msgid_list)

    for msgid in msgid_list:

        content = service.users().messages().get(userId='me', id=msgid).execute()
       
        headers = content['payload']['headers']
        subject = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']

        #pp.pprint(content) 

        if 'parts' in content['payload']:
            parts = content['payload']['parts']
            part = parts[0]
            body = part['body']
            txt = base64.b64decode(body['data'])
            print("subject [%s], content [%s]" % (subject, txt.decode('utf-8')))            
            ptext = u'\U0001F4E3' + " PriceAlerts \n[%s]\n\n" % subject + txt.decode('utf-8')
            
            bot_sender.broadcast_list(ptext, 'telegram-ptgroup')
            #bot_sender.broadcast_list(ptext)
        
        # only one body, no parts
        elif 'body' in content['payload']: 

            #body = content['payload']['body']
            #content = base64.b64decode(body['data'], '-_')
            #soup = BeautifulSoup(content)
            #content = ''.join(soup.findAll(text=True))
            #while "\n\n" in content: content = content.replace("\n\n", "\n")
            #content = content.replace("  ", "").replace
            txt = content['snippet']
            print("subject [%s], content [%s]" % (subject, txt))            
            #print("subject [%s], content [%s]" % (subject, content.decode('utf-8')))            
            ptext = u'\U0001F4E3' + " PriceAlerts \n[%s]\n\n" % subject + txt
            
            bot_sender.broadcast_list(ptext, 'telegram-ptgroup')
            #bot_sender.broadcast_list(ptext)


if __name__ == '__main__':
    main()
