from cryptography.fernet import Fernet

pwd = input("enter the master password: ")

key_g = Fernet.generate_key()
with open("password-manager/secret.txt", "wb") as key_file:
    key_file.write(key_g)

def load_key():
  with open("password-manager/secret.txt", "rb") as key_file:
    key = key_file.read()
  cipher = Fernet(key)
  return cipher

def add(account,password):
  
  cipher = load_key()

  with open("password-manager/password_manager.txt","a") as f:
    f.write(f'{account}|{cipher.encrypt(password.encode()).decode()}\n')
  
def view():
  cipher = load_key()
  with open("password-manager/password_manager.txt","r") as f:
    details = {}
    for line in f:
      user,passw = line.rstrip().split("|") 
      
      try:
        passw = cipher.decrypt(passw.encode()).decode()
        details[user] = passw
      except Exception as e:
        print(f"Error decrypting password for {user}: {e}")

      details[user] = passw
  for key in sorted(details):
    print(f'account: {key} || password: {details[key]}')

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
    quit()
  else:
    print('invalid input')
    continue