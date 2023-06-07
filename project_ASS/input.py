import math
import re
import logger

logger = logger.getLogger()

'''
judge if str contains only numeric
'''
def is_digits_only(input_str):
    pattern = r'^\d+$'
    match = re.match(pattern, input_str)
    return match is not None


'''
get the ID and make a simple judgement
'''
def getID():
    userID = input("please input your usr ID, which can only contain numeric: ")
    if is_digits_only(userID):
        return userID
    else:
        return None

'''
get the password
'''
def getPassword():
    password = input("please input your password, which can contain numeric、character ans special characer: ")
    '''
    now we need to make sure that if we need to encode the password
    '''
    return password
