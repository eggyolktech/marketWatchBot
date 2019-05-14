#!/usr/bin/python

from market_watch.util import config_loader
import sys
import time
import telepot
from telepot.loop import MessageLoop

config = config_loader.load()

MAX_MSG_SIZE = 4096
 
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

TOKEN = '764381129:AAFimhTCTvvodBXmZopXalZvJyv-B61OpCs'  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

