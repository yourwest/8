__author__ = 'angelinaprisyazhnaya'

import re
import csv

features = []
example = 'мне нужна двухкомнатная квартира площ. 60 кв. м. от 3000000 рублей'

flats_list = open('2016-06-14 Best_2.csv', 'r', encoding='utf8', errors='ignore')
flats_list = flats_list.read()


def find_rooms_number(query):
    rooms = re.compile('(\\d|\\w+)-?\\w?х?\\s?комн', flags=re.I)
    one_room = re.compile('1|одн(а|у|ой?)', flags=re.I)
    two_rooms = re.compile('2|дв(е|у(х|мя?))', flags=re.I)
    three_rooms = re.compile('3|тр(и|(е|ё)(х|м)|емя)', flags=re.I)
    four_rooms = re.compile('4|четыр(е|(е|ё)(х|м)|ьмя)', flags=re.I)
    studio = re.compile('студи(я|и|ю|ей)')
    find = rooms.search(query)
    room_number = find.group(1)

    if one_room.search(room_number) is not None:
        number = '1'
    elif two_rooms.search(room_number) is not None:
        number = '2'
    elif three_rooms.search(room_number) is not None:
        number = '3'
    elif four_rooms.search(room_number) is not None:
        number = '4'
    elif studio.search(query) is not None:
        number = 'ст'
    else:
        number = '0'

    return number


def find_square(query):
    min_square = 0.0
    max_square = 10000.0
    square = re.compile('\\bплощ(адью?)?\.?\\s(\\d+?(,|\.)?\\d+?)', flags=re.I)
    find = square.search(query)
    if find is not None:
        number = float(find.group(2).replace(',', '.'))
        min_square = number - 10
        max_square = number + 10
    return min_square, max_square


def find_price(query):
    min_price = 0.0
    max_price = 1000000000.0
    price_from_to = re.compile('от\\s(\\d+?(,|\.)?(\\d+?)?)\\sдо\\s(\\d+?(,|\.)?(\\d+?)?)\\s(млн|мил)', flags=re.I)
    price = re.compile('(\\w+?)\\s(\\d+?(,|\.)?(\\d+?)?)\\s(млн|мил)', flags=re.I)
    price_full = re.compile('(\\w+?)\\s(\\d{7,11})')
    price_full_from_to = re.compile('от\\s(\\d{7,11})\\sдо\\s(\\d{7,11})')
    find = price_from_to.search(query)
    find_2 = price.search(query)
    find_3 = price_full.search(query)
    find_4 = price_full_from_to.search(query)

    if find_4 is not None:
        min_price = float(find.group(1))
        max_price = float(find.group(4))

    elif find_3 is not None:
        if find_3.group(1) == 'от':
            min_price = float(find_3.group(2))
        elif find_3.group(1) == 'до':
            max_price = float(find_3.group(2))
        else:
            max_price = float(find_3.group(2)) + 200000
            min_price = float(find_3.group(2)) - 200000

    elif find is not None:
        min_price = float(find.group(1)) * 1000000
        max_price = float(find.group(4)) * 1000000

    elif find_2 is not None:
        if find_2.group(1) == 'от':
            min_price = float(find_2.group(2)) * 1000000
        elif find_2.group(1) == 'до':
            max_price = float(find_2.group(2)) * 1000000
        else:
            max_price = float(find_2.group(2)) * 1000000 + 200000
            min_price = float(find_2.group(2)) * 1000000 - 200000
    return min_price, max_price


features.append(find_rooms_number(example))
features.append(find_square(example))
features.append(find_price(example))


def search_flats(parameters, flats):
    csv_iter = csv.reader(flats.split('\n'), delimiter=';')
    next(csv_iter)
    for row in csv_iter:
        if row[1] == parameters[0] or row[1] == '0':
            if parameters[1][0] < float(row[2].replace(',', '.')) < parameters[1][1]:
                if parameters[2][0] < float(row[4].replace(',', '.')) < parameters[2][1]:
                    print(row[5])


search_flats(features, flats_list)
