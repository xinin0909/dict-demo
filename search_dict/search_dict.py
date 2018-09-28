import pymysql

#连接数据库
def sear_connect():
    db = pymysql.connect(
        host ="localhost",
        port = 3306,
        user = 'root',
        passwd = 'root',
        charset='utf8',
        database='seardict',
    )
    cursor = db.cursor()
    with open("dict.txt",'r') as w:
        while True:
            s = w.readline()[:-1]
            if  not s:
                break
            a=s.split(maxsplit=1)
            # for x in a:
            #     print(x)
            if len(a) !=2:
                a.append('null')
            cursor.execute("insert into words(word1,means) values(%s,%s)",[a[0],a[1]])
    cursor.close()
    db.commit()
    db.close()
if __name__ ==   "__main__":
    #sear_connect()
    sear_connect()