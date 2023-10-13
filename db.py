import sqlite3
from datetime import datetime, timedelta
conn = sqlite3.connect('maa_tg.db')
cursor = conn.cursor()

# 创建一个名为client的表
cursor.execute('''CREATE TABLE IF NOT EXISTS client
                  (user_id INTEGER PRIMARY KEY, user TEXT, device TEXT)''')


# 创建任务表
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   type TEXT,
                   params TEXT,
                   user_id INTEGER,
                   time DATETIME)''')

one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
# 执行删除操作
cursor.execute("DELETE FROM tasks WHERE time < ?", (one_hour_ago,))

# 提交更改并关闭连接
conn.commit()
conn.close()




