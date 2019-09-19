from classes import *
from functions import *

class Verb_list:
      forms = ['first_singular', 'second_singular', 'second_formal', 'third_singular', 'first_plural', 'second_plural', 'third_plural']
      verbs = []
      no_IPA = []
      no_sound = []

      @classmethod
      def get_conjugations(cls, verb):
            webpage = requests.get('http://conjugator.reverso.net/conjugation-german-verb-' + verb + '.html')
            tree = html.fromstring(webpage.content)
            try:
                  present_tense = tree.xpath("//div[@id = 'ch_divSimple']/child::*")[1].xpath("child::*/child::*/child::div")[0].xpath("child::*/child::i/text()")
                  conjugations = []

                  if len(present_tense) == 12:
                        for i in range(6):
                              conjugations.append(present_tense[2*i + 1])
                  if len(present_tense) == 18:
                        verb.seperable = True
                        verb.prefix = present_tense[2]
                        verb.prefix_len = len(verb.prefix)
                        
                        for i in range(6):
                              root = present_tense[3*i + 1]
                              conjugations.append(verb.prefix+root)

                  print(conjugations)

                  return conjugations
            
            except:
                  print('No Conjugation:', verb)


      @classmethod
      def create_form_set(cls):
            for verb in cls.verbs:
                  for form in cls.forms:

                        verb_ins = eval('verb.' + form)
                        
                        question = 'Conjugation || ' + verb_ins.german
                        answer = verb_ins.form
                        title = question
                        create_card(verb_ins, question, answer, title, 'form', paths)


      @classmethod
      def create_conjugate_set(cls):
            for verb in cls.verbs:
                  for form in cls.forms:
                        verb_ins = eval('verb.' + form)
                        question = 'Conjugate || ' + verb.infinitive + ' | ' + verb_ins.form
                        answer = verb_ins.german
                        if verb.seperable == True:
                              answer += ', ' + verb_ins.german[verb.prefix_len:] + ' ' + verb.prefix
                        title = question
                        card = Card(title, question, answer, 'spelling')
                        verb_ins.cards.append(card)


      @classmethod
      def create_listen_set(cls):
            for verb in cls.verbs:
                  for form in cls.forms:
                        verb_ins = eval('verb.' + form)


      @classmethod
      def create_pronounce_set(cls, paths):
            for verb in cls.verbs:
                  for form in cls.forms:
                        verb_ins = eval('verb.' + form)
                        
                        if verb_ins.has_sound == True:
                              question = 'Pronounce || ' + verb.infinitive + ' | ' + verb_ins.form
                              answer = verb_ins.german
                              title = question
                              create_audio_card(verb_ins, verb_ins.german, question, answer, title, 'pronounciation', paths)


      @classmethod
      def create_translation_set(cls, paths):
            for verb in cls.verbs:
                  for form in cls.forms:
                        verb_ins = eval('verb.' + form)
                        
                        if verb_ins.has_sound == False:
                              question = 'Translate || ' + verb.infinitive + ' | ' + verb_ins.form
                              answer = verb_ins.german
                              title = question
                              create_card(verb_ins, question, answer, title, 'translate')


      @classmethod
      def get_web_resources(cls, paths):
            if not os.path.exists(paths.audio_folder):
                  os.makedirs(paths.audio_folder)

            for verb in cls.verbs:
                  for child in cls.forms:
                        verb_ins = eval('verb.' + child)
                        get_audio_and_ipa(verb_ins.german, verb_ins, cls, paths)
            write_missing_lists(cls, paths)
                        
                        
      @classmethod
      def write_XML_file(cls, paths):            
            with open(paths.xml, 'wb+') as file:
                  file.write(XML.collection_header)
                  count = 2
                  file.write(XML.topic_header('Verbs', count))

            cls.write_cards(count, paths)

            with open(paths.xml, 'ab+') as file:         
                  file.write(XML.topic_footer)
                  file.write(XML.collection_footer)

                  
      @classmethod
      def write_cards(cls, count, paths):
            with open(paths.xml, 'ab+') as file:                        
                  index_structure = cls.create_index_structure()
                  card_index = 'Initial'

                  form_range = 0

                  while cls.has_a_non_empty_list(index_structure):
                        verb_index = 0
                        num_of_forms = len(cls.forms)
                        form_range += 1
                        form_index = -1
                        
                        for iteration_num in range(form_range):                              
                              form_index += 1
                              if form_index == num_of_forms:
                                    form_index = 0
                                    verb_index += 1
                              if verb_index is len(cls.verbs):
                                    verb_index -= 1
                                    
                              if len(index_structure[verb_index][form_index]) > 0:
                                    card_index = index_structure[verb_index][form_index][0]
                                    card = eval('cls.verbs[verb_index].' + cls.forms[form_index] + '.cards[card_index]')
                                    del index_structure[verb_index][form_index][0]
                                    
                                    count += 1
                                    file.write(card.convert_to_XML(count))
            

      def has_a_non_empty_list(structure):
            """Determines if an iterable has any non empty lists in it.

            Takes in an iterable of arbitrary depth. Determines depth. Decompresses the iterable into a list of sets.

            structure: list of lists containing lists and so on

            iterable-of-lists -> Boolean"""
            variables = 'abcdefghijklmnopqrstuvwxyz'
            condition = True
            depth = 0
            while condition:                
                  try:
                        depth += 1
                        eval('structure' + depth*'[0]')
                  except:
                        condition = False

            command = '[' + variables[depth - 2] + ' for a in structure]'
            if depth > 2:
                  command = command[:-1]
                  for level in range(depth - 2):
                        command += ' for ' + variables[level + 1] + ' in ' + variables[level]
                  command += ']'

            list_of_lists = eval(command)

            for element in list_of_lists:
                  if element != []:
                        return True
            return False


      def create_list_of_lens(structure):
            len_index_structure = []
            for i in structure:
                  len_i = []
                  for j in i:
                        len_i.append(len(j))
                  len_index_structure.append(len_i)

            return len_index_structure
                        

      @classmethod
      def create_index_structure(cls):
            index_structure = []
            for verb in cls.verbs:
                  verb_structure = []
                  for form in cls.forms:
                        form_structure = []
                        for i in range(len(eval('verb.' + form + '.cards'))):
                              form_structure.append(i)
                        verb_structure.append(form_structure)
                  index_structure.append(verb_structure)
            return index_structure
