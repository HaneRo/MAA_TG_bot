from flask import Flask , request, jsonify
import sqlite3
import telebot
telegram_bot = telebot.TeleBot("XXXXXXXXX:XXXXXXXXXXXXXXXX")

app = Flask(__name__)

# 配置数据库连接
db_connection = sqlite3.connect('maa_tg.db', check_same_thread=False)
db_cursor = db_connection.cursor()

# 获取任务端点
@app.route('/getTask', methods=['POST'])
def query_data():
    try:
        user = request.json.get("user")
        device = request.json.get("device")
        # 执行查询
        db_cursor.execute("SELECT tasks.id, tasks.type,tasks.params FROM tasks INNER JOIN client ON client.user_id = tasks.user_id WHERE user=? and device = ?", (user, device))
        data = db_cursor.fetchall()[-3:]

        result = {"tasks": []}

        for item in data:
            task = {"id": str(item[0]), "type": item[1]}
            if item[2] is not None:
                task["params"] = item[2]
            result["tasks"].append(task)

        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

# 汇报任务端点
@app.route('/reportStatus', methods=['POST'])
def report_data():
    try:
        user = request.json.get("user")
        device = request.json.get("device")
        task = request.json.get("task")
        status = request.json.get("status")
        payload = request.json.get("payload")
        db_cursor.execute("SELECT user_id FROM client WHERE user=? and device = ?", (user, device))
        id = db_cursor.fetchall()[0][0]
        db_cursor.execute("SELECT type FROM tasks WHERE id=?", (task))
        task_name = db_cursor.fetchall()[0][0]
        print("用户" )
        print(id)
        print("任务")
        print(task_name)
        print(status)
        text="任务"+str(task_name)+" "+str(status)+",详细信息： "+payload
        if payload :
            print (payload)
        
        telegram_bot.send_message(chat_id=id, text=text)

        return jsonify(id)
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True,threaded=True,host='0.0.0.0',port=5000,ssl_context=('server.crt','server.key'))
