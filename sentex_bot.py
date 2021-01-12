import telebot
import traceback
from sentex_maker import *
from texts import TEXTS

# bot config
BOT_TOKEN = '1475460308:AAEV9OM3GNBCSN01HA4OcVDfEaRzAjqTjvI'
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# functions


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    try:
        chat_id = message.chat.id
        user = User(chat_id)
        user_dict[chat_id] = user
        dif_levels = TEXTS['start_handler']
        intro = TEXTS['comm'][0]
        keyboard = types.InlineKeyboardMarkup()
        btn_el = types.InlineKeyboardButton(text=dif_levels[0], callback_data="el")
        btn_pre = types.InlineKeyboardButton(text=dif_levels[1], callback_data="pre")
        btn_inter = types.InlineKeyboardButton(text=dif_levels[2], callback_data="int")
        btn_adv = types.InlineKeyboardButton(text=dif_levels[3], callback_data="adv")
        keyboard.add(btn_el, btn_pre, btn_inter, btn_adv)
        bot.send_message(message.chat.id, intro, reply_markup=keyboard)
    except Exception as e:
        print('Start Handler Error: ', e, traceback.format_exc())
        bot.send_message(message.chat.id, TEXTS['error'][0])
        pass


def el_course_select(message):
    rules = TEXTS['comm'][3]
    btn_text = TEXTS['el_select']
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=str(btn_text[0]), callback_data="pres_s")
    btn2 = types.InlineKeyboardButton(text=str(btn_text[1]), callback_data="past_s")
    btn3 = types.InlineKeyboardButton(text=str(btn_text[2]), callback_data="pres_cont")
    btn4 = types.InlineKeyboardButton(text=str(btn_text[3]), callback_data="tis")
    btn5 = types.InlineKeyboardButton(text=str(btn_text[4]), callback_data="going_to")
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, rules, reply_markup=keyboard)


def pre_course_select(message):
    rules = TEXTS['comm'][3]
    btn_text = TEXTS['pre_select']
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=str(btn_text[0]), callback_data="pp_vs_ps")
    btn2 = types.InlineKeyboardButton(text=str(btn_text[1]), callback_data="ppc")
    btn3 = types.InlineKeyboardButton(text=str(btn_text[2]), callback_data="ppc_vs_ps")
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, rules, reply_markup=keyboard)


def int_course_select(message):
    rules = TEXTS['comm'][3]
    btn_text = TEXTS['int_select']
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=str(btn_text[0]), callback_data="passive")
    btn2 = types.InlineKeyboardButton(text=str(btn_text[1]), callback_data="mv_a")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, rules, reply_markup=keyboard)


def adv_course_select(message):
    rules = TEXTS['comm'][3]
    btn_text = TEXTS['adv_select']
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=str(btn_text[0]), callback_data="all_tenses")
    btn2 = types.InlineKeyboardButton(text=str(btn_text[1]), callback_data="emph_str")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, rules, reply_markup=keyboard)


def quiz(message):
    chat_id = message.chat.id
    if message.text.lower() == 'стоп':
        msg = bot.send_message(message.chat.id, "Упражнение прервано!")
        bot.register_next_step_handler(msg, start_handler)
    else:
        try:
            user = user_dict[chat_id]
        except Exception as e:
            print('Quiz Error: ', e, traceback.format_exc())
            user = User(chat_id)
            user_dict[chat_id] = user
            bot.send_message(message.chat.id, TEXTS['error'][0])
            pass
        rules = TEXTS['comm'][2]
        keyboard = error_handler(TEXTS['error'][0])
        if user.exercise == 'pres_s':
            keyboard = start_drill(TEXTS['el']['pres_simple'], user, 'act', 'n')
        elif user.exercise == 'past_s':
            keyboard = start_drill(TEXTS['el']['past_simple'], user, 'act', 'n')
        elif user.exercise == 'pres_cont':
            keyboard = start_drill(TEXTS['el']['pres_cont'], user, 'act', 'n')
        elif user.exercise == 'tis':
            keyboard = start_drill(TEXTS['el']['tis'], user, 'act', 'n')
        elif user.exercise == 'going_to':
            keyboard = start_drill(TEXTS['el']['going_to'], user, 'act', 'y')
        elif user.exercise == 'pp_vs_ps':
            keyboard = start_drill(TEXTS['pre']['pp_vs_ps'], user, 'act', 'n')
        elif user.exercise == 'ppc':
            keyboard = start_drill(TEXTS['pre']['ppc'], user, 'act', 'n')
        elif user.exercise == 'ppc_vs_ps':
            keyboard = start_drill(TEXTS['pre']['ppc_vs_ps'], user, 'act', 'n')
        elif user.exercise == 'passive':
            keyboard = start_drill(TEXTS['inter']['passive'], user, 'pass', 'n')
        elif user.exercise == 'mv_a':
            keyboard = start_drill(TEXTS['inter']['mv_a'], user, 'pass', 'n')
        elif user.exercise == 'emph_str':
            keyboard = start_drill(TEXTS['adv']['emph_str'], user, 'act', 'n')
        elif user.exercise == 'all_tenses':
            keyboard = start_drill(TEXTS['adv']['all_tenses'], user, 'act', 'n')
        msg = bot.send_message(message.chat.id, rules, reply_markup=keyboard)
        bot.register_next_step_handler(msg, check_answer)


def check_answer(message):
    chat_id = message.chat.id
    if message.text.lower() == 'стоп':
        msg = bot.send_message(message.chat.id, "Упражнение прервано!")
        bot.register_next_step_handler(msg, start_handler)
    else:
        try:
            user = user_dict[chat_id]
        except Exception as e:
            print('Check answer Error: ', e, traceback.format_exc())
            user = User(chat_id)
            user_dict[chat_id] = user
            bot.send_message(message.chat.id, TEXTS['error'][0])
            pass
        user_answer = message.text
        check(user_answer, user)
        bot.send_message(message.chat.id, "Ваш счет: " + str(user.score_per_sent) + "\nОбщий счет: " + str(user.score)
                         + "\nОригинал: " + str(user.original_text))
        for i, v in user_dict.items():
            print('User id: ', i, '; Exercise: ', v.exercise, '; Score: ', v.score)
        if user.score < 10:
            quiz(message)
        else:
            msg = bot.send_message(message.chat.id, "Упражнение закончено!")
            bot.register_next_step_handler(msg, start_handler)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    expl = TEXTS['comm'][1]
    chat_id = call.message.chat.id
    c_user = User(chat_id)
    try:
        user_dict[chat_id] = c_user
        user = user_dict[chat_id]
    except Exception as e:
        print('Callback Error: ', e, traceback.format_exc())
        user_dict[chat_id] = c_user
        user = user_dict[chat_id]
    if call.message.text.lower() == 'стоп':
        msg = bot.send_message(call.message.chat.id, "Упражнение прервано!")
        bot.register_next_step_handler(msg, start_handler)
    if call.data == "el":
        msg = bot.send_message(call.message.chat.id, expl)
        bot.register_next_step_handler(msg, el_course_select)
    if call.data == "pres_s":
        user.exercise = 'pres_s'
        message = TEXTS['comm'][6]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "past_s":
        user.exercise = 'past_s'
        message = TEXTS['comm'][7]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "pres_cont":
        user.exercise = 'pres_cont'
        message = TEXTS['comm'][13]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "tis":
        user.exercise = 'tis'
        message = TEXTS['comm'][14]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "going_to":
        user.exercise = 'going_to'
        message = TEXTS['comm'][15]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "pre":
        msg = bot.send_message(call.message.chat.id, expl)
        bot.register_next_step_handler(msg, pre_course_select)
    if call.data == "pp_vs_ps":
        user.exercise = 'pp_vs_ps'
        message = TEXTS['comm'][10]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "ppc":
        user.exercise = 'ppc'
        message = TEXTS['comm'][11]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "ppc_vs_ps":
        user.exercise = 'ppc_vs_ps'
        message = TEXTS['comm'][12]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "int":
        msg = bot.send_message(call.message.chat.id, expl)
        bot.register_next_step_handler(msg, int_course_select)
    if call.data == "passive":
        user.exercise = 'passive'
        message = TEXTS['comm'][8]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "mv_a":
        user.exercise = 'mv_a'
        message = TEXTS['comm'][9]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "adv":
        msg = bot.send_message(call.message.chat.id, expl)
        bot.register_next_step_handler(msg, adv_course_select)
    if call.data == "emph_str":
        user.exercise = 'emph_str'
        message = TEXTS['comm'][4]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "all_tenses":
        user.exercise = 'all_tenses'
        message = TEXTS['comm'][5]
        msg = bot.send_message(call.message.chat.id, message)
        bot.register_next_step_handler(msg, quiz)
    if call.data == "check_word":
        at = '/ '.join([i for i in user.analyzed_text])
        bot.send_message(call.message.chat.id, at)
    if call.data == "error":
        message = TEXTS['error'][1]
        bot.send_message(call.message.chat.id, message)


if __name__ == "__main__":
    bot.infinity_polling()
