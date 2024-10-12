from cryptography.fernet import Fernet
import sqlite3

def create_connection() :
  return sqlite3.connect('password_manager.db')

def close_connection(connection):
  connection.close()

#//////////////////////////////////////database creation//////////////////////////////////////////////
def create_db():
    connection = create_connection() #database file
    cursor = connection.cursor()

    cursor.execute('''                        
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY,
            encryption_key TEXT NOT NULL
        )
    ''')                                          #table for key

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')                                          #table for passwords
    connection.commit()
    close_connection(connection)

 
#//////////////////////////////////encrypted key creation and storage/////////////////////////////////////
def initialize_key():
  while True:
    pwd = input("enter the master password: ")

    if pwd == "shri0809":
      key_g = Fernet.generate_key()
      connection = create_connection()
      cursor = connection.cursor()
      cursor.execute('INSERT INTO keys (id,encryption_key) VALUES (?,?)', (1,key_g.decode()))
      connection.commit()
      close_connection(connection)
      print("encryption of the key is done!")
      break
    else:
        print("Incorrect master password!")
        continue

#////////////////////////////////////////loading of key to decrypt passwords/////////////////////////////////
def load_key():
  connection = create_connection()
  cursor = connection.cursor()
  cursor.execute('SELECT encryption_key FROM keys WHERE id = 1')
  key = cursor.fetchone()[0].encode()
  connection.commit()
  close_connection(connection)
  return Fernet(key)
#////////////////////////////////////////deletion of key for simple re-auth////////////////////////////////////////
def delete_key():
   connection = create_connection()
   cursor = connection.cursor()
   cursor.execute("DELETE FROM keys WHERE id=1")
   connection.commit()
   close_connection(connection)
#//////////////////////////////////////////username and password addition///////////////////////////////////////////////////
def add(account,password):
  
  cipher = load_key()
  encrypted_password = cipher.encrypt(password.encode()).decode()
  connection = create_connection()
  cursor = connection.cursor()
  cursor.execute('INSERT INTO passwords (account, password) VALUES (?, ?)', (account, encrypted_password)) 
  connection.commit() 
  close_connection(connection)
#////////////////////////////////////view the username and password non decrypted format/////////////////////////////////
def view():
    cipher = load_key()

    connection = create_connection()
    cursor = connection.cursor()
    
 
    cursor.execute('SELECT account, password FROM passwords')
    rows = cursor.fetchall()  
    
    close_connection(connection) 
    for account, encrypted_password in rows:
        try:
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            print(f'Account: {account} || Password: {decrypted_password}')
        except Exception as e:
            print(f"Error decrypting password for {account}: {e}")


#////////////////////////calling to create///////////////////////////  
create_db()
#//////////////////////////calling for key initialization/////////////////////////
initialize_key()
while True:
  mode = input("if you like to add password the write \"add\" and for viewing password write \"view\" or to quite enter \"q\": ")

  if mode == "view":
    view()
  elif mode == "add":
    account = input("enter the account name: ")
    password = input("enter the acount password: ")
    add(account,password)
  elif mode =="q":
    print("visit again")
    delete_key()
    quit()
  else:
    print('invalid input')
    continue