# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  The third-party libraries and their versions information has shown below when it run success, 
#  and you can install them one by one or copy them to a new TXT file with PIP at one time:：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os


STATUS_FIRST_FRAME = 0  # The identity of the first frame
STATUS_CONTINUE_FRAME = 1  # Intermediate frame identification
STATUS_LAST_FRAME = 2  # The identity of the last frame, that means the end of audio transmission


class Ws_Param(object):
    # Initializing
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # common
        self.CommonArgs = {"app_id": self.APPID}
        # business
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "yingying", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    def create_url(self):
        url = 'wss://tts-api-sg.xf-yun.com/v2/tts'
        # Generating a timestamp in RFC1123 format
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # Combining Strings
        signature_origin = "host: " + "tts-api-sg.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # Hmac-sha256 is used for encryption
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # Combines the request of authentication parameters into a dictionary
        v = {
            "authorization": authorization,
            "date": date,
            "host": "tts-api-sg.xf-yun.com"
        }
        # Concatenate the authentication parameters and generate the URL
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # print('websocket url :', url)
        return url

def on_message(ws, message):
    try:
        message =json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:

            with open('./demo.pcm', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)



# the error websocket message has been received and handling 
def on_error(ws, error):
    print("### error:", error)


# the closed websocket message has been received and handling 
def on_close(ws):
    print("### closed ###")


# The connecting websocket message has been received and handling 
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        print("------>Start sending data")
        ws.send(d)
        if os.path.exists('./demo.pcm'):
            os.remove('./demo.pcm')

    thread.start_new_thread(run, ())


def Voice(txt):
	if __name__ == "__main__":
	   # Access from the Console to find TTS webapi 
	   wsParam = Ws_Param(APPID='ga2b2603', APIKey='714ab90dba05d03ec7f8c72eeaba2d84',
	   APISecret='e9025d0fb8053cdf9f7cc14b2c59006e', Text=txt)
	   websocket.enableTrace(False)
	   wsUrl = wsParam.create_url()
	   ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
	   ws.on_open = on_open
	   ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})