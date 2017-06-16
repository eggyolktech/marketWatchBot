#!/usr/bin/python

import configparser
import os
import urllib.request
import urllib.parse

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
config.read(config_path)

def send_to_chat(passage): 

    chat_list = config.items("telegram-chat")
    bot_send_url = config.get("telegram","bot-send-url")
    
    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id);

        result = urllib.request.urlopen(bot_send_url, urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": chat_id, "text": passage }).encode("utf-8")).read()
        
        print(result)

def main():
    
    passage = "Test"

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    send(passage)

if __name__ == "__main__":
    main() 
