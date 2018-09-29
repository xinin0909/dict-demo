# dict-demo
实现英文字典的查询的小demo，有简单的登录与历史记录的查询。

# search_server.py
1，通过mysql存储用户名，用户密码，单词，解释，查询记录，查询时间，查询用户名
2, 通过os.fork()实现多客户端登录查询

# search_dict.py
1, 通过分割把dict.txt插入mysql数据表
2，创建三个表，users，hists，words

# search_client.py
1, 实现简单的二级界面
2，通过向客户端发送请求，实现单词的查询
