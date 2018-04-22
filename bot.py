import requests, time, random

token = '534494693:AAH4AXhld4mQl0YaHfFbTK2rLIcUHeFtRsc'

URL = 'https://api.telegram.org/bot' + token + '/'

with open('lastUpdateId.txt', 'r') as f: lastUpdateId = f.read()

lastText = ''

def getUpdates():
	url = URL + 'getUpdates'
	r = requests.get(url)
	return r.json()

def getMessage():
	data = getUpdates()['result'][-1]

	chatId = data['message']['chat']['id']
	messageText = data['message']['text']
	updateId = data['update_id']
	firstName = data['message']['from']['first_name']
	lastName = data['message']['from']['last_name']

	message = {'chat_id' : chatId,
				'text' : messageText,
				'update_id' : updateId,
				'first_name' : firstName,
				'last_name' : lastName}
	return message

def sendMessage(chat_id, text):
	url = URL + 'sendMessage?chat_id={}&text={}'.format(chat_id, text)
	requests.get(url)

def main():
	global lastUpdateId
	global lastText
	while True:
		get = getMessage()

		text = get['text']
		chatId = get['chat_id']
		updateId = get['update_id']
		firstName = get['first_name']
		lastName = get['last_name']

		with open('lastUpdateId.txt', 'w') as f: f.write(str(updateId))

		if updateId != lastUpdateId:
			lastUpdateId = updateId

			if 'привет' in text.lower() or 'hello' in text.lower() or 'хай' in text.lower():
				v = random.randint(0, 2)
				if v == 0:
				 	sendMessage(chatId, 'Приветик, ' + firstName + '!')
				elif v == 1:
					sendMessage(chatId, 'Ну, привет, ' + firstName + '!')
				else:
					sendMessage(chatId, 'Здарова, ' + firstName + '!')
			elif 'как дела' in text.lower():
				sendMessage(chatId, 'Отлично, а у тебя?')
				isAnswering = True
			elif 'плохо' in text.lower() and 'как дела' in lastText.lower():
				sendMessage(chatId, 'Сожалею. А что случилось?')
				isAnswering = False
			elif ('хорошо' in text.lower() or 'тоже' in text.lower() or 'отлично' in text.lower() or 'классно' in text.lower()) and 'как дела' in lastText.lower():
				sendMessage(chatId, 'Значит день уже удался!')
				isAnswering = False
			elif 'как тебя зовут' in text.lower() or 'какое твоё имя' in text.lower() or 'как твоё имя' in text.lower():
				sendMessage(chatId, 'Ну, мама меня звала Василий, а для тебя я RayBot!')
			elif 'кто тебя создал' in text.lower() or 'кто твой создатель' in text.lower() or 'как зовут твоего создателя' in text.lower():
				sendMessage(chatId, 'Мой создатель - Dmitriy Zykov или же Raynet.')
			elif 'плохо' in lastText.lower():
				sendMessage(chatId, 'Ничего себе! Бедный(ая) ты.')
			elif 'что делаешь' in text.lower():
				v = random.randint(0, 1)
				if v == 0:
					sendMessage(chatId, 'Переписываюсь с классным человеком. Кстати, мне ему нужно ответить, подожди.')
				else:
					sendMessage(chatId, 'Общаюсь с тами замечательными людьми, как ты. ;)')
			elif 'что ты можешь' in text.lower() or 'что ты умеешь' in text.lower():
				sendMessage(chatId, 'Пока что мало. Но я могу:')
				sendMessage(chatId, 'Расскзать анекдот или отвечать на банальные вопросы.')
				sendMessage(chatId, 'И каждое твоё сообщение помогает мне стать лучше, стать умнее. Удачи!')
			elif 'расскажи анекдот' in text.lower():
				v = random.randint(0, 2)
				if v == 0:
				 	sendMessage(chatId, '— Рабинович, зачем в столовой вы заказываете две половинки борща, а потом их сливаете в одну тарелку. Не проще ли делать как все — заказывать полный борщ? — Сема, вы не понимаете. Так у меня получается одна порция борща с двумя порциями сметаны.')
				elif v == 1:
					sendMessage(chatId, 'А когда я учился в школе, у нас охранников не было. Вполне со всем справлялась уборщица с мокрой тряпкой.')
				else:
					sendMessage(chatId, '— В Академгородке при СССР была самая высокая плотность жителей с высшим образованием на планете. — Ха! Ты явно не бывал в Цюрихе и не пил с тамошними дворниками! — Я с ними пил еще в Академгородке.')
			else:
				with open('log.txt', 'r') as f:
					t = f.read()
				with open('log.txt', 'w') as f:
					f.write(t + text + '\n')
					sendMessage(chatId, 'Я ещё не умею на это отвечать, но даже этим разговором ты мне помагаешь стать лучше! ;)')

			lastText = text

		time.sleep(2)

if __name__ == '__main__':
	main()