import secretflow as sf
import spu
import copy
import db
import logger
import corn
import jax
from utils import dict_encode,array2int,decode_unicode
logger = logger.getLogger()

'''
aby3 means the party: user、chrome、TTP
semi2k means the party: webserver1-5
'''
aby3_spu_dic = {}
semi2k_spu_dic = {}


'''
we need to declare some variable so that we can use it from every function
'''
pyu_user = None
pyu_TTP = None
pyu_chrome = None
pyu_webserver = None
aby3_config = None
semi2k_config = None
spu_aby3 = None
spu_semi2k = None

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

# ===============================================================================
'''
init the aby3_spu_dic and semi2k_spu_dic
then web can search on above dicts
'''
def ABY3_semi2k_simulator():
    user_dic = db.getUser()
    user_dic = dict_encode(user_dic)
    device_dic = corn.ABY3_semi2k()
    global pyu_user, pyu_TTP, pyu_TTP, pyu_chrome, pyu_webserver, aby3_config, semi2k_config, spu_aby3, spu_semi2k
    pyu_user = device_dic['pyu_user']
    pyu_TTP= device_dic['pyu_TTP']
    pyu_chrome = device_dic['pyu_chrome']
    pyu_webserver = device_dic['pyu_webserver']
    aby3_config = device_dic['aby3_config']
    semi2k_config = device_dic['semi2k_config']

    spu_aby3 = sf.SPU(aby3_config)
    spu_semi2k = sf.SPU(semi2k_config)
    
    transfer_password(user_dic, pyu_user, spu_aby3, aby3_spu_dic)
    transfer_password(user_dic, pyu_webserver, spu_semi2k, semi2k_spu_dic)
    
    reveal_test = sf.reveal(semi2k_spu_dic['david'])
    print(reveal_test)
    reveal_test = array2int(reveal_test)
    print(reveal_test)
    reveal_test = decode_unicode(reveal_test)
    print(reveal_test)

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

def add_user_2_semi2k_spu_dic(user_name,password):
    dic = {user_name:password}
    dic = dict_encode(dic)
    transfer_password(dic, pyu_webserver, spu_aby3, semi2k_spu_dic)

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
Output : password revealed by semi2k from webserver1-5
'''
def get_password_from_semi2k_spu_dic(user_name):
    return decode_unicode(array2int(sf.reveal(semi2k_spu_dic[user_name])))

def get_all_from_aby3_spu_dic():
    new_dic = {}
    for key in aby3_spu_dic:
        value = get_password_from_aby3_spu_dic(key)
        new_dic[key] = value
    return new_dic

def get_all_from_semi2k_spu_dic():
    new_dic = {}
    for key in semi2k_spu_dic:
        value = get_password_from_semi2k_spu_dic(key)
        new_dic[key] = value
    return new_dic



if __name__ == '__main__':
    ABY3_semi2k_simulator()











