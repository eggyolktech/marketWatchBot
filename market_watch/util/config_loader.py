#!/usr/bin/python

import os
import configparser

class ConfigLoader:
    __single = None
    __conifg = None

    def __init__(self):
        if ConfigLoader.__single:
            raise ConfigLoader.__single
        ConfigLoader.__single = self
 
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
        print(config_path)
        config.read(config_path)
        ConfigLoader.__config = config

    def getSingleton():
        if not ConfigLoader.__single:
            ConfigLoader.__single = ConfigLoader()
        return ConfigLoader.__single

    def getConfig(self):
        return ConfigLoader.__config

def load():

    singleton = ConfigLoader.getSingleton()
    config = singleton.getConfig()
    
    #config = configparser.ConfigParser()
    #config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
    #print(config_path)
    #config.read(config_path)
    return config

def main():

    config = load()
    print("Load Config Test: [%s]" % config.items("ibcard"))
   
if __name__ == "__main__":
    main()        
        

