import random
import nltk
from telebot import types
from analyzer import get_deps as gd, get_translation as gt


# a dictionary to store data
user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.russian_text = None
        self.original_text = None
        self.exercise = None
        self.score_per_sent = 0
        self.score = 0


# functions

def create_drill(source, voice, intent):
    phrases = source
    raw_sent = random.choice(phrases)
    analyzed_sent = gd(raw_sent, voice, intent)
    translated_sent = gt(analyzed_sent)
    sents = [raw_sent, translated_sent, analyzed_sent]
    return sents


def check(user_sentence, user):
    dist = nltk.edit_distance(str(user.original_text), user_sentence)
    dist_num = dist / 10
    user.score_per_sent = 2 - dist_num
    if user.score_per_sent < 0:
        user.score_per_sent = 0
    user.score += user.score_per_sent
    user.score = round(user.score, 1)
    return user.score


def start_drill(text, user, voice, intent):
    sents = create_drill(text, voice, intent)
    user.original_text = sents[0]
    user.russian_text = sents[1]
    user.analyzed_text = sents[2]
    keyboard = types.InlineKeyboardMarkup()
    for i in user.russian_text:
        text_button = types.InlineKeyboardButton(text=str(i), callback_data="nothing")
        keyboard.add(text_button)
    check_words_button = types.InlineKeyboardButton(text='ПОДСКАЗКА', callback_data="check_word")
    keyboard.add(check_words_button)
    return keyboard


def error_handler(text):
    keyboard = types.InlineKeyboardMarkup()
    error_btn = types.InlineKeyboardButton(text=str(text), callback_data="error")
    keyboard.add(error_btn)
    return keyboard
