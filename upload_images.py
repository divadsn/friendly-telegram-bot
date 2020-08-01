#!/usr/bin/env python3

import os
import asyncio

from telethon import TelegramClient

client = TelegramClient("wypierdalajbot", os.getenv("APP_ID"), os.getenv("APP_HASH"))
client.start(bot_token=os.getenv("BOT_TOKEN"))

async def main():
    ids = []

    for filename in sorted(os.listdir("images")):
        path = os.path.join("images", filename)
        file_handle = await client.upload_file(
            file=path,
            part_size_kb=512,
            file_name=os.path.basename(path)
        )

        ids.append(f"{file_handle.id}:{file_handle.parts}:{file_handle.name}:{file_handle.md5_checksum}")

    with open("ids.txt", "w") as f:
        for fileid in ids:
            f.write(fileid + "\n")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
