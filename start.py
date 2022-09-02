# (©)Codexbotz
# Zelda-Projects

import asyncio
from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import ADMINS, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, FORCE_MSG, START_MSG, FORCE_SUB_CHANNEL, CHANNEL_ID
from database.sql import add_user, full_userbase, query_msg
from helper_func import decode, get_messages, subscribed, zeldauser

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 ** 2 * 24),
    ("hour", 60 ** 2),
    ("min", 60),
    ("sec", 1),
)

OWNER_CH =[-1001531498594]


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Bot.on_message(filters.command("start") & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    user_name = "@" + message.from_user.username if message.from_user.username else None
    try:
        await add_user(id, user_name)
    except:
        pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except BaseException:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except BaseException:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except BaseException:
                return
        temp_msg = await message.reply("`Tunggu Sebentar...`")
        try:
            messages = await get_messages(client, ids)
        except BaseException:
            await message.reply_text("Telah Terjadi Error 🥺")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name,
                )
            else:
                caption = "" if not msg.caption else msg.caption.html

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
            try:
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            except BaseException:
                pass
    else:
        buttons = [
            [InlineKeyboardButton("ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ", callback_data="about")],
            [
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink),
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink3),
            ],
            [
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink4),
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink5),
            ],
            [
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink6),
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink2),
            ],
            [
                InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close"),
            ],
        ]
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None
                if not message.from_user.username
                else "@" + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
            quote=True,
        )

    return


@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink),
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink3),
        ],
        [
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink4),
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink5),
        ],
        [
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink6),
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close"),
        ],
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ]
        )
    except IndexError:
        pass
    
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None
            if not message.from_user.username
            else "@" + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command("users") & filters.private & filters.user(1977120689))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="`Processing ...`")
    link = await client.export_chat_invite_link(CHANNEL_ID)
    users = await full_userbase()
    await msg.edit(f"{len(users)} Pengguna menggunakan bot ini\n\nDatabase Channel : {link}")
    

@Bot.on_message(filters.command("addusers") & filters.private & filters.user(ADMINS))
async def add_users(client: Bot, message: Message):
    msg = await client.send_message(
        chat_id=message.chat.id, text="`Processing ...`"
    )
    users = await full_userbase()
    await bot.add_chat_members(FORCE_SUB_CHANNEL, [users])
    await msg.edit(f"{len(users)} Pengguna ditambahkan ke Channel")
    

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply(
            "`Broadcasting Message Tunggu Sebentar...`"
        )
        for row in query:
            chat_id = int(row[0])
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except BaseException:
                unsuccessful += 1
            total += 1

        status = f"""<u>Berhasil Broadcast</u>
Jumlah Pengguna: `{total}`
Berhasil: `{successful}`
Gagal: `{unsuccessful}`
Pengguna diblokir: `{blocked}`
Akun Terhapus: `{deleted}`"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(
            "`Gunakan Perintah ini Harus Sambil Reply ke pesan telegram yang ingin di Broadcast.`"
        )
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "PONG!!🏓 \n"
        f"• Pinger - `{delta_ping * 1000:.3f}ms`\n"
        f"• Uptime - `{uptime}`\n"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 Bot Status:\n"
        f"• Uptime: `{uptime}`\n"
        f"• Start Time: `{START_TIME_ISO}`"
    )
 