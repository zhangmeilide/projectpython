# -*- coding: utf-8 -*-
import psycopg2
import dmPython  # 达梦数据库驱动
import pymysql  # MySQL 数据库驱动
import json
from datetime import datetime
import logging
# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 对接达梦数据库的连接参数 对接用户信息的
dm_conn_params_user = {
    'server': '192.168.0.138',  # 网闸 达梦数据库服务器地址 172.21.140.106:5236
    'port': 50338,  # 达梦数据库默认端口号
    'user': 'QBUSER',  # 用户名
    'password': 'OB!q@w#e$r2024',  # 密码
}

# 对接待办任务的链接参数
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
# PostgreSQL 数据库连接参数
pg_conn_params = {
    'dbname': "wjxt_sx",        # 数据库名
    'user': "system",          # 用户名
    'password': "12345678ab",  # 密码
    'host': "192.168.0.138",   # 主机地址
    'port': "50153",           # 端口
    'options': "-c search_path=wjxt_sx"  # 指定模式
}

def default_serializer(obj):
    """
    自定义 JSON 序列化函数，用于处理 datetime 对象
    :param obj: 需要序列化的对象
    :return: 可序列化的对象
    """
    if isinstance(obj, datetime):
        return obj.isoformat()  # 将 datetime 转换为 ISO 格式的字符串
    raise TypeError(f"Type {type(obj)} not serializable")

def connect_db(db_type, conn_params, schema=None):
    """连接数据库并返回连接对象和游标"""
    try:
        if db_type == "dm":
            conn = dmPython.connect(**conn_params)
            cursor = conn.cursor()
            if schema:
                cursor.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {schema}")
                print(f"连接达梦数据库并切换到 {schema} 模式成功！")
            else:
                print("连接达梦数据库成功！")
        elif db_type == "pg":
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            print("连接 PostgreSQL 数据库成功！")
        else:
            raise ValueError("不支持的数据库类型！")
        return conn, cursor
    except Exception as e:
        print(f"连接数据库时出错: {e}")
        return None, None

def query_data_json(cursor, table_name, columns="*", condition=None, limit=None):
    """
    从指定表中查询数据，结果是 json 格式的字符串
    :param cursor: 数据库游标对象
    :param table_name: 表名
    :param columns: 要查询的列，默认为所有列
    :param condition: 查询条件，默认为 None
    :param limit: 查询结果的条数限制，默认为 None 表示不限制
    :return: json 格式的字符串，查询出错时返回 None
    """
    try:
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        if limit is not None:
            # 处理不同数据库的限制语法
            if isinstance(cursor.connection, dmPython.Connection):
                query += f" FETCH FIRST {limit} ROWS ONLY"
            elif isinstance(cursor.connection, psycopg2.extensions.connection):
                query += f" LIMIT {limit}"
            else:
                print("不支持的数据库类型，无法添加条数限制")

        cursor.execute(query)
        rows = cursor.fetchall()
        # 获取列名
        col_names = [desc[0] for desc in cursor.description]

        # 将查询结果转换为字典列表
        result = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)

        # 将字典列表转换为 JSON 格式
        json_result = json.dumps(result, indent=4, default=default_serializer, ensure_ascii=False)
        print(f"从表 {table_name} 中查询到的数据（JSON 格式）：")
        # print(json_result)
        return json_result
    except Exception as e:
        print(f"查询数据时出错: {e}")
        return None


def query_data_v1(cursor, table_name, columns="*", condition=None):
    """
       从指定表中查询数据
       返回的数据类型是 list，是一个包含查询结果的列表。
       列表中的每个元素通常是一个元组（tuple），表示数据库中的一行数据
       fetchall() 方法返回一个包含所有查询结果的列表。
       列表中的每个元素是一个元组，表示数据库中的一行数据。
       [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
    """
    try:
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(f"从表 {table_name} 中查询到的数据：")
        # for row in rows:
        #    print(row)
        return rows
    except Exception as e:
        print(f"查询数据时出错: {e}")
        return None

def query_data(cursor, table_name, columns="*", condition=None):
    """
    查询数据库表数据并返回 JSON 格式的结果
    """
    try:
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        cursor.execute(query)
        rows = cursor.fetchall()
        # 获取列名
        col_names = [desc[0] for desc in cursor.description]
        # 将查询结果转换为字典列表
        result = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)

        # 返回字典列表，而不是 JSON 字符串
        return result
    except Exception as e:
        print(f"查询数据时出错: {e}")
        return None

def insert_data_a(db_type, cursor, table_name, data):
    """
    向指定表中插入数据
    :param db_type: 数据库类型，'dm' 表示达梦数据库，'pg' 表示 PostgreSQL 数据库
    :param cursor: 数据库游标对象
    :param table_name: 表名
    :param data: 要插入的数据（字典，键为列名，值为数据）
    :return: 成功返回 True，失败返回 False
    """
    try:
        columns = ", ".join(data.keys())
        if db_type == "dm":
            # 达梦数据库使用 ? 作为占位符
            placeholders = ", ".join(["?"] * len(data))
        elif db_type == "pg":
            # PostgreSQL 使用 %s 作为占位符
            placeholders = ", ".join(["%s"] * len(data))
        else:
            raise ValueError("不支持的数据库类型！")

        # 生成 SQL 语句
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        # print(f"生成的 SQL 语句: {query}")  # 打印生成的 SQL 语句

        # 执行 SQL 语句
        cursor.execute(query, list(data.values()))
        print(f"数据插入到表 {table_name} 成功！")
        return True
    except Exception as e:
        print(f"插入数据时出错: {e}")
        return False

def get_columns(pg_cursor, table_name):
    # 查询表的列名
    query = f"""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = %s;
    """
    pg_cursor.execute(query, (table_name,))
    columns = pg_cursor.fetchall()
    return [column[0] for column in columns]


def insert_data(db_type, cursor, table_name, data):
    """
    向指定表中插入数据
    :param db_type: 数据库类型，'dm' 表示达梦数据库，'pg' 表示 PostgreSQL 数据库
    :param cursor: 数据库游标对象
    :param table_name: 表名
    :param data: 要插入的数据（字典，键为列名，值为数据）
    :return: 成功返回 True，失败返回 False
    """
    try:
        columns = ", ".join(data.keys())
        if db_type == "dm":
            # 达梦数据库使用 ? 作为占位符
            placeholders = ", ".join(["?"] * len(data))
        elif db_type == "pg":
            # PostgreSQL 使用 %s 作为占位符
            placeholders = ", ".join(["%s"] * len(data))
        else:
            raise ValueError("不支持的数据库类型！")

        # 生成 SQL 语句
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # 输出调试信息
        logging.debug(f"生成的 SQL 语句: {query}")
        logging.debug(f"要插入的数据: {data}")

        # 执行 SQL 语句
        cursor.execute(query, list(data.values()))
        logging.info(f"数据插入到表 {table_name} 成功！")
        return True
    except psycopg2.Error as e:
        # 捕获 PostgreSQL 错误并输出详细信息
        logging.error(f"PostgreSQL 错误: {e.pgcode}, {e.pgerror}, SQL: {query}, 参数: {data}")
        return False
    except Exception as e:
        logging.error(f"插入数据时出错: {e}")
        return False


def update_data_v1(db_type,cursor, table_name, data, condition):
    """更新指定表中的数据"""
    try:
        if db_type == "dm":
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        elif db_type == "pg":
            set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        else:
            raise ValueError("不支持的数据库类型！")

        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        print(f"更新生成的 SQL 语句: {query}")
        cursor.execute(query, list(data.values()))
        print(f"表 {table_name} 中的数据更新成功！")
        return True
    except Exception as e:
        print(f"更新数据时出错: {e}")
        return False

def update_data(db_type, cursor, table_name, data, condition, condition_values):
    """
    更新指定表中的数据

    :param db_type: 数据库类型 ("dm" 或 "pg")
    :param cursor: 数据库游标
    :param table_name: 表名
    :param data: 要更新的数据，字典形式，例如 {"SYNC_FLAG": "D"}
    :param condition: 更新条件，字符串形式，例如 "ID = ?"
    :param condition_values: 更新条件的值，元组形式，例如 (task_id,)
    :return: 更新成功返回 True，失败返回 False
    """
    try:
        if db_type == "dm":
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            params = list(data.values()) + list(condition_values)
        elif db_type == "pg":
            set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            params = list(data.values()) + list(condition_values)
        else:
            raise ValueError("不支持的数据库类型！")

        print(f"更新生成的 SQL 语句: {query}")
        print(f"参数: {params}")
        cursor.execute(query, params)
        print(f"表 {table_name} 中的数据更新成功！")
        return True
    except Exception as e:
        print(f"更新数据时出错: {e}")
        return False

def update_sync_flag(cursor, table_name: str, record_id: str):
    """
    更新 SYNC_FLAG 为 1，表示数据已同步
    """
    try:
        update_sql = f"UPDATE {table_name} SET SYNC_FLAG = 1 WHERE ID = %s"
        cursor.execute(update_sql, (record_id,))
        print(f"表 {table_name} 中的数据标示更新成功！")
        return True
    except Exception as e:
        print(f"更新更新标示时出错: {e}")
        return False



def delete_data(cursor, table_name, condition):
    """删除指定表中的数据"""
    try:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        print(f"表 {table_name} 中的数据删除成功！")
        return True
    except Exception as e:
        print(f"删除数据时出错: {e}")
        return False

def close_connection(conn, cursor):
    """关闭数据库连接"""
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("数据库连接已关闭。")
    except Exception as e:
        print(f"关闭数据库连接时出错: {e}")

def test():
    try:
        # 连接达梦数据库
        dm_conn = dmPython.connect(**dm_conn_params_user)
        dm_cursor = dm_conn.cursor()
        # 切换到指定的模式（如果需要）
        dm_cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = QBUSER")
        print("连接达梦数据库并切换到 QBUSER 模式成功！")
        # 连接 MySQL 数据库
        mysql_conn = psycopg2.connect(**pg_conn_params)
        mysql_cursor = mysql_conn.cursor()
        print("连接 MySQL 数据库成功！")
    except dmPython.Error as e:
        print(f"连接或操作达梦数据库时出错: {e}")
    except pymysql.Error as e:
        print(f"连接或操作 MySQL 数据库时出错: {e}")

# 链接达梦用户信息表 并查询数据
def userinfolist():
    # 连接达梦数据库，用于查询表名
    dm_conn_tables, dm_cursor_tables = connect_db("dm", dm_conn_params_user, schema="QBDATA")
    try:
        # 查询达梦数据库中 QBUSER 模式下的所有表名
        table_query = "SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = 'QBUSER'"
        dm_cursor_tables.execute(table_query)
        tables = dm_cursor_tables.fetchall()
        print("达梦数据库 QBUSER 模式下的所有表名：")
        for table in tables:
            print(table[0])
    except Exception as e:
        print(f"查询表名时出错: {e}")
    finally:
        # 关闭查询表名的数据库连接
        close_connection(dm_conn_tables, dm_cursor_tables)

    # 连接达梦数据库
    dm_conn, dm_cursor = connect_db("dm", dm_conn_params_user, schema="QBDATA")
    # 连接 MySQL 数据库
    mysql_conn, mysql_cursor = connect_db("pg", mysql_conn_params)

    try:
        # 尝试查询数据前，再次确认模式
        # 可以根据实际情况修改模式名
        dm_cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = QBDATA")

        # 查询数据
        print("尝试查询 SYS_DEPART 表数据")
        org_dpt_rows = query_data_json(dm_cursor, "SYS_DEPART","*", None, limit=10)
        
        # 可以添加日志，方便调试
        print("尝试查询 SYS_USER 表数据")
        user_info_rows = query_data_json(dm_cursor, "SYS_USER","*", None, limit=10)

        print(org_dpt_rows)
        print(user_info_rows)
    except Exception as e:
        print(f"查询数据时发生异常: {e}")
    finally:
        # 关闭数据库连接
        close_connection(dm_conn, dm_cursor)
        close_connection(mysql_conn, mysql_cursor)

    

def testv2():
    # 连接达梦数据库
    dm_conn, dm_cursor = connect_db("dm", dm_conn_params, schema="LBUSER")
    # 连接 PostgreSQL 数据库
    pg_conn, pg_cursor = connect_db("pg", pg_conn_params)
    # 插入数据
    # 插入到 TODO_TASK 表
    # todo_task_id = str(uuid.uuid4())
    # task_user_rel_id = str(uuid.uuid4())

    task_user_data = {
        "REL_ID": "1893900",
        "TASK_ID": "1807611",
        "USER_ID": "18611111111",
        "DATA_OPER_IDENT": "I",
        "DATA_STOR_TIME": "2025-02-27 17:00:12",
        "DEPART_CODE": ""
    }
    # insert_data('dm',dm_cursor, "TASK_USER_RELATION", task_user_data)
    task_data = {
        "ID": "186487098",
        "TASK_ID": "1807611",
        "SYSTEM_ID": "",
        "TASK_NAME": "线索管理",
        "BUSINESS_SYSTEM_NAME": "智慧网监一体化平台",
        "TASK_TYPE": "待处理",
        "TASK_DESCRIPTION": "智慧网监一体化平台线索待处理任务",
        "TASK_REDIRECT_URL": "http://172.29.66.16:8018/cluesCentreStatu",
        "TASK_START_TIME": "2025-02-27 17:00:12",
        "TASK_END_TIME": "2025-02-27 17:00:12",
        "ISSUING_DEPARTMENT": "网监处",
        "COMPLETION_STATUS": "0",
        "COMPLETION_TIME": "2025-02-27 17:00:12",
        "DATA_OPER_IDENT": "I",
        "DATA_STOR_TIME": "2025-02-27 17:00:12",
        "ADVENT_DAYS": "126",
        "LOGIC_FLAG": "0"
    }
    # insert_data('dm',dm_cursor, "TODO_TASK", task_data)

    # 删除数据
    # delete_data(dm_cursor, "TASK_USER_RELATION", "REL_ID = 1893900")
    # delete_data(dm_cursor, "TODO_TASK", "ID = 186487098")

    # 更新数据
    task_user_update_data = {'DATA_OPER_IDENT': 'D'}
    task_user_update_condition = "REL_ID = 1893900"
    # update_data('dm',dm_cursor, "TASK_USER_RELATION", task_user_update_data, task_user_update_condition)

    task_update_data = {'DATA_OPER_IDENT': 'D'}
    task_update_condition = "ID = 186487098"
    # update_data('dm', dm_cursor, "TODO_TASK", task_update_data, task_update_condition)

    task_user_rows = query_data_json(dm_cursor, "TASK_USER_RELATION", columns="*", condition="")
    task_rows = query_data_json(dm_cursor, "TODO_TASK", columns="*", condition="")

    print(task_user_rows)
    print(task_rows)


def main_v1():
    """
    进行数据同步 根据任务和任务下的关联关系进行同步
    """
    # 连接达梦数据库
    dm_conn, dm_cursor = connect_db("dm", dm_conn_params, schema="LBUSER")
    # 连接 PostgreSQL 数据库
    pg_conn, pg_cursor = connect_db("pg", pg_conn_params)
    # 插入数据
    # 插入到 TODO_TASK 表
    # todo_task_id = str(uuid.uuid4())
    # task_user_rel_id = str(uuid.uuid4())

    pg_task_rows = query_data(pg_cursor, "TODO_TASK_XZ", columns="*", condition="")
    # print(pg_task_rows)
    # 循环处理 TODO_TASK_XZ 表数据并插入到目标数据库
    for task_row in pg_task_rows:
        # print(task_row)
        # print(type(task_row))
        task_data = {
            "ID": task_row.get("ID"),  # 从查询结果中获取 ID
            "TASK_ID": task_row.get("TASK_ID"),  # 从查询结果中获取 TASK_ID
            "SYSTEM_ID": task_row.get("SYSTEM_ID", ""),  # 如果字段可能为空，提供默认值
            "TASK_NAME": task_row.get("TASK_NAME", ""),
            "BUSINESS_SYSTEM_NAME": task_row.get("BUSINESS_SYSTEM_NAME", ""),
            "TASK_TYPE": task_row.get("TASK_TYPE", ""),
            "TASK_DESCRIPTION": task_row.get("TASK_DESCRIPTION", ""),
            "TASK_REDIRECT_URL": task_row.get("TASK_REDIRECT_URL", ""),
            "TASK_START_TIME": task_row.get("TASK_START_TIME", ""),
            "TASK_END_TIME": task_row.get("TASK_END_TIME", ""),
            "ISSUING_DEPARTMENT": task_row.get("ISSUING_DEPARTMENT", ""),
            "COMPLETION_STATUS": task_row.get("COMPLETION_STATUS", ""),
            "COMPLETION_TIME": task_row.get("COMPLETION_TIME", ""),
            "DATA_OPER_IDENT": task_row.get("DATA_OPER_IDENT", ""),
            "DATA_STOR_TIME": task_row.get("DATA_STOR_TIME", ""),
            "ADVENT_DAYS": task_row.get("ADVENT_DAYS", ""),
            "LOGIC_FLAG": task_row.get("LOGIC_FLAG", "")
        }
        # print(task_data)
        # 插入数据到目标数据库
        insert_data('dm', dm_cursor, "TODO_TASK", task_data)
        # 查询 TASK_USER_RELATION_XZ 表数据，条件是 TASK_ID 等于当前任务的 TASK_ID
        condition = f"TASK_ID = '{task_row.get('TASK_ID')}'"
        pg_task_user_rows = query_data(pg_cursor, "TASK_USER_RELATION_XZ", columns="*", condition=condition)

        # 循环处理 TASK_USER_RELATION_XZ 表数据
        for task_user_row in pg_task_user_rows:
            # 构造任务与用户关系数据
            task_user_data = {
                "REL_ID": task_user_row.get("REL_ID"),  # 从查询结果中获取 REL_ID
                "TASK_ID": task_user_row.get("TASK_ID"),  # 从查询结果中获取 TASK_ID
                "USER_ID": task_user_row.get("USER_ID"),  # 从查询结果中获取 USER_ID
                "DATA_OPER_IDENT": task_user_row.get("DATA_OPER_IDENT", "I"),  # 默认值为 "I"
                "DATA_STOR_TIME": task_user_row.get("DATA_STOR_TIME", ""),  # 从查询结果中获取 DATA_STOR_TIME
                "DEPART_CODE": task_user_row.get("DEPART_CODE", "")  # 从查询结果中获取 DEPART_CODE
            }
            # print(task_user_data)
            # return
            # 插入任务与用户关系数据到目标数据库
            insert_data('dm', dm_cursor, "TASK_USER_RELATION", task_user_data)

    # 提交事务
    dm_conn.commit()
    task_user_rows = query_data_json(dm_cursor, "TASK_USER_RELATION", columns="*", condition="")
    task_rows = query_data_json(dm_cursor, "TODO_TASK", columns="*", condition="")
    # 关闭数据库连接
    close_connection(dm_conn, dm_cursor)
    close_connection(pg_conn, pg_cursor)

    # print(task_user_rows)
    # print(task_rows)
    # 构造输出的 JSON 格式
    result = {
        'status': 200,
        'Msg': '同步达梦待办任务数据成功',
        'data': [task_user_rows, task_rows]
    }
    # 输出结果
    print(result)

def main():
    """
    进行数据同步 任务和执行人关系表分别同步 不看关系 增量添加
    """
    dm_conn = None
    pg_conn = None
    try:
        # 连接达梦数据库
        dm_conn, dm_cursor = connect_db("dm", dm_conn_params, schema="LBUSER")
        # 连接 PostgreSQL 数据库
        pg_conn, pg_cursor = connect_db("pg", pg_conn_params)
        # 插入数据
        # 插入到 TODO_TASK 表
        # todo_task_id = str(uuid.uuid4())
        # task_user_rel_id = str(uuid.uuid4())
        # dm_conn.begin()
        pg_task_rows = query_data(pg_cursor, "TODO_TASK_XZ", columns="*", condition="SYNC_FLAG = 0")
        # print(pg_task_rows)
        # 循环处理 TODO_TASK_XZ 表数据并插入到目标数据库
        for task_row in pg_task_rows:
            # print(task_row)
            # print(type(task_row))
            task_data = {
                "ID": task_row.get("ID"),  # 从查询结果中获取 ID
                "TASK_ID": task_row.get("TASK_ID"),  # 从查询结果中获取 TASK_ID
                "SYSTEM_ID": task_row.get("SYSTEM_ID", ""),  # 如果字段可能为空，提供默认值
                "TASK_NAME": task_row.get("TASK_NAME", ""),
                "BUSINESS_SYSTEM_NAME": task_row.get("BUSINESS_SYSTEM_NAME", ""),
                "TASK_TYPE": task_row.get("TASK_TYPE", ""),
                "TASK_DESCRIPTION": task_row.get("TASK_DESCRIPTION", ""),
                "TASK_REDIRECT_URL": task_row.get("TASK_REDIRECT_URL", ""),
                "TASK_START_TIME": task_row.get("TASK_START_TIME", ""),
                "TASK_END_TIME": task_row.get("TASK_END_TIME", ""),
                "ISSUING_DEPARTMENT": task_row.get("ISSUING_DEPARTMENT", ""),
                "COMPLETION_STATUS": task_row.get("COMPLETION_STATUS", ""),
                "COMPLETION_TIME": task_row.get("COMPLETION_TIME", ""),
                "DATA_OPER_IDENT": task_row.get("DATA_OPER_IDENT", ""),
                "DATA_STOR_TIME": task_row.get("DATA_STOR_TIME", ""),
                "ADVENT_DAYS": task_row.get("ADVENT_DAYS", ""),
                "LOGIC_FLAG": task_row.get("LOGIC_FLAG", "")
            }
            # print(task_data)
            # 插入数据到目标数据库
            insert_data('dm', dm_cursor, "TODO_TASK", task_data)
            # 更新 SYNC_FLAG 为 1，表示已同步
            # update_sync_flag(pg_cursor, "TODO_TASK_XZ", task_row["ID"])
            task_update_data = {'SYNC_FLAG': 1}
            task_update_condition = "ID = %s"  # 或者 "ID = %s" 对于 PostgreSQL
            task_update_condition_values = (task_row.get('ID'),)  # 条件值
            update_data('pg', pg_cursor, "TODO_TASK_XZ", task_update_data, task_update_condition,
                        task_update_condition_values)

        # 查询 TASK_USER_RELATION_XZ 表数据，条件是 TASK_ID 等于当前任务的 TASK_ID
        pg_task_user_rows = query_data(pg_cursor, "TASK_USER_RELATION_XZ", columns="*", condition="SYNC_FLAG = 0")
        # 循环处理 TASK_USER_RELATION_XZ 表数据
        for task_user_row in pg_task_user_rows:
            # 构造任务与用户关系数据
            task_user_data = {
                "REL_ID": task_user_row.get("REL_ID"),  # 从查询结果中获取 REL_ID
                "TASK_ID": task_user_row.get("TASK_ID"),  # 从查询结果中获取 TASK_ID
                "USER_ID": task_user_row.get("USER_ID"),  # 从查询结果中获取 USER_ID
                "DATA_OPER_IDENT": task_user_row.get("DATA_OPER_IDENT", "I"),  # 默认值为 "I"
                "DATA_STOR_TIME": task_user_row.get("DATA_STOR_TIME", ""),  # 从查询结果中获取 DATA_STOR_TIME
                "DEPART_CODE": task_user_row.get("DEPART_CODE", "")  # 从查询结果中获取 DEPART_CODE
            }
            # print(task_user_data)
            # return
            # 插入任务与用户关系数据到目标数据库
            insert_data('dm', dm_cursor, "TASK_USER_RELATION", task_user_data)
            # 更新 SYNC_FLAG 为 1，表示已同步
            task_user_update_data = {'SYNC_FLAG': 1}
            task_user_update_condition = "REL_ID = %s"  # 或者 "ID = %s" 对于 PostgreSQL
            task_user_update_condition_values = (task_user_row.get('REL_ID'),)  # 条件值
            update_data('pg', pg_cursor, "TASK_USER_RELATION_XZ", task_user_update_data, task_user_update_condition,
                        task_user_update_condition_values)

        # 提交事务
        dm_conn.commit()
        pg_conn.commit()

        task_user_rows = query_data_json(dm_cursor, "TASK_USER_RELATION", columns="*", condition="")
        task_rows = query_data_json(dm_cursor, "TODO_TASK", columns="*", condition="")
        # print(task_user_rows)
        # print(task_rows)
        # 构造输出的 JSON 格式
        result = {
            'status': 200,
            'Msg': '同步达梦待办任务数据成功',
            'data': [task_user_rows, task_rows]
        }
    except Exception as e:
        # 回滚事务
        if dm_conn:
            dm_conn.rollback()
        result = {
            'status': 500,
            'Msg': f'同步达梦待办任务数据失败: {e}',
            'data': []
        }
    finally:
        # 关闭数据库连接
        close_connection(dm_conn, dm_cursor)
        close_connection(pg_conn, pg_cursor)

        # 输出结果
    # print(result)
    return result

def sync_table_data(dm_cursor, pg_cursor, dm_table, pg_table):
    try:
        import datetime
        # 计算两天前的时间
        two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
        # 格式化时间为适合数据库查询的格式，具体格式可能需要根据数据库要求调整
        formatted_time = two_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        # 构建查询条件
        condition = f"CREATE_TIME >= '{formatted_time}'"
       # condition = None
        # 首次同步，查询所有数据
        # condition = None  # 解除注释以恢复首次同步逻辑
        print(f"查询条件: {condition}")
        dm_data = query_data(dm_cursor, dm_table, columns="*", condition=condition)

        if not dm_data:
            print(f"表 {dm_table} 没有数据需要同步。")
            return True
        
        # 获取 PostgreSQL 表的列名
        columns = get_columns(pg_cursor, pg_table)
        print(f"列名：{columns}")

        if dm_data:
            for row in dm_data:
                print(f"当前处理的行: {row}")

                rowdata = {}
                if dm_table == "SYS_USER":
                    rowdata = {
                        "id": row.get('ID', None),
                        "username": row.get('USERNAME', None),
                        "realname": row.get('REALNAME', None),
                        "password": row.get('PASSWORD', None),
                        "salt": row.get('SALT', None),
                        "avatar": row.get('AVATAR', None),
                        "birthday": row.get('BIRTHDAY', None),
                        "sex": row.get('SEX', None),
                        "email": row.get('EMAIL', None),
                        "phone": row.get('PHONE', None),
                        "org_code": row.get('ORG_CODE', None),
                        "status": row.get('STATUS', None),
                        "del_flag": row.get('DEL_FLAG', None),
                        "third_id": row.get('THIRD_ID', None),
                        "third_type": row.get('THIRD_TYPE', None),
                        "activiti_sync": row.get('ACTIVITI_SYNC', None),
                        "work_no": row.get('WORK_NO', None),
                        "post": row.get('POST', None),
                        "telephone": row.get('TELEPHONE', None),
                        "create_by": row.get('CREATE_BY', None),
                        "create_time": row.get('CREATE_TIME', None),
                        "update_by": row.get('UPDATE_BY', None),
                        "update_time": row.get('UPDATE_TIME', None),
                        "user_identity": row.get('USER_IDENTITY', None),
                        "depart_ids": row.get('DEPART_IDS', None),
                        "rel_tenant_ids": row.get('REL_TENANT_IDS', None),
                        "client_id": row.get('CLIENT_ID', None),
                        "identity_number": row.get('IDENTITY_NUMBER', None),
                        "idt_user_custom_unique": row.get('IDT_USER_CUSTOM_UNIQUE', None),
                        "apps": row.get('APPS', None),
                        "attribute": row.get('ATTRIBUTE', None),
                    }
                elif dm_table == "SYS_DEPART":
                    rowdata = {
                        "id": row.get('ID', None),
                        "parent_id": row.get('PARENT_ID', None),
                        "depart_name": row.get('DEPART_NAME', None),
                        "depart_name_en": row.get('DEPART_NAME_EN', None),
                        "depart_name_abbr": row.get('DEPART_NAME_ABBR', None),
                        "depart_order": row.get('DEPART_ORDER', None),
                        "description": row.get('DESCRIPTION', None),
                        "org_category": row.get('ORG_CATEGORY', None),
                        "org_type": row.get('ORG_TYPE', None),
                        "org_code": row.get('ORG_CODE', None),
                        "mobile": row.get('MOBILE', None),
                        "fax": row.get('FAX', None),
                        "address": row.get('ADDRESS', None),
                        "memo": row.get('MEMO', None),
                        "status": row.get('STATUS', None),
                        "del_flag": row.get('DEL_FLAG', None),
                        "qywx_identifier": row.get('QYWX_IDENTIFIER', None),
                        "create_by": row.get('CREATE_BY', None),
                        "create_time": row.get('CREATE_TIME', None),
                        "update_by": row.get('UPDATE_BY', None),
                        "update_time": row.get('UPDATE_TIME', None),
                        "pids": row.get('PIDS', None),
                        "idt_org_custom_unique": row.get('IDT_ORG_CUSTOM_UNIQUE', None),
                        "up_org_code": row.get('UP_ORG_CODE', None),
                    }
                else:
                    raise ValueError(f"不支持的表名: {dm_table}")

                print(f"处理后的 rowdata: {rowdata}")

                # 检查数据是否已经存在于 PostgreSQL 数据库中
                #check_query = f'SELECT 1 FROM "{pg_table}" WHERE "id" = %s'
               # check_query = f'SELECT 1 FROM {pg_table} WHERE id = %s'
                check_query = f'SELECT id, update_time FROM {pg_table} WHERE id = %s'
                print(f"完整 SQL 语句: {check_query % (row['ID'],)}")  # 仅用于调试，生产环境避免这样做
                pg_cursor.execute(check_query, (row['ID'],))
                existing_data = pg_cursor.fetchone()

                if existing_data:
                    # 如果更新时间和创建时间不一致，执行更新操作
                    if row.get('UPDATE_TIME') != existing_data[1]:  # 使用索引访问元组中的 update_time
                        print(f"准备更新数据: {rowdata}")
                        # update_data('pg', pg_cursor, pg_table, rowdata, "id = %s", (row['ID'],))
                        print(f"更新数据到 PostgreSQL 数据库: {row}")
                    else:
                        print(f"数据 {row['ID']} 已经存在于 PostgreSQL 数据库中，跳过插入。")
                else:
                    # 插入数据到 PostgreSQL 数据库
                    print(f"准备插入数据: {rowdata}")
                    insert_data('pg', pg_cursor, pg_table, rowdata)

            print(f"表 {dm_table} 数据同步到 {pg_table} 成功！")
        return True
    except Exception as e:
        print(f"同步 {dm_table} 到 {pg_table} 时出错: {e}")
        return False


# 新增同步函数
def sync_table_datab(dm_cursor, pg_cursor, dm_table, pg_table):
    try:
        import datetime
        # 计算两天前的时间
        two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
        # 格式化时间为适合数据库查询的格式，具体格式可能需要根据数据库要求调整
        formatted_time = two_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        # 构建查询条件
        condition = f"XZ_CREATE_TIME >= '{formatted_time}'"
        # 首次同步，查询所有数据
        condition = None
        dm_data = query_data(dm_cursor, dm_table, columns="*", condition=condition)

       # select_query = 'SELECT "ID", "USERNAME", "REALNAME" FROM "SYS_USER" LIMIT 1'
       # pg_cursor.execute(select_query)
      #  result = pg_cursor.fetchone()
      #  print(result)
        #return True
        if dm_data:
            for row in dm_data:
                 # 确保访问字段时使用正确的键
                rowdata = {}
                if dm_table == "SYS_USER":
                    rowdata = {
                        "id": row['ID'],
                        "username": row['USERNAME'],
                        "realname": row['REALNAME'],
                        "password": row['PASSWORD'],
                        "salt": row['SALT'],
                        "avatar": row['AVATAR'],
                        "birthday": row['BIRTHDAY'],
                        "sex": row['SEX'],
                        "email": row['EMAIL'],
                        "phone": row['PHONE'],
                        "org_code": row['ORG_CODE'],
                        "status": row['STATUS'],
                        "del_flag": row['DEL_FLAG'],
                        "third_id": row['THIRD_ID'],
                        "third_type": row['THIRD_TYPE'],
                        "activiti_sync": row['ACTIVITI_SYNC'],
                        "work_no": row['WORK_NO'],
                        "post": row['POST'],
                        "telephone": row['TELEPHONE'],
                        "create_by": row['CREATE_BY'],
                        "create_time": row['CREATE_TIME'],
                        "update_by": row['UPDATE_BY'],
                        "update_time": row['UPDATE_TIME'],
                        "user_identity": row['USER_IDENTITY'],
                        "depart_ids": row['DEPART_IDS'],
                        "rel_tenant_ids": row['REL_TENANT_IDS'],
                        "client_id": row['CLIENT_ID'],
                        "identity_number": row['IDENTITY_NUMBER'],
                        "idt_user_custom_unique": row['IDT_USER_CUSTOM_UNIQUE'],
                        "apps": row['APPS'],
                        "attribute": row['ATTRIBUTE'],
                    }
                elif dm_table == "SYS_DEPART":
                    rowdata = {
                        "id": row['ID'],
                        "parent_id": row['PARENT_ID'],
                        "depart_name": row['DEPART_NAME'],
                        "depart_name_en": row['DEPART_NAME_EN'],
                        "depart_name_abbr": row['DEPART_NAME_ABBR'],
                        "depart_order": row['DEPART_ORDER'],
                        "description": row['DESCRIPTION'],
                        "org_category": row['ORG_CATEGORY'],
                        "org_type": row['ORG_TYPE'],
                        "org_code": row['ORG_CODE'],
                        "mobile": row['MOBILE'],
                        "fax": row['FAX'],
                        "address": row['ADDRESS'],
                        "memo": row['MEMO'],
                        "status": row['STATUS'],
                        "del_flag": row['DEL_FLAG'],
                        "qywx_identifier": row['QYWX_IDENTIFIER'],
                        "create_by": row['CREATE_BY'],
                        "create_time": row['CREATE_TIME'],
                        "update_by": row['UPDATE_BY'],
                        "update_time": row['UPDATE_TIME'],
                        "pids": row['PIDS'],
                        "idt_org_custom_unique": row['IDT_ORG_CUSTOM_UNIQUE'],
                        "up_org_code": row['UP_ORG_CODE'],
                    }
                else:
                    raise ValueError(f"不支持的表名: {dm_table}")

                # 检查数据是否已经存在于 PostgreSQL 数据库中
               # check_query = f"SELECT 1 FROM {pg_table} WHERE ID = %s"
                check_query = f'SELECT 1 FROM "{pg_table}" WHERE "id" = %s'
                pg_cursor.execute(check_query, (row['ID'],))
                existing_data = pg_cursor.fetchone()
                if existing_data:
                    # 查看更新时间和创建时间是否一致
                    if row['UPDATE_TIME'] != rowdata['update_time']:
                        # 如果更新时间和创建时间不一致，执行更新操作
                        update_data('pg', pg_cursor, pg_table, rowdata, "id = %s", (row['ID'],))
                        print(f"更新数据到 PostgreSQL 数据库: {row}")
                    else:
                        print(f"数据 {row['ID']} 已经存在于 PostgreSQL 数据库中，跳过插入。")
                # 插入数据到 PostgreSQL 数据库
                print(f"插入数据到 PostgreSQL 数据库: {row}")
      
                insert_data('pg', pg_cursor, pg_table, rowdata)
            print(f"表 {dm_table} 数据同步到 {pg_table} 成功！")
        else:
            print(f"表 {dm_table} 没有数据需要同步。")
        return True
    except Exception as e:
        print(f"同步 {dm_table} 到 {pg_table} 时出错: {e}")
        return False

def sync_user_org_data():
    dm_conn = None
    pg_conn = None
    try:
        # 连接达梦数据库
        dm_conn, dm_cursor = connect_db("dm", dm_conn_params_user, schema="QBDATA")
        # 连接 PostgreSQL 数据库
        pg_conn, pg_cursor = connect_db("pg", pg_conn_params)

    
        sync_table_data(dm_cursor, pg_cursor, "SYS_DEPART", "sys_depart")
        sync_table_data(dm_cursor, pg_cursor, "SYS_USER", "sys_user_xz")
        # 提交事务
        pg_conn.commit()
        result = {
            'status': 200,
            'Msg': '用户表和组织机构表数据同步成功',
            'data': []
        }

    except Exception as e:
        # 回滚事务
        if pg_conn:
            pg_conn.rollback()
        result = {
            'status': 500,
            'Msg': f'用户表和组织机构表数据同步失败: {e}',
            'data': []
        }
    finally:
        # 关闭数据库连接
        close_connection(dm_conn, dm_cursor)
        close_connection(pg_conn, pg_cursor)
    return result

if __name__ == "__main__":

   # userinfolist()
   
    sync_user_org_data()
    main()
    #user_result = test()
    #print(user_result)
# 由于 "return" 只能在函数中使用，这里移除 return 语句
# 若 user_result 有后续使用需求，可直接保留该变量


    # 调用新的同步函数
    # sync_result = sync_user_org_data()
    # print(sync_result)
    # result = main()
    # result = testv2()
    # print(result)