from datetime import datetime
from json import loads
from logging import INFO, basicConfig, error, info, warning

from requests import get
from requests.exceptions import ConnectionError


# Звернення до "Професіоналів"
# В цьому коді я часто використовую str, int, bool, float, list і їм подібні.
# Меню плювати чи це гарно і правильно. Мені просто так простіше орієнтуватися в коді.
# І ще... Всі коментарі в цьому проекті, я пишу українською.
basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=INFO)

def json_check_func(json_):
	# Я не знаю як пояснити присутність ціїє функції. Мені так подобається.
	if json_['status'] == 'ok': return True
	elif json_['status'] == 'error' and json_['error']['code'] == 407:
		error('func json_check_func - error code 407')
		return False
	else: return False # Усі інші випадки

def get_price(tank_status, cost):
	try:
		if bool(tank_status): return cost['price_gold'] # Якщо танк преміумний
		else: return cost['price_credit'] # Інакше перевіряємо ціну в сріблі
	except: pass

def get_price_type(tank_status, cost):
	# Передається оригінальне булентне значення
	if bool(tank_status): return 'Premium'
	else: return 'Standart'

def tank_type(tank_):
	# Тяжкий - 0, Середній - 1, Легкий - 2, ПТ-САУ - 3
	tank_types = ['heavyTank', 'mediumTank', 'lightTank', 'AT-SPG',]
	step = 0
	for i in tank_types:
		if i == tank_: return step
		step += 1

def tank_nation(tank_):
	# США - 0, Франція - 1, СРСР - 2, Китай - 3, Британія - 4,
	# Японія - 5, Німеччина - 6, Інші (спеціальні) - 7, Європа - 8
	tank_nations = ['usa', 'france', 'ussr', 'china', 'uk', 'japan',
		'germany', 'other', 'european',]
	step = 0
	for i in tank_nations:
		if i == tank_: return step
		step += 1

class BlitzModuleApiPy:
	
	def __init__(self, api_token, api_host = 'https://api.wotblitz.ru/wotb/'):
		self.api_token = str(api_token)
		self.api_host = str(api_host)
		info('BlitzModuleApiPy successfully inited.')

	def search_player_func(self, player_name, limit = 100):
		"""
		
		example find player:
		search_player_func('player_name', limit_num)[player_num_in_list][player_index_data]

		get first player name in list:
		search_player_func('player_name', limit_num)[1]['nickname']

		get find players count:
		search_player_func('player_name', limit_num)[0]
		
		"""
		api_addr = self.api_host + 'account/list/'
		continue_ok = connect_ok = True
		if not bool(str(limit).isdigit()):
			continue_ok = False
			error('func search_player_func - limit is num var.')
		if bool(continue_ok):
			params = {
				'application_id': self.api_token,
				'search': str(player_name),
				'limit': int(limit),
			}
			try: response_http__ = get(api_addr, params=params).text
			except ConnectionError: connect_ok = False
			if bool(connect_ok):
				json_resp = loads(str(response_http__))
				if bool(json_check_func(json_resp)):
					# Індекси
					# 0 - Кількість знайдених облікових записів
					# - nickname - Нікнейм гравця
					# - account_id - Номер облікового запису гравця
					players_find = json_resp['meta']['count']
					temp_array = []
					temp_array.append(players_find)
					for i in json_resp['data']: temp_array.append(i)
					return temp_array
				else: error('func search_player_func - error check json response.')
			else: error("func search_player_func - error connect to server Wargaming.")

	def search_player_id_func(self, player_id, unix_time = False, test = False):
		"""
	
		example find user:
		search_player_id_func('user_id', bool_unix_time, bool_test)

		return list:

		account_id
		created_at
		updated_at
		last_battle_time
		nickname
		spotted
		max_frags_tank_id
		hits
		frags
		max_xp
		max_xp_tank_id
		wins
		losses
		capture_points
		battles
		damage_dealt
		damage_received
		max_frags
		shots
		frags8p
		xp
		win_and_survived
		survived_battles
		dropped_capture_points
		
		"""
		api_addr = self.api_host + 'account/info/'
		# Можна отримати інформацію лише за один гравцем
		# Ліміт не задається
		params = {
			'application_id': self.api_token,
			'account_id': str(player_id),
		}
		try: 
			response_http__ = get(api_addr, params=params).text
			connect_ok = True
		except ConnectionError: connect_ok = False
		if bool(connect_ok):
			json_resp = loads(str(response_http__))
			if bool(json_check_func(json_resp)):
				stat_all = json_resp['data'][player_id]['statistics']['all'] # Основна статистика гравця
				stat_ = json_resp['data'][player_id] # Отримуємо всю інформацію про гравця
				step_list = 0
				array_data = []
				array_names = ['account_id', 'created_at', 'updated_at', 'last_battle_time', 'nickname'] # Пізніше список буде очищений
				for i in array_names:
					if bool(test): print(f'{str(array_names[step_list])}: {str(stat_[array_names[step_list]])}')
					if bool(unix_time): array_data.append(str(stat_[array_names[step_list]]))
					else:
						if i != 'account_id' and i != 'nickname': array_data.append(str(
							datetime.utcfromtimestamp(stat_[array_names[step_list]]
						).strftime('%d-%m-%Y %H:%M:%S'))) # День-Місяць-Рік Година:Хвилина:Секунда
						else: array_data.append(str(stat_[array_names[step_list]]))
					step_list += 1
				step_list = 0
				array_names.clear()
				for i in stat_all: array_names.append(i)
				for i in stat_all:
					if bool(test): print(f'{str(array_names[step_list])}: {str(stat_all[array_names[step_list]])}')
					array_data.append(str(stat_all[array_names[step_list]]))
					step_list += 1
				return array_data
			else: error('func search_player_id_func - error check json response.')
		else: error("func search_player_id_func - error connect to server Wargaming.")

		def tank_find(tank_id, many_tanks = False, formatted = False, language = 'ru'):
			"""


			"""
			api_addr = self.api_host + 'encyclopedia/vehicles/'
			if bool(many_tanks): tank_id = ', '.join(tank_id)
			params = {
				'application_id': self.api_token,
				'tank_id': str(tank_id), # Можна передати як число, так і строку
				'language': str(language).lower(), # По стандарту стоїть Російська мова
			}
			try: response_http__ = get(api_addr, params=params).text
			except ConnectionError: connect_ok = False
			if bool(connect_ok):
				json_resp = loads(str(response_http__))
				if bool(json_check_func(json_resp)):
					pass

				else: error('func search_player_func - error check json response.')
			else: error("func search_player_func - error connect to server Wargaming.")

	def __exit__(self):
		pass
