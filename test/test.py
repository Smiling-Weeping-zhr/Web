import psycopg2
 
try:
    # 建立数据库连接
    connection = psycopg2.connect(
        user="postgres",
        password="smilingweeping",
        host="localhost",
        port="5432",
        database="postgres"
    )
 
    # 创建一个游标对象
    cursor = connection.cursor()
 
    # 执行 SQL 查询
    cursor.execute("SELECT version();")
 
    # 获取查询结果
    record = cursor.fetchone()
    print("You are connected to - ", record)
 
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # 关闭游标和连接
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")