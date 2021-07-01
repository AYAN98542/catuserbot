from telethon.tl.types import ChannelParticipantsAdmins as cp
from . import catub, bot,edit_delete, edit_or_reply, reply_id 
from userbot.utils import register
from time import sleep

plugin_category = "extra"


@catub.cat_cmd(
    pattern="tag (.*)",
    command=("tag", plugin_category),
    info={
        "header": "Tag everyone in a group.",
        "description": "Mention everyone in the group (with custom text)",
        "options": "If you want text along with tags, use .tag text",
        "usage": [
            "{tr}tag",
            "{tr}tag <text>",
        ],
        "examples": "{tr}tag Hello",
      
    },
)
async def _(tag):
	"To tag everyone in a group."

	if tag.pattern_match.group(1):
		tagall = tag.pattern_match.group(1)
	else:
		tagall = ""
	prsn1 = await reply_id(tag)
	chat = await tag.get_input_chat()
	a_=0
	await tag.delete()
	async for i in bot.iter_participants(chat):
		if a_ == 500:
			break
		a_+=5
		await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, tagall), reply_to = prsn1)
		sleep(0.1)
		
				
@catub.cat_cmd(
    pattern="tagadmin (.*)",
    command=("tagadmin", plugin_category),
    info={
        "header": "Tag all admins in a group.",
        "description": "Mention all the admins in the group (with custom text)",
        "options": "If you want text along with tags, use .tagadmin text",
        "usage": [
            "{tr}tagadmin",
            "{tr}tagadmin <text>",
        ],
        "examples": "{tr}tagadmin Spam",
      
    },
)
async def _(tagadmin):
	"To tag every admin in a group"
	
	if tagadmin.pattern_match.group(1):
		tagtxt = tagadmin.pattern_match.group(1)
	else:
		tagtxt = ""
	prsn = await reply_id(tagadmin)
	chat = await tagadmin.get_input_chat()
	a_=0
	await tagadmin.delete()
	async for i in bot.iter_participants(chat, filter=cp):
		if a_ == 500:
			break
		a_+=5
		await tagadmin.client.send_message(tagadmin.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, tagtxt), reply_to = prsn)
		sleep(1.5)
		
		