from telethon.sync import TelegramClient, events
import sqlite3
from datetime import datetime
api_id = 'XXXXXXX'
api_hash = 'XXXXXXXXXXXXXXX'

bot = TelegramClient('bot_session', api_id, api_hash)

@bot.on(events.NewMessage(pattern=r'/'))
async def command(event):
    user_id = event.sender_id
    message = event.message.text.replace("/", "").split()
    command = message[0] if len(message) > 0 else None
    params = " ".join(message[1:]) if len(message) > 1 else None
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    if command == "start":
        cursor.execute('INSERT OR IGNORE  INTO client (user_id, user, device) VALUES (?, ?, ?)', (user_id, "NULL","NULL"))
        await event.respond(f'欢迎使用bot.')
    elif command == "user":
        cursor.execute('UPDATE client SET user = ? WHERE user_id = ?', (params, user_id))
        await event.respond(f'用户标识符设置为 {params} .')
    elif command == "device":
        cursor.execute('UPDATE client SET device = ? WHERE user_id = ?', (params, user_id))
        await event.respond(f'设备标识符设置为 {params} .')
    else:
        cursor.execute('INSERT INTO tasks (type, params, user_id, time) VALUES (?, ?, ?, ?)', (command, params, user_id, current_time))
        await event.respond(f'{command} 已添加到队列.')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    bot.start(bot_token='XXXXXXXXXX:XXXXXXXXXXXXXXX')
    bot.run_until_disconnected()
