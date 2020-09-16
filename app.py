from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

import gspread
from oauth2client.service_account import ServiceAccountCredentials



scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)

client = gspread.authorize(creds)
sheet = client.open("test_1_db").sheet1


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate




app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token
line_bot_api = LineBotApi('MBzS1ky44RKM/kfRt70FjKCXIcjdPtbPTirlnrBcllV3dlJL+j5cHCk/rfEWHM/Mnnfx2aak3NcWJzSVk/AQ9Fh2wu+YrldRU7uMowmsTbLoMzmYqLx4mLb5iXNSxY8fE5el4n071I8LFQCOI17e8AdB04t89/1O/w1cDnyilFU=')

# Channel Secret
handler = WebhookHandler('8d52e9a3b33bafa81896c30ee33144ad')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def next_available_row(sheet):
    try:
        str_list = list(filter(None, sheet.col_values(1)))
        return len(str_list)+1
   except:
        return 0

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
@static_vars(counter=0)

def handle_message(event):

    msg = event.message.text
    user_id = event.source.user_id
    if 'test1' in msg:
        message = TextSendMessage(text= 'Hello Sally')
        line_bot_api.reply_message(event.reply_token, message)
    if 'test2' in msg:
        message = TextSendMessage(text= str(sheet.cell(1,2).value))
        line_bot_api.reply_message(event.reply_token, message)
    if 'test3' in msg:
        row = next_available_row(sheet)
        sheet.update_cell(row, 1, row-1)
        sheet.update_cell(row, 2, '測試經度')
        sheet.update_cell(row, 3, '測試緯度') 
        message = TextSendMessage(text= '已寫入'+str(row))
        line_bot_api.reply_message(event.reply_token, message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
