from classes import *
from functions import *
from Verbs import *
import shutil


class Weekly_Vocab:
      """Container for preliminary operations and word sets."""
      
      words = []
      no_sound = []
      no_IPA = []

      @classmethod
      def process_list(cls):
            """Seperates vocab list into singulars, plurals, and non nouns.

             Verb portion should be at the end.""" 
            notverbs = []
            notverbchunk = []
            verbs= []
            verbindicator = False
            contents = []
            with open(IO_Ops.listend) as file:
                  contents = file.readlines()
            
            for line in contents:
                  line = line.strip()
                  if verbindicator:
                        verbs.append(line)
                  else:
                        if line == 'VERBS':
                              verbindicator = True
                        else:
                              if line == '':
                                    notverbs.append(notverbchunk)
                                    notverbchunk = []
                              else:
                                    notverbchunk.append(line)                  

            if verbindicator:
                  cls.process_verbs(contents[index:], Verb_list)
            
            for notverbchunk in notverbs:
                  english = notverbchunk[-1]
                  german = notverbchunk[0]
                  if len(notverbchunk) == 3:
                        plural = notverbchunk[1]
                        word = Noun(english, german, plural)
                  else:
                        if german[:3]  in ['der', 'das', 'die']:
                              word = Noun(english, german)
                        else:
                              word = Non_Noun(english, german)
                              
                  cls.words.append(word)



      @classmethod
      def write_XML_file(cls, organization):
            if organization == 'intermixed':
                  cls.write_XML_file_intermixed()
            else:
                  cls.write_XML_file_foldered()
                  


      @classmethod
      def write_XML_file_intermixed(cls,):
            #has not been updated to handle plurals
            with open(IO_Ops.xml, 'wb+') as file:
                  file.write(XML.collection_header)
                  count = 2
                  file.write(XML.topic_header('Weekly Vocab', count))
                  num_of_words = len(cls.words)
                  
                  for iteration in range(num_of_words):
                        for card_index, word_index in enumerate(reversed(range(iteration+1))):
                              num_of_cards = len(cls.words[word_index].cards)
                              
                              if card_index < num_of_cards:
                                    count += 1
                                    card = cls.words[word_index].cards[card_index]
                                    file.write(card.convert_to_XML(count))

##            Verb_list.write_cards(count)
            
            with open(IO_Ops.xml, 'ab+') as file:
                  file.write(XML.topic_footer)
                  file.write(XML.collection_footer)


      @classmethod
      def write_XML_file_foldered(cls):
            """Constructs XML code with cards for each word in the same subfolder.

            None -> None"""
            with open(IO_Ops.xml, 'wb+') as file:
                  file.write(XML.collection_header)
                  count = 2
                  file.write(XML.topic_header('Weekly Vocab', count))

                  for word in cls.words:
                        count += 1
                        folder_title = word.german + ' (' + word.english + ')'
                        file.write(XML.topic_header(folder_title , count))

                        if word.is_plural():
                              que = [word, word.plural]
                        else:
                              que = [word]
                              
                        for element in que:
                              for card in element.cards:
                                    count += 1
                                    file.write(card.convert_to_XML(count))
                              
                        file.write(XML.topic_footer)
                  file.write(XML.topic_footer)

##            Verb_list.write_cards(count)
            
            with open(IO_Ops.xml, 'ab+') as file:
                  file.write(XML.collection_footer)

      
      @classmethod
      def scrape_the_web(cls):
            for word in cls.words:
                  get_IPA(word, cls)
                  
                  if os.path.exists(IO_Ops.converted + '/' + word.german + '.mp3'):
                        print(word.german + ' previously downloaded')

                  else:
                        get_sound(word, cls)

                  if word.is_plural():
                        get_IPA(word.plural, cls)
                        
                        if os.path.exists(IO_Ops.converted + '/' + word.plural.german + '.mp3'):
                              print(word.plural.german + ' previously downloaded')

                        else:
                              get_sound(word.plural, cls)

            write_missing_lists(cls)

      ####################
      @classmethod
      def makecards(cls):
            
            for word in cls.words:
                  if not word.hassound():
                        create_german_to_english_card(word)

                  else:
                        create_pronounciation_card(word)
                        if word.is_plural():
                              create_pronounciation_card(word.plural)

                  if word.is_noun():
                        create_gender_from_german_card(word)
                        
                  create_spelling_card(word)
                  if word.is_plural():
                        create_gender_from_german_card(word.plural)
                        create_spelling_card(word.plural)


      ####################
                        
      def __repr__(self):
            output = ''
            for index, word in enumerate(self.words):
                  output += repr(word) + '\n'

            return output
