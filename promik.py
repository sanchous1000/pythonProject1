import telebot

from telebot import types
import datetime

from getpass import getpass
from mysql.connector import connect, Error
from telebot.async_telebot import AsyncTeleBot
import asyncio


def gid_namer(a):
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            namer = []
            selec_time_query = f"""
select name_guide from guide join
(select id_guide from workhours where workdate = "{a}") as q1 
on q1.id_guide = guide.id_guide;"""

            with connection.cursor() as cursor:
                cursor.execute(selec_time_query)
                for row in cursor.fetchall():
                    namer.append(row[0])
                return namer

    except Error as e:
        print(e)


def sql_adder(massiv):
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            print(tuple(massiv))
            selec_time_query = f"""call boter.add_apply{tuple(massiv)};"""
            print(selec_time_query)
            with connection.cursor() as cursor:
                cursor.execute(selec_time_query)
                connection.commit()
            return True

    except Error as e:
        print(e)


global timer
timer = ["09:00", "09:30"]
for i in range(10, 24):
    timer.append(str(i) + ":00")
    timer.append(str(i) + ":30")
timer.append('00:00')

print(timer)


def prov_time(massiv, timer, namer):
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            connectiom = []
            for time in timer:
                for name in namer:
                    print(time)

                    selec_time_query = f"""select boter.is_excurtion_available('{massiv[0]}', '{massiv[1]}',
            '{massiv[2]}','{daterik(massiv[3])}','{time}','{name}');"""
                    with connection.cursor() as cursor:
                        cursor.execute(selec_time_query)
                        for row in cursor.fetchall():
                            if str(row[0]) == "1" and time[0:5] not in connectiom:
                                print(connectiom)
                                print(row)
                                print(time[0:5])
                                connectiom.append(time[0:5])
            print("??????")
            return connectiom


    except Error as e:
        print(e)


def get_pass():
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            passer = []
            log_pas = f"""SELECT login_promik, pass_promik FROM boter.promik;"""
            print(log_pas)
            with connection.cursor() as cursor:
                cursor.execute(log_pas)
                for row in cursor.fetchall():
                    passer.append(row)

            return passer
    except Error as e:
        print(e)


def get_id_promik(massiv):
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            passer = []
            log_pas = f"""select id_promik from promik where 
            login_promik='{massiv[0]}' and pass_promik='{massiv[1]}';"""
            with connection.cursor() as cursor:
                cursor.execute(log_pas)
                for row in cursor.fetchall():
                    passer.append(row)
            return passer
    except Error as e:
        print(e)


print(get_pass())


bot = telebot.TeleBot('5047987551:AAGwl2gGDMqrV0p-v0okuhFjPi83y0zAx0E')
excur_up = {'????????????????????????????': ['??????????????', '????????', '????????????????', '??????????????', '????????????????'], '??????????????????': ['??????????????']}
excur_down = ['?????????????????? ?????? ??????????']
kombi = {'????????????????????????????':['???????????? ????????????????????', '?????????????????? ?? ????????????', '?????????????? ??????????????????????', '?????????????? ????????']}

places = {'??????????': excur_up, '????????????????': excur_down,
          '??????????': kombi}

print(excur_up.values())
for i in excur_up.values():
    print(i)
global users
users = {}

log_parol = {}
linkin = {}


def creation(id, information):
    users[id].append(information)
    print(users)
    return users


def add_log_par(id, information):
    log_parol[id].append(information)
    print(log_parol)
    return log_parol


def button_call(callback, massiv, texti):
    prmt_keyboard = types.InlineKeyboardMarkup()
    for i in massiv:
        prmt_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=texti,
                          reply_markup=prmt_keyboard)


def button_mes(message, massiv, texti):
    prmt_keyboard = types.InlineKeyboardMarkup()
    for i in massiv:
        prmt_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))

    bot.send_message(message.chat.id, texti, reply_markup=prmt_keyboard)


dater = []


def show_date(
        k):  # ??????????????, ???????????????????????? ???????? ?? ?????????????? %m.%d ?????? ????????????, ?????? ???????? ???????????? ?????? ?????? ????????????????????, ?????????? ???????????????? :(
    s = datetime.date.today()
    data = (s + datetime.timedelta(days=k)).strftime('%d.%m')
    return data


a = []
for i in range(7):
    a.append(str(show_date(i)))

print(a)


def daterik(date_):
    from datetime import datetime
    daterik = datetime.strptime(date_ + ".22", "%d.%m.%y")
    return daterik.date()


a.append('??????????????')


def get_passik(log):
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="boter",
        ) as connection:
            feedback = {}
            log_pas = f"""
select id_apply, type_excur, category_excur, name_excur, date_app, time_app, amount_app, infa, comment, if(name_guide is null, '?????? ???????? ???? ????????????????', name_guide) as gid, login_promik from apply 
join excurtion on apply.id_excur=excurtion.id_excur
left join guide on guide.id_guide=apply.id_guide
join promik on promik.id_promik=apply.id_promik
where date_app>=date_sub(current_date(), INTERVAL 1 day) and  login_promik = "{log}" order by date_app, time_app;"""

            with connection.cursor() as cursor:
                print("dzbd")
                cursor.execute(log_pas)
                for row in cursor.fetchall():
                    feedback[str(row[0])] = row[1:len(row)]

            return feedback
    except Error as e:
        print(e)

print(get_passik('serega228'))
information = {}

print(gid_namer("2022-07-04"))

@bot.message_handler(commands=['start'])
@bot.message_handler(
    func=lambda m: m.text == "???????????? ?????????? ?? ???????????? ?????? ??????" or m.text == "?????????????? ?? ????????????")
def check_log(message):
    nextmsg = bot.send_message(message.chat.id, text="????????????! ?????????? ???????? ??????????")
    bot.register_next_step_handler(nextmsg, check_pass)


def check_pass(message):

    log_parol[message.chat.id] = []
    log_parol.update(add_log_par(message.chat.id, message.text))
    nextmsg2 = bot.send_message(message.chat.id, text="???????????? ?????????? ????????????")
    bot.register_next_step_handler(nextmsg2, check_pass_2)


def check_pass_2(message):
    log_parol.update(add_log_par(message.chat.id, message.text))
    print(get_id_promik(log_parol[message.chat.id]))
    s = get_id_promik(log_parol[message.chat.id])
    print(s)
    if len(s) == 0:
        start_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        start_keyboard.add(types.KeyboardButton(text='???????????? ?????????? ?? ???????????? ?????? ??????'))
        bot.send_message(message.chat.id, "???????????? ????????????????, ???????????????? ???????????? ????????????", reply_markup=start_keyboard)
    else:
        start_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for i in ["?????????????????????? ?????????????????? ????????????", "?????????????? ????????????"]:
            start_keyboard.add(types.KeyboardButton(text=i))
        bot.send_message(message.chat.id, "???????????? ??????????????????", reply_markup=start_keyboard)





@bot.message_handler(
    func=lambda m: m.text == "?????????????????????? ?????????????????? ????????????")
def proger(message):
    texter = ''
    for i in get_passik(log_parol[message.chat.id][0]).keys():
        print(log_parol[message.chat.id][0])
        texter += f"\n???????????? ?????????? {i} \n"
        k = 0
        for j in get_passik(log_parol[message.chat.id][0])[i]:
            print(j)
            k += 1
            texter += f"{str(k)}){str(j)} \n"
    start_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    """
    for i in ["?????????????? ?? ????????????"]:
        start_keyboard.add(types.KeyboardButton(text=i))
    """
    bot.send_message(message.chat.id, "???????? ?????????????????? ???????????? \n" + texter, reply_markup=start_keyboard)


@bot.message_handler(
    func=lambda m: m.text == "?????????????? ????????????")
def start_kb(message):
    start_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for i in places.keys():
        start_keyboard.add(types.KeyboardButton(text=i))
    bot.send_message(message.chat.id, "????????????! ???????????? ??????????????????", reply_markup=start_keyboard)


@bot.message_handler(
    func=lambda m: m.text == "??????????" )
def exc_cur(message):
    global mes
    mes = message.text
    users[message.chat.id] = []
    users.update(creation(message.chat.id, message.text))
    button_mes(message, places[message.text], f'{mes}')


@bot.callback_query_handler(func=lambda c: c.data in ["????????????????????????????", "??????????????????"])
def excur_up(callback):
    users.update(creation(callback.message.chat.id, callback.data))
    button_call(callback, places[mes][callback.data], f'{callback.data} ??????????????????')


@bot.message_handler(
    func=lambda m: m.text == "????????????????")
def ex_down(message):
    users[message.chat.id] = []
    users.update(creation(message.chat.id, message.text))
    button_mes(message, places[message.text], '???????????? ??????????????????')


@bot.message_handler(
    func=lambda m: m.text == "??????????")
def ex_down(message):
    users[message.chat.id] = []
    users.update(creation(message.chat.id, message.text))
    users.update(creation(message.chat.id, "????????????????????????????"))
    button_mes(message, places[message.text]["????????????????????????????"], '???????????? ??????????????????')


@bot.callback_query_handler(
    func=lambda c: c.data == "?????????????? ???????????? ????????" or c.data in ['??????????????', '????????', '????????????????', '??????????????', '????????????????',
                                                                 '?????????????????? ?????? ??????????', '???????????? ????????????????????',
                                                                 '?????????????????? ?? ????????????', '?????????????? ??????????????????????',
                                                                 '?????????????? ????????'])
def promowter_dates_kb(callback):
    if callback.data != "?????????????? ???????????? ????????":
        print("???????????????? ???? ????????????????")
        users.update(creation(callback.message.chat.id, callback.data))

    button_call(callback, a, '???????????????? ????????')




@bot.callback_query_handler(
    func=lambda c: c.data in a[0:len(a)-2])
def promowter_dates_kb(callback):
    users.update(creation(callback.message.chat.id, callback.data))
    print("vvvvvvvvvvvvvv")
    try:
        if prov_time(users[callback.message.chat.id], timer,
                                              gid_namer(daterik(users[callback.message.chat.id][3]))) == []:
            users[callback.message.chat.id].pop()
            button_call(callback, ["?????????????? ???????????? ????????"], "???? ???????? ???????? ?????? ???????????????????? ??????????????!")
        else:
            button_call(callback,
                        prov_time(users[callback.message.chat.id], timer,
                                              gid_namer(daterik(users[callback.message.chat.id][3])))
                                    , "???????????????? ???????????????????? ?????? ??????????!")

    except IndexError:
        users[callback.message.chat.id].pop()
        button_call(callback, ["?????????????? ???????????? ????????"], "???? ???????? ???????? ?????? ???????????????????? ??????????????!")


@bot.callback_query_handler(
    func=lambda c: c.data == '??????????????')
@bot.message_handler(
    func=lambda m: m.text == "???? ???????????????? ?????? ????????????")
def dati(callback):
    date_ = bot.send_message(chat_id=callback.message.chat.id,
                             text="?????????????? ???????? ?? ?????????????? ????????.??????????")
    bot.register_next_step_handler(date_, addict)


def addict(message):

    try:
        print(message.text + "++++")

        users.update(creation(message.chat.id, message.text))
        zalupa = types.InlineKeyboardMarkup()
        btn1487 = types.InlineKeyboardButton(text='????!', callback_data='Date')
        btn1488 = types.InlineKeyboardButton(text='??????, ???????????? ?????? ??????', callback_data='Vruch')
        zalupa.add(btn1487, btn1488)
        bot.send_message(message.chat.id, f'?????????????????????????? ????????{message.text}, ?????? ???????????', reply_markup=zalupa)
    except ValueError:

        zalupa = types.InlineKeyboardMarkup()
        btn1488 = types.InlineKeyboardButton(text='?????? ??????', callback_data='??????????????')
        zalupa.add(btn1488)
        bot.send_message(chat_id=message.chat.id,
                         text="?? ?????? ???? ??????????????:( ?????????????? ???????? ?? ?????????????? ????????.??????????, ????????????????, 31.05",
                         reply_markup=zalupa)


@bot.callback_query_handler(
    func=lambda c: c.data == "Date")
def timerson(callback):
    button_call(callback, timer, "???????????????? ???????????????????? ?????? ??????????")


@bot.callback_query_handler(
    func=lambda c: c.data in timer)
def promowter_dates_kb(callback):
    users.update(creation(callback.message.chat.id, callback.data))
    sent = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                 text="?????????????? ???????????????????? ?????????????? ?? ?????????????????? (????????????: 2*1400)")
    bot.register_next_step_handler(sent, amount)


def amount(message):
    users.update(creation(message.chat.id, message.text))
    pipi = bot.send_message(message.chat.id, text="?????????????? ?????? ?????????????? ?? ?????? ???????????????????? ?????????? (1 ????????????????????)")
    bot.register_next_step_handler(pipi, contacts)


def contacts(message):
    users.update(creation(message.chat.id, message.text))
    com = bot.send_message(message.chat.id, text="?????????????? ?????????????????????? ?? ????????????")
    bot.register_next_step_handler(com, comment)


def comment(message):
    users.update(creation(message.chat.id, message.text))
    itoger = ""
    k = 0
    print(tuple(users[message.chat.id]))
    for index, item in enumerate(users[message.chat.id]):
        if index == 3:
            users[message.chat.id][index] = str(daterik(item))
        elif index == 4:
            users[message.chat.id][index] += ":00"
        k += 1
        itoger += f"{index + 1}){item};\n"
    print(log_parol)
    users[message.chat.id].append(str(log_parol[message.chat.id][0]))
    button_mes(message, ["?????? ???????????", "?????????????? ???????????? ?????? ??????"], "?????????????? ????????????" + "\n" + itoger)


@bot.callback_query_handler(
    func=lambda c: c.data == "?????? ???????????")
def itog(callback):
    print(log_parol)
    print(users)
    sql_adder(users[callback.message.chat.id])
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text="?????? /start ?????? ???? ???????????? ??????????,?????????? ?????????????? ?????????? ????????????")


bot.polling(none_stop=True, interval=0)