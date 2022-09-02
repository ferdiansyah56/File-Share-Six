# (©)Codexbotz
# Zelda-Projects

import asyncio
import base64
import re
import os

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from config import ADMINS, FORCE_SUB_CHANNEL, FORCE_SUB_GROUP, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, FORCE_SUB_CHANNEL_5

OWNER_CH = int(os.environ.get("OWNER_ID", "-1001531498594"))


async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL:
        return True
    if not FORCE_SUB_CHANNEL_2:
        return True
    if not FORCE_SUB_CHANNEL_3:
        return True
    if not FORCE_SUB_CHANNEL_4:
        return True
    if not FORCE_SUB_CHANNEL_5:
        return True
    if not FORCE_SUB_GROUP:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL, user_id=user_id)
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL_5, user_id=user_id)
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL_4, user_id=user_id)
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL_3, user_id=user_id)
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL_2, user_id=user_id)
        member = await client.get_chat_member(chat_id=FORCE_SUB_GROUP, user_id=user_id)
        # member = await client.get_chat_member(chat_id=OWNER_CH, user_id=user_id)
    except UserNotParticipant:
        return False
        
    # await client.add_chat_members(chat_id=OWNER_CH, user_id=user_id)

    
    return member.status in ["creator", "administrator", "member"]
    
    
async def is_zeldauser(filter, client, update):
    if not OWNER_CH:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=OWNER_CH, user_id=user_id)
    except UserNotParticipant:
        return False
        
    return member.status in ["creator", "administrator", "member"]
    
    
async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    return base64_bytes.decode("ascii")


async def decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    return string_bytes.decode("ascii")


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages : total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except BaseException:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message):
    if (
        message.forward_from_chat
        and message.forward_from_chat.id == client.db_channel.id
    ):
        return message.forward_from_message_id
    elif message.forward_from_chat or message.forward_sender_name or not message.text:
        return 0
    else:
        pattern = "https://t.me/(?:c/)?(.*)/(\\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        elif channel_id == client.db_channel.username:
            return msg_id


subscribed = filters.create(is_subscribed)
zeldauser = filters.create(is_zeldauser)
