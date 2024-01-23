from fbchat import Client
from fbchat.models import *
import json
from pathlib import Path
#import commands 
import Cmd.Chatbot as chat
import Cmd.Img_generator as g

msg_list = []

system_msg = ""
messages.append({"role": "system", "content": system_msg})

class MesBot(Client):
    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(', ')[15][14:-1]
            print(msg)
            if ("//video.xx.fbcdn" in msg):
                msg = msg
            else:
                msg = str(message_object).split(', ')[19][20:-1]
        except:
            try:
                msg = str(message_object.text).lower()
                print(msg)
            except:
                pass

        if (author_id != self.uid):
            first_letter = msg.split()[0]
            if  first_letter == prefix:
                msg = msg.replace(prefix, "")
                if "generate" in msg:
                	prompt = msg.replace("generate", "")
                	img_location = str(g.generateImg(prompt))
                	if 'Cmd' not in img_location:
                		self.sendMsg(img_location, thread_id, thread_type)
                	else:
                		text = "Image generated successfully"
                		self.sendImg(img_location, text, thread_id, thread_type)
                		Path(img_location).unlink()
                else:
                	reply = chat.ChatBot(msg)
                	msg_list.append({"role": "assistant", "content": reply})
                	
                	self.sendMsg(reply, thread_id, thread_type)

    def sendMsg(self, reply, thread_id, thread_type):
        self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
        
    def sendImg(self, image_path, reply, thread_id, thread_type):
    	self.sendLocalImage(image_path, message=Message(text=reply), thread_id=thread_id, thread_type=thread_type)

try:
	with open("Cookies.json", 'r') as file:
		session_cookies = json.load(file)
#		session_cookies = {
#		"sb": "'',
#		"fr": "",
#		"c_user": "",
#		"datr":"",
#		"xs": ""
#		}
	with open("Config.json", 'r') as file:
		config = json.load(file)
		prefix = config['prefix']
		
except FileNotFoundError:
	print("Please make sure you've all the files")
	exit()
	
bot = MesBot('EMAIL', 'PASSWORD', session_cookies=session_cookies)
print(bot.isLoggedIn())

try:
    bot.listen()
except:
    bot.listen()