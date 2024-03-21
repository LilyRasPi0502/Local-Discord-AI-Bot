import discord

from random import *
from discord.ext import commands
from discord.ext import tasks
from datetime import *
from Fnc.Chat import *

intents		= discord.Intents.default()
intents.message_content = True
intents.members = True

bot_ID = ""
Token = ""
Model = ""	#"openchat-3.5-7b"
Server = ""

class MyBot(commands.Bot):
	
	def __init__(self, command_prefix, intent):
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intent)
		self.Chat = ChatAPI(Server, Model)
		self.Reflash_CharacterAI.start()

	async def on_ready(self):
		self.message1 = f"正在使用身分: {self.user}({self.user.id})"
		self.message2 = f"正在使用身分: {self.user}({self.user.id})"
		print(self.message1)
		await self.change_presence(activity=discord.Activity(name="ゲーム", type=0))

	async def on_message(self, message):
		#排除自己的訊息，避免陷入無限循環
		if str(message.author).find(str(self.user)) != -1:
			return
		Send = True
		#列印接收到的訊息
		print(f"[{Get_Time()}] Get Message from {str(message.guild)}.{str(message.channel)}.{str(message.author.display_name)}: {str(message.content)}")
	
		#聊天程序
		if message.reference is not None:
			ctx = await message.channel.fetch_message(message.reference.message_id)
			if str(ctx.author).find(str(self.user)) != -1:
				await self.chat(message)
				Send = False
		if (message.content.find(bot_ID) != -1) and Send:
			await self.chat(message)
			Send = False

	async def chat(self, message):
		if str(message.content).find("ReAI") != -1:
			await self.CloseSelf()
		async with message.channel.typing():
			f = open("data/CharacterSet.md", "r", encoding="utf-8")
			file = f.read()
			file = file.split("# Character info")[1]
			files = file.split("\n\n# Hello User\n- ")
			file = files[0].replace("\n- ", "")
			Ass = files[1].split("\n- ")
			prompt = [
				{
					"content": f"Time:[{Get_Time()}] {file}",
					"role": "system"
				},
				{
					"content": f"{Ass[randrange(len(Ass))]}",
					"role": "assistant"
				}
			]
			UserMSG = []
	
			if message.reference is not None:
				ctx = await message.channel.fetch_message(message.reference.message_id)
				
				MSG_Serial = [message, ctx]
				MSG_Count = 0
				while MSG_Serial[MSG_Count].reference is not None:
					MSG_Serial.append(await MSG_Serial[MSG_Count].channel.fetch_message(MSG_Serial[MSG_Count].reference.message_id))
					MSG_Count = MSG_Count + 1
				for MSG in MSG_Serial:
					if str(MSG.author).find(str(self.user)) != -1:
						UserMSG.append({"content": MSG.content, "role": "assistant"})
					else:
						UserMSG.append({"content": f"{str(MSG.guild)}.{str(MSG.channel)}{str(MSG.author.display_name)}： {MSG.content}", "role": "user"})	
	
			else:
				UserMSG.append({"content": f"{str(message.guild)}.{str(message.channel)}{str(message.author.display_name)}： {message.content}", "role": "user"})	
	
			UserMSG.reverse()
			prompt = prompt + UserMSG
			#print(prompt)
			Str = self.Chat.chat(prompt)
			await message.reply(Str)
			print(f"[{Get_Time()}] Reply message to {str(message.guild)}.{str(message.channel)}.{message.author.display_name}: {str(Str)}")
		
	

	utc = timezone.utc
	times = [
		time(hour=0, tzinfo=utc),
		time(hour=8, tzinfo=utc),
		time(hour=16, tzinfo=utc)
	]
	#Reflash CharacterAI
	@tasks.loop(time=times)
	async def Reflash_CharacterAI(self):
		await self.CloseSelf()

	async def CloseSelf(self):
		try:
			await self.close()
		except:
			pass
		finally:
			exit()
	

def getSetting():
	global bot_ID
	global Token
	global Model
	global Server
	f = open("data/CharacterSet.md", "r", encoding="utf-8")
	file = f.read()
	file = file.replace("# Discord API setting", "")
	file = file.replace("\n", "")
	Setting= file.split("# Character info")
	Setting = Setting[0].split("- ")
	Token = Setting[2]
	bot_ID = Setting[4]
	Model = Setting[6]
	Server = Setting[8]
	f.close()
	del file, Setting

def bot1():
	getSetting()
	bot = MyBot(command_prefix="/", intent=intents)
	bot.run(Token)

	

#獲取時間
def Get_Time():
  
	dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
	dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

	#timezone_TW = pytz.timezone('ROC')
	#now = datetime.now(timezone_TW)
	return dt2.strftime("%Y-%m-%d %H:%M:%S")

bot1()