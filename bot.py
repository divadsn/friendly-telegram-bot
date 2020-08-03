#!/usr/bin/env python3

import os
import random
import logging

from telethon import TelegramClient, events
from telethon.tl.types import InputFile

max_stickers = len(os.listdir("images"))

client = TelegramClient("wypierdalajbot", os.getenv("APP_ID"), os.getenv("APP_HASH"))
client.start(bot_token=os.getenv("BOT_TOKEN"))

@events.register(events.NewMessage(incoming=True, forwards=False, pattern=r"^.*(?i)wypierdalaj.*$"))
async def handler(event):
    r = random.Random().randint(1, max_stickers)
    await client.send_file(
        entity=event.chat_id,
        file=os.path.join("images", str(r).zfill(4) + ".webp"),
        reply_to=event.reply_to_msg_id if event.is_reply else event.message.id
    )

if __name__ == "__main__":
    client.add_event_handler(handler)
    client.run_until_disconnected()
