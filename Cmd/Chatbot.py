import openai

openai.api_key = "sk-"

def ChatBot(msg, msg_list):
	response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",
	messages=msg_list)
	reply = response["choices"][0]["message"]["content"]
	return reply