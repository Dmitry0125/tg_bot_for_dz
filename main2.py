import telebot
from tg_token import token
from telebot import types # модуль для кнопок бота
import time
# from rassilca import * # подключение текстового файла с ID пользователей для рассылки и управление им
# print(time.time()) # узнать время
# print(int(time.mktime(time.strptime('2023-12-18 01:05:00', '%Y-%m-%d %H:%M:%S')))) # перевести время из человекопонятного в UNIX
# https://i-leon.ru/tools/time - Unix time конвертер (Конвертер времени Unix онлайн) С ИНСТРУКЦИЯМИ И ОБЪЯСНЕНИЯМИ!

# ниже попытка использования актуального времени
'''
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
'''

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

joinedFile = open('/home/dmitry/Projects/Botдлядомашкиv.2/joinedID.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

joinedFile1 = open('/home/dmitry/Projects/Botдлядомашкиv.2/joinedName.txt', 'r')
joinedUsers1 = set()
for line in joinedFile1:
    joinedUsers1.add(line.strip())
joinedFile1.close()

@bot.message_handler(commands=['rassilca'])
def rassilca(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('/home/dmitry/Projects/Botдлядомашкиv.2/joinedID.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)
        joinedFile.close()
        bot.send_message(message.chat.id, 'Ты успешно зарегистрирован на рассылку!)')
    # пока вроде не работает(
    # else:
    #     bot.send_message(message.chat.id, 'Ты уже подписан на рассылку)')

    # Добавлять Имя и Фамилию
    # if not (message.chat.first_name + message.chat.last_name) in joinedUsers1:
    #     joinedFile1 = open('/home/dmitry/Projects/Botдлядомашкиv.2/joinedName.txt', 'a')
    #     joinedFile1.write((message.chat.first_name + message.chat.last_name) + '\n')
    #     joinedUsers1.add(message.chat.first_name + message.chat.last_name)
    #     joinedFile1.close()

    if not str(message.chat.id) in joinedUsers1:
        joinedFile1 = open('/home/dmitry/Projects/Botдлядомашкиv.2/joinedName.txt', 'a')
        joinedFile1.write(f'id: {message.chat.id}; first_name: {message.chat.first_name}; last_name: {message.chat.last_name}; username: {message.chat.username}; date: {message.date}; is_bot: {message.from_user.is_bot}; is_premium: {message.from_user.is_premium}; language_code: {message.from_user.language_code}; message_id: {message.message_id}; text: {message.text}' + '\n')
        joinedUsers1.add(message.chat.first_name + message.chat.last_name)
        joinedFile1.close()



@bot.message_handler(commands=['special'])
def mess(message):
    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])

@bot.message_handler(commands=['write'])
def write(message):
    with open('dz_technical_class.txt', 'r+') as file:
        content = file.read()  # Чтение
        file.seek(0)  # Переход в начало файла
        file.write(message.text[message.text.find(' ')+1:]+'\n')  # Запись новой строки
        file.write(content)  # Запись старого содержимого
        # file.seek(0)
        # d = file.read()
    # print(d)

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
    current_date = time.strftime("%d.%m", time.localtime(message.date)) # вывод даты строкой в формате ДД.ММ
    # https: // docs - python.ru / standart - library / modul - datetime - python / kody - formatirovanija - strftime - strptime - modulja - datetime / - статья о форматах и %d и т.д
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
        if message.text[:2].isdigit() and message.text[2] == '.' and message.text[3:5].isdigit(): # без .isdigit() не работает! # это условие если человек введёт любую дату года. Надо подумать, как сделать чтобы были даты только учебного года!
            # В верхнем условии первая скобка отвечает за проверку формата ДД.ММ, а вторая за Д.ММ
            # в будущем в message.text.lower()[2]=='.' можно добавить не только точку, но и другие знаки. Например, в начале проги есть переменная со всем служебными символами, и тут просто идёт проверка, есть ли message.text.lower()[2] в списке этих символов
            return True

    # Обработка кнопок под вводом сообщения
    if message.text.lower() == 'завтра':
        read_dz_technical(str(int(current_date[:2])+1)+current_date[2:])
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
    elif message.text.lower() == 'зимние каникулы':
        bot.send_message(message.chat.id, 'Литература:\n'
                         '- Большие произведения на 2 полугодие:\n'
                         '-- "Тихий Дон"\n'
                         '-- рассказы Шаламова\n'
                         '-- "Мастер и Маргарита"\n'
                         '- Стихи:\n'
                         '-- Есенин: "Гой ты Русь моя родная" + 1 на выбор + 1 любовная лирика\n'
                         '-- Маяковский: 1 любое на выбор\n'
                         'Информатика: есть в вк в группе "11 проф. математика 134"\n'
                         'Физика: есть в тг в группе "11 ЕГЭ"')
    # Ответ на неопределённое сообщение
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не знаю как отвечать на такое сообщение( Обратись к разработчику (команда "/help") и опиши свою проблему, чтобы я совершенствовался и был ещё лучше для вас)')

bot.polling(none_stop = True)

# Неосуществлённые идеи в Боте (коде)( :
# [] Если человек ввёл дату, которая выпала на воскресенье, бот бы отвечал "Воскресенье. В этот день мы не учимся)"
# [] Сделать чтобы когда вводим ДД.ММ не обязательно была только "." а можно было поставить и "-", и ":" и т.д. А ещё по хорошему чтобы можно было и Д.ММ, и Д.М писать, и бот всё равно понял какую дату человек написал!
