import random

def make_exercise(action, user):
    use_nr = []
    # print(str(user['mult_opt_nr']))
    for nr in user['mult_opt_nr']:
        if (user['mult_opt_nr'][nr]):
            use_nr.append(nr)

    a_temp = random.randint(0, len(use_nr)-1)
    a = use_nr[a_temp]
    b = random.randint(1, 12)

    hint = int(a)
    keep_b = int(b)

    if user['mult_opt_can_be_inverted']:
        x = random.randint(0, 1)
        if x:
            a, b = b, a

    c = int(a)*int(b)

    """ generate options """
    if user['mult_opt_answer_type'] > 1:
        rand_range = 2*user['mult_opt_answer_type']
        range_low = hint - random.randint(1, rand_range)
        low = range_low if range_low > 0 else 1
        options = random.sample(
            range(low, low+rand_range), user['mult_opt_answer_type'])
        if not (keep_b in options):
            options.pop(0)
            options.insert(0, keep_b)
            random.shuffle(options)
        new_list = [x*hint for x in options]

    mult_tuple = [int(a), int(b), c, hint, new_list] if action == 'multiply' else [4, 5, 6]

    return mult_tuple