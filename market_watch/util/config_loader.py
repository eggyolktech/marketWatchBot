#!/usr/bin/python

import os
import configparser

def load():

    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
    print(config_path)
    config.read(config_path)
    return config

def main():

    config = load()
    print("Load Config Test: [" + config.get("telegram","bot-send-url") + "]")
   
if __name__ == "__main__":
    main()        
        

