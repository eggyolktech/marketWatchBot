#!/usr/bin/python

import os
import configparser

class ConfigLoader:
    __single = None
    __conifg = None
    __config_dev = None

    def __init__(self):
        if ConfigLoader.__single:
            raise ConfigLoader.__single
        ConfigLoader.__single = self
 
        config = configparser.ConfigParser()
        config_dev =  configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
        print(config_path)
        config.read(config_path)
        
        config_path_dev = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config-dev.properties')
        config_dev.read(config_path_dev)

        ConfigLoader.__config = config
        ConfigLoader.__config_dev = config_dev

    def getSingleton():
        if not ConfigLoader.__single:
            ConfigLoader.__single = ConfigLoader()
        return ConfigLoader.__single

    def getConfig(self):
        return ConfigLoader.__config

    def getConfigDev(self):
        return ConfigLoader.__config_dev

def load(env = "PROD"):

    singleton = ConfigLoader.getSingleton()
    config = singleton.getConfig()
    configDev = singleton.getConfigDev()
    #config = configparser.ConfigParser()
    #config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.properties')
    #print(config_path)
    #config.read(config_path)
    if env == "PROD":
        return config
    elif env == "DEV":
        return configDev

def main():

    config = load("DEV")
    print("Load Config Test: [%s]" % config.items("ibcard"))
   
if __name__ == "__main__":
    main()        
        

