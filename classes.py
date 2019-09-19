import os
from lxml import html
import requests
import shutil
from Verbs import *

class Card:
      """What will be a single Supermemo item."""
      def __init__(self, title, question, answer, kind, url = None):
            self.title = title
            self.question = question
            self.answer = answer
            self.url = url
            self.kind = kind


      def convert_to_XML(self, count):
            """Formats card contents into XML.

            int -> bstr"""
            header = '\n'*2 + '\t'*3 + '<SuperMemoElement>'\
                     + '\n'*1 + '\t'*4 + '<ID>'+ str(count) + '</ID>'\
                     + '\n'*1 + '\t'*4 + '<Title>' + self.title + '</Title>'\
                     + '\n'*1 + '\t'*4 + '<Type>Item</Type>'
            
            content = '\n'*1 + '\t'*4 + '<Content>'\
                      + '\n'*1 + '\t'*5 + '<Question>' + self.question + '</Question>'\
                      + '\n'*1 + '\t'*5 + '<Answer>' + self.answer + '</Answer>'
            
            footer = '\n'*1 + '\t'*4 + '</Content>'\
                     + '\n'*1 + '\t'*3 + '</SuperMemoElement>'

            if self.url != None:
                  sound  = '\n'*1 + '\t'*5 + '<Sound>'\
                           + '\n'*1 + '\t'*6 + '<URL>' + self.url + '</URL>'\
                           + '\n'*1 + '\t'*5 + '</Sound>'
            else:
                  sound = ''
                  
            card = header + content + sound + footer
            return card.encode()


      def __repr__(self):
            output = 'Title: ' + self.title + '\nQuestion: ' + self.question + '\nAnswer: ' + self.answer
            
            if self.url != None:
                  output += '\nUrl: ' + self.url
            return output          
                  
      


class IO_Ops:
      """Stores and creates file paths."""
      
      @classmethod
      def initpaths(cls, week, sets_to_create):
            """Initializes paths used by program.

            week: name of this week's folder
            sets_to_create: self explanatory

            str, dict{str:bool} -> None"""
            cls.root = 'C:/Users/Mykhaylo Severinov/Desktop/Classes/German/'
            cls.week = cls.root + 'Vocab/' + week
            cls.download = os.path.normpath(cls.week + '/'+ 'Audio')
            cls.converted = os.path.normpath(cls.root+ '/' + 'Converted')
            cls.nosound = os.path.normpath(cls.week+ '/' + 'no_sound.txt')
            cls.noIPA = os.path.normpath(cls.week+ '/' + 'no_IPA.txt')
            cls.xml = os.path.normpath(cls.week + '/'+ 'import.xml')

            if sets_to_create['Weekly Vocab'] == True:
                  cls.liststart = os.path.normpath(cls.root + '/' + 'vocab.txt')
                  cls.listend = os.path.normpath(cls.week+ '/' + 'vocab.txt')

            if sets_to_create['Verbs'] == True:
                  cls.liststart = os.path.normpath(self.root + '/'+ 'verbs.txt')
                  cls.listend = os.path.normpath(cls.week + '/'+ 'verbs.txt')
      

      @classmethod
      def initfolders(cls):
            if not os.path.exists(IO_Ops.download):
                  os.makedirs(IO_Ops.download)
            if not os.path.exists(IO_Ops.converted):
                  os.makedirs(IO_Ops.converted)
            if not os.path.exists(IO_Ops.root):
                  os.makedirs(IO_Ops.root)
            if os.path.exists(IO_Ops.liststart):
                  shutil.move(IO_Ops.liststart, IO_Ops.listend)
      

      @classmethod
      def convertaudio(cls):
            """Converts downloaded audio files into a format usable by Supermemo.

             -> None"""
            for file in os.scandir(cls.download):
                filename, ext = os.path.splitext(file.name)
                if '.ogg' == ext:
                    dirchangecmd = 'CD '+cls.download
                    convcmd = 'ffmpeg -i '+filename+'.ogg'+' '+filename+'.mp3'
                    os.system(dirchangecmd+' && '+convcmd)
                    
                    startloc = os.path.normpath(cls.download+'/'+filename+'.mp3')
                    endloc = os.path.normpath(cls.converted+'/'+filename+'.mp3')
                    if not os.path.exists(endloc):
                          os.rename(startloc, endloc)
                    else:
                        print(filename, 'has already been converted.')
         




class XML:
      """Stores and creates auxillary XML code."""
      def __init__(week):
            """Sets the non-dynamic XML code.

            collection_header:  Specifiy the start of a Supermemo collection +
                                       the code for the week's topic card/title.

            topic_footer:          Specifies the end of a category.

            collection_footer:   Specifies the end of the collection.
            """
            collection_header = '\t'*0 + '<SuperMemoCollection>'\
                          + '\n'*1 + '\t'*1 + '<SuperMemoElement>'\
                          + '\n'*1 + '\t'*2 + '<ID>1</ID>'\
                          + '\n'*1 + '\t'*2 + '<Title>' + week + '</Title>'\
                          + '\n'*1 + '\t'*2 + '<Type>Topic</Type>'
            
            collection_footer = '\n'*1 + '\t'*1 + '</SuperMemoElement>'\
                          + '\n'*1 + '\t'*0 + '</SuperMemoCollection>'

            topic_footer =  '\n'*1 + '\t'*2 + '</SuperMemoElement>'

            XML.collection_header = collection_header.encode()
            XML.collection_footer = collection_footer.encode()
            XML.topic_footer = topic_footer.encode()


      def topic_header(topic, count):
            """Creates XML code for a topic card."""
            header = '\n'*2 + '\t'*2 + '<SuperMemoElement>'\
                     + '\n'*1 + '\t'*3 + '<ID>' + str(count) + '</ID>'\
                     + '\n'*1 + '\t'*3 + '<Title>' + topic + '</Title>'\
                     + '\n'*1 + '\t'*3 + '<Type>Topic</Type>'

            return header.encode()
      
#######################################################################################################################################################

class Word:
      def __init__(self, german, english = ''):
            self.german = german
            self.english = english
            self.IPA = None
            self.has_sound = True
            self.cards = []

      def is_noun(self):
            return self.noun

      def is_plural(self):
            return self.plurality

      def hassound(self):
            return self.has_sound
      
      def __repr__(self):
            output = 'Word' + str(index) + ': ' + word.german + '\n'
            for index, card in enumerate(self.cards):
                  output += '\tCard ' + str(index) + ': '
                  output += card.kind + '\n'
                  #output +=  repr(card)
            return output


class Noun(Word):
      noun = True

      def __init__(self, english, german, plural = None):
            super().__init__(german, english)
            self.german = german[4:]

            article = german[:3]

            if article == 'der':
                  self.gender = 'Masculine'
            elif article == 'das':
                  self.gender = 'Neutered'
            else:
                  self.gender = 'Feminine'
                  
            if plural == None:
                  self.plurality = False
            else:
                  self.plurality = True
                  self.plural = Plural(english, plural)


class Non_Noun(Word):
      noun = False
      plurality = False
      def __init__(self, english, german):
            super().__init__(german, english)


class Plural(Word):
      noun = True
      plurality = True
      def __init__(self, english, german):
            english += ' (plural)'
            super().__init__(german, english)
            self.gender = 'Plural'


class Verb(Word):
      noun = False
      plurality = False
      def __init__(self, infinitive, fs, ss, ts, fp, sp, tp_sf, verb_list_cls):
            self.infinitive = infinitive
            self.seperable = False
            self.prefix = ''
            self.prefix_length = 0
            self.first_singular = First_Singular(fs, infinitive)
            self.second_singular = Second_Singular(ss, infinitive)
            self.second_formal = Second_Formal(tp_sf, infinitive)
            self.third_singular = Third_Singular(ts, infinitive)
            self.first_plural = First_Plural(fp, infinitive)
            self.second_plural = Second_Plural(sp, infinitive)
            self.third_plural = Third_Plural(tp_sf, infinitive)
            
            verb_list_cls.verbs.append(self)

      def call_super_init(self, german)   :
            super().__init__(german)

      def __str__(self):
            return 'Verb: ' + self.infinitive + 'Form: ' + self.form


class First_Singular(Verb):
      form = 'First Person Singular'
      def __init__(self, german, infinitive):
            super().call_super_init(german)


class Second_Singular(Verb):
      form = 'Second Person Singular'
      def __init__(self, german, infinitive):
            super().call_super_init(german)


class Second_Formal(Verb):
      form = 'Second Person Formal'
      def __init__(self, german, infinitive):
            super().call_super_init(german)


class Third_Singular(Verb):
      form = 'Third Person Singular'
      def __init__(self, german, infinitive):
            super().call_super_init(german)
            

class First_Plural(Verb):
      form = 'First Person Plural'
      def __init__(self, german, infinitive):
            super().call_super_init(german)


class Second_Plural(Verb):
      form = 'Second Person Plural'
      def __init__(self, german, infinitive):
            super().call_super_init(german)


class Third_Plural(Verb):
      form = 'Third Person Plural'
      def __init__(self, german, infinitive):
            super().call_super_init(german)
