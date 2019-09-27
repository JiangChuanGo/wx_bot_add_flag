import itchat, time
from itchat.content import *
import json

import pasteFlag 

# use local flag image
pasteFlag.set_local_flag("./tmp/flag.jpg")


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
	HEAD_FILE = "./tmp/head.jpg"
	OK_FILE = "./tmp/ok.jpg"

	# chatroom filter
	if msg.User["NickName"] != "祖国万岁":
		return

	# message filter
	if msg.text != "祖国万岁":
		return

	head = itchat.get_head_img(userName=msg["ActualUserName"])
	fileImage = open(HEAD_FILE,'wb')
	fileImage.write(head)
	fileImage.close()

	pasteFlag.add_flag(HEAD_FILE).save(OK_FILE)
	itchat.send_image(OK_FILE, toUserName=msg.User["UserName"])

	return  u'@%s\u2005' % (msg.actualNickName)

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run(True)
