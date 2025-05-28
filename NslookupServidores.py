import socket

from telegram import Bot
import asyncio

# === Configuración ===
TELEGRAM_BOT_TOKEN = '7953082943:AAHzroP7AuF9okzI0PikJMixLaXjb_KpqFA'
TELEGRAM_CHAT_ID = '6543042526'  # Puede ser negativo si es un grupo
IP_LIST = [
    "181.112.55.149",   # Enlace CNT
    "186.5.42.226",     # Enlace alterno
    "192.168.10.192",   #Correo electrónico
    "10.220.0.88",      #Pagina web: www.sce.gob.ec
    "10.220.0.9",       #Servicio de aplicaciones: siscpm.scpm.gob.ec
    "10.220.0.47",      #Extranet: servicios.scpm.gob.ec
    "11.0.5.2",         #BD: PostgreSql dbpos.scpm.gob.ec
    "11.0.1.4",         #Control Asistencia: atiempo.scpm.gob.ec
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
