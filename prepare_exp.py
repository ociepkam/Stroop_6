#!/usr/bin/env python
# -*- coding: utf8 -*

import random
import numpy as np
from psychopy import visual
import copy

stim_text = {'CZERWONY': 'red', 'NIEBIESKI': '#5e75d9', 'BRAZOWY': '#574400', 'ZIELONY': 'green'}  # text: color
# stim_neutral = "HHHHHHHH"
stim_distractor = ['WYSOKA', 'UKRYTA', u'GŁĘBOKA', 'DALEKA']

colors_text = list(stim_text.keys())
random.shuffle(colors_text)
colors_names = [stim_text[color] for color in colors_text]
left_hand = colors_text[:2]
right_hand = colors_text[2:]

last_text = None
last_text_2 = None
last_color = None


def prepare_trial(trial_type_org, win, text_height, words_dist):
    global last_color, last_text, last_text_2
    text = None
    stim_distr = None

    if trial_type_org.endswith("bil1"):
        bil = 1
        trial_type = trial_type_org[:-5]
    elif trial_type_org.endswith("bil2"):
        bil = 2
        trial_type = trial_type_org[:-5]
    else:
        bil = 0
        trial_type = trial_type_org

    if trial_type == 'trials_con_con':
        possible_text = list(stim_text.keys())
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
            try:
                possible_text.remove([k for k, v in stim_text.iteritems() if v == last_color][0])
            except:
                pass
        text = random.choice(possible_text)
        color = stim_text[text]
        words = [text, text]

    elif trial_type == 'trials_con_neu':
        possible_text = list(stim_text.keys())
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
            try:
                possible_text.remove([k for k, v in stim_text.iteritems() if v == last_color][0])
            except:
                pass
        text = random.choice(possible_text)
        color = stim_text[text]
        possible_distr = copy.deepcopy(stim_distractor)
        if last_text_2 is not None:
            possible_distr.remove(last_text_2)
        stim_distr = random.choice(possible_distr)
        words = [text, stim_distr]

    elif trial_type == 'trials_inc1_inc1':
        possible_text = list(stim_text.keys())
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = random.choice(possible_text)
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        words = [text, text]

    elif trial_type == 'trials_inc1_inc2':
        possible_text = list(stim_text.keys())
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = random.choice([left_hand, right_hand])
        if text == left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        words = [text[0], text[1]]

    elif trial_type == 'trials_inc_neu':
        possible_text = list(stim_text.keys())
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = random.choice(possible_text)
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        possible_distr = copy.deepcopy(stim_distractor)
        if last_text_2 is not None:
            possible_distr.remove(last_text_2)
        stim_distr = random.choice(possible_distr)
        words = [text, stim_distr]

    elif trial_type == 'neutral':
        possible_text = stim_distractor[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text)
        words = [text, text]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    elif trial_type == 'neutral_2':
        possible_text = stim_distractor[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text, 2)
        words = [text[0], text[1]]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    else:
        raise Exception('Wrong trigger type')

    last_color = color
    last_text = text if len(text) == 2 else [text]
    last_text_2 = stim_distr

    random.shuffle(words)
    stim1 = visual.TextStim(win, color=color, text=words[0], height=text_height, pos=(0, words_dist / 2))
    stim2 = visual.TextStim(win, color=color, text=words[1], height=text_height, pos=(0, -words_dist / 2))
    stims = [stim1, stim2]

    stims_to_change = random.sample(range(len(stims)), bil)
    for elem in stims_to_change:
        stims[elem].bold = True
        stims[elem].italic = True
        stims[elem].text = stims[elem].text.lower()

    return {'trial_type': trial_type_org, 'text': words, 'color': color, 'stim': stims}


def prepare_part(trials_con_con, trials_con_neu, trials_inc_neu, trials_inc1_inc2, trials_inc1_inc1,
                 trials_con_con_bil1, trials_con_neu_bil1, trials_inc_neu_bil1, trials_inc1_inc2_bil1, trials_inc1_inc1_bil1,
                 trials_con_con_bil2, trials_con_neu_bil2, trials_inc_neu_bil2, trials_inc1_inc2_bil2, trials_inc1_inc1_bil2,
                 trials_neutral, trials_neutral_2,
                 win, text_height, words_dist):
    trials = ['trials_con_con'] * trials_con_con + \
             ['trials_con_neu'] * trials_con_neu + \
             ['trials_inc_neu'] * trials_inc_neu + \
             ['trials_inc1_inc2'] * trials_inc1_inc2 + \
             ['trials_inc1_inc1'] * trials_inc1_inc1 + \
             ['trials_con_con_bil1'] * trials_con_con_bil1 + \
             ['trials_con_neu_bil1'] * trials_con_neu_bil1 + \
             ['trials_inc_neu_bil1'] * trials_inc_neu_bil1 + \
             ['trials_inc1_inc2_bil1'] * trials_inc1_inc2_bil1 + \
             ['trials_inc1_inc1_bil1'] * trials_inc1_inc1_bil1 + \
             ['trials_con_con_bil2'] * trials_con_con_bil2 + \
             ['trials_con_neu_bil2'] * trials_con_neu_bil2 + \
             ['trials_inc_neu_bil2'] * trials_inc_neu_bil2 + \
             ['trials_inc1_inc2_bil2'] * trials_inc1_inc2_bil2 + \
             ['trials_inc1_inc1_bil2'] * trials_inc1_inc1_bil2 + \
             ['neutral'] * trials_neutral + \
             ['neutral_2'] * trials_neutral_2
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, text_height, words_dist) for trial_type in trials]


def prepare_exp(data, win, text_size, words_dist):
    text_height = 1.5 * text_size
    training1_trials = prepare_part(data['Training1_trials_con_con'],
                                    data['Training1_trials_con_neu'],
                                    data['Training1_trials_inc_neu'],
                                    data['Training1_trials_inc1_inc2'],
                                    data['Training1_trials_inc1_inc1'],
                                    data['Training1_trials_con_con_bil1'],
                                    data['Training1_trials_con_neu_bil1'],
                                    data['Training1_trials_inc_neu_bil1'],
                                    data['Training1_trials_inc1_inc2_bil1'],
                                    data['Training1_trials_inc1_inc1_bil1'],
                                    data['Training1_trials_con_con_bil2'],
                                    data['Training1_trials_con_neu_bil2'],
                                    data['Training1_trials_inc_neu_bil2'],
                                    data['Training1_trials_inc1_inc2_bil2'],
                                    data['Training1_trials_inc1_inc1_bil2'],
                                    data['Training1_trials_neutral'],
                                    data['Training1_trials_neutral_2'],
                                    win, text_height, words_dist)

    training2_trials = prepare_part(data['Training2_trials_con_con'],
                                    data['Training2_trials_con_neu'],
                                    data['Training2_trials_inc_neu'],
                                    data['Training2_trials_inc1_inc2'],
                                    data['Training2_trials_inc1_inc1'],
                                    data['Training2_trials_con_con_bil1'],
                                    data['Training2_trials_con_neu_bil1'],
                                    data['Training2_trials_inc_neu_bil1'],
                                    data['Training2_trials_inc1_inc2_bil1'],
                                    data['Training2_trials_inc1_inc1_bil1'],
                                    data['Training2_trials_con_con_bil2'],
                                    data['Training2_trials_con_neu_bil2'],
                                    data['Training2_trials_inc_neu_bil2'],
                                    data['Training2_trials_inc1_inc2_bil2'],
                                    data['Training2_trials_inc1_inc1_bil2'],
                                    data['Training2_trials_neutral'],
                                    data['Training2_trials_neutral_2'], win, text_height, words_dist)

    experiment_trials = prepare_part(data['Experiment_trials_con_con'],
                                     data['Experiment_trials_con_neu'],
                                     data['Experiment_trials_inc_neu'],
                                     data['Experiment_trials_inc1_inc2'],
                                     data['Experiment_trials_inc1_inc1'],
                                     data['Experiment_trials_con_con_bil1'],
                                     data['Experiment_trials_con_neu_bil1'],
                                     data['Experiment_trials_inc_neu_bil1'],
                                     data['Experiment_trials_inc1_inc2_bil1'],
                                     data['Experiment_trials_inc1_inc1_bil1'],
                                     data['Experiment_trials_con_con_bil2'],
                                     data['Experiment_trials_con_neu_bil2'],
                                     data['Experiment_trials_inc_neu_bil2'],
                                     data['Experiment_trials_inc1_inc2_bil2'],
                                     data['Experiment_trials_inc1_inc1_bil2'],
                                     data['Experiment_trials_neutral'],
                                     data['Experiment_trials_neutral_2'], win, text_height, words_dist)

    return [training1_trials, training2_trials], experiment_trials, colors_text, colors_names
