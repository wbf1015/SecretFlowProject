import secretflow as sf
import spu
import copy
import db
import corn
import jax
import ray
import random
import copy
from shamir import generate_webserver_shares, reconstruct_webserver_secret, webserver_selfcheck
from utils import dict_encode,array2int,decode_unicode
from logger import *

'''
aby3 means the party: user、chrome、TTP
semi2k means the party: webserver1-5
'''
aby3_spu_dic = {}
shamir_dic={}

'''
we need to declare some variable so that we can use it from every function
'''
pyu_user = None
pyu_TTP = None
pyu_chrome = None
pyu_webserver1 = None
pyu_webserver2 = None
pyu_webserver3 = None
pyu_webserver4 = None
pyu_webserver5 = None
aby3_config = None
spu_aby3 = None

# ===============================================================================
'''get return the password encode list'''
def get_password(encode_list):
    return encode_list


'''
transfer all the password to the SPUobject then update the dict
return the dict
'''
def transfer_password(up_dict, pyu, spu_device,store_dic):
    # password = next(iter(up_dict.values()))
    for key in up_dict:
        value = up_dict[key]
        password_pyu = pyu(get_password)(value)
        password_spu = password_pyu.to(spu_device)
        make_ABY3_Logger('ABY3成功分享'+key+'的秘密份额于'+str(password_spu.shares_name))
        store_dic[key] = password_spu
    # return up_dict

'''
store the shamir-based serect shares
'''
def share_shamir_secret(n,t,user_dic,store_dic):
    for key in user_dic:
        value = user_dic[key]
        shares = generate_webserver_shares(n,t,value)
        ss_pyu_webserver1 = pyu_webserver1(get_password)(shares[0])
        ss_pyu_webserver2 = pyu_webserver2(get_password)(shares[1])
        ss_pyu_webserver3 = pyu_webserver3(get_password)(shares[2])
        ss_pyu_webserver4 = pyu_webserver4(get_password)(shares[3])
        ss_pyu_webserver5 = pyu_webserver5(get_password)(shares[4])
        shares = [ss_pyu_webserver1,ss_pyu_webserver2,ss_pyu_webserver3,ss_pyu_webserver4,ss_pyu_webserver5]
        tmp = ''
        for pyu in shares:
            tmp += str(pyu)
        make_shamir_Logger('shamir成功分享'+key+'的秘密份额于'+tmp)
        store_dic[key] = shares

# ===============================================================================
def attack_simulator(server_list,username):
    '''
    shamir_dic={user_name,[[pyu_webserver1],[pyu_webserver2]...[pyu_webserver5]]}
    pyu_webserver1.data = [(1,2),(3,4)...(100,101)]
    '''
    for index in server_list:
        key = username
        value = ray.get(shamir_dic[key][index].data)
        make_shamir_Logger('网站服务器正在从 '+str(shamir_dic[key][index])+' 提取'+username+'的shamir秘密份额并重构')
        element_index = random.randint(0, len(value)-1)
        print('key=',key,'index=',index,'element_index=',element_index)
        print(value)
        for i in range(0,len(value)):
            if i != len(value) - 1:
                tmp = list(value[i])
                tmp[1] += 1
                value[i] = tuple(tmp)
        print(value)
        print(index)
        print(type(shamir_dic[key][index]))
        if index == 0 :
            change_value = pyu_webserver1(get_password)(value)
            make_shamir_Logger(str(index)+'号服务器的内容被更改为'+str(change_value))
            shamir_dic[key][index] = change_value
        elif index == 1 :
            change_value = pyu_webserver2(get_password)(value)
            make_shamir_Logger(str(index)+'号服务器的内容被更改为'+str(change_value))
            shamir_dic[key][index] = change_value
        elif index == 2 :
            change_value = pyu_webserver3(get_password)(value)
            make_shamir_Logger(str(index)+'号服务器的内容被更改为'+str(change_value))
            shamir_dic[key][index] = change_value
        elif index == 3 :
            change_value = pyu_webserver4(get_password)(value)
            make_shamir_Logger(str(index)+'号服务器的内容被更改为'+str(change_value))
            shamir_dic[key][index] = change_value
        elif index == 4 :
            change_value = pyu_webserver5(get_password)(value)
            make_shamir_Logger(str(index)+'号服务器的内容被更改为'+str(change_value))
            shamir_dic[key][index] = change_value
        # check()

# ===============================================================================
def server_check(username):
    make_shamir_Logger('正在进行服务器自测')
    value = copy.deepcopy(shamir_dic[username])
    # check()
    for i in range(0,5):
        value[i] = ray.get(value[i].data)
        make_shamir_Logger('正在从'+str(shamir_dic[username][i])+'提取秘密份额')
    # print(get_password_from_aby3_spu_dic(username))
    attcked_node = webserver_selfcheck(5,3,value,get_password_from_aby3_spu_dic(username))
    return attcked_node

# 如果是那些没有在浏览器保存秘密份额的用户想要报警请调用这个函数
def server_check_2(username,password):
    make_shamir_Logger('正在进行服务器自测')
    add_user_2_aby3_spu_dic(username, password)
    value = copy.deepcopy(shamir_dic[username])
    # check()
    for i in range(0,5):
        value[i] = ray.get(value[i].data)
        make_shamir_Logger('正在从'+str(shamir_dic[username][i])+'提取秘密份额')
    # print(get_password_from_aby3_spu_dic(username))
    attcked_node = webserver_selfcheck(5,3,value,get_password_from_aby3_spu_dic(username))
    erase_user_from_aby3_spu_dic(username)
    return attcked_node
    
    


def check():
    for key in shamir_dic.keys():
        value = shamir_dic[key]
        for i in range(len(value)):
            print(' key=',key,' server_index=',i,' type=',type(value[i]))

        
        
        
        
        
        
    

# ===============================================================================
'''
init the aby3_spu_dic and semi2k_spu_dic
then web can search on above dicts
'''
def ABY3_shamir_simulator():
    user_dic = db.getUser()
    user_dic = dict_encode(user_dic)
    device_dic = corn.ABY3_shamir()
    global pyu_user, pyu_TTP, pyu_TTP, pyu_chrome, pyu_webserver1, pyu_webserver2, pyu_webserver3, pyu_webserver4\
        , pyu_webserver5, aby3_config, spu_aby3
    pyu_user = device_dic['pyu_user']
    pyu_TTP= device_dic['pyu_TTP']
    pyu_chrome = device_dic['pyu_chrome']
    pyu_webserver1 = device_dic['pyu_webserver1']
    pyu_webserver2 = device_dic['pyu_webserver2']
    pyu_webserver3 = device_dic['pyu_webserver3']
    pyu_webserver4 = device_dic['pyu_webserver4']
    pyu_webserver5 = device_dic['pyu_webserver5']
    aby3_config = device_dic['aby3_config']

    spu_aby3 = sf.SPU(aby3_config)
    
    transfer_password(user_dic, pyu_user, spu_aby3, aby3_spu_dic)
    share_shamir_secret(5, 3, user_dic, shamir_dic)
    
    # reveal_test = sf.reveal(semi2k_spu_dic['david'])
    # print(reveal_test)
    # reveal_test = array2int(reveal_test)
    # print(reveal_test)
    # reveal_test = decode_unicode(reveal_test)
    # print(reveal_test)

'''
init the cheetah_spu_dic and semi2k_spu_dic
then web can search on above dicts
'''
def cheetah_semi2k():
    pass
    
 
 # ===============================================================================

def add_user_2_aby3_spu_dic(user_name,password):
    dic = {user_name:password}
    dic = dict_encode(dic)
    transfer_password(dic, pyu_user, spu_aby3, aby3_spu_dic)

def erase_user_from_aby3_spu_dic(user_name):
    aby3_spu_dic.pop(user_name)
    make_ABY3_Logger(user_name+'在ABY3中的暂存记录被删除')

def add_user_2_shamir_pyu_dic(user_name,password):
    dic = {user_name:password}
    dic = dict_encode(dic)
    share_shamir_secret(5,3,dic,shamir_dic)

def add_user_2_cheetah_spu_dic(user_name,password):
    pass

'''
Input : username
Output : password revealed by aby3 from user、chrome、TTP
'''
def get_password_from_aby3_spu_dic(user_name):
    make_ABY3_Logger('浏览器、用户、可信第三方正在从 '+str(aby3_spu_dic[user_name].shares_name)+' 提取'+user_name+'的ABY3秘密份额并重构')
    return decode_unicode(array2int(sf.reveal(aby3_spu_dic[user_name])))

'''
Input : username
Output : password revealed by shamir from webserver1-5
'''
def get_password_from_shamir_pyu_dic(n,t,user_name):
    # check()
    value = copy.deepcopy(shamir_dic[user_name])
    # check()
    make_shamir_Logger('网站服务器正在从 '+str(shamir_dic[user_name])+' 提取'+user_name+'的shamir秘密份额并重构')
    for i in range(0,n):
        value[i] = ray.get(value[i].data)
    random_sequence = random.sample(range(n), t)
    # print('value=',value)
    ret = reconstruct_webserver_secret(value,random_sequence)
    ret = decode_unicode(ret)
    # check()
    return ret
    
def get_all_from_aby3_spu_dic():
    new_dic = {}
    for key in aby3_spu_dic:
        value = get_password_from_aby3_spu_dic(key)
        new_dic[key] = None
    return new_dic

def get_all_from_shamir_pyu_dic():
    new_dic = {}
    for key in shamir_dic:
        value = get_password_from_shamir_pyu_dic(5,3,key)
        new_dic[key] = value
    return new_dic



if __name__ == '__main__':
    ABY3_semi2k_simulator()











