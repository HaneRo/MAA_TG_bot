import sqlite3

# 替换为你的SQLite数据库文件路径
db_file = 'maa_tg.db'

def read_sqlite_db(db_file):
    # 连接到数据库
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 获取数据库中所有表的表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    for table_name in table_names:
        table_name = table_name[0]
        print(f"表名: {table_name}")
        print("字段名和值:")

        # 获取表的列名
        cursor.execute(f"PRAGMA table_info({table_name});")
        column_names = [column[1] for column in cursor.fetchall()]

        # 查询表中的所有数据
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        for row in rows:
            for i in range(len(column_names)):
                column_name = column_names[i]
                value = row[i]
                print(f"{column_name}: {value}")
            print()

    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    read_sqlite_db(db_file)
