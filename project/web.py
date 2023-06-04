from pywebio.output import put_markdown, put_buttons, put_html, put_text
from pywebio import start_server
import random
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info

import sys
from demo import ABY3_semi2k_simulator,\
    get_all_from_aby3_spu_dic,\
    add_user_2_aby3_spu_dic, add_user_2_semi2k_spu_dic,\
    get_password_from_aby3_spu_dic,get_password_from_semi2k_spu_dic


# 注册页面
def register():
    # 获取用户输入的用户名和密码
    info = input_group(('输入用户名和密码', '进行身份验证：'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您的密码："), name="password", type=PASSWORD),
    ])

    # 更新用户名和密码
    add_user_2_aby3_spu_dic(str(info['username']),str(info['password']))
    add_user_2_semi2k_spu_dic(str(info['username']),str(info['password']))
    
    # 更新主页展示的用户名和密码
    put_html('<meta http-equiv="refresh" content="0;url=/">')

    # 提示注册成功
    put_text('注册成功！')


def login():
    # 获取用户输入的用户名
    username_input = input("请输入您的用户名：")

    # 如果找到了对应的密码，则自动填写密码输入框
    if username_input in get_all_from_aby3_spu_dic():
        password_input = input(("请输入您的密码："),  type=PASSWORD, value=get_password_from_aby3_spu_dic(username_input))
    else:
        password_input = input(("请输入您的密码："), type=PASSWORD)

    # 验证用户名和密码
    if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_semi2k_spu_dic(username_input):
        put_text('登录成功！')
    else:
        # 显示注册按钮
        # put_buttons(['注册'], onclick=[register])
        put_text('登录失败！')

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
    put_buttons(['登录', '注册'], onclick=[login, register])

# 启动应用
ABY3_semi2k_simulator()
start_server(home, port=8080)
