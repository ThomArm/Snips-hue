#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from snipshue.snipshue import SnipsHue
import io
import math

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details. 
    """ 
    if len(intentMessage.slots.house_room):
    	for room in intentMessage.slots.house_room:
    		#snipshue.light_down(20, room)
            snipshue.light_down(20, "chambre")
    else:
        snipshue.light_down(20, None)

    current_session_id = intentMessage.session_id
    result_sentence="Luminosite diminue dans la chambre"
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    snipshue= SnipsHue("192.168.1.84","YFuLloeVWUTdSO8IJKZi2OYXZJKsEFPAfatS0Fq2")
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("lightsTurnDown", subscribe_intent_callback) \
.start()
