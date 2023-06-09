from pywebio.output import put_markdown, put_buttons, put_html, put_text
from pywebio import start_server
import random
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from demo import ABY3_shamir_simulator,\
    get_all_from_aby3_spu_dic,get_all_from_shamir_pyu_dic,\
    add_user_2_aby3_spu_dic, add_user_2_shamir_pyu_dic,erase_user_from_aby3_spu_dic,\
    get_password_from_aby3_spu_dic,get_password_from_shamir_pyu_dic,\
    attack_simulator,check,server_check,server_check_2
from logger import *

# 注册页面
def register():
    # 获取用户输入的用户名和密码
    info = input_group(('输入您的自定义用户名和密码'), [
        input(("请输入您的用户名："), name="username", type=TEXT),
        input(("请输入您的密码："), name="password", type=PASSWORD),
    ])
    if info['username'] in get_all_from_shamir_pyu_dic():
        popup('注册错误', '用户名重复')
        make_WebInfo_Logger(info['username'] + '注册失败，已存在同名用户')
    else:
    # 更新用户名和密码
        sel = select("是否在浏览器中保存密码:", options=["保存", "不保存"])
        add_user_2_shamir_pyu_dic(str(info['username']),str(info['password']))
        if sel == '保存':
            add_user_2_aby3_spu_dic(str(info['username']),str(info['password']))

        # 更新主页展示的用户名和密码
        put_html('<meta http-equiv="refresh" content="0;url=/">')

        # 提示注册成功
        with use_scope('register',clear=True):
            put_text('注册成功！')
            make_WebInfo_Logger(info['username'] + '成功注册账户')

# 注册页面
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

    # 用户名和密码可以通过ABY3协议和shamir恢复，并且二者可以匹配
    if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_shamir_pyu_dic(5, 3, username_input):
        with use_scope('login',clear=True):
            put_text(username_input,'登录成功！')
            make_WebInfo_Logger(str(username_input)+'使用ABY3协议以及shamir协议恢复密码,登录系统成功')
    
    # 用户名和密码可以通过ABY3协议和shamir恢复，但二者不能匹配
    elif username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) != get_password_from_shamir_pyu_dic(5,3, username_input):
        # 显示注册按钮
        # put_buttons(['注册'], onclick=[register])
        with use_scope('login',clear=True):
            put_text(username_input,'登录失败！')
            make_WebInfo_Logger(str(username_input)+'登录系统失败')
    
    
    # 在浏览器找不到这个用户名对应的密码，但是这个账户是有的，那就根据用户的密码进行比对
    else:
        if username_input in get_all_from_shamir_pyu_dic():
            add_user_2_aby3_spu_dic(username_input,password_input) #这一步是暂存，还会删掉
            if username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) == get_password_from_shamir_pyu_dic(5, 3, username_input):
                with use_scope('login',clear=True):
                    put_text(username_input,'登录成功！')
                    make_WebInfo_Logger(str(username_input)+'使用ABY3协议以及shamir协议恢复密码,登录系统成功')
        
            # 比对失败
            elif username_input in get_all_from_aby3_spu_dic() and get_password_from_aby3_spu_dic(username_input) != get_password_from_shamir_pyu_dic(5, 3, username_input):
                # 显示注册按钮
                # put_buttons(['注册'], onclick=[register])
                with use_scope('login',clear=True):
                    put_text(username_input,'登录失败！')
                    make_WebInfo_Logger(str(username_input)+'登录系统失败')
            # 删掉暂时存储的密码
            erase_user_from_aby3_spu_dic(username_input)
        else:
            put_text(username_input,'登录失败！')
            make_WebInfo_Logger(str(username_input)+'不存在该账号')

# 攻击页面
def attack():
    info = input_group(('分别输入想攻击的服务器台数和想要攻击的对象：'), [
        input(("输入要攻击的服务器台数："), name="num", type=TEXT),
        input(("输入要攻击的对象："), name="name", type=TEXT),
    ])
    if int(info['num']) > 5 or info['name'] not in get_all_from_shamir_pyu_dic():
        put_text('服务器数量为5台,无法攻击超过五台的服务器数量或者攻击对象不存在')
        make_WebInfo_Logger('攻击失败，攻击详情为：攻击的台数为 '+info['num']+'攻击的对象为'+info['name'])
    else :
        random_sequence = random.sample(range(5), int(info['num']))
        put_text('目标攻击的服务器是：',random_sequence)
        attack_simulator(random_sequence,info['name'])
        make_WebInfo_Logger('攻击成功，攻击详情为：攻击的服务器为 '+str(random_sequence)+'攻击的对象为'+info['name'])
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
    if username_input in get_all_from_aby3_spu_dic():
        result = server_check(username_input)
        if result is None :
            put_markdown('没有检测到被攻击的服务器')
        elif result == 'WARNING' :
            put_text('大于等于三台服务器被攻击！：',result)
        else:
            put_text('系统自检到被攻击的服务器是：',result)
        print(result)
    else:
        password = input("由于您未在浏览器中保存密码，请输入您的密码进行验证：")
        result = server_check_2(username_input,password)
        if result is None :
            put_markdown('没有检测到被攻击的服务器')
        elif result == 'WARNING' :
            put_text('大于等于三台服务器被攻击！：',result)
        else:
            put_text('系统自检到被攻击的服务器是：',result)
        print(result)
        


# 主页
def home():
    # 显示已有的用户名和密码
    put_markdown('### 应用端服务器已有的用户名和密码')
    users = get_all_from_shamir_pyu_dic()
    for username, password in users.items():
        put_markdown('- {}: {}'.format(username, password))

    # 显示登录页面
    put_markdown('### 用户自行选择操作')
    # 展示登录和注册按钮
    put_buttons(['登录', '注册'], onclick=[login, register])
    put_buttons(['攻击','报警'], onclick=[attack,servercheck])
    put_buttons(['查看日志'], onclick=[lambda: go_app('log')])

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
        if memory_logger[i] == 'shamirInfo':
            put_text(memory_logger[i+1]).style('color: RosyBrown; font-size: 10px')
            i+=1
    
def index():
    put_link('进入主页面\n', app='home')  # Use `app` parameter to specify the task name
    put_link('进入日志页面', app='log')

# 启动应用
ABY3_shamir_simulator()
start_server([index,home,log], port=8080)
