__author__ = 'angelinaprisyazhnaya'

import re

# Массив с параметрами.
features = []
# Пример запроса.
example = 'мне нужна двухкомнатная квартира площ. 70 кв. м. за 2 миллиона рублей'

# Поиск количества комнат (и числом, и буквами).
def find_rooms_number(query):
    rooms = re.compile('(\\d|\\w+)-?\\w?х?\\s?комн', flags=re.I)
    one_room = re.compile('1|одн(а|у|ой?)', flags=re.I)
    two_rooms = re.compile('2|дв(е|у(х|мя?))', flags=re.I)
    three_rooms = re.compile('3|тр(и|(е|ё)(х|м)|емя)', flags=re.I)
    four_rooms = re.compile('4|четыр(е|(е|ё)(х|м)|ьмя)', flags=re.I)
    find = rooms.search(query)
    room_number = find.group(1)

    if one_room.search(room_number) is not None:
        number = 1
    elif two_rooms.search(room_number) is not None:
        number = 2
    elif three_rooms.search(room_number) is not None:
        number = 3
    elif four_rooms.search(room_number) is not None:
        number = 4
    else:
        number = 0

    return number

# Поиск площади.
def find_square(query):
    square = re.compile('\\bплощ(адью?)?\.?\\s(\\d+?(,|\.)?\\d+?)', flags=re.I)
    find = square.search(query)
    number = float(find.group(2).replace(',', '.'))
    return number

# Поиск цены.
def find_price(query):
    min_price = ''
    max_price = ''
    mean_price = ''
    price_from_to = re.compile('от\\s(\\d+?)\\sдо\\s(\\d+?)\\s(млн|мил)', flags=re.I)
    price = re.compile('(\\w+?)\\s(\\d+?)\\s(млн|мил)', flags=re.I)
    find = price_from_to.search(query)
    find_2 = price.search(query)
    if find is not None:
        min_price = find.group(1)
        max_price = find.group(2)
    elif find_2 is not None:
        if find_2.group(1) == 'от':
            min_price = find_2.group(2)
        elif find_2.group(1) == 'до':
            max_price = find_2.group(2)
        else:
            mean_price = find_2.group(2)

    return min_price, max_price, mean_price


features.append(find_rooms_number(example))
features.append(find_square(example))
features.append(find_price(example))
print(features)
