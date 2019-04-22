import pymysql
import uuid

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
def excuteData(sql,args=None):
    try:
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()

def queryData(sql,args=None):
    try:
        # 执行SQL语句
        cursor.execute(sql,args)
        # 获取所有记录列表
        return cursor.fetchall()
    except Exception:
        print("Error: unable to fetch data")

def queryCount(sql,args):
    try:
        # 执行SQL语句
        cursor.execute(sql, args)
        # 获取所有记录列表
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print("Error: unable to fetch data")

'''
    初始化主数据
'''
def buildMainData(sightSpotList):
    querySql = "SELECT COUNT(ID) FROM scenicSpot WHERE name = %s ";
    queryAll = "SELECT ID,NAME FROM scenicSpot"
    saveSql = "INSERT INTO scenicSpot (ID,Name) VALUES (%s, %s)"
    result = []
    for name in sightSpotList:
        count = queryCount(querySql,name);
        if count == 0:
            excuteData(saveSql,(str(uuid.uuid4()),name))
    qd = queryData(queryAll)
    for row in qd:
        ID = row[0]
        scenicName = row[1]
        result.append({"name":scenicName,"id":ID})
    # 关闭数据库连接
    #close()
    return result

def saveLog(updateCount,Code,LastUpPID,PgNo):
    saveSql = "INSERT INTO update_data_log (updateDate,updateCount,Code,LastUpPID,PgNo) VALUES (SYSDATE(),%s,%s,%s,%s)"
    excuteData(saveSql,(updateCount, Code, LastUpPID, PgNo))

'''
    保存数据
'''
def saveData(id,md):
    queryCountSql = "SELECT COUNT(ID) FROM evalDtl WHERE ID = %s ";
    saveSql = "INSERT INTO evalDtl (ID,Name,Content,starText,date,PID,pageNo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for data in md:
        count = queryCount(queryCountSql,data['id']);
        if count == 0:
            starText = data['starText'].replace('\n', '').replace(' ', '')
            excuteData(saveSql,(data['id'], data['name'], data['content'], starText, data['date'], id, data['pageNo']))

def saveErrorLog(Code,parms,pid):
    queryCountSql = "SELECT COUNT(ID) FROM update_error_log WHERE parms = %s";
    count = queryCount(queryCountSql, str(parms));
    if count == 0:
        saveSql = "INSERT INTO update_error_log (updateTime,Code,parms,status,pid) VALUES (SYSDATE(),%s,%s,0,%s)"
        excuteData(saveSql,(Code, str(parms), pid))

def updateErrorLog(id):
    sql = "UPDATE update_error_log SET status = 1 WHERE ID = %s"
    excuteData(sql,(id))

def deleteErroeLog():
    sql = "DELETE FROM update_error_log WHERE status = 1"
    excuteData(sql)
    deleteScore()

def queryErrorLog(code):
    sql = "SELECT ID,parms,pid FROM update_error_log WHERE status = 0 AND code = %s"
    return queryData(sql,code)

def updateScore(proxy):
    sql = "UPDATE proxys SET score = score-1 WHERE score > 0 AND ip = %s AND port = %s"
    excuteData(sql,(proxy['ip'],proxy['port']))

def deleteScore():
    sql = "DELETE FROM proxys WHERE score = 0"
    excuteData(sql)

def close():
    db.close()