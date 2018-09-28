from socket import *
import sys,getpass

#创建网络连接
def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    ADDR=(HOST,PORT)
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while 1:
        print('''
            =================界面==================
            ----1,注册---2,登录 ----3，退出--------
            =======================================
            ''')
        try:

            cmd = int(input('输入：'))
        except Exception as e:
            print("命令错误")
            continue
        if cmd not in [1,2,3]:
            print('请输入正确的')
            sys.stdin.flush()
        elif cmd == 1:
            r = do_register(s)
            if r== 0:
                print("注册成功")
                # logins(s,name) #进入2级界面
            elif r==1:
                print("用户已存在")
            else:
                print("注册失败")
        elif cmd == 2:
            name = do_login(s)
            if name:
                print('登陆成功')
                logins(s,name)
            else:
                print('用户名或密码不正确')

        elif cmd == 3:
            s.send(b'E')
            sys.exit('谢谢使用')


def do_register(s):
    while True:
        name = input("请输入用户名")
        passwd = getpass.getpass("请输入密码")
        passwd1 = getpass.getpass("Again:")
        if (' ' in name)or (' ' in passwd):
            print("用户名密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = 'Z {} {}'.format(name,passwd)
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data =='ok':
            return  0
        elif data =='EXISTS':
            return 1
        else:
            return 2

def do_login(s):
    name = input('用户名')
    passwd= getpass.getpass('密码')
    msg = 'L {} {}'.format(name,passwd)
    s.send(msg.encode())
    data =s.recv(128).decode()
    if data =='ok':
        return name
    else:
        return



def logins(s,name):
    while True:
        print('''
        ===========查询界面==============
        ----1，查词--2，历史--3，退出----
        =================================

        ''')
        try:

            cmd = int(input('输入：'))
        except Exception as e:
            print("命令错误")
            continue
        if cmd not in [1, 2, 3]:
            print('请输入正确的')
            sys.stdin.flush()
            continue
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return
def do_query(s,name):
    while True:
        word = input('单词：')
        if word=='##':
            break
        msg ='Q {} {}'.format(name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        if data =='OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("查询失败")
def do_hist(s,name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data =='OK':
        while True:
            data = s.recv(1024).decode()
            if data =='##':
                break
            print(data)
    else:
        print("没有历史记录")



if __name__=="__main__":
    main()
