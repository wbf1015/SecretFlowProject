import pymysql #导入模块
import logger
logger = logger.getLogger()

'''
connect to the mysql and use the cursor to obtain an operation cursor
'''
db = pymysql.connect(
         host='10.136.104.53',
         port=3306,
         user='root',
         passwd='wbf20011015',
         db='secretflow',
         charset='utf8'
         )
cursor = db.cursor()


'''
get all users from mysql with there username and password
'''
def getUserFromSQL():
    sql = """SELECT * FROM `users`"""
    try:
        cursor.execute(sql)  # Execute the SQL statement
        # result = cursor.fetchone()  # Fetch the first row of the query result as a tuple
        result = cursor.fetchall()  # Fetch all rows of the query result as a list of tuples
        db.commit()  # Save the changes made to the database by the transaction
        logger.info('mysql qury result ='+ str(result))
        return result
        
    except Exception:
        db.rollback()  # Roll back the transaction when an error occurs
        logger.critical('ERROR WITH FETCH DATA IN MYSQL')
        print("Query failed")

'''
translate the str 2 unicode
'''
def encode_unicode(string):
    encoded = []
    for char in string:
        encoded.append(ord(char))
    return encoded


def getUser():
    '''
    if you do not have a mysql just use the below sentence 2 inplace users = getUserFromSQL()
    users =  = [['alice', '123456'], ['bob', 'qwer1234'], ['carol', 'rs90123'], ['david', '5678!dbn'], ['eva', 'serectflow']]
    '''
    users = getUserFromSQL()
    users = [list(user) for user in users]
    users = {user[0]: user[1] for user in users}
    # users = [[encode_unicode(m) for m in user] for user in users]
    # print(users)
    return users




# you can not use it directly, it`s only for test
if __name__=='__main__':
    getUser()