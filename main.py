#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE

import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import tgcrypto
import pyrogram
from pyrogram import Client, filters
import time
from pyrogram.types import User, Message
from p_bar import progress_bar
import time
from subprocess import getstatusoutput
import logging
import os
import re
import simplejson



#from jinja2 import Template
# from details import api_id, api_hash, bot_token
from urllib.parse import unquote

# import requests
# bot = Client(
#     "bot",
#     api_id=api_id,
#     api_hash=api_hash,
#     bot_token=bot_token)



bot = Client("CW", bot_token=os.environ.get("BOT_TOKEN"), api_id=int(os.environ.get("API_ID")), api_hash=os.environ.get("API_HASH"))

logger = logging.getLogger()

#rwa_url="https://rozgarapinew.teachx.in/post/login"

hdr = {"Auth-Key": "appxapi",
       "User-Id": "-2",
       "Authorization": "",
       "User_app_category": "",
       "Language": "en",
       "Content-Type": "application/x-www-form-urlencoded",
       "Content-Length": "227",
       "Accept-Encoding": "gzip, deflate",
       "User-Agent": "okhttp/4.9.1"
       }

cour_url = "https://rozgarapinew.teachx.in/get/mycourse?userid="

sub_id_url="https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid="

data = {"email": "", "password": ""}

@bot.on_message(filters.command(["login"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    data["email"] = raw_text.split("*")[0]
    data["password"] = raw_text.split("*")[1]

    res = requests.post("https://rozgarapinew.teachx.in/post/login", data=data, headers=hdr).json()
    await m.reply_text(res)
    userid = res["data"]["userid"]
    token = res["data"]["token"]
    hdr1 = {
       "Host": "rozgarapinew.teachx.in",
       "Client-Service": "Appx",
       "Auth-Key": "appxapi",
       "User-Id": userid,
       "Authorization": token
       }
    res1 = requests.get("https://rozgarapinew.teachx.in/get/mycourse?userid="+userid, headers=hdr1)
    b_data = res1.json()['data']
    cool=""
    for data in b_data:
        FFF = "**BATCH-ID - BATCH NAME - INSTRUCTOR**"
        aa = f" ```{data['id']}```      - **{data['course_name']}**\n\n"
        # aa=f"**Batch Name -** {data['batchName']}\n**Batch ID -** ```{data['id']}```\n**By -** {data['instructorName']}\n\n"
        if len(f'{cool}{aa}') > 4096:
           print(aa)
           cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1=await m.reply_text("**Now send the Batch ID to Download** : ")


    res2 = requests.get("https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid="+editable1, headers=hdr1)
    await m.reply_text(res2)
    b_data1 = res2.json()['data']
    await m.reply_text(b_data1)
    SubiD=await m.reply_text("Enter the Subject Id Show in above Response")
    Class_url = "https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=16&subjectid=25"

    res3 = requests.get("https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid="+editable1,"&subjectid="+SubiD, headers=hdr1)
    #print(res3)
    b_data2 = res3.json()['data']
    await m.reply_text(b_data2)

    await m.reply_text('Done')   

       
            


