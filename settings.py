#---libs---
import sqlite3 as sq
import bcrypt
import jwt 
import time
#---setup---
con = sq.connect("database.db")
setcursor = con.cursor()
setcursor.execute("""CREATE TABLE IF NOT EXISTS User (
                    username TEXT NOT NULL,
                    pass TEXT NOT NULL,
                    id TEXT PRIMARY KEY
                );""")
#---sign up---
def sign_up():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    username = input("Enter your username: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    setcursor.execute("INSERT INTO User (username, pass, id) VALUES (?, ?, ?);", [username, hashed_password, email]) 
    con.commit()
    con.close()
#---sign in---
def sign_in():
    check_sign_in = int(input("Give token[1]/Sign in[2]:"))
    if check_sign_in == 2:
     text = input("Enter your email:")
     password_check = input("Enter your password:")
     result = setcursor.execute("SELECT * FROM User WHERE id=?;", [text])
     mate = result.fetchone()
     data = {"username":mate[0],
             "email":mate[2]}
     encoded_jwt = jwt.encode(data, "secret", algorithm="HS256") 
     if mate and bcrypt.checkpw(password_check.encode('utf-8'), mate[1]):
         print("Sign up successful!")
         print("Username:", mate[0], "\nEmail:", mate[2],"\nYour token:\n",encoded_jwt)

     else:
         print("Sign up failed.")
    elif check_sign_in ==1:
      encoded_jwt = input("Your Token:")
      try:
         decode_token= jwt.decode(encoded_jwt,"secret",algorithms="HS256")
         print(decode_token)
      except jwt.ExpiredSignatureError:
         print("Token has expired.")
      except jwt.InvalidTokenError:
         print("Invalid token.Token verification failed.")
         
#---check-auth---
def check_auth():
    text = input("Enter your email:")
    password_check = input("Enter your password:")
    result = setcursor.execute("SELECT * FROM User WHERE id=?;", [text])
    mate = result.fetchone()

    if mate and bcrypt.checkpw(password_check.encode('utf-8'), mate[1]):
        print("Authentication successful!")
        print("Username:", mate[0], "\nEmail:", mate[2])
    else:
        print("Authentication failed.")
#---conditions---
detail = int(input("sign up[1]/sign in[2]/check auth[3]:"))
if detail == 1:
   sign_up()
elif detail ==2:
   sign_in()
elif detail == 3:
   check_auth()    
    
