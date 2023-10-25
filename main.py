import telebot
import sqlite3
from datetime import datetime
import threading
from flask import Flask, request, jsonify
import base64
from io import BytesIO
import time
import sys
import os

sys.stdout = open(os.devnull, "w") #使用pyinstaller  -w  时需重定向标准输出

TOKEN = 'XXXXXXXXX:XXXXXXXXXXXXXXXX'  # 替换为从 BotFather 获取的你的 TOKEN

ro_conn = sqlite3.connect('maa_tg.db', check_same_thread=False)
ro_cursor = ro_conn.cursor()

help = "/start 添加用户ID \n/user XXXXXX 绑定MAA用户标识符 \n/device YYYYYY 绑定MAA设备标识符 \n/help 显示帮助 \n/LinkStart - 一键开始 \n/CaptureImage - 截图\n/CaptureImageNow - 立刻截图\n/LinkStart-WakeUp - 开始唤醒\n/LinkStart-Combat - 刷理智\n/LinkStart-Recruiting - 公开招募\n/LinkStart-Mall - 获取信用及购物\n/LinkStart-Mission - 领取奖励\n/LinkStart-AutoRoguelike - 肉鸽\n具体参考 https://maa.plus/docs/3.8-%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%8D%8F%E8%AE%AE.html "

bot = telebot.TeleBot(TOKEN)
# 处理 / 开头的消息
@bot.message_handler(content_types=["text"], func=lambda message: True, regexp="^/")
def received_command(message):
    user_id = message.chat.id
    string = message.text.replace("/", "").split()
    command = string[0] if len(string) > 0 else None
    params = " ".join(string[1:]) if len(string) > 1 else None
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('maa_tg.db', check_same_thread=False)
    cursor = conn.cursor()
    if command == "start":
        cursor.execute('INSERT OR IGNORE  INTO client (user_id, user, device) VALUES (?, ?, ?)', (user_id, "NULL", "NULL"))
        bot.reply_to(message, f'欢迎使用bot.' + help)
    elif command == "user":
        cursor.execute('UPDATE client SET user = ? WHERE user_id = ?', (params, user_id))
        bot.reply_to(message, f'用户标识符设置为 {params} .')
    elif command == "device":
        cursor.execute('UPDATE client SET device = ? WHERE user_id = ?', (params, user_id))
        bot.reply_to(message, f'设备标识符设置为 {params} .')
    elif command == "help":
        bot.reply_to(message, help)
    else:
        cursor.execute('INSERT INTO tasks (type, params, user_id, time) VALUES (?, ?, ?, ?)',
                       (command, params, user_id, current_time))
        bot.reply_to(message, f'{command} 已添加到队列.')
    conn.commit()
    conn.close()


web = Flask(__name__)
# 获取任务端点
@web.route('/getTask', methods=['POST'])
def query_data():
    try:
        user = request.json.get("user")
        device = request.json.get("device")
        # 执行查询
        ro_cursor.execute("SELECT tasks.id, tasks.type,tasks.params FROM tasks INNER JOIN client ON client.user_id = tasks.user_id WHERE user=? and device = ?", (user, device))
        data = ro_cursor.fetchall()[-3:]

        result = {"tasks": []}

        for item in data:
            task = {"id": str(item[0]), "type": item[1]}
            if item[2] is not None:
                task["params"] = item[2]
            result["tasks"].append(task)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

# 汇报任务端点
@web.route('/reportStatus', methods=['POST'])
def report_data():
    try:
        user = request.json.get("user")
        device = request.json.get("device")
        task = request.json.get("task")
        status = request.json.get("status")
        payload = request.json.get("payload")
        ro_cursor.execute("SELECT client.user_id, tasks.id, tasks.type FROM tasks INNER JOIN client ON client.user_id = tasks.user_id WHERE user=? and device = ? and tasks.id = ?", (user, device, task))
        data = ro_cursor.fetchall()[0]
        user_id = data[0]
        tasks_id = data[1]
        tasks_type = data[2]
        if data:
            del_conn = sqlite3.connect('maa_tg.db', check_same_thread=False)
            del_cursor = del_conn.cursor()
            del_cursor.execute("DELETE FROM tasks WHERE tasks.id = ? and user_id = ?", (task,user_id))
            del_conn.commit()
            del_conn.close()
        try:
            image_data = base64.b64decode(payload)
            # 发送图像给用户
            bot.send_photo(chat_id=user_id, photo=BytesIO(image_data))
            return "ok"
        except:
            pass
            # print("payload不是图像")
        text = "编号"+str(tasks_id)+"任务"+str(tasks_type)+"执行"+str(status)
        if payload:
            text += ",详细信息： "+payload
        try:
            bot.send_message(chat_id=user_id, text=str(text))
        except:
            print("消息发送失败")

        return jsonify({'ok': str(id)})
    except Exception as e:
        return jsonify({'error': str(e)})


def start_telebot():
    while True:
        try:
            # 启动Telebot
            bot.polling()
        except Exception as e:
            # 处理连接错误
            print(f"连接错误: {e}")
            # 等待一段时间，然后重试连接
            time.sleep(10)

def start_flask():
    while True:
        try:
            # 启动Flask
            web.run(debug=False, threaded=True, host='0.0.0.0',port=5000, ssl_context=('server.crt', 'server.key'))
        except Exception as e:
            # 处理连接错误
            print(f"Flask错误: {e}")
            # 等待一段时间，然后重试连接
            time.sleep(10)

if __name__ == '__main__':
    # 使用多线程同时运行 Telebot 和 Flask
    thread_telebot = threading.Thread(target=start_telebot)
    thread_telebot.start()
    start_flask()