import ssl
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import time
import base64
import getpass

#Setup here

MASTER_KEY =  3464 # Must be a number less than 10000
url = 'https://172.16.1.1:8090/login.xml' # Set POST destination URL here
username = 'be1005815' #Set your username here

#Setup ends

# Don't modify anything below this line

password = ''

def encrypt_val(input_text):
    b = len(input_text)
    input_text = input_text * MASTER_KEY
    i = 0
    box = [['a' for x in range(MASTER_KEY)] for y in range(b)]
    for j in range(b):
        for k in range(MASTER_KEY):
            box[j][k] = input_text[i]
            i+=1
    output_text = ""
    c = MASTER_KEY % 256
    for k in range(MASTER_KEY):
        for j in range(b):
            output_text += chr((ord(box[j][k])+c)%256)
    return output_text

def decrypt_val(input_text):
    b = len(input_text)//MASTER_KEY
    i = 0
    box = [['a' for x in range(MASTER_KEY)] for y in range(b)]
    for k in range(MASTER_KEY):
        for j in range(b):
            box[j][k] = input_text[i]
            i += 1
    output_text = ""
    c = MASTER_KEY % 256
    for j in range(b):
        for k in range(MASTER_KEY):
            output_text += chr((ord(box[j][k])-MASTER_KEY+256)%256)
    return output_text[0:b]


def hardLogin():
    global password
    while(True):
        password = getpass.getpass('Enter the password: ')
        data = {'username': username, 'password': password, 'mode': '191'}
        res = str(urlopen(Request(url, urlencode(data).encode()),context=ctx).read())
        if(len(res.split('<![CDATA[You have successfully logged in]]>'))>1):
            break
        else:
            print("Incorrect Username/Password. Please try again..")
    password = encrypt_val(password)
    file = open("pass.enc","w")
    file.write(password)
    file.close()
    time.sleep(1)

# The following lines invalidate SSL errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    file = open("pass.enc","r")
    password = file.read()
    file.close()
except:
    pass

if (not password):
    hardLogin() # Ask for password from user since no password was saved earlier

while(True):
    password = decrypt_val(password)

    data = {'username': username, 'password': password, 'mode': '191'}
    res = str(urlopen(Request(url, urlencode(data).encode()),context=ctx).read())

    if(len(res.split('<![CDATA[You have successfully logged in]]>'))>1):
        #Login successful
        print("Login Successful..")
        time.sleep(1)
        exit(0)
    else:
        print("Incorrect Username/Password. Please try again..")
        hardLogin() # Ask for password again as the saved password was incorrect

