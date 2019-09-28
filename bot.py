from PIL import Image
import itchat, time
from itchat.content import *
import json

import pasteFlag 

from io import BytesIO

# use local flag image
pasteFlag.set_local_flag("./tmp/flag.jpg")


HEAD_FILE = "./tmp/head.jpg"
OK_FILE = "./tmp/ok.jpg"


@itchat.msg_register([PICTURE],isGroupChat = True)
def download_files(msg):
    global OK_FILE
    global HEAD_FILE

    if msg.User["NickName"] != "祖国万岁" and msg.User["NickName"] != "test" :
        return

    msg.download(HEAD_FILE)
    
    headImg = Image.open(HEAD_FILE)

    pasteFlag.add_flag(img = headImg).save(OK_FILE)
    itchat.send_image(OK_FILE, toUserName=msg.User["UserName"])
    
    return  u'@%s' % (msg.actualNickName)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):

    global OK_FILE
    global HEAD_FILE

    # chatroom filter
    if msg.User["NickName"] != "祖国万岁" and msg.User["NickName"] != "test" :
        return
    
    # message filter
    if msg.text != "祖国万岁":
        return "@{}\u2005发送任意图片，你会得到加了红旗的头像。请不要发无关的信息，打扰其他人。".format(msg.actualNickName)

    print(json.dumps(msg))
    
    #itchat.get_head_img(userName=msg["ActualUserName"], picDir = OK_FILE)
    head = itchat.get_head_img(userName=msg["ActualUserName"])

    #return "%s 我们还不是好友，您需要将头像发给我，才能加红旗。".format(msg.actualNickName)
    if str(type(head)) != "<class 'bytes'>":
        print(json.dumps(head))
        return "@{}\u2005你需要将图片发到群里，才能加红旗。".format(msg.actualNickName)

    byte_stream = BytesIO(head)
    headImg = Image.open(byte_stream)

    pasteFlag.add_flag(img = headImg).save(OK_FILE)
    itchat.send_image(OK_FILE, toUserName=msg.User["UserName"])
    
    return  u'@%s' % (msg.actualNickName)

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run(True)
