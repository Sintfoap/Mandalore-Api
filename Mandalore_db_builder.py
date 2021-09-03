# Builds the Mandalore db if it doesn't exist

from getpass import getpass
from mysql.connector import connect, Error

code_file = open('Mandalore_source_code.txt', 'r')
db_build_query = code_file.read()
# for line in code_file:
#     db_build_query += line 

if __name__ == '__main__':
    try:
        with connect(
            host = '127.0.0.1',
            port = '3306',
            user = input('Username: '),
            password = getpass('Password: '),
        ) as connection:
            with connection.cursor() as cursor:
                print(cursor.execute(db_build_query, multi = True))
                print(connection.commit())
                print('Success!')

    except Error as e:
        print(e)

# Close all the files
code_file.close()