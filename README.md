# MAA_TG_bot
使用TGbot控制MAA
  
db.py初始化数据库及定期清除数据，db-see.py用于查看数据库  
请自行获取证书替换 “server.crt”与“server.key”，示例证书域名为 maa.lolicon.space  
机器人相关指令:  
/start 添加用户ID  
/user XXXXXX 绑定MAA用户标识符  
/device YYYYYY 绑定MAA设备标识符  
/AAAAA BBBBB 其余指令会将会按照type=AAAAA，params=BBBBB传输给MAA，MAA返回执行完成后会删除任务（不存在的任务MAA不会返回结果）  
不会处理非"/" 开头的消息