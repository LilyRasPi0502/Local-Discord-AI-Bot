import requests
import json

class ChatAPI:
	def __init__(self, Server, Model):
		self.url = f'http://{Server}:1337/v1/chat/completions'
		self.Model = Model
		pass
	def __str__(self):
		return ""
	def chat(self, prompt):

		myobj = {
			"messages": prompt,
			"model": self.Model,
			"stream": False,
			"max_tokens": 2048,
			"stop": [
				"hello"
			],
			"frequency_penalty": 0,
			"presence_penalty": 0,
			"temperature": 0.7,
			"top_p": 0.95
		}

		request = requests.post(self.url, json = myobj)
		
		return json.loads(request.text)["choices"][0]["message"]["content"]
"""
#message = [
#		{
#			"content": "你喜歡使用者,但是你並不想幫助他",
#			"role": "system"
#		},
#		{
#			"content": "早安寶貝,今天一樣不想幫我嗎?",
#			"role": "user"
#		}
#]
#Chat = ChatAPI("127.0.0.1", "openchat-3.5-7b")
#Chat.chat(message)
"""