import os
from lxml import html
import requests
import shutil

from functions import *
from classes import *
from weekly_vocab import *
from Verbs import *

def create_sets(sets_to_create, name = None):
      """Instructs classes to create card sets.

      sets_to_create: specifies which classes to activate

      name: topic header for custom set

      dict{str: bool}, str -> None}"""
      
      if sets_to_create['Weekly Vocab'] == True:
            Weekly_Vocab.process_list()

            Weekly_Vocab.scrape_the_web()
            Weekly_Vocab.makecards()
##            Weekly_Vocab.create_audio_cards()
##            Weekly_Vocab.create_translation_cards()
##            Weekly_Vocab.create_gender_cards()
##            Weekly_Vocab.create_spelling_cards()
            
            #Verb_list.get_web_resources()
##            Verb_list.create_conjugate_set()
            #Verb.create_translation_set()
      
            Weekly_Vocab.write_XML_file('foldered')

      if sets_to_create['Verbs'] == True:
            Verb_list.process_list(paths.list)
            #Verb_list.get_web_resources()
            Verb_list.create_conjugate_set()
            #Verb_list.create_translation_set()
            Verb_list.write_XML_file()

######################################################################################################################################

sets_to_create = {'Weekly Vocab': True, 'Verbs': False, 'Custom': False}
week = 'Week 3'

XML.__init__(week)
IO_Ops.initpaths(week, sets_to_create)
IO_Ops.initfolders()

create_sets(sets_to_create)
IO_Ops.convertaudio()
