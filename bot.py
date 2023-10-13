from telethon.sync import TelegramClient, events
import sqlite3
from datetime import datetime
api_id = 'XXXXXXX'
api_hash = 'XXXXXXXXXXXXXXX'

bot = TelegramClient('bot_session', api_id, api_hash)
# 添加客户端部分
@bot.on(events.NewMessage(pattern=r'/start'))
async def add_user(event):
    user_id = event.sender_id
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE  INTO client (user_id, user, device) VALUES (?, ?, ?)', (user_id, "NULL","NULL"))
    conn.commit()
    conn.close()
    await event.respond(f'欢迎使用bot.')

@bot.on(events.NewMessage(pattern=r'/user (\S+)'))
async def add_user(event):
    user_id = event.sender_id
    username = event.pattern_match.group(1)
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE client SET user = ? WHERE user_id = ?', (username, user_id))
    conn.commit()
    conn.close()
    
    await event.respond(f'User {username} added.')

@bot.on(events.NewMessage(pattern=r'/device (\S+)'))
async def add_device(event):
    user_id = event.sender_id
    device_name = event.pattern_match.group(1)
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE client SET device = ? WHERE user_id = ?', (device_name, user_id))
    conn.commit()
    conn.close()
    
    await event.respond(f'Device {device_name} added.')

# 任务部分
@bot.on(events.NewMessage(pattern=r'/CaptureImage'))
async def capture_image(event):
    user_id = event.sender_id
    task_type = "CaptureImage"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (type, user_id, time) VALUES (?, ?, ?)', (task_type, user_id, current_time))
    conn.commit()
    conn.close()
    
    await event.respond(f'CaptureImage task added.')

@bot.on(events.NewMessage(pattern=r'/LinkStart'))
async def link_start(event):
    user_id = event.sender_id
    task_type = "LinkStart"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (type, user_id, time) VALUES (?, ?, ?)', (task_type, user_id, current_time))
    conn.commit()
    conn.close()
    
    await event.respond(f'LinkStart task added.')

@bot.on(events.NewMessage(pattern=r'/LinkStart-(\S+)'))
async def link_start_with_arg(event):
    user_id = event.sender_id
    task_type = event.pattern_match.group(1)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (type, user_id, time) VALUES (?, ?, ?)', (task_type, user_id, current_time))
    conn.commit()
    conn.close()
    
    await event.respond(f'LinkStart-{task_type} task added.')

@bot.on(events.NewMessage(pattern=r'/Toolbox-(\S+)'))
async def toolbox_with_arg(event):
    user_id = event.sender_id
    task_type = event.pattern_match.group(1)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (type, user_id, time) VALUES (?, ?, ?)', (task_type, user_id, current_time))
    conn.commit()
    conn.close()
    
    await event.respond(f'Toolbox-{task_type} task added.')

@bot.on(events.NewMessage(pattern=r'/Settings-(\S+)(?: (\S+))?'))
async def settings_with_params(event):
    user_id = event.sender_id
    task_type = event.pattern_match.group(1)
    params = event.pattern_match.group(2)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not params:
        await event.respond('参数不能为空')
        return
    
    conn = sqlite3.connect('maa_tg.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (type, params, user_id, time) VALUES (?, ?, ?, ?)', (task_type, params, user_id, current_time))
    conn.commit()
    conn.close()
    
    await event.respond(f'Settings-{task_type} task with parameters "{params}" added.')

if __name__ == '__main__':
    bot.start(bot_token='XXXXXXXXXX:XXXXXXXXXXXXXXX')
    bot.run_until_disconnected()
