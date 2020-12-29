# WoT Blitz RU Api for Python

Давайте я Вам расскажу как использовать эту библиотеку.

Для начала импортируйте её в Ваш код - 
```python
from wotblitzpyapi import BlitzModuleApiPy
```
Дальше нужно классу BlitzModuleApiPy дать короткое название для удобства - 
```python
wb = BlitzModuleApiPy('Ваш_api_токен')
```
Ну а теперь самое главное, работа с методами. Создадим константу которая будет возвращать данные о 
игроке ksvarog200421_21 (Можно отправлять неполный никнейм, но тогда есть шанс получить большой список 
игроков) -
```python
player = wb.search_player_func('ksvarog200421_21', 10)
```
(Никнейм, максимум игроков в списке).

А как же нам теперь разобрать ответ?
Очень просто. Если нужно узнать сколько игроков было найдено по запросу - 
```python
print(player[0])
```
Ну если, Вам нужно получить информацию о самих игроках из списка, то (Игроки начинуються с индекса 1) -
```python
print(player[1]['nickname'])
```
- вернётся никнейм
Вот пример получения никнейма и ID игрока -
```python
print(f'Имя игрока - {player[1]['nickname']}\nНомер аккаунта игрока - {player[1]['account_id']}')
```
Возможно у Вас возник вопрос, как узнать сколько игроков в списке. Это просто, нужно узнать длину списка - len(player) - если было 
найдено 10 игроков, то вернётся цифра 11, не забываем и числе найденный игроков. Тоисть берём len(player) - 1 (Длина списка минус 1), и получаем
кол-во игроков в списке.

```python
from wotblitzpyapi import BlitzModuleApiPy

wb = BlitzModuleApiPy('e067c6e14dea6dd648fb0bc6d7c4d73d')

player = wb.search_player_func('ksvarog200421_21', 10)
player_ = wb.search_player_id_func(str(player[1]['account_id']), test = True)

print(player_)

"""

['97941296', '30-09-2018 10:02:16', '29-12-2020 15:45:39', '29-12-2020 15:03:09', 'ksvarog200421_21', '1998', '3361', '13031', '1050', '1948', '9745', '1028', '1200', '1258', '2243', '1472655', '2010693', '6', '18187', '217', '851656', '649', '696', '1634']

"""

# Тестовый режим

from wotblitzpyapi import BlitzModuleApiPy

wb = BlitzModuleApiPy('e067c6e14dea6dd648fb0bc6d7c4d73d')

player = wb.search_player_func('ksvarog200421_21', 10)
player_ = wb.search_player_id_func(str(player[1]['account_id']), test = True)

print(player_)

"""

account_id: 97941296
created_at: 1538301736
updated_at: 1609256739
last_battle_time: 1609254189
nickname: ksvarog200421_21
spotted: 1998
max_frags_tank_id: 3361
hits: 13031
frags: 1050
max_xp: 1948
max_xp_tank_id: 9745
wins: 1028
losses: 1200
capture_points: 1258
battles: 2243
damage_dealt: 1472655
damage_received: 2010693
max_frags: 6
shots: 18187
frags8p: 217
xp: 851656
win_and_survived: 649
survived_battles: 696
dropped_capture_points: 1634
['97941296', '30-09-2018 10:02:16', '29-12-2020 15:45:39', '29-12-2020 15:03:09', 'ksvarog200421_21', '1998', '3361', '13031', '1050', '1948', '9745', '1028', '1200', '1258', '2243', '1472655', '2010693', '6', '18187', '217', '851656', '649', '696', '1634']

"""
```
