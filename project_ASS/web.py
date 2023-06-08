from pywebio.output import put_markdown, put_buttons, put_html, put_text
from pywebio import start_server
import random
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.session import info as session_info

import sys
import random
from demo import ABY3_ASS_simulator,\
    get_all_from_aby3_spu_dic,get_all_from_ASS_pyu_dic,\
    add_user_2_aby3_spu_dic, add_user_2_ASS_pyu_dic,\
    get_password_from_aby3_spu_dic,get_password_from_ASS_pyu_dic,\
    check, refresh_shares
from logger import *
logger = getLogger()

# 注册页面
def register():
    # 获取用户输入的用户名和密码
    info = input_group(('输入您的自定义用户名和密码'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您的密码："), name="password", type=PASSWORD),
    ])
    if info['username'] in get_all_from_aby3_spu_dic():
        popup('注册错误', '用户名重复')
        make_WebInfo_Logger(info['username'] + '注册失败，已存在同名用户')
    else:
    # 更新用户名和密码
        add_user_2_aby3_spu_dic(str(info['username']),str(info['password']))
        add_user_2_ASS_pyu_dic(str(info['username']),str(info['password']))
        
        # 更新主页展示的用户名和密码
        put_html('<meta http-equiv="refresh" content="0;url=/">')

        # 提示注册成功
        with use_scope('register',clear=True):
            put_text('注册成功！')
            make_WebInfo_Logger(info['username'] + '成功注册账户')

# 登录页面
def login():
    # 获取用户输入的用户名
    username_input = input("请输入您的用户名：")
    # 如果找到了对应的密码，则自动填写密码输入框
    if username_input in get_all_from_aby3_spu_dic():
        password_input = input(("请输入您的密码："),  type=PASSWORD, value='xxxxxxxx')
        make_ABY3_Logger('成功找到对应的用户名' + username_input + '并置位占位符 ')
    else:
        password_input = input(("请输入您的密码："), type=PASSWORD)
        make_ABY3_Logger('没有找到对应用户 '+ username_input)

    # 验证用户名和密码
    if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_ASS_pyu_dic(5, username_input):
        with use_scope('login',clear=True):
            put_text(username_input,'登录成功！')
            make_WebInfo_Logger(str(username_input)+'登录系统成功')
    else:
        # 显示注册按钮
        # put_buttons(['注册'], onclick=[register])
        with use_scope('login',clear=True):
            put_text(username_input,'登录失败！')
            make_WebInfo_Logger(str(username_input)+'登录系统失败')

def refresh_button():
    info = input_group(('请输入您的用户名用户名,系统将自动刷新存在应用服务端的秘密份额'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您想刷新份额的服务器："), name="server", type=TEXT),
    ])
    if info['username'] in get_all_from_aby3_spu_dic():
        before,after = refresh_shares(5,info['username'],int(info['server']))
        with use_scope('refresh',clear=True):
            put_text(info['username'],'的秘密份额刷新成功！')
            make_WebInfo_Logger(info['username'] + '的秘密份额刷新成功！')
            put_text(before)
            put_text(after)
    else:
        put_text('非法的用户名！')
        make_WebInfo_Logger(info['username'] + '刷新错误')

  
# 主页
def home():
    # 显示已有的用户名和密码
    put_markdown('### 应用端服务器已有的用户名和密码')
    users = get_all_from_ASS_pyu_dic(5)
    for username, password in users.items():
        put_markdown('- {}: {}'.format(username, password))

    # 显示登录页面
    put_markdown('### 用户自行选择操作')
    # 展示登录和注册按钮
    put_buttons(['登录', '注册','刷新','查看日志'], onclick=[login, register, refresh_button,lambda: go_app('log')])

def log():
    put_buttons(['返回主界面'], [lambda: go_app('home')])
    
    put_text('这里是日志记录')
    put_scrollable(content=memory_logger, height=200)
    for i in range(len(memory_logger)):
        if memory_logger[i] == 'StartInfo':
            put_text(memory_logger[i+1]).style('color: blue; font-size: 10px')
            i+=1
        if memory_logger[i] == 'WebInfo':
            put_text(memory_logger[i+1]).style('color: red; font-size: 10px')
            i+=1
        if memory_logger[i] == 'ABY3Info':
            put_text(memory_logger[i+1]).style('color: purple; font-size: 10px')
            i+=1
        if memory_logger[i] == 'ASSInfo':
            put_text(memory_logger[i+1]).style('color: RosyBrown; font-size: 10px')
            i+=1
    
def index():
    put_link('进入主页面\n', app='home')  # Use `app` parameter to specify the task name
    put_link('进入日志页面', app='log')

# 启动应用
ABY3_ASS_simulator()
start_server([index,home,log], port=8080)
