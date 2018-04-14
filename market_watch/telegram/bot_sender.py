#!/usr/bin/python

import configparser
import os
import io
import urllib.request
import urllib.parse
import requests
from market_watch.util import config_loader

config = config_loader.load()

MAX_MSG_SIZE = 4096

def broadcast(passage, is_test=False):

    if (is_test):
        chat_list = config.items("telegram-chat-test")
    else:
        chat_list = config.items("telegram-chat")
    bot_send_url = config.get("telegram","bot-send-url")

    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id);

        messages = [passage[i:i+MAX_MSG_SIZE] for i in range(0, len(passage), MAX_MSG_SIZE)]

        for message in messages:

            result = urllib.request.urlopen(bot_send_url, urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": chat_id, "text": message }).encode("utf-8")).read()
            print(result)

def broadcast_list(passage, chatlist="telegram-chat-test"): 
    
    chat_list = config.items(chatlist)
    bot_send_url = config.get("telegram","bot-send-url")
    
    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id);

        messages = [passage[i:i+MAX_MSG_SIZE] for i in range(0, len(passage), MAX_MSG_SIZE)]

        for message in messages:

            result = urllib.request.urlopen(bot_send_url, urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": chat_id, "text": message }).encode("utf-8")).read()
        
            print(result)

def send_image(image_path, chatlist="telegram-chat-test"):
    
    chat_list = config.items(chatlist)
    bot_send_url = config.get("telegram","bot-send-photo-url")
    local_image = open(image_path, 'rb')
    
    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id)
        files = {'photo': local_image}
        data = {'chat_id' : chat_id}
        r= requests.post(bot_send_url, files=files, data=data)
        print(r.status_code, r.reason, r.content)

def send_remote_image(image_url, chatlist="telegram-chat-test"):

    chat_list = config.items(chatlist)
    bot_send_url = config.get("telegram","bot-send-photo-url")
    remote_image = requests.get(image_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    
    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id)
        files = {'photo': photo}
        data = {'chat_id' : chat_id}
        r= requests.post(bot_send_url, files=files, data=data)
        print(r.status_code, r.reason, r.content)     
            
def main():
    
    passage = "Test"

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    #broadcast(passage, True)
    
    local_image_path = "C:\\Temp\\trumptrump.jpg"
    send_image(local_image_path)
    
    image_url = "http://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg"
    
    send_remote_image(image_url)

if __name__ == "__main__":
    main() 
