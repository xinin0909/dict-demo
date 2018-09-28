'''
name:Tedu
date:2018-9-28
email:3275049908@qq.com

'''
import pymysql
import re,time
from socket import  *
import os,sys,signal



#登录
def do_login(c,db,data):
    print('登陆操作')
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor= db.cursor()
    sql = "select * from users where name = '%s' and passwd = '%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()


    if r ==None:
        c.send(b'FALL')
    else:
        print('%s登陆成功'%name)
        c.send(b'ok')

#注册
def do_register(c, db, data):
    print('注册操作')
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from users where name = '%s'" % name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return
    # 用户不存在时
    sql = "insert into users (name,passwd)values ('%s','%s')" % (name, passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'ok')
    except:
        db.rollback()
        c.send(b'FALL')
    else:
        print('注册成功')

#查词
def do_query(c,db,data):
    print("查询操作")
    l =data.split(' ')
    name= l[1]
    word=l[2]
    cursor =db.cursor()
    sql="select * from words where word1='%s'"%word
    cursor.execute(sql)
    a = cursor.fetchone()
    print(a)
    if a == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')
        time.sleep(0.1)
        c.send(a[1].encode())
    cursor.close()
    db.commit()
    #------------------------
    #文本查询
    # try:
    #     f=open()
    # except:
    #     print()
    #     for line in

#插入记录
def insert_history(c,db,data):
    print("执行插入历史记录")
    l= data.split(" ")
    name = l[1]
    word=l[2]
    tm=time.ctime()
    cursor = db.cursor()
    sql ="insert into hist(name,word,time) values ('%s','%s','%s')"%(name,word,tm)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


#查询历史记录
def do_hist(c,db,data):
    print('历史记录')
    l=data.split(' ')
    name =l[1]
    cursor =db.cursor()
    sql="select * from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'FALL')
        return
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg="%s    %s    %s"%(i[1],i[2],i[3])
        print(msg)
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')

# def do_parent(s):
#     user={}
#     while True:
#         msg,addr = s.recvfrom(1024)
#         msgList=msg.decode().split(' ')
#
#         if msgList[0]=='Z':
#             do_login(s,msgList[1],msgList[2])

def do_child(c,db):
    while True:
        msg = c.recv(128).decode()
        print(c.getpeername(),':',msg)
        if (not msg) or msg[0]=='E':
            c.close()
            sys.exit(0)
        elif  msg[0]=='Z':
            do_register(c,db,msg)
            # c.send()
        elif msg[0]=='L':
            do_login(c,db,msg)
        elif msg[0]=='Q':
            do_query(c,db,msg)
            insert_history(c,db,msg)
        elif msg[0]=='H':
            do_hist(c,db,msg)


#实现多线程
def main():
    db = pymysql.connect(
        host="localhost",
        user='root',
        password='root',
        charset='utf8',
        database='seardict',
        port=3306)
    ADDR = ('0.0.0.0',8888)

    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while 1:
        try:
            c,addr =s.accept()
            print("等待连接",addr)
        except KeyboardInterrupt:
            print('服务端退出')
        except Exception as e:
            print(e)
            continue
        pid = os.fork()
        if pid < 0:
            sys.exit('创建进程失败')
        elif pid ==0:
            s.close()
            do_child(c,db)
            # sys.exit()
        else:
            # do_parent(s)
            c.close()
            continue

if __name__ ==   "__main__":
    #sear_connect()
    main()