from pywebio.output import put_markdown, put_buttons, put_html, put_text
from pywebio import start_server
import random
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info

import sys
import random
from demo import ABY3_ASS_simulator,\
    get_all_from_aby3_spu_dic,get_all_from_ASS_pyu_dic,\
    add_user_2_aby3_spu_dic, add_user_2_ASS_pyu_dic,\
    get_password_from_aby3_spu_dic,get_password_from_ASS_pyu_dic,\
    check, refresh_shares


# 注册页面
def register():
    # 获取用户输入的用户名和密码
    info = input_group(('输入用户名和密码', '进行身份验证：'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您的密码："), name="password", type=PASSWORD),
    ])

    # 更新用户名和密码
    add_user_2_aby3_spu_dic(str(info['username']),str(info['password']))
    add_user_2_ASS_pyu_dic(str(info['username']),str(info['password']))
    
    # 更新主页展示的用户名和密码
    put_html('<meta http-equiv="refresh" content="0;url=/">')

    # 提示注册成功
    put_text('注册成功！')

# 注册页面
def login():
    # 获取用户输入的用户名
    username_input = input("请输入您的用户名：")

    # 如果找到了对应的密码，则自动填写密码输入框
    if username_input in get_all_from_aby3_spu_dic():
        password_input = input(("请输入您的密码："),  type=PASSWORD, value='xxxxxxxx')
    else:
        password_input = input(("请输入您的密码："), type=PASSWORD)

    # 验证用户名和密码
    if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_ASS_pyu_dic(5, username_input):
        put_text('登录成功！')
    else:
        # 显示注册按钮
        # put_buttons(['注册'], onclick=[register])
        put_text('登录失败！')

def refresh_button():
    info = input_group(('请输入您的用户名用户名,系统将自动刷新存在应用服务端的秘密份额'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您想检查的服务器："), name="server", type=TEXT),
    ])
    if info['username'] in get_all_from_aby3_spu_dic():
        before,after = refresh_shares(5,info['username'],int(info['server']))
        put_text('刷新成功！')
        put_text(before)
        put_text(after)
    else:
        put_text('非法的用户名！')
        

# 主页
def home():
    # 显示已有的用户名和密码
    put_markdown('### 应用端服务器已有的用户名和密码')
    users = get_all_from_aby3_spu_dic()
    for username, password in users.items():
        put_markdown('- {}: {}'.format(username, password))

    # 显示登录页面
    put_markdown('### 用户自行选择操作')
    # 展示登录和注册按钮
    put_buttons(['登录', '注册','刷新'], onclick=[login, register, refresh_button])

# 启动应用
ABY3_ASS_simulator()
start_server(home, port=8080)
