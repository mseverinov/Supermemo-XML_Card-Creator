import os
from lxml import html
import requests
import shutil
from classes import *

def get_IPA(word_ins, operation_cls):
    try:
        tree = get_tree(word_ins.german, 'https://de.wiktionary.org/wiki/', 'wiktionary')
        try:
            IPA = tree.xpath('//span[@class="ipa"]/text()')
            IPA = '[' + str(IPA[0]) + ']'
            word_ins.IPA = IPA
        except:
            operation_cls.no_IPA.append(word_ins.german)
            print('No IPA:', word_ins.german)
    except:
        print('Unable to connect to wiktionary. Check internet connection.')


def get_sound(word_ins, operation_cls):
    tree = get_tree(word_ins.german, 'https://de.wiktionary.org/wiki/', 'wiktionary')
##    print(tree, word_ins.german)
    try:
        xpath_cmd = """//a[@title="De-""" + word_ins.german + """.ogg"]"""
        retrieve_and_save_sound(tree, xpath_cmd, 'wiktionary', word_ins.german)
    except:
        print('Wiktionary No sound:', word_ins.german)
        tree = get_tree(word_ins.german, 'https://www.duden.de/rechtschreibung/', 'duden')
        
        try:
            xpath_cmd =  """//a[@title="Als mp3 abspielen - © Aussprachedatenbank der ARD"]"""
            retrieve_and_save_sound(tree, xpath_cmd, 'duden', word_str)
        except:
            operation_cls.no_sound.append(word_ins.german)
            print('Duden No sound:', word_ins.german)
            word_ins.has_sound = False


def write_missing_lists(operation_cls): 
    with open(IO_Ops.nosound, 'w+') as file:
        for word_str in operation_cls.no_sound:
            output = word_str + '\n'
            file.write(output)
    
    with open(IO_Ops.noIPA, 'w+') as file:
        for word_str in operation_cls.no_IPA:
            output = word_str + '\n'
            file.write(output)


def get_audio_and_ipa(word_ins, operation_cls):
    get_IPA(word_ins, operation_cls)
    get_sound(word_ins, operation_cls)


def retrieve_and_save_sound(tree, xpath_cmd, site, word):
    xml = tree.xpath(xpath_cmd)[0]
    url = 'https:' + xml.get('href')
    sound = requests.get(url, stream=True)
    
    if site == 'wiktionary':
          save_path = IO_Ops.download + '/' + word + '.ogg'
    if site == 'duden':
          save_path = IO_Ops.converted + '/'  + word + '.mp3'
    soundpath = os.path.normpath(save_path)
        
    with open(soundpath, 'wb') as file:
        shutil.copyfileobj(sound.raw, file)
    

def html_check_and_correction(word_str, site):
    if ' ' in word_str:
        html_str = word_str.replace(' ', '_')
    else:
        html_str = word_str

    if site == 'duden':
        if 'ß' in html_str:
            html_str.replace('ß', 'sz')
    return html_str


def get_tree(word_str, webpage_html, site):
    html_str = html_check_and_correction(word_str, site)
    webpage = requests.get(webpage_html + html_str)
    tree = html.fromstring(webpage.content)
    return tree


########################################################################################################################################################
    

def create_audio_card(word_ins, question, answer, title, card_set_type):
    if word_ins.hassound():
        urlpath = os.path.normpath(IO_Ops.converted+'/'+word_ins.german+'.mp3')
    else:
        urlpath= None
        
    if word_ins.IPA != None:
        answer += '\n' + word_ins.IPA

    card = Card(title, question, answer, card_set_type, urlpath)
    word_ins.cards.append(card)


def create_card(word_ins, question_prefix, language, card_set_type):
    question = question_prefix + eval('word_ins.' + language[0])
    answer = eval('word_ins.' + language[1])
    title = question
    answer = gender_check(word_ins, card_set_type, language[1])
    
    card = Card(title, question, answer, card_set_type)
    word_ins.cards.append(card)
    

def gender_check(word_ins, card_set_type, language):
    if 'gender' in card_set_type:
        return word_ins.gender
    else:
        return eval('word_ins.' + language)        

def create_english_to_german_card(word_ins):
    create_card(word_ins, 'Translate || ', ['english', 'german'], 'english to german')
    
def create_german_to_english_card(word_ins):
    create_card(word_ins, 'Translate || ', ['german', 'english'], 'german to english')

def create_spelling_card(word_ins):
    create_card(word_ins, 'Spell || ', ['english', 'german'], 'spelling')

def create_gender_from_german_card(word_ins):
    create_card(word_ins, 'Gender || ', ['german', 'english'], 'gender from german')

def create_gender_from_english_card(word_ins):
    create_card(word_ins, 'Gender || ', ['english', 'german'], 'gender from english')

def create_pronounciation_card(word_ins):    
    question = 'Pronounce || ' + word_ins.english
    answer = word_ins.german
    title = question
    create_audio_card(word_ins, question, answer, title, 'pronounce')

def create_listen_card(word_ins):
    question =  'Listen ||'
    answer = word_ins.english
    title = question + ' ' + word_ins.german
    create_audio_card(word_ins, question, answer, title, 'listen')
