import telebot
from tg_token import token
from telebot import types # модуль для кнопок бота
import pytz # модуль для смены часового пояса https://andreyex.ru/programmirovanie/python/kak-ispolzovat-modul-pytz-v-python/
from datetime import datetime # https://otus.ru/journal/tekushhaya-data-i-vremya-v-python/ - Хорошая статья про библиотеку datetime
# Не осуществилась идея ниже, т.к. тогда надо чтобы в файлике тоже было столько же видов символов между числом и месяцом ИЛИ какая то другая проверка (например по index смотреть число до нужного нам знака пунктуации но тогда нужно много .index() т.к в аргумент этой функции нельзя запихать много символов)
# string_punctuation_for_date = '-.:' # Вспом. строка для разнообразия ввода даты пользователем, символы взяты из string.punctuation https://docs.python.org/3/library/string.html#string.punctuation
# Предположительно, МОЖНО осуществить идею выше тремя проверками INDEX (3 символа в строке => 3 проверки), но это будет немного глупенько
# Да и впринцепи в данном коде достаточно объёмная и сложная задача
tz = pytz.timezone('Etc/GMT-7')
# https://qna.habr.com/q/1237780 - статья в которой была подсказка про UTF+7 + про форматы даты и времени
krasnoyarsk_current_datetime = datetime.now(tz)
# print(datetime.isoweekday(krasnoyarsk_current_datetime)) # если .weekday(now) - понедельник - 0, воскресенье - 6; если isoweekday(now) - понедельник - 1, воскресенье - 7 https://ru.stackoverflow.com/questions/1247680/%D0%94%D0%B5%D0%BD%D1%8C-%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D0%B8-%D0%BF%D0%BE-%D0%B4%D0%B0%D1%82%D0%B5-%D0%B2-python

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard = True - чтобы в чате красиво отображались кнопки
    # Просто добавить кнопку
    # markup.add(types.KeyboardButton('Нажми на меня'))
    # Разместить кнопки по рядам
    btn1 = types.KeyboardButton('Завтра')
    btn2 = types.KeyboardButton('Другая дата')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Донат')
    # btn4 = types.KeyboardButton('Дз за всё (учебное) время')
    markup.row(btn3) #, btn4
    # markup.add(btn1, btn2, btn3, btn4) - просто добавить кнопки в markup
    bot.send_message(message.chat.id, 'Привет. На какой день недели хочешь узнать дз?)', reply_markup = markup)


# В видео Гоши Дударя https://youtu.be/RpiWnPNTeww?si=1nnEh1twqoZmnOVH&t=977 Говориться о добавлении строчки bot.register_next_step_handler(message, on_clic), но она реагирует на кнопку лишь один раз.
# Поэтому, посмотрев видео https://youtu.be/LnherAK6NFA?si=sesjKyTM5BVLgfkV&t=533, пришёл к выводу, что проще сделать декоратор @bot.message_handler(content_types=['text']), который сможет обрабатывать сообщения чата, в которого будут отправлятся сообщения-команды после нажатия кнопок

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id,
                     '<b>Есть вопросы?</b> <em><u>Срочно пиши разработчику этого бота!!!</u></em> @Dimasik0125'
                     '\nПозже в этой команде будут добавлены все возможности и команды бота!', parse_mode='html')


with open('dz_technical_class.txt', encoding='utf-8') as f:
    datef = f.readlines()  # datef - данные fizмата

# Вызывает много ошибок
'''
all_dz = '' # все дз в виде одной строчки для кнопки "Дз за всё (учебное) время"
for i in datef:
    all_dz += i
print(type(all_dz))
'''

@bot.message_handler(content_types=['text'])
def on_click(message):
    def read_dz_technical(date):  # функция составления и высылания домашки из файла
        need_dz = ''  # нельзя делать эту переменную пустой строкой - программа ругается, что не может отправить пустую строку!!!
        for i in range(57):  # после большего кол-ва дз будет range(96) - написал ниже почему!)
            # смотрим последние 6 дней по 6 предметов (строчек) на каждый день предположительно + 10 доп. инфа по предметам на каждый день (т.к например в литературе на 12.10 (и э/п 04.10) - на дз не хватило одной строчки, поэтому использовали ещё (по фану (приколу) взял именно 10 доп. строчек)) => 16 строчек * 6 дней = 96 строк
            # использую именно range(), а не просто in date, чтобы каждый раз не пересматривать целый файл, который постепенно увеличивается, а лишь полсдение строки, именно в которых нам скорее всего нужно дз
            if datef[i][:5] == date:
                need_dz += datef[i][6:]  # [6:] - убираем дату в формате ДД.ММ и пробел
            elif datef[i][:4] == date:
                need_dz += datef[i][5:]
        if len(need_dz)>0:
            bot.send_message(message.chat.id, need_dz[:-1])  # т.к. последний символ '\n', а он нам не нужен
            '''
        elif datetime.isoweekday(krasnoyarsk_current_datetime)==7:
            bot.send_message(message.chat.id, 'Воскресенье. В этот день мы не учимся)')
        '''
        # Не смог до конца продумать и сделать этот блок, т.к. возникли трудности при передаче года в параметр datetime.datetime (ведь в message.text мы его не пишем, а ориентироваться здесь должны на данные message.text!) и из-за разности длины числа месяца (Д. или ДД.).
        # Проверка должна была осуществляться примерно таким образом: elif datetime.datetime(date[Год], date[Месяц], date[Число]).isoweekday() == 7:
        # https://sky.pro/media/poluchenie-dnya-nedeli-po-date-v-python/
        else:
            bot.send_message(message.chat.id, 'Разраб пока не внёс дз на эту дату. Можешь попробовать поторопить его в лс, но не советую😅 (у него наверное дела, не успевает немного...). Заранее приносит сильные извинения!')  # т.к. последний символ '\n', а он нам не нужен

    def check():  # проверка что начало сообщения это дата, чтобы не писать много текста в условие
        if (message.text[:2].isdigit() and message.text[2] == '.' and message.text[3:5].isdigit()) or (message.text[:1].isdigit() and message.text[1] == '.' and message.text[2:4].isdigit()):  # без .isdigit() не работает! # это условие если человек введёт любую дату года. Надо подумать, как сделать чтобы были даты только учебного года!
            # В верхнем условии первая скобка отвечает за проверку формата ДД.ММ, а вторая за Д.ММ
            # в будущем в message.text.lower()[2]=='.' можно добавить не только точку, но и другие знаки. Например, в начале проги есть переменная со всем служебными символами, и тут просто идёт проверка, есть ли message.text.lower()[2] в списке этих символов
            return True

    # Обработка кнопок под вводом сообщения
    if message.text.lower() == 'завтра':
        read_dz_technical(str(krasnoyarsk_current_datetime.day + 1) + '.' + str(krasnoyarsk_current_datetime.month))
    elif message.text.lower() == 'другая дата':
        bot.send_message(message.chat.id, 'Введи дату на которую хочешь узнать дз в формате ДД.ММ')
    # elif message.text.lower() == 'дз за всё (учебное) время':
    #     bot.send_message(message.chat.id, all_dz) # Проще уже файлом сделать, а то много ошибок вызывает
    elif message.text.lower() == 'донат':
        bot.send_message(message.chat.id,
                         'Номер карты (Сбербанк):\n'
                         '2022 2036 4752 7052\n'
                         'Номер телефона, к которому привязана карта:\n'
                         '+79504342736\n'
                         'Также желательно либо в комментарии к переводу либо в лс писать кто сделал перевод, чтобы знал кто сделал мне приятно и кому нужно быть бесконечно благодарным!)')
    # Обработка кнопки 'Другая дата'
    elif check():
        read_dz_technical(message.text)
    # Формально-развлекательные сообщения
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'как дела?':
        bot.send_message(message.chat.id, 'Хорошо. у тебя как?)')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == 'message':  # команда только для меня!
        bot.send_message(message.chat.id, message)
    # Ответ на неопределённое сообщение
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не знаю как отвечать на такое сообщение( Обратись к разработчику (команда "/help") и опиши свою проблему, чтобы я совершенствовался и был ещё лучше для вас)')

bot.polling(none_stop = True)

# Неосуществлённые идеи в Боте (коде)( :
# [] Если человек ввёл дату, которая выпала на воскресенье, бот бы отвечал "Воскресенье. В этот день мы не учимся)"
# [] Сделать чтобы когда вводим ДД.ММ не обязательно была только "." а можно было поставить и "-", и ":" и т.д. А ещё по хорошему чтобы можно было и Д.ММ, и Д.М писать, и бот всё равно понял какую дату человек написал!
