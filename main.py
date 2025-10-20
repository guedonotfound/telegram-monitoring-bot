from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from telethon.errors import RPCError
import asyncio
import sys
import ast
import requests
import json

load_dotenv()

api_id = int(os.getenv("API_ID"))  # type: ignore
api_hash = str(os.getenv("API_HASH"))  # type: ignore
meu_id = int(os.getenv("MEU_ID"))  # type: ignore
BOT_TOKEN = os.getenv("TOKEN")  # type: ignore
CHAT_ID = int(os.getenv("CHAT_ID"))  # type: ignore
canais = ast.literal_eval(os.getenv("CANAIS"))  # type: ignore
KEYWORDS_FILE = "keywords.json"

required_envs = ["API_ID", "API_HASH", "MEU_ID", "CANAIS", "TOKEN", "CHAT_ID"]
for var in required_envs:
    if os.getenv(var) is None:
        raise EnvironmentError(f"❌ Variável de ambiente {var} não está definida no .env")

def carregar_keywords():
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_keywords(lista):
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def notificar_telegram(texto: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": texto}
    resp = requests.post(url, data=data)
    if not resp.ok:
        print(f"[ERRO] Falha ao enviar notificação: {resp.text}")

async def main():
    try:
        async with TelegramClient("session_name", api_id, api_hash) as client:

            # 📡 Monitoramento de canais
            @client.on(events.NewMessage(chats=canais))
            async def handle_message(event):
                texto = event.raw_text.lower()
                if any(palavra in texto for palavra in carregar_keywords()):
                    print(f"🔔 Palavra-chave detectada em: {texto[:50]}...")
                    notificar_telegram(f"🔔 Palavra-chave detectada:\n\n{event.raw_text}")

            # 🛠️ Comandos de gerenciamento
            @client.on(events.NewMessage)
            async def comandos_pessoais(event):
                if event.sender_id != meu_id:
                    return

                texto = event.raw_text.strip().lower()

                if texto.startswith("/add "):
                    nova = texto[5:].strip()
                    palavras = carregar_keywords()
                    if nova in palavras:
                        await event.reply(f"❗ '{nova}' já está na lista.")
                    else:
                        palavras.append(nova)
                        salvar_keywords(palavras)
                        await event.reply(f"✅ Palavra '{nova}' adicionada.")

                elif texto.startswith("/remove "):
                    alvo = texto[8:].strip()
                    palavras = carregar_keywords()
                    if alvo in palavras:
                        palavras.remove(alvo)
                        salvar_keywords(palavras)
                        await event.reply(f"🗑️ Palavra '{alvo}' removida.")
                    else:
                        await event.reply(f"❌ Palavra '{alvo}' não está na lista.")

                elif texto == "/list":
                    palavras = carregar_keywords()
                    if palavras:
                        lista = "\n".join(f"- {p}" for p in palavras)
                        await event.reply(f"📋 Palavras atuais:\n{lista}")
                    else:
                        await event.reply("📭 Nenhuma palavra cadastrada.")

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
