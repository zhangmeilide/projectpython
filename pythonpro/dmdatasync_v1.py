# -*- coding: utf-8 -*-
import psycopg2
import dmPython  # 达梦数据库驱动
import pymysql  # MySQL 数据库驱动

# 达梦数据库连接参数
dm_conn_params_one = {
    'server': '127.0.0.1',  # 达梦数据库服务器地址 西藏50本地的达梦数据库
    'port': 5236,  # 达梦数据库默认端口号
    'user': 'SYSDBA',  # 用户名
    'password': 'Xswl6666',  # 密码
}
dm_conn_params = {
    'server': '192.168.0.138',  # 网闸 达梦数据库服务器地址 172.21.140.106:5236
    'port': 50338,  # 达梦数据库默认端口号
    'user': 'XBUSER',  # 用户名
    'password': 'XB!q@w#e$r2024',  # 密码
}
# 连接数据库
mysql_conn_params = {
    'dbname':"wjxt_sx",        # 数据库名
    'user':"system",          # 用户名
    'password':"12345678ab",  # 密码
    'host':"192.168.0.138",   # 主机地址
    'port':"50153",           # 端口
    'options':f"-c search_path=wjxt_sx"  # 指定模式
}

try:
    # 连接达梦数据库
    dm_conn = dmPython.connect(**dm_conn_params)
    dm_cursor = dm_conn.cursor()
    # 切换到指定的模式（如果需要）
    dm_cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = LBUSER")
    print("连接达梦数据库并切换到 LBUSER 模式成功！")

    # 从达梦数据库的 your_table1_name 表中查询 name 和 email
    #dm_cursor.execute("SELECT name, email FROM your_table1_name")  # 查询表1的数据
    #rows = dm_cursor.fetchall()  # 获取所有查询结果

    # 打印查询结果
    #print("从达梦数据库的 your_table1_name 表中查询到的数据：")
    #for row in rows:
    #    print(row)

    # 连接 MySQL 数据库
    mysql_conn = psycopg2.connect(**mysql_conn_params)
    mysql_cursor = mysql_conn.cursor()
    print("连接 MySQL 数据库成功！")

    # 将查询到的数据插入到 MySQL 的 your_table2_name 表中

    # for row in rows:
    #     name, email = row  # 解包每一行的数据
    #     mysql_cursor.execute("INSERT INTO your_table2_name (name, email) VALUES (%s, %s)", (name, email))
    #
    # mysql_conn.commit()  # 提交事务
    # print("数据插入到 MySQL 的 your_table2_name 表成功！")
    #
    # # 关闭达梦数据库连接
    # dm_cursor.close()
    # dm_conn.close()
    # print("达梦数据库连接已关闭。")
    #
    # # 关闭 MySQL 数据库连接
    # mysql_cursor.close()
    # mysql_conn.close()
    # print("MySQL 数据库连接已关闭。")

except dmPython.Error as e:
    print(f"连接或操作达梦数据库时出错: {e}")
except pymysql.Error as e:
    print(f"连接或操作 MySQL 数据库时出错: {e}")