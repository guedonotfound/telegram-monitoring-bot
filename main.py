from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from telethon.errors import RPCError
import asyncio

load_dotenv()

import os

api_id_str = os.getenv("API_ID")
if api_id_str is None:
    raise ValueError("API_ID não está definida no ambiente")

api_hash = os.getenv("API_HASH")
if api_hash is None:
    raise ValueError("API_HASH não está definida no ambiente")

meu_id_str = os.getenv("MEU_ID")
if meu_id_str is None:
    raise ValueError("MEU_ID não está definida no ambiente")

api_id = int(api_id_str)
meu_id = int(meu_id_str)


user = TelegramClient("session_name", api_id, api_hash)

palavras_chave = ["cupom", "mercado livre", "promo", "off"]
canais = ["LinksBrazil", "pobregram"]

@user.on(events.NewMessage(chats=canais))
async def main():
    while True:
        try:
            user.start()
            print("🤖 Bot rodando...")
            user.run_until_disconnected()
        except RPCError as e:
            print(f"Erro RPC: {e}, tentando reconectar em 5 segundos...")
        except Exception as e:
            print(f"Erro inesperado: {e}, tentando reconectar em 5 segundos...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
