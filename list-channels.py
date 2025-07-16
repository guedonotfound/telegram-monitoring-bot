from telethon import TelegramClient
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_id = int(os.getenv("API_ID")) # type: ignore
api_hash = str(os.getenv("API_HASH")) # type: ignore

async def listar_dialogos():
    async with TelegramClient("session_name", api_id, api_hash) as client:
        dialogs = await client.get_dialogs()
        print("Seus canais/grupos/chat e seus respectivos IDs:\n")
        for dialog in dialogs:
            print(f"Nome: {dialog.name}\nID: {dialog.id}\nTipo: {type(dialog.entity).__name__}\n---")

if __name__ == "__main__":
    asyncio.run(listar_dialogos())
