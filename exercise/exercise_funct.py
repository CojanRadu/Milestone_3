import random
import json
from types import SimpleNamespace
from collections import namedtuple

def make_exercise(action, user):
    use_nr = []
    checkbox_options = []
    options = []
    all_hint = []
    dict_user_options= {}

    for nr in user['exercise'][action]['opt_nr']:
        if (user['exercise'][action]['opt_nr'][nr]):
            use_nr.append(nr)

    for option in user['exercise'][action]:
        if ((option != 'opt_nr') and (option != 'opt_can_be_inverted')):
            dict_user_options[option] = user['exercise'][action][option]

    # print(dict_user_options)
    print(action)
    
    a_temp = random.randint(0, len(use_nr)-1)
    a = use_nr[a_temp]
    b = random.randint(1, 12)

    hint = int(a)
    keep_b = int(b)

    if user['exercise'][action]['opt_can_be_inverted']:
        x = random.randint(0, 1)
        if x:
            a, b = b, a

    

    """ generate options """
    if user['exercise'][action]['opt_answer_type'] > 1:
        rand_range = 2*user['exercise'][action]['opt_answer_type']
        range_low = hint - random.randint(1, rand_range)
        low = range_low if range_low > 0 else 1

        
        options = random.sample(range(low, low+rand_range), user['exercise'][action]['opt_answer_type'])
        if not (keep_b in options):
            options.pop(0)
            options.insert(0, keep_b)
        random.shuffle(options)
        
    if action == 'add': 
        c = int(a)+int(b)
        checkbox_options = [x+hint for x in options]
        for n in range(1,13):
            all_hint.append(str(a) + ' + ' + str(n) + ' = ' + str(int(a)+int(n)))
        my_tuple = [int(a), int(b), c, '+', all_hint, checkbox_options, dict_user_options] 
    elif action == 'substract':
        c = int(a)+int(b)
        checkbox_options = [x for x in options]
        for n in range(1,13):
            if (c - n >= 0 ):
                all_hint.append(str(c) + ' - ' + str(n) + ' = ' + str(c - n ))
        my_tuple = [c, int(a), int(b), '-', all_hint, checkbox_options, dict_user_options]  
    elif action == 'multiply':
        c = int(a)*int(b)
        checkbox_options = [x*hint for x in options] 
        for n in range(1,13):
            all_hint.append(str(a) + ' * ' + str(n) + ' = ' + str(int(a)*int(n)))
        my_tuple = [int(a), int(b), c, '*', all_hint, checkbox_options, dict_user_options]   
    else:      
        c = int(a)*int(b)   
        checkbox_options = [x for x in options]
        for n in range(1,13):
            if (c % n == 0):
                all_hint.append(str(c) + ' / ' + str(n) + ' = ' + str(int(c / n)))
        my_tuple = [c, int(a), int(b), '/', all_hint, checkbox_options, dict_user_options]
    
        # if not (c in checkbox_options):
        #     print(checkbox_options)
        #     checkbox_options.pop(0)
        #     checkbox_options.insert(0, c)
        #     print(checkbox_options)
        # random.shuffle(checkbox_options)

    return my_tuple