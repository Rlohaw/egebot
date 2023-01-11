import re

import mysql.connector
import asyncio
import numpy as np
import telebot.types
import bs4


class DataBase:
    def __init__(self, host='localhost', user='root', password='75645', database='ege'):
        self.mydb = mysql.connector.connect(host=host,
                                            user=user,
                                            password=password,
                                            database=database)
        self.cursor = self.mydb.cursor()

    def create_tables(self):
        db = DataBase()
        alf = 'abcdefghijklmnopqrstuvwxyz'
        alf = [i for i in alf] + [i * 2 for i in alf]
        db.cursor.execute(f'''create table math(num int PRIMARY KEY AUTO_INCREMENT, {' int, '.join(alf[0:18])} int)''')
        db.cursor.execute(f'''create table ru(num int PRIMARY KEY AUTO_INCREMENT, {' int, '.join(alf[0:27])} int)''')
        db.cursor.execute(f'''create table inf(num int PRIMARY KEY AUTO_INCREMENT, {' int, '.join(alf[0:27])} int)''')
        self.mydb.commit()


class Bot:
    def __init__(self):
        self.__token = '5775142133:AAHBKvFJ-uj_M70AZmcLl_ungspCgNPnZuc'
        self.__bot = telebot.TeleBot(self.__token)

        @self.__bot.message_handler(commands=['start'])
        def start(msg):
            try:
                self.verif(msg)
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                sp = ['/add', '/get']
                sp = map(lambda x: telebot.types.KeyboardButton(x), sp)
                markup.add(*sp)
                self.__bot.send_message(msg.chat.id, f"Hello Admin", reply_markup=markup)
            except Exception as e:
                self.__bot.send_message(msg.chat.id, str(e))

        @self.__bot.message_handler(commands=['add'])
        def add(msg):
            try:
                self.verif(msg)
                data = self.__bot.send_message(msg.chat.id, 'insert data:')
                self.__bot.register_next_step_handler(data, results)
            except Exception as e:
                self.__bot.send_message(msg.chat.id, str(e))

        def results(msg):
            try:
                self.verif(msg)
                db = DataBase()
                profile = re.findall(r'(\w+)\s', msg.text)[0].lower()
                res = re.findall(r'\d', msg.text)
                alf = 'abcdefghijklmnopqrstuvwxyz'
                alf = [i for i in alf] + [i * 2 for i in alf]
                alf = alf[0:27] if profile == 'inf' or profile == 'ru' else alf[0:18]
                db.cursor.execute(f'''insert into {profile} ({', '.join(alf)}) values ({', '.join(res)})''')
                db.mydb.commit()
                self.__bot.send_message(msg.chat.id, 'Success!')
            except Exception as e:
                self.__bot.send_message(msg.chat.id, str(e))

        @self.__bot.message_handler(commands=['get'])
        def get(msg):
            try:
                self.verif(msg)
                data = self.__bot.send_message(msg.chat.id, 'insert data:')
                self.__bot.register_next_step_handler(data, stats)
            except Exception as e:
                self.__bot.send_message(msg.chat.id, str(e))

        def stats(msg):
            try:
                self.verif(msg)
                db = DataBase()
                txt = re.findall(r'\w+', msg.text.lower())
                db.cursor.execute(f'select * from {txt[0]}')
                mass = [list(i)[1:] for i in db.cursor.fetchall()][-6:]
                shp = 27 if txt[0] in ('ru', 'inf') else 18
                arr = np.array(mass)
                arr = np.rot90(arr, k=-1)
                res = np.array([sum(i) / len(i)for i in arr], dtype='f')
                dct = self.get_parts()[txt[0]]
                fin = [
                    f"{dct[i]}: {res[i]}" + '‼' if res[i] < 0.75 else f"{dct[i]}: {res[i]}" for i in range(shp)]
                if len(txt) == 2 and txt[1] == '1':
                    fin = '\n'.join(filter(lambda x: x.endswith('‼'), fin))
                else:
                    fin = '\n'.join(fin)
                r1 = sum(res)
                r2 = 31 if txt[0] == 'math' else 58 if txt[0] == 'ru' else 29
                self.__bot.send_message(msg.chat.id, fin + f'\n\nTotal:{r1}|||{r2}|||{round(r1 / r2, 3)}')

            except Exception as e:
                self.__bot.send_message(msg.chat.id, str(e))

    @classmethod
    def get_parts(cls):
        dct = {'ru': ['1: Средства связи предложений в тексте', '2: Определение лексического значения слова',
                      '3: Информационная обработка текстов различных стилей и жанров', '4: Постановка ударения',
                      '5: Употребление паронимов', '6: Лексические нормы',
                      '7: Морфологические нормы (образование форм слова)',
                      '8: Синтаксические нормы. Нормы согласования. Нормы управления', '9: Правописание корней',
                      '10: Правописание приставок', '11: Правописание суффиксов (кроме -Н-/-НН-)',
                      '12: Правописание личных окончаний глаголов и суффиксов причастий', '13: Правописание НЕ и НИ',
                      '14: Слитное, дефисное, раздельное написание слов', '15: Правописание -Н- и -НН- в суффиксах',
                      '16: Пунктуация в сложносочиненном предложении и в предложении с однородными членами',
                      '17: Знаки препинания в предложениях с обособленными членами',
                      '18: Знаки препинания при словах и конструкциях, не связанных с членами предложения',
                      '19: Знаки препинания в сложноподчиненном предложении',
                      '20: Знаки препинания в сложных предложениях с разными видами связи',
                      '21: Постановка знаков препинания в различных случаях',
                      '22: Смысловая и композиционная целостность текста', '23: Функционально-смысловые типы речи',
                      '24: Лексическое значение слова', '25: Средства связи предложений в тексте',
                      '26: Языковые средства выразительности', '27: Сочинение'],
               'inf': ['1: Анализ информационных моделей', '2: Построение таблиц истинности логических выражений',
                       '3: Поиск информации в реляционных базах данных', '4: Кодирование и декодирование информации',
                       '5: Анализ и построение алгоритмов для исполнителей',
                       '6: Определение результатов работы простейших алгоритмов',
                       '7: Кодирование и декодирование информации. Передача информации',
                       '8: Перебор слов и системы счисления', '9: Работа с таблицами',
                       '10: Поиск символов в текстовом редакторе', '11: Вычисление количества информации',
                       '12: Выполнение алгоритмов для исполнителей', '13: Поиск путей в графе',
                       '14: Кодирование чисел. Системы счисления', '15: Преобразование логических выражений',
                       '16: Рекурсивные алгоритмы', '17: Обработки числовой последовательности',
                       '18: Робот-сборщик монет',
                       '19: Выигрышная стратегия. Задание 1', '20: Выигрышная стратегия. Задание 2',
                       '21: Выигрышная стратегия. Задание 3', '22: Многопроцессорные системы',
                       '23: Оператор присваивания и ветвления. Перебор вариантов, построение дерева',
                       '24: Обработка символьных строк', '25: Обработка целочисленной информации',
                       '26: Обработка целочисленной информации', '27: Программирование',
                       '28: Анализ информационных моделей'],
               'math': ['1: Планиметрия', '2: Стереометрия', '3: Начала теории вероятностей',
                        '4: Вероятности сложных событий', '5: Простейшие уравнения', '6: Вычисления и преобразования',
                        '7: Производная и первообразная', '8: Задачи с прикладным содержанием', '9: Текстовые задачи',
                        '10: Графики функций', '11: Наибольшее и наименьшее значение функций', '12: Уравнения',
                        '13: Стереометрическая задача', '14: Неравенства', '15: Финансовая математика',
                        '16: Планиметрическая задача', '17: Задача с параметром', '18: Числа и их свойства']}
        return dct

    @classmethod
    def verif(cls, msg):
        assert msg.chat.id == 5463317462, 'no access'

    def run(self):
        while True:
            try:
                asyncio.run(self.__bot.polling(none_stop=True))
            except Exception as e:
                print(e)


class Results:
    def __init__(self, matrix):
        pass


if __name__ == '__main__':
    bot = Bot()
    bot.run()
