import socket
import dns.resolver

from telegram import Bot
import asyncio

# === Configuración ===
TELEGRAM_BOT_TOKEN = '7953082943:AAHzroP7AuF9okzI0PikJMixLaXjb_KpqFA'
TELEGRAM_CHAT_ID = '6543042526'  # Puede ser negativo si es un grupo
IP_LIST = [
    "181.112.55.149",
    "186.5.42.226",
    "192.168.68.148",
]


# === Funciones ===

def reverse_dns_lookup(ip):
    try:
        # Usamos socket para hacer el nslookup inverso
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception as e:
        return f"Error resolviendo {ip}: {str(e)}"


async def send_to_telegram(bot, message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


# === Main ===
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    results = []
    for ip in IP_LIST:
        result = reverse_dns_lookup(ip)
        if "Error" in result:
            status_text = "❌ Inactivo"
        else:
            status_text = "✅ Activo"
        results.append(f"Estado: {status_text} IP: {ip} -> Hostname: {result}")

    full_message = "🔍 Resultados del NSLookup:\n\n" + "\n".join(results)

    # Enviar por Telegram
    await send_to_telegram(bot, full_message)


# === Ejecutar ===
if __name__ == '__main__':
    asyncio.run(main())