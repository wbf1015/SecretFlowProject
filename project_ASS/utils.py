import secretflow as sf
import spu
import jax
import sys





# ========================================================================
def is_valid_unicode(i):
    if i<0:
        return False
    if i >= 1114112:
        return False
    return True

'''we need to transfer the string type to the int list'''
def encode_unicode(string):
    encoded = []
    for char in string:
        encoded.append(ord(char))
    return encoded

'''we can choose to transfer the int list to the string type'''
def decode_unicode(int_list):
    for i in int_list:
        if is_valid_unicode(i) == False:
            return ''
    string = ''.join([chr(i) for i in int_list])
    return string

'''we need to transfer the password in dict to SPUobject'''
def dict_encode(up_dict):
    for key in up_dict:
        value = up_dict[key]
        new_value = encode_unicode(value)
        up_dict[key] = new_value
    return up_dict

# ========================================================================

'''here we want to peel off the jax array'''
def array2int(list_of_arrays):
    new_list = [arr.item() for arr in list_of_arrays]
    return new_list
