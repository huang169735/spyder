import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "spyder_data")
# 使用cursor()方法获取操作游标
cursor = db.cursor()

'''
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
           LAST_NAME, AGE, SEX, INCOME) \
           VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
           ('Mac', 'Mohan', 20, 'M', 2000):
'''
def excuteData(sql):
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

def queryData(sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        return cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()