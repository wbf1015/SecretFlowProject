import secretflow as sf
import spu
# import db
import logger

logger = logger.getLogger()


'''we need to transfer the string type to the int list'''
def encode_unicode(string):
    encoded = []
    for char in string:
        encoded.append(ord(char))
    return encoded


'''we can choose to transfer the int list to the string type'''
def decode_unicode(int_list):
    string = ''.join([chr(i) for i in int_list])
    return string


'''get return the password encode list'''
def get_password(encode_list):
    return encode_list


'''
transfer all the password to the SPUobject then update the dict
return the dict
'''
def transfer_password(up_dict, pyu, spu_device):
    # password = next(iter(up_dict.values()))
    for key in up_dict:
        value = up_dict[key]
        password_pyu = pyu(get_password)(value)
        password_spu = password_pyu.to(spu_device)
        up_dict[key] = password_spu
    return up_dict


'''here we want to peel off the jax array'''
def array2int(list_of_arrays):
    new_list = [arr.item() for arr in list_of_arrays]
    return new_list


'''we need to transfer the password in dict to SPUobject'''
def dict_encode(up_dict):
    for key in up_dict:
        value = up_dict[key]
        new_value = encode_unicode(value)
        up_dict[key] = new_value
    return up_dict


'''
init a sf with user,chrome which compose a Cheetah 2PC model
to simulate the web server get 5 participants
'''
sf.shutdown()
sf.init(['user', 'chrome', 'TTP', 'Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'], address='local')

# init the PYU unit
pyu_user = sf.PYU('user')
pyu_TTP= sf.PYU('TTP')
pyu_chrome = sf.PYU('chrome')
pyu_webserver = sf.PYU('Webserver1')

# the aby3 config
aby3_config = sf.utils.testing.cluster_def(
    parties=['user', 'chrome', 'TTP'],
    runtime_config={
        'protocol': spu.spu_pb2.ABY3,
        'field': spu.spu_pb2.FM64,
    })

# the Cheetah config
cheetah_config = sf.utils.testing.cluster_def(
    parties=['user', 'chrome'],
    runtime_config={
        'protocol': spu.spu_pb2.CHEETAH,
        'field': spu.spu_pb2.FM64,
    },
)

# the Semi2k config
semi2k_config = sf.utils.testing.cluster_def(
    parties=['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'],
    runtime_config={
        'protocol': spu.spu_pb2.SEMI2K,
        'field': spu.spu_pb2.FM64,
    },
)

# the 2PC device
spu_cheetah = sf.SPU(cheetah_config)
# the npc device
spu_semi2k = sf.SPU(semi2k_config)

'''
simulate the web username and password dict
the reality is: user account -> website -> fill the username and password
user account: here when we login we will get the dict
here we just get 1 website
'''
up_dict = {'zzekun': 'fzk123456'}
up_dict = dict_encode(up_dict)
print(up_dict)

# 这块儿要改一下，要集成俩函数把整个的dict中的所有键值对的value给换成SPUObject
up_dict = transfer_password(up_dict, pyu_user, spu_cheetah)
print(up_dict['zzekun'].shares_name)

# transmit the password spu to the web server pyu
password_toweb_pyu = up_dict['zzekun'].to(pyu_webserver)
password_reveal = sf.reveal(password_toweb_pyu)
print(password_reveal)

# peel off the jax array
password_reveal = array2int(password_reveal)
password_reveal = decode_unicode(password_reveal)
# here we get the password(string)
print(password_reveal)


'''
simulate the reality web server verify login
web have the user-password dict
'''
web_up_dict = {'zzekun': 'fzk123456', 'wbf': 'wbf123456'}
web_up_dict = dict_encode(web_up_dict)

web_up_dict = transfer_password(web_up_dict, pyu_webserver, spu_semi2k)
print(web_up_dict['wbf'].shares_name)

# test web reveal wbf password
print(web_up_dict['wbf'])
# print('here')
web_password_reveal = sf.reveal(web_up_dict['wbf'])
web_password_reveal = array2int(web_password_reveal)
web_password_reveal = decode_unicode(web_password_reveal)
print(web_password_reveal)
