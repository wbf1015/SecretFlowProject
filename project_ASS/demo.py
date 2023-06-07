import secretflow as sf
import spu
import copy
import db
import logger
import corn
import jax
import ray
import random
import copy
from ASS import generate_webserver_shares, reconstruct_webserver_secret, refresh_webserver_secret
from utils import dict_encode,array2int,decode_unicode
logger = logger.getLogger()

'''
aby3 means the party: user、chrome、TTP
semi2k means the party: webserver1-5
'''
aby3_spu_dic = {}
ASS_dic={}

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
        store_dic[key] = password_spu
    # return up_dict

'''
store the ASS-based serect shares
'''
def share_ASS_secret(n,user_dic,store_dic):
    for key in user_dic:
        value = user_dic[key]
        shares = generate_webserver_shares(n,value)
        ss_pyu_webserver1 = pyu_webserver1(get_password)(shares[0])
        ss_pyu_webserver2 = pyu_webserver2(get_password)(shares[1])
        ss_pyu_webserver3 = pyu_webserver3(get_password)(shares[2])
        ss_pyu_webserver4 = pyu_webserver4(get_password)(shares[3])
        ss_pyu_webserver5 = pyu_webserver5(get_password)(shares[4])
        shares = [ss_pyu_webserver1,ss_pyu_webserver2,ss_pyu_webserver3,ss_pyu_webserver4,ss_pyu_webserver5]
        store_dic[key] = shares

# ===============================================================================
def display(share_list,k):
    new_list = []
    for share in share_list:
        share = str(share)
        if len(share) <=2*k:
            new_list.append(share)
        else:
            new_list.append(share[:k] + '****' + share[-k:])
    return new_list
        
def refresh_shares(n,username,index):
    value = copy.deepcopy(ASS_dic[username])
    # check()
    for i in range(0,n):
        value[i] = ray.get(value[i].data)
    
    index -= 1
    if (index<0) or (index>5):
        return None
    before = value[index]    
    value = refresh_webserver_secret(value)
    after = value[index]
    ss_pyu_webserver1 = pyu_webserver1(get_password)(value[0])
    ss_pyu_webserver2 = pyu_webserver2(get_password)(value[1])
    ss_pyu_webserver3 = pyu_webserver3(get_password)(value[2])
    ss_pyu_webserver4 = pyu_webserver4(get_password)(value[3])
    ss_pyu_webserver5 = pyu_webserver5(get_password)(value[4])
    values = [ss_pyu_webserver1,ss_pyu_webserver2,ss_pyu_webserver3,ss_pyu_webserver4,ss_pyu_webserver5]
    ASS_dic[username] = values
    return display(before,3),display(after[:-1],3)
        
# ===============================================================================

    
    


def check():
    for key in ASS_dic.keys():
        value = ASS_dic[key]
        for i in range(len(value)):
            print(' key=',key,' server_index=',i,' type=',type(value[i]))


# ===============================================================================
'''
init the aby3_spu_dic and semi2k_spu_dic
then web can search on above dicts
'''
def ABY3_ASS_simulator():
    user_dic = db.getUser()
    user_dic = dict_encode(user_dic)
    device_dic = corn.ABY3_ASS()
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
    share_ASS_secret(5, user_dic, ASS_dic)
    
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

def add_user_2_ASS_pyu_dic(user_name,password):
    dic = {user_name:password}
    dic = dict_encode(dic)
    share_ASS_secret(5,dic,ASS_dic)

def add_user_2_cheetah_spu_dic(user_name,password):
    pass

'''
Input : username
Output : password revealed by aby3 from user、chrome、TTP
'''
def get_password_from_aby3_spu_dic(user_name):
    return decode_unicode(array2int(sf.reveal(aby3_spu_dic[user_name])))

'''
Input : username
Output : password revealed by ASS from webserver1-5
'''
def get_password_from_ASS_pyu_dic(n, user_name):
    # check()
    value = copy.deepcopy(ASS_dic[user_name])
    # check()
    for i in range(0,n):
        value[i] = ray.get(value[i].data)
    ret = reconstruct_webserver_secret(n,value)
    ret = decode_unicode(ret)
    # check()
    return ret
    
def get_all_from_aby3_spu_dic():
    new_dic = {}
    for key in aby3_spu_dic:
        value = get_password_from_aby3_spu_dic(key)
        new_dic[key] = value
    return new_dic

def get_all_from_ASS_pyu_dic():
    new_dic = {}
    for key in ASS_dic:
        value = get_password_from_ASS_pyu_dic(5,3,key)
        new_dic[key] = value
    return new_dic



if __name__ == '__main__':
    ABY3_semi2k_simulator()











