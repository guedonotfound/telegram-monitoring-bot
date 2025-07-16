from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from telethon.errors import RPCError
import asyncio
import sys
import ast
import requests

load_dotenv()

api_id = int(os.getenv("API_ID")) # type: ignore
api_hash = str(os.getenv("API_HASH")) # type: ignore
meu_id = int(os.getenv("MEU_ID")) # type: ignore

palavras_chave = ["mercado livre"]
canais = ast.literal_eval(os.getenv("CANAIS")) # type: ignore
BOT_TOKEN = os.getenv("TOKEN") # type: ignore
CHAT_ID = os.getenv("CHAT_ID") # type: ignore

required_envs = ["API_ID", "API_HASH", "MEU_ID", "CANAIS", "TOKEN", "CHAT_ID"]
for var in required_envs:
    if os.getenv(var) is None:
        raise EnvironmentError(f"❌ Variável de ambiente {var} não está definida no .env")

def notificar_telegram(texto: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": texto}
    resp = requests.post(url, data=data)
    if not resp.ok:
        print(f"[ERRO] Falha ao enviar notificação: {resp.text}")

async def main():
    try:
        async with TelegramClient("session_name", api_id, api_hash) as client:
            @client.on(events.NewMessage(chats=canais))
            async def handle_message(event):
                texto = event.raw_text.lower()
                if any(palavra in texto for palavra in palavras_chave):
                    print(f"🔔 Palavra-chave detectada em: {texto[:50]}...")
                    notificar_telegram(f"🔔 Palavra-chave detectada:\n{event.raw_text}")

            print("🤖 Bot rodando...")
            await client.run_until_disconnected()

    except asyncio.CancelledError:
        print("\n🛑 Bot cancelado (CancelError)")
        raise
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
