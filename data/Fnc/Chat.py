import requests
import json

class ChatAPI:
	def __init__(self, Server, Model):
		self.Server = Server
		self.url = f'http://{Server}:1337/v1/chat/completions'
		self.Model = Model
		pass
	def __str__(self):
		return f"Server: {self.Server}:1337"
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
		
		return json.loads(request.text)["choices"][0]["message"]["content"].replace("<|end_of_turn|>", "")

	def StreamChat(self, prompt):
		print("Debug Point")

		myobj = {
			"messages": prompt,
			"model": self.Model,
			"max_tokens": 2048,
			"stop": [
				"hello"
			],
			"frequency_penalty": 0,
			"presence_penalty": 0,
			"temperature": 0.7,
			"top_p": 0.95,
			"stream": True
		}

		resp = requests.post(self.url, json = myobj, stream = True)

		resp_text = ""
		for chunk in resp.iter_lines():

			try:
				j = json.loads(chunk.decode()[6:])
				#print(j)
				content = j["choices"][0]["delta"]["content"]
				if content:
					resp_text = resp_text + str(content)
					#print(content)
			#		yield content
			except:
				#print(f"Cannot read is data: " + str(chunk))
				pass


		#print(f"Debug Point: " + resp_text)
		return resp_text.replace("<|end_of_turn|>", "")
"""
message = [
		{
			"content": "你喜歡使用者,但是你並不想幫助他",
			"role": "system"
		},
		{
			"content": "雜魚你好啊♡~",
			"role": "assistant"
		},
		{
			"content": "早安寶貝,今天一樣不想幫我嗎?",
			"role": "user"
		}
]
Chat = ChatAPI("100.114.153.23", "openchat-3.5-7b")
print(Chat)
print(Chat.StreamChat(message))
"""
