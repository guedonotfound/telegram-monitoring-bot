from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from telethon.errors import RPCError
import asyncio
import sys

load_dotenv()

api_id = int(os.getenv("API_ID")) # type: ignore
api_hash = str(os.getenv("API_HASH")) # type: ignore
meu_id = int(os.getenv("MEU_ID")) # type: ignore

palavras_chave = ["mercado livre"]
canais = [-1001260857435, -1001836277485, -1002807632272]

async def main():
    try:
        async with TelegramClient("session_name", api_id, api_hash) as client:
            @client.on(events.NewMessage(chats=canais))
            async def handle_message(event):
                texto = event.raw_text.lower()
                if any(palavra in texto for palavra in palavras_chave):
                    print(f"🔔 Palavra-chave detectada em: {texto[:50]}...")
                    await client.send_message(meu_id, f"Palavra-chave detectada:\n{event.raw_text}")

            print("🤖 Bot rodando...")
            await client.run_until_disconnected()

    except asyncio.CancelledError:
        print("\n🛑 Bot cancelado (CancelError)")
        raise  # para permitir que o asyncio.run saiba que foi cancelado
    except KeyboardInterrupt:
        print("\n🤖 Bot finalizado pelo usuário")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Encerrado com Ctrl+C")
