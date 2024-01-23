import openai

openai.api_key = "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"

def ChatBot(msg, msg_list):
	messages.append({"role": "user", "content": msg})
	response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",
	messages=msg_list)
	reply = response["choices"][0]["message"]["content"]
	return reply