from pywebio.output import put_markdown, put_buttons, put_html, put_text
from pywebio import start_server
import random
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info

import sys
import random
from demo import ABY3_shamir_simulator,\
    get_all_from_aby3_spu_dic,get_all_from_shamir_pyu_dic,\
    add_user_2_aby3_spu_dic, add_user_2_shamir_pyu_dic,\
    get_password_from_aby3_spu_dic,get_password_from_shamir_pyu_dic,\
    attack_simulator,check,server_check


# 注册页面
def register():
    # 获取用户输入的用户名和密码
    info = input_group(('输入用户名和密码', '进行身份验证：'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您的密码："), name="password", type=PASSWORD),
    ])

    # 更新用户名和密码
    add_user_2_aby3_spu_dic(str(info['username']),str(info['password']))
    add_user_2_shamir_pyu_dic(str(info['username']),str(info['password']))
    
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
    if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_shamir_pyu_dic(5,3,username_input):
        put_text('登录成功！')
    else:
        # 显示注册按钮
        # put_buttons(['注册'], onclick=[register])
        put_text('登录失败！')

# 攻击页面
def attack():
    info = input_group(('分别输入想攻击的服务器台数和想要攻击的对象：'), [
        input(("输入要攻击的服务器台数："), name="num", type=TEXT),
        input(("输入要攻击的对象："), name="name", type=TEXT),
    ])
    if int(info['num']) > 5 or info['name'] not in get_all_from_aby3_spu_dic():
        put_text('服务器数量为5台,无法攻击超过五台的服务器数量或者攻击对象不存在')
    else :
        random_sequence = random.sample(range(5), int(info['num']))
        put_text('目标攻击的服务器是：',random_sequence)
        attack_simulator(random_sequence,info['name'])
        # check()
        # print('11111')
        # put_html('<meta http-equiv="refresh" content="0;url=/">')
        put_markdown('### 被劫持后已有的用户名和密码')
        users = get_all_from_shamir_pyu_dic()
        for username, password in users.items():
            put_markdown('- {}: {}'.format(username, password))
        # check()
        
        
# 提示服务器自检
def servercheck():
    username_input = input("请输入您的用户名：")
    result = server_check(username_input)
    if result is None :
        put_markdown('没有检测到被攻击的服务器')
    elif result == 'WARNING' :
        put_text('大于等于三台服务器被攻击！：',result)
    else:
        put_text('系统自检到被攻击的服务器是：',result)
    print(result)

# def refresh():
#     ABY3_shamir_simulator()
#     home()
#     put_html('<meta http-equiv="refresh" content="0;url=/">')

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
    put_buttons(['攻击','报警'], onclick=[attack,servercheck])

# 启动应用
ABY3_shamir_simulator()
start_server(home, port=8080)
