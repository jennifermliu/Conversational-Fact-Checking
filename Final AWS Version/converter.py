#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:36:02 2018

@author: carlosbelardi
"""

import json
import codecs
from pprint import pprint

with open('sampleoutput.json') as data_file:
    data = json.load(data_file)
#pprint(data)
curr_file = codecs.open('thisJSON.txt', 'w', encoding='utf-8')
for curr_dict in data:
    curr_headline = curr_dict['ruling_headline']
    curr_url = curr_dict['statement_url']
    curr_output = curr_headline + "\n" + "www.politifact.com" + curr_url + "\n"
    curr_output.encode("utf-8")
    curr_file.write(curr_output)
